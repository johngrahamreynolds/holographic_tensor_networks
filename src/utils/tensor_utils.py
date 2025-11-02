# Tensor Network Utilities
# Author: John Graham Reynolds
# Reusable components for tensor networks, quantum state representation and computation, etc.
# *************************************************************

import numpy as np
from scipy.sparse import kron
from functools import reduce
from typing import List, Union


# ============================================================================
# Pauli Matrices in the computational basis, we choose 16-bit precision for complex numbers
# ============================================================================

PAULI_I = np.array([[1, 0], [0, 1]], dtype=np.complex128)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

# ============================================================================
# Kronecker and Operator Product Utilities
# ============================================================================

def kron_product(matrices: List[Union[np.ndarray, any]]) -> Union[np.ndarray, any]:
    """
    Compute the Kronecker product of a list of matrices.
    
    This is a convenience wrapper around scipy.sparse.kron that uses functools.reduce
    to handle lists of arbitrary length. Works with both dense and sparse matrices.
    
    Args:
        matrices: List of matrices (numpy arrays or scipy sparse matrices)
    
    Returns:
        Kronecker product of all matrices in the list
    
    Example:
        >>> Z = np.array([[1, 0], [0, -1]])
        >>> I = np.eye(2)
        >>> result = kron_product([I, Z, I])  # I ⊗ Z ⊗ I
    """
    if not matrices:
        raise ValueError("Must provide at least one matrix")
    if len(matrices) == 1:
        return matrices[0]
    
    return reduce(kron, matrices)


def build_operator_at_site(operator: np.ndarray, site: int, num_sites: int, 
                          identity: np.ndarray = None) -> np.ndarray:
    """
    Construct a single-site operator acting on a specific site in a chain.
    
    Builds: I ⊗ ... ⊗ I ⊗ O_site ⊗ I ⊗ ... ⊗ I
    
    Args:
        operator: The single-site operator to place
        site: Index of the site where the operator acts (0-indexed)
        num_sites: Total number of sites in the chain
        identity: Identity matrix to use (default: 2×2 identity)
    
    Returns:
        Full operator as Kronecker product
    
    Example:
        >>> Z = np.array([[1, 0], [0, -1]])
        >>> op = build_operator_at_site(Z, site=3, num_sites=8)  # Z acts on site 3
    """
    if site < 0 or site >= num_sites:
        raise ValueError(f"Site index {site} out of range [0, {num_sites-1}]")
    
    if identity is None:
        identity = np.eye(2, dtype=operator.dtype)
    
    ops = [identity] * num_sites
    ops[site] = operator
    
    return kron_product(ops)


def build_two_site_operator(operator1: np.ndarray, site1: int, 
                            operator2: np.ndarray, site2: int, 
                            num_sites: int,
                            identity: np.ndarray = None) -> np.ndarray:
    """
    Construct a two-site operator acting on specific sites in a chain.
    
    Builds: I ⊗ ... ⊗ O1_site1 ⊗ I ⊗ ... ⊗ O2_site2 ⊗ I ⊗ ... ⊗ I
    
    Args:
        operator1: First operator
        site1: Index of first site (0-indexed)
        operator2: Second operator
        site2: Index of second site (0-indexed)
        num_sites: Total number of sites in the chain
        identity: Identity matrix to use (default: 2×2 identity)
    
    Returns:
        Full operator as Kronecker product
    
    Example:
        >>> Z = np.array([[1, 0], [0, -1]])
        >>> op = build_two_site_operator(Z, site1=2, Z, site2=5, num_sites=8)
    """
    if site1 < 0 or site1 >= num_sites or site2 < 0 or site2 >= num_sites:
        raise ValueError(f"Site indices out of range [0, {num_sites-1}]")
    if site1 == site2:
        raise ValueError("site1 and site2 must be different")
    
    if identity is None:
        identity = np.eye(2, dtype=operator1.dtype)
    
    ops = [identity] * num_sites
    ops[site1] = operator1
    ops[site2] = operator2
    
    return kron_product(ops)


# ============================================================================
# State Weighting Utilities
# ============================================================================

def compute_state_weights(eigenvalues: np.ndarray, 
                         num_excited: int = 0,
                         base_energy_weight: float = 1.0,
                         excited_weight: float = 0.1,
                         degeneracy_info: dict = None,
                         weight_by_degeneracy: bool = True) -> np.ndarray:
    """
    Compute training weights for multiple quantum states, optionally accounting for degeneracy.
    
    Implements a two-tier weighting scheme:
    1. Energy-based: Ground state gets higher weight than excited states
    2. Degeneracy-based: Weight is distributed equally among degenerate states
    
    Args:
        eigenvalues: Array of all eigenvalues (sorted)
        num_excited: Number of excited states to include (total states = num_excited + 1)
        base_energy_weight: Weight for the ground state (default: 1.0)
        excited_weight: Base weight for each excited state level (default: 0.1)
        degeneracy_info: Dictionary from check_degeneracies() with degenerate group info
        weight_by_degeneracy: If True, normalize weights within degenerate multiplets
    
    Returns:
        Array of weights (one per state) normalized to sum to 1.0
    
    Example:
        >>> eigenvalues = np.array([0.0, 1.0, 1.0, 1.0, 2.0])  # Degenerate level at E=1
        >>> deg_info = check_degeneracies(eigenvalues)
        >>> weights = compute_state_weights(eigenvalues, num_excited=4, 
        ...                                  degeneracy_info=deg_info,
        ...                                  weight_by_degeneracy=True)
        >>> # Ground gets 1.0, degenerate triplet shares 0.1, highest gets 0.05
    """
    num_states = min(num_excited + 1, len(eigenvalues))
    
    # Start with energy-based weights
    weights = np.array([base_energy_weight] + [excited_weight] * num_excited)
    weights = weights[:num_states]  # Trim if needed
    
    # Apply degeneracy correction if requested
    if weight_by_degeneracy and degeneracy_info is not None and degeneracy_info.get('has_degeneracies'):
        for group in degeneracy_info.get('degenerate_groups', []):
            # Only process groups within our num_states range
            group_in_range = [idx for idx in group if idx < num_states]
            if group_in_range:
                num_in_group = len(group_in_range)
                # Use weight from first state in group
                group_weight = weights[group_in_range[0]]
                # Distribute equally within multiplet
                weights[group_in_range] = group_weight / num_in_group
    
    # Normalize to sum to 1.0
    weights = weights / np.sum(weights)
    
    return weights
