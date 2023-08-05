import astropy.units as u
import numpy as np
from astropy.wcs import WCS

from .core import Spec214Dataset, TimeVaryingWCSGenerator


class BaseVISPDataset(Spec214Dataset):
    """
    A base class for VISP datasets.
    """

    def __init__(
        self,
        n_maps,
        n_steps,
        n_stokes,
        time_delta,
        *,
        linewave,
        detector_shape=(1000, 2560),
    ):
        array_shape = [1] + list(detector_shape)
        dataset_shape = [n_steps] + list(detector_shape)

        if n_maps > 1:
            dataset_shape = [n_maps] + dataset_shape
        if n_stokes > 1:
            dataset_shape = [n_stokes] + dataset_shape

        super().__init__(
            dataset_shape,
            array_shape,
            time_delta=time_delta,
            instrument="visp",
        )

        self.add_constant_key("DTYPE1", "SPECTRAL")
        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DTYPE3", "SPATIAL")
        self.add_constant_key("DPNAME1", "wavelength")
        self.add_constant_key("DPNAME2", "slit position")
        self.add_constant_key("DPNAME3", "raster position")
        self.add_constant_key("DWNAME1", "wavelength")
        self.add_constant_key("DWNAME2", "helioprojective latitude")
        self.add_constant_key("DWNAME3", "helioprojective longitude")
        self.add_constant_key("DUNIT1", "nm")
        self.add_constant_key("DUNIT2", "arcsec")
        self.add_constant_key("DUNIT3", "arcsec")

        next_index = 4
        if n_maps > 1:
            self.add_constant_key(f"DTYPE{next_index}", "TEMPORAL")
            self.add_constant_key(f"DPNAME{next_index}", "scan number")
            self.add_constant_key(f"DWNAME{next_index}", "time")
            self.add_constant_key(f"DUNIT{next_index}", "s")
            next_index += 1

        if n_stokes > 1:
            self.add_constant_key(f"DTYPE{next_index}", "STOKES")
            self.add_constant_key(f"DPNAME{next_index}", "stokes")
            self.add_constant_key(f"DWNAME{next_index}", "stokes")
            self.add_constant_key(f"DUNIT{next_index}", "")

        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        self.linewave = linewave
        self.plate_scale = 0.06 * u.arcsec / u.pix
        self.spectral_scale = 0.01 * u.nm / u.pix
        self.slit_width = 0.06 * u.arcsec
        self.n_stokes = n_stokes


class SimpleVISPDataset(BaseVISPDataset):
    """
    A VISP cube with regular raster spacing.
    """

    name = "visp-simple"

    @property
    def non_temporal_file_axes(self):
        if self.n_stokes > 1:
            # This is the index in file shape so third file dimension
            return (0,)
        return super().non_temporal_file_axes

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @property
    def fits_wcs(self):
        if self.array_ndim != 3:
            raise ValueError(
                "VISP dataset generator expects a three dimensional FITS WCS."
            )

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = (
            self.array_shape[1] / 2,
            self.array_shape[0] / 2,
            self.file_index[-1] * -1,
        )
        # TODO: linewav is not a good centre point
        w.wcs.crval = self.linewave.to_value(u.nm), 0, 0
        w.wcs.cdelt = (
            self.spectral_scale.to_value(u.nm / u.pix),
            self.plate_scale.to_value(u.arcsec / u.pix),
            self.slit_width.to_value(u.arcsec),
        )
        w.wcs.cunit = "nm", "arcsec", "arcsec"
        w.wcs.ctype = "WAVE", "HPLT-TAN", "HPLN-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


class TimeDependentVISPDataset(SimpleVISPDataset):
    """
    A version of the VBI dataset where the CRVAL and PC matrix change with time.
    """

    name = "visp-time-dependent"

    def __init__(
        self,
        n_maps,
        n_steps,
        n_stokes,
        time_delta,
        *,
        linewave,
        detector_shape=(1000, 2560),
        pointing_shift_rate=10 * u.arcsec / u.s,
        rotation_shift_rate=0.5 * u.deg / u.s,
    ):

        super().__init__(
            n_maps,
            n_steps,
            n_stokes,
            time_delta,
            linewave=linewave,
            detector_shape=detector_shape,
        )

        self.wcs_generator = TimeVaryingWCSGenerator(
            cunit=(u.nm, u.arcsec, u.arcsec),
            ctype=("WAVE", "HPLT-TAN", "HPLN-TAN"),
            crval=(self.linewave.to_value(u.nm), 0, 0),
            rotation_angle=-2 * u.deg,
            crpix=(
                self.array_shape[1] / 2,
                self.array_shape[0] / 2,
                self.file_index[-1] * -1,
            ),
            cdelt=(
                self.spectral_scale.to_value(u.nm / u.pix),
                self.plate_scale.to_value(u.arcsec / u.pix),
                self.slit_width.to_value(u.arcsec),
            ),
            pointing_shift_rate=u.Quantity([pointing_shift_rate, pointing_shift_rate]),
            rotation_shift_rate=rotation_shift_rate,
            jitter=False,
            static_axes=[0],
        )

    @property
    def fits_wcs(self):
        return self.wcs_generator.generate_wcs(self.time_index * self.time_delta * u.s)
