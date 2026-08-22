# Ising Model in 1D: Data Generation and Computation
# Author: John Graham Reynolds
# *************************************************************

import numpy as np
import torch
from scipy.sparse.linalg import eigsh
from scipy.sparse import csr_matrix
from typing import Dict

# Import shared tensor utilities from utils package
from utils import (
    PAULI_X, PAULI_Z, 
    build_operator_at_site, build_two_site_operator,
    compute_state_weights,
)

# ============================================================================
# 1D Ising Hamiltonian Construction and Ground State Computation
# ============================================================================

def build_ising_hamiltonian_open(
    num_sites: int,
    J: float = 1.0,
    h: float = 0.5,
    boundary_condition: str = "open"
) -> csr_matrix:
    """
    Build 1D Ising Hamiltonian: H = -J * Σ_i σ_i^z σ_{i+1}^z - h * Σ_i σ_i^x
    
    Args:
        num_sites: Number of sites in the chain
        J: Coupling strength for ZZ interactions (default: 1.0)
        h: Transverse field strength (default: 0.5, gapped phase)
        boundary_condition: "open" or "periodic" (currently supports open)
    
    Returns:
        Hamiltonian as scipy sparse matrix
    """
    
    if boundary_condition not in ["open", "periodic"]:
        raise ValueError("boundary_condition must be 'open' or 'periodic'")
    
    # Build two-body ZZ term: -J * σ_i^z σ_{i+1}^z
    H_zz = None
    num_zz_terms = num_sites - 1 if boundary_condition == "open" else num_sites
    
    for i in range(num_zz_terms):
        if boundary_condition == "open":
            j_next = i + 1
        else:  # periodic
            j_next = (i + 1) % num_sites
        
        # Use shared utility for two-site operator
        term = -J * build_two_site_operator(PAULI_Z, i, PAULI_Z, j_next, num_sites)
        
        if H_zz is None:
            H_zz = term
        else:
            H_zz = H_zz + term
    
    # Build single-body X field: -h * σ_i^x
    H_x = None
    for i in range(num_sites):
        term = -h * build_operator_at_site(PAULI_X, i, num_sites)
        
        if H_x is None:
            H_x = term
        else:
            H_x = H_x + term
    
    H = H_zz + H_x
    return H


def compute_ground_state_ising(
    num_sites: int,
    J: float = 1.0,
    h: float = 0.5,
    boundary_condition: str = "open",
    num_excited: int = 0
) -> Dict:
    """
    Compute ground state (and optionally excited states) of 1D Ising model via ED.
    
    Args:
        num_sites: Number of sites
        J: Coupling strength
        h: Transverse field
        boundary_condition: "open" or "periodic"
        num_excited: Number of excited states to compute (0 = ground state only)
    
    Returns:
        Dictionary containing:
            - 'ground_state': Ground state wavefunction (numpy array)
            - 'ground_energy': Ground state energy (float)
            - 'excited_states': List of excited state wavefunctions (if num_excited > 0)
            - 'excited_energies': List of excited state energies (if num_excited > 0)
            - 'eigenvalues': All eigenvalues (sorted)
            - 'num_sites': System size
            - 'hamiltonian': Sparse Hamiltonian matrix
    """
    
    print(f"Computing ground state for {num_sites}-site Ising chain ({boundary_condition} BC)...")
    
    # Build Hamiltonian
    H = build_ising_hamiltonian_open(num_sites, J=J, h=h, boundary_condition=boundary_condition)
    
    # Compute ground state + excited states
    num_eigenvals = min(num_excited + 1, 2**num_sites - 1)
    eigenvalues, eigenvectors = eigsh(H, k=num_eigenvals, which='SA', return_eigenvectors=True)
    
    ground_energy = eigenvalues[0]
    ground_state = eigenvectors[:, 0]
    
    # Check for degeneracies
    degeneracy_info = check_degeneracies(eigenvalues, tolerance=1e-6)
    
    # TODO: we dont need to print this warning
    # if degeneracy_info['has_degeneracies']:
    #     print(f"\n⚠️  WARNING: Found {degeneracy_info['num_degenerate_levels']} degenerate energy level(s):")
    #     for group_idx, group in enumerate(degeneracy_info['degenerate_groups']):
    #         E_deg = eigenvalues[group[0]]
    #         print(f"   Level {group_idx}: indices {group}, E = {E_deg:.8f} ({len(group)}-fold degenerate)")
    #         print(f"      → Only the first eigenvector was returned by eigsh()")
    
    result = {
        'ground_state': ground_state,
        'ground_energy': ground_energy,
        'num_sites': num_sites,
        'hamiltonian': H,
        'J': J,
        'h': h,
        'boundary_condition': boundary_condition,
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors,
        'degeneracy_info': degeneracy_info,
    }
    
    if num_excited > 0:
        result['excited_states'] = [eigenvectors[:, i] for i in range(1, min(num_excited + 1, len(eigenvalues)))]
        result['excited_energies'] = eigenvalues[1:min(num_excited + 1, len(eigenvalues))]
    
    return result


# ============================================================================
# Observable Computation Functions 
# ============================================================================

def compute_local_magnetization(state: np.ndarray, num_sites: int) -> np.ndarray:
    """
    Compute local Z-magnetization: ⟨σ_i^z⟩ for each site i.
    
    Args:
        state: Wavefunction (2^num_sites,)
        num_sites: Number of sites
    
    Returns:
        Array of local magnetizations (num_sites,)
    """
    magnetization = np.zeros(num_sites)
    
    for i in range(num_sites):
        # Use shared utility for single-site operator
        z_op = build_operator_at_site(PAULI_Z, i, num_sites)
        magnetization[i] = np.real(state.conj() @ z_op @ state)
    
    return magnetization


def compute_two_point_correlations(state: np.ndarray, num_sites: int) -> np.ndarray:
    """
    Compute two-point Z-Z correlations: ⟨σ_i^z σ_j^z⟩.
    
    Args:
        state: Wavefunction
        num_sites: Number of sites
    
    Returns:
        Correlation matrix (num_sites, num_sites)
    """
    correlations = np.zeros((num_sites, num_sites))
    
    # Calculate the correlation matrix
    for i in range(num_sites):
        # Loop over only the upper triangle of the correlation matrix and use symmetry to fill the lower triangle
        for j in range(i, num_sites):
            if i == j:
                # Local term: ⟨σ_i^z σ_i^z⟩ = 1
                correlations[i, j] = 1.0
            else:
                # Use shared utility for two-site operator
                corr_op = build_two_site_operator(PAULI_Z, i, PAULI_Z, j, num_sites)
                correlations[i, j] = np.real(state.conj() @ corr_op @ state)
                correlations[j, i] = correlations[i, j]  # Symmetric
    
    return correlations


def compute_entanglement_entropy(state: np.ndarray, num_sites: int, cut_position: int) -> float:
    """
    Compute entanglement entropy at a given cut in the chain.
    
    Args:
        state: Wavefunction
        num_sites: Total number of sites
        cut_position: Position of the cut (0 < cut_position < num_sites)
    
    Returns:
        Entanglement entropy (float)
    """
    # Reshape wavefunction into left-right subsystems
    dim_left = 2**cut_position
    dim_right = 2**(num_sites - cut_position)
    
    state_reshaped = state.reshape((dim_left, dim_right))
    
    # Compute reduced density matrix of left system
    rho_left = state_reshaped @ state_reshaped.conj().T
    
    # Compute eigenvalues and entropy
    eigenvalues = np.linalg.eigvalsh(rho_left)
    eigenvalues = eigenvalues[eigenvalues > 1e-14]  # Remove numerical noise
    
    entropy = -np.sum(eigenvalues * np.log2(eigenvalues))
    return entropy


def check_degeneracies(eigenvalues: np.ndarray, tolerance: float = 1e-6) -> Dict:
    """
    Identify and characterize near-degenerate eigenvalue levels.
    
    Args:
        eigenvalues: Sorted array of eigenvalues
        tolerance: Energy threshold for considering states degenerate
    
    Returns:
        Dictionary with degeneracy information
    """
    degenerate_groups = []
    current_group = [0]
    
    for i in range(1, len(eigenvalues)):
        if abs(eigenvalues[i] - eigenvalues[i-1]) < tolerance:
            current_group.append(i)
        else:
            if len(current_group) > 1:
                degenerate_groups.append(current_group)
            current_group = [i]
    
    # Check last group
    if len(current_group) > 1:
        degenerate_groups.append(current_group)
    
    return {
        'has_degeneracies': len(degenerate_groups) > 0,
        'degenerate_groups': degenerate_groups,
        'num_degenerate_levels': len(degenerate_groups),
    }


def build_ising_1d_open_dataset(num_sites: int = 5, 
                               J: float = 1.0, 
                               h: float = 0.5,
                               num_excited: int = 0,
                               weight_by_degeneracy: bool = True,
                               base_energy_weight: float = 1.0,
                               excited_weight: float = 0.1,
                            #    pull_from_hf: bool = False
                               ) -> Dict:
    """
    Construct complete dataset for 1D Ising system with open boundary conditions.
    
    Supports multi-state datasets with degeneracy-aware weighting.
    
    Args:
        num_sites: System size
        J: Coupling strength for ZZ interaction
        h: Transverse field strength
        num_excited: Number of excited states to include (0 = ground state only)
        weight_by_degeneracy: If True, weight states by degeneracy multiplicity
        base_energy_weight: Weight for ground state (default: 1.0)
        excited_weight: Base weight for excited states (default: 0.1)
    
    Returns:
        Comprehensive dataset dictionary with:
            - Single ground state (if num_excited=0)
            - Multiple states with weights (if num_excited>0)
            - All observables computed for each state
    """

    # if pull_from_hf:
    #     # try to pull the prebuilt dataset from Hugging Face, if it fails, compute the dataset from scratch
    #     try:
    #         dataset = load_dataset(f"MarioBarbeque/ising_1d_open_n{num_sites}_s{num_excited}")
    #         return dataset
    #     except Exception as e:
    #         print(f"Error pulling dataset from Hugging Face: {e}")
    #         print(f"The dataset for the {num_sites}-site Ising chain with {num_excited} excited states may not yet be on the author's Hugging Face repository. Computing dataset from scratch...")
    #         pass
    
    # Compute ground and excited states
    ed_data = compute_ground_state_ising(
        num_sites=num_sites,
        J=J,
        h=h,
        boundary_condition="open",
        num_excited=num_excited
    )
    
    ground_state = ed_data['ground_state']
    degeneracy_info = ed_data['degeneracy_info']
    
    # Compute state weights (accounting for degeneracy if requested)
    print(f"Computing state weights...")
    state_weights = compute_state_weights(
        eigenvalues=ed_data['eigenvalues'],
        num_excited=num_excited,
        base_energy_weight=base_energy_weight,
        excited_weight=excited_weight,
        degeneracy_info=degeneracy_info,
        weight_by_degeneracy=weight_by_degeneracy
    )
    
    # Print weight summary
    num_states_actual = len(state_weights)
    print(f"State weights (num_states={num_states_actual}):")
    for i, (E, w) in enumerate(zip(ed_data['eigenvalues'][:num_states_actual], state_weights)):
        deg_marker = ""
        if degeneracy_info['has_degeneracies']:
            for group in degeneracy_info['degenerate_groups']:
                if i in group:
                    deg_marker = f" ({len(group)}-fold)"
                    break
        state_type = "Ground" if i == 0 else f"Excited {i}"
        print(f"  State {i:2d} ({state_type:12s}): E = {E:8.4f}{deg_marker:12s} w = {w:.4f}")
    
    # Compute observables for ground state
    print(f"Computing observables for ground state...")
    local_mag = compute_local_magnetization(ground_state, num_sites)
    correlations = compute_two_point_correlations(ground_state, num_sites)
    
    entanglement_entropies = []
    for cut in range(1, num_sites):
        S_cut = compute_entanglement_entropy(ground_state, num_sites, cut)
        entanglement_entropies.append(S_cut)
    
    # Build base dataset
    dataset = {
        'name': f'ising_1d_open_n{num_sites}_s{num_states_actual}',
        'num_sites': num_sites,
        'num_states': num_states_actual,
        'J': J,
        'h': h,
        'boundary_condition': 'open',
        
        # States and energies
        'ground_state': ground_state,  # Full state vector (numpy)
        'ground_energy': ed_data['ground_energy'],
        'ground_state_torch': torch.tensor(ground_state, dtype=torch.complex128),
        'all_energies': ed_data['eigenvalues'][:num_states_actual],
        
        # State weights (accounts for degeneracy)
        'state_weights': state_weights,
        'weight_by_degeneracy': weight_by_degeneracy,
        
        # Observables for ground state
        'local_magnetization': local_mag,
        'two_point_correlations': correlations,
        'entanglement_entropies': entanglement_entropies,
        
        # Full eigenvalue spectrum and degeneracy info
        'hamiltonian': ed_data['hamiltonian'],
        'eigenvalues': ed_data['eigenvalues'],
        'degeneracy_info': degeneracy_info,
    }
    
    # Add excited states if requested
    if num_excited > 0:
        excited_states = [ed_data['eigenvectors'][:, i] for i in range(1, num_states_actual)]
        excited_energies = ed_data['eigenvalues'][1:num_states_actual]
        
        dataset['excited_states'] = excited_states
        dataset['excited_energies'] = excited_energies
        
        # Compute observables for each excited state
        print(f"Computing observables for {num_excited} excited state(s)...")
        excited_magnetizations = []
        excited_correlations = []
        
        for i, exc_state in enumerate(excited_states):
            mag = compute_local_magnetization(exc_state, num_sites)
            corr = compute_two_point_correlations(exc_state, num_sites)
            excited_magnetizations.append(mag)
            excited_correlations.append(corr)
        
        dataset['excited_magnetizations'] = excited_magnetizations
        dataset['excited_correlations'] = excited_correlations
    
    return dataset


def build_ising_1d_closed_dataset(num_sites: int = 5, 
                               J: float = 1.0, 
                               h: float = 0.5,
                               num_excited: int = 0,
                               weight_by_degeneracy: bool = True,
                               base_energy_weight: float = 1.0,
                               excited_weight: float = 0.1) -> Dict:
    """
    Construct complete dataset for 1D Ising system with closed boundary conditions.
    """
    pass


# ============================================================================
# TODO: remove. Example usage for validation purposes only
# NOTE: This is a research based repository, but we could consider implementing unit tests for the codebase.
# ============================================================================

if __name__ == "__main__":
    # Example 1: Ground state only dataset (default)
    print("\n" + "="*70)
    print("EXAMPLE 1: Ground State Only")
    print("="*70)
    dataset_gs = build_ising_1d_open_dataset(num_sites=8, J=1.0, h=0.5)
    
    print(f"\nDataset: {dataset_gs['name']}")
    print(f"System size: {dataset_gs['num_sites']} sites")
    print(f"Ground state energy: {dataset_gs['ground_energy']:.6f}")
    print(f"Ground state shape: {dataset_gs['ground_state'].shape}")
    print(f"Local magnetization: {dataset_gs['local_magnetization']}")
    print(f"Entanglement entropies: {np.array(dataset_gs['entanglement_entropies'])}")
    
    # Example 2: Multi-state dataset with degeneracy weighting
    print("\n" + "="*70)
    print("EXAMPLE 2: Ground State + 3 Excited States (with degeneracy weighting)")
    print("="*70)
    dataset_ms = build_ising_1d_open_dataset(
        num_sites=8,
        J=1.0,
        h=0.5,
        num_excited=3,
        weight_by_degeneracy=True
    )
    
    print(f"\nDataset: {dataset_ms['name']}")
    print(f"Number of states: {dataset_ms['num_states']}")
    print(f"All energies: {dataset_ms['all_energies']}")
    print(f"State weights sum: {np.sum(dataset_ms['state_weights']):.6f}")
    
    if 'excited_states' in dataset_ms:
        print(f"\nExcited states stored: {len(dataset_ms['excited_states'])}")
        print(f"Excited energies: {dataset_ms['excited_energies']}")
    
    print("\n" + "="*70 + "\n")
