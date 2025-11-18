# Training framework for MPS tensor networks using gradient descent.
# Author: John Graham Reynolds
# *************************************************************

import torch
from tensor_networks.mps import MPS
from quantum_systems.one_dimensional import build_ising_1d_open_dataset, build_ising_1d_closed_dataset


possible_datasets = {
    "ising_1d_open": build_ising_1d_open_dataset,
    "ising_1d_closed": build_ising_1d_closed_dataset,
}

def train_mps(
    mps: MPS, 
    num_epochs: int = 1000,
    learning_rate: float = 0.01,
    batch_size: int = 100,
    num_sites: int = 5, 
    J: float = 1.0, 
    h: float = 0.5, 
    num_excited: int = 0, 
    weight_by_degeneracy: bool = True, 
    base_energy_weight: float = 1.0, 
    excited_weight: float = 0.1,
    data: torch.Tensor = None,
    dataset_name: str = "ising_1d_open") -> MPS:
    """
    Train a MPS tensor network using gradient descent.
    
    Args:
        mps: The MPS to train.
        data: The data to train the MPS on.
    
    Returns:
        The trained MPS.
    """

    if dataset_name not in possible_datasets:
        raise ValueError(f"Invalid dataset name: {dataset_name}. Must be one of: {list(possible_datasets.keys())}")

    dataset = possible_datasets[dataset_name](
        num_sites=num_sites, 
        J=J, 
        h=h, 
        num_excited=num_excited, 
        weight_by_degeneracy=weight_by_degeneracy, 
        base_energy_weight=base_energy_weight, 
        excited_weight=excited_weight,
        data=data)

    print(dataset)

    return mps

if __name__ == "__main__":
    mps = MPS(num_sites=5)
    train_mps(mps, num_epochs=1000, learning_rate=0.01, batch_size=100, num_sites=5, J=1.0, h=0.5, num_excited=0, weight_by_degeneracy=True, base_energy_weight=1.0, excited_weight=0.1, dataset_name="ising_1d_open")
    print(f"Trained MPS: {mps}")