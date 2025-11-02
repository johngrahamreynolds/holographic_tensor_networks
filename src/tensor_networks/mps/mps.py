# Matrix Product States (MPS)
# Author: John Graham Reynolds
# *************************************************************
# In this example, we use PyTorch to optimally learn the tensor values 
# in the MPS representation of a 1D quantum many-body system.
# *************************************************************

import torch
import torch.nn as nn
import torch.optim as optim
import tensornetwork as tn

class MPS(nn.Module):
    def __init__(self, num_sites: int, bond_dim: int, physical_dim: int):
        super(MPS, self).__init__()
        self.num_sites = num_sites
        self.bond_dim = bond_dim
        self.physical_dim = physical_dim
        self.tensors = nn.ParameterList([nn.Parameter(torch.randn(bond_dim, bond_dim)) for _ in range(num_sites)])
    
    def forward(self, state: torch.Tensor):
        pass

    def compute_energy(self, state: torch.Tensor):
        pass

    def compute_magnetization(self, state: torch.Tensor):
        pass

    def compute_correlation(self, state: torch.Tensor):
        pass

    def compute_entanglement_entropy(self, state: torch.Tensor):
        pass



def build_mps_from_tensor(tensor: torch.Tensor):
    pass