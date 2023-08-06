from numpy import (int8, int16, int32, int64,
                   uint8, uint16, uint32, uint64,
                   )
from numpy import iinfo

from typing import Dict


def np_int_scalars() -> Dict:
    """A convenience function to define data structures and ranges of common numpy integer scalars.

    :return: A dictionary of numpy floating point sclars and their associated ranges
    """
    scalars = [int8, int16, int32, int64,
               uint8, uint16, uint32, uint64]

    return {scalar: range(iinfo(scalar).min, iinfo(scalar).max + 1) for scalar in scalars}
