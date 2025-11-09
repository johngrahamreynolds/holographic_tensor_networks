# Example Tensor Networks

This directory contains a variety of examples implementing various tensor networks. As discussed in [Evenbly and Vidal's review](../../references/EvenblyVidal_TensorNetsAndGeometry.pdf), the geometric structure of a tensor network state can be classified as either *physical* or *holographic*. We partition this section accordingly and connect each class to related algorithmic and geometric perspectives elsewhere in the repo.

## Physical Geometry

In a quantum many-body problem where particles are situated on a D-dimensional lattice *L*, the Hamiltonian *H* of interactions between neighboring states in *L* forms a *physical geometry* of the system. Given a short–range set of interactions in *H*––that is, only particles close to one another in *L* have interaction terms–– the physical geometry associated with the Hamiltonian is also D-dimensional and is essentially equivalent to the geometry of the lattice itself. An important class of tensor networks are those whose tensors are connected in lattice so as to recreate this physical geometry.

Examples include:

- [Matrix Product States (MPS)](./mps/)

- [Projected Entangled Pair States (PEPS)](./peps/)

## Holographic Geometry

Holographic tensor networks associate to a D-dimensional physical system an additional dimension, understood as an emergent length or energy scale, generated from entanglement in the ground state |ψ<sub>GS</sub>⟩ of the Hamiltonian *H*. As such, the (D + 1)-dimensional geometry generated in this way from the entanglement in the ground state |ψ<sub>GS</sub>⟩ is called a *holographic geometry*. This naming is motivated by the holographic principle. 

Of particular interest to our study is the best known realization of the holographic principle, known as the Anti-de Sitter/Conformal Field Theory (AdS/CFT) correspondence, which proposes an exact duality between a D-dimensional, gravity-free boundary CFT living on the codimension-one conformal boundary of gravitational, (D + 1)-dimensional AdS. Put simply, AdS/CFT proposes an exact relationship between gravitational and non-gravitational physics in dimensions which differ by 1. Holographic tensor networks, by their manifestation of an emergent additional dimension through ground state entanglement, propose an exciting avenue to better understand this duality.

Examples of tensor networks with manifest holographic geometry include:

- [Multiscale Entanglement Renormalization ansatz (MERA)](./mera/)

- [Hyper-invariant Tensor Networks](./hyperinvariant/)

## See Also

- Canonical quantum algorithms as tensor networks: [`../quantum_algorithms/`](../quantum_algorithms/)
- Quantum machine learning: [`../quantum_machine_learning/`](../quantum_machine_learning/)
- Loop quantum gravity (spin networks, spin foams): [`../loop_quantum_gravity/`](../loop_quantum_gravity/)
- Background literature: [`../../references/`](../../references/)
- Utilities: [`../utils/`](../utils/)

