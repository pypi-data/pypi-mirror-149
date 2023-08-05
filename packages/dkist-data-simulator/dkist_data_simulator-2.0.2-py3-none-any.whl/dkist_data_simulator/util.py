import numpy as np
from astropy.io.fits import CompImageHDU as _CompImageHDU
from astropy.io.fits.column import _FormatP
from astropy.io.fits.hdu.table import _binary_table_byte_swap

__all__ = ["CompImageHDU"]

# This class is a backport of https://github.com/astropy/astropy/pull/12138
# Once that makes it to a released version of astropy this can be removed.


class CompImageHDU(_CompImageHDU):
    def _calculate_datasum_with_heap(self):
        """
        Calculate the value for the ``DATASUM`` card given the input data
        """

        with _binary_table_byte_swap(self.data) as data:
            dout = data.view(type=np.ndarray, dtype=np.ubyte)
            csum = self._compute_checksum(dout)

            # Now add in the heap data to the checksum (we can skip any gap
            # between the table and the heap since it's all zeros and doesn't
            # contribute to the checksum
            if data._get_raw_data() is None:
                # This block is still needed because
                # test_variable_length_table_data leads to ._get_raw_data
                # returning None which means _get_heap_data doesn't work.
                for idx in range(data._nfields):
                    if isinstance(data.columns._recformats[idx], _FormatP):
                        for coldata in data.field(idx):
                            # coldata should already be byteswapped from the call
                            # to _binary_table_byte_swap
                            if not len(coldata):
                                continue

                            csum = self._compute_checksum(coldata, csum)
            else:
                csum = self._compute_checksum(data._get_heap_data(), csum)

            return csum
