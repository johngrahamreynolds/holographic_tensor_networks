# One-Dimensional Quantum Systems
# Author: John Graham Reynolds
# *************************************************************

from .ising import build_ising_1d_open_dataset, build_ising_1d_closed_dataset
# TODO: Add other 1D systems here (e.g., Heisenberg, XYZ, etc.)

__all__ = [
    'build_ising_1d_open_dataset',
    'build_ising_1d_closed_dataset',
]

