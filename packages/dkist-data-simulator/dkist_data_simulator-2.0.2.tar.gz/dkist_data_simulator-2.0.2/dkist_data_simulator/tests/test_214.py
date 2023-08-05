import astropy.units as u
import numpy as np
from astropy.table import Table

from dkist_data_simulator.spec214.vbi import (
    MosaicedVBIBlueDataset,
    TimeDependentVBIDataset,
)
from dkist_data_simulator.spec214.visp import (
    SimpleVISPDataset,
    TimeDependentVISPDataset,
)
from dkist_data_simulator.spec214.vtf import SimpleVTFDataset


def test_vbi_mosaic():
    ds = MosaicedVBIBlueDataset(n_time=2, time_delta=10, linewave=400 * u.nm)
    headers = ds.generate_headers()
    h_table = Table(headers)

    # Assert that between index 1 and 2 we have 9 unique positions
    tile_grouped = h_table.group_by(("MINDEX1", "MINDEX2"))
    assert len(tile_grouped.groups) == 9

    for tile in tile_grouped.groups:
        assert (tile["CRVAL1"] == tile["CRVAL1"][0]).all()
        assert (tile["CRVAL2"] == tile["CRVAL2"][0]).all()
        assert (tile["CRPIX1"] == tile["CRPIX1"][0]).all()
        assert (tile["CRPIX2"] == tile["CRPIX2"][0]).all()

    assert (h_table["MAXIS"] == 2).all()
    assert (h_table["MAXIS1"] == 3).all()
    assert (h_table["MAXIS2"] == 3).all()


def test_time_varying_vbi():
    ds = TimeDependentVBIDataset(n_time=5, time_delta=10, linewave=400 * u.nm)
    headers = ds.generate_headers()
    h_table = Table(headers)

    constant_keys = ["CRPIX1", "CRPIX2", "CTYPE1", "CTYPE2", "CUNIT1", "CUNIT2"]
    varying_keys = ["CRVAL1", "CRVAL2", "PC1_1", "PC1_2", "PC2_1", "PC2_2"]

    for key in constant_keys:
        assert (h_table[key] == h_table[0][key]).all()

    for key in varying_keys:
        assert not (h_table[key] == h_table[0][key]).all()


def test_time_varying_visp():
    ds = TimeDependentVISPDataset(3, 4, 1, 10, linewave=500 * u.nm)
    headers = ds.generate_headers()
    h_table = Table(headers)

    crval1 = h_table["CRVAL1"]
    crval2 = h_table["CRVAL2"]
    crval3 = h_table["CRVAL3"]

    keys = []
    for i in range(1, 4):
        for j in range(1, 4):
            keys.append(f"PC{i}_{j}")

    pc = np.array([np.array(h_table[key]) for key in keys]).reshape(
        (3, 3, len(h_table))
    )
    assert np.allclose(pc[0, 0, 0], pc[0, 0])
    assert not np.allclose(pc[:, :, 0:1], pc)

    assert np.allclose(crval1[0], crval1)
    assert not np.allclose(crval2[0], crval2)
    assert not np.allclose(crval3[0], crval3)


def test_vtf_stokes_time():
    ds = SimpleVTFDataset(
        n_wave=2, n_repeats=2, n_stokes=4, time_delta=10, linewave=500 * u.nm
    )

    # assert ds.non_temporal_file_axes == (0,)
    # ds._index = 5
    # assert ds.time_index == 1

    # ds._index = 0
    headers = Table(ds.generate_headers())
    time = np.unique(headers["DATE-AVG"])
    assert time.shape == (4,)


def test_visp_4d():
    ds = SimpleVISPDataset(
        n_steps=2, n_maps=1, n_stokes=4, time_delta=10, linewave=500 * u.nm
    )

    headers = Table(ds.generate_headers())
    assert headers[0]["DTYPE4"] == "STOKES"
    assert "DTYPE5" not in headers.colnames

    ds = SimpleVISPDataset(
        n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=500 * u.nm
    )

    headers = Table(ds.generate_headers())
    assert headers[0]["DTYPE4"] == "TEMPORAL"
    assert "DTYPE5" not in headers.colnames
