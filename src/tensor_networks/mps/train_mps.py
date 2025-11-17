# Training framework for MPS tensor networks using gradient descent.
# Author: John Graham Reynolds
# *************************************************************

import torch
from tensor_networks.mps import MPS

def train_mps(mps: MPS, data: torch.Tensor) -> MPS:
    """
    Train a MPS tensor network using gradient descent.
    
    Args:
        mps: The MPS to train.
        data: The data to train the MPS on.
    
    Returns:
        The trained MPS.
    """
    pass