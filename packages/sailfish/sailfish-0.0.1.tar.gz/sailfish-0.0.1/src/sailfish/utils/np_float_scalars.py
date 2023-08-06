from numpy import (float16, float32, float64)
from numpy import finfo

from typing import Dict


def np_float_scalars() -> Dict:
    """A convenience function to define data structures and ranges of common numpy float scalars.

    :return: A dictionary of numpy floating point sclars and their associated ranges
    """
    scalars = [float16, float32, float64]

    return {scalar: (finfo(scalar).min, finfo(scalar).max + 1.) for scalar in scalars}
