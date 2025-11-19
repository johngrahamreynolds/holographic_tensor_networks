# Matrix Product States (MPS): Learning the MPS from data
# Author: John Graham Reynolds
# *************************************************************

import torch
import torch.nn as nn
import torch.optim as optim
import tensornetwork as tn
from typing import List
from utils.tensor_utils import visualize_tensor_network

class MPS(nn.Module):
    def __init__(self, num_sites: int, bond_dim: int, physical_dim: int):
        super(MPS, self).__init__()
        
        self.num_sites = num_sites
        self.bond_dim = bond_dim
        self.physical_dim = physical_dim
        self.left_boundary = nn.Parameter(torch.randn(1, physical_dim, bond_dim, dtype=torch.complex128, requires_grad=True)) # left boundary tensor
        self.right_boundary = nn.Parameter(torch.randn(bond_dim, physical_dim, 1, dtype=torch.complex128, requires_grad=True)) # right boundary tensor
        self.middle_tensors = [
            nn.Parameter(torch.randn(bond_dim, physical_dim, bond_dim, dtype=torch.complex128, requires_grad=True)) for _ in range(num_sites - 2) # middle tensors except for the last site
        ]
        self.mps_tensors = nn.ParameterList([self.left_boundary, *self.middle_tensors, self.right_boundary]) # list of all tensors in the MPS

        # set TensorNetwork backend to PyTorch
        tn.set_default_backend("pytorch")

    def contract(self, state: torch.Tensor, visualize: bool = False):
        """
        Contract the MPS. Equivalent to the forward pass. See forward() for more details.
        Returns:
            The contracted MPS state.
        """
        return self.forward(state, visualize)
    
    def forward(self, state: torch.Tensor, visualize: bool = False):
        """
        Forward pass of the MPS. # TODO: do we need to pass a current state?

        Args:
            state: The initial state of the system.
            visualize: If True, visualize the tensor network before and after contraction.

        Returns:
            The MPS state.
        """
        
        # build the MPS network from the tensors
        mps_graph = self.build_mps_from_tensors(self.mps_tensors)

        # Visualize before contraction if requested
        if visualize:
            visualize_tensor_network(mps_graph, title="MPS before contraction")

        output_edges = []
        for node in mps_graph:
            for edge in node.get_all_edges():
                if edge.is_dangling():
                    output_edges.append(edge)

        # contract the nodes to get the MPS state
        result = tn.contractors.greedy(mps_graph, output_edge_order=output_edges)
        # TODO: remove print statements
        print(f"Contracted MPS shape: {result.tensor.shape}")  # Shape: (1, physical_dim, physical_dim, ..., physical_dim, 1)
        print(f"This represents the full quantum state\n")

        # Visualize after contraction if requested
        if visualize:
            visualize_tensor_network([result], title="MPS after contraction")

        return result.tensor.reshape(-1) # return the physical tensor as a 1D vector with 2 ** num_sites elements as complex numbers

    def build_mps_from_tensors(self, tensors: List[torch.Tensor]) -> List[tn.Node]:
        """
        Build the MPS from the list of tensors.

        Args:
            tensors: The list of tensors to build the MPS from.

        Returns:
            The list of nodes in the MPS connected by edges to form a graph.
        """
        # create the nodes
        nodes = [tn.Node(tensor) for tensor in tensors]

        # connect the nodes
        for i in range(len(tensors) - 1):
            nodes[i][2] ^ nodes[i + 1][0]  # Connect right edge of site i to left edge of site i + 1

        return nodes

    def get_physical_tensor(self, contracted_result: torch.Tensor) -> torch.Tensor:
        """
        Extract the actual N-site tensor by removing trivial boundary dimensions.
        
        Args:
            contracted_result: The tensor from forward() before reshape, shape (1, physical_dim, ..., physical_dim, 1)
        
        Returns:
            Tensor of shape (physical_dim, physical_dim, ..., physical_dim) representing the N-site quantum state
        """
        # Remove the first and last dimensions (the trivial boundary bonds)
        return contracted_result.squeeze((0, -1))
    
    def compute_energy(self, state: torch.Tensor):
        pass

    def compute_magnetization(self, state: torch.Tensor):
        pass

    def compute_correlation(self, state: torch.Tensor):
        pass

    def compute_entanglement_entropy(self, state: torch.Tensor):
        pass


# TODO: remove
if __name__ == "__main__":
    # create a random state
    state = torch.randn(2, 2)
    print(f"Initial state: {state}")

    # create an MPS
    mps = MPS(num_sites=5, bond_dim=3, physical_dim=2)
    print(f"MPS: {mps}")

    # forward pass with visualization
    mps_state = mps.contract(state, visualize=True)
    print(f"MPS state: {mps_state}")