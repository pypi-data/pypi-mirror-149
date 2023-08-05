import astropy.units as u
import numpy as np
from astropy.wcs import WCS

from .core import Spec214Dataset


class BaseCryoDataset(Spec214Dataset):
    """
    A base class for Cryo-NIRSP datasets.
    """

    def __init__(
        self,
        n_raster,
        n_scans,
        n_stokes,
        time_delta,
        *,
        linewave,
        detector_shape=(4096, 4096)
    ):

        if (not n_raster) or (not n_scans):
            raise NotImplementedError(
                "Support for less than 4D VISP datasets is not implemented."
            )

        array_shape = [1] + list(detector_shape)

        dataset_shape_rev = list(detector_shape) + [n_raster, n_scans]
        if n_stokes > 1:
            dataset_shape_rev += [n_stokes]

        super().__init__(
            dataset_shape_rev[::-1],
            array_shape,
            time_delta=time_delta,
            instrument="cryonirsp",
        )

        self.add_constant_key("DTYPE1", "SPECTRAL")
        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DTYPE3", "SPATIAL")
        self.add_constant_key("DTYPE4", "TEMPORAL")
        self.add_constant_key("DPNAME1", "wavelength")
        self.add_constant_key("DPNAME2", "slit position")
        self.add_constant_key("DPNAME3", "raster position")
        self.add_constant_key("DPNAME4", "scan number")
        self.add_constant_key("DWNAME1", "wavelength")
        self.add_constant_key("DWNAME2", "helioprojective latitude")
        self.add_constant_key("DWNAME3", "helioprojective longitude")
        self.add_constant_key("DWNAME4", "time")
        self.add_constant_key("DUNIT1", "nm")
        self.add_constant_key("DUNIT2", "arcsec")
        self.add_constant_key("DUNIT3", "arcsec")
        self.add_constant_key("DUNIT4", "s")

        if n_stokes > 1:
            self.add_constant_key("DTYPE5", "STOKES")
            self.add_constant_key("DPNAME5", "stokes")
            self.add_constant_key("DWNAME5", "stokes")
            self.add_constant_key("DUNIT5", "")

        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        self.linewave = linewave

        # TODO: Numbers
        self.plate_scale = 0.06 * u.arcsec / u.pix
        self.spectral_scale = 0.01 * u.nm / u.pix
        self.slit_width = 0.06 * u.arcsec
        self.n_stokes = n_stokes


class SimpleCryoDataset(BaseCryoDataset):
    """
    A five dimensional Cryo cube with regular raster spacing.
    """

    name = "cryo-simple"

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
