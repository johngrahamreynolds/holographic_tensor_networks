# Example Tensor Networks

This directory contains a variety of examples implementing various tensor networks. As discussed in [Evenbly and Vidal's review](../references/EvenblyVidal_TensorNetsAndGeometry.pdf), the geometric structure of a tensor network state can be classified as either *physical* or *holographic*. We partition this section of examples accordingly.

## Physical Geometry

In a quantum many-body problem where particles are situated on a D-dimensional lattice *L*, the Hamiltonian *H* of interactions between neighboring states in *L* forms a *physical geometry* of the system. Given a short–range set of interactions in *H*––that is, only particles close to one another in *L* have iteractions terms–– the physical geometry associated with the Hamiltonian is also D-dimensional and is essentially equivalent to the geometry of the lattice itself. An important class of tensor networks are those whose tensors are connected in lattice so as to recreate this physical geometry.

Examples include:

- [Matrix Product States (MPS)](./mps/)

- [Projected Entangled Pair States (PEPS)](./peps/)

## Holographic Geometry

Holographic tensor networks 

Examples include: MERA, hyper-invariant tensor networks, etc.

[Multiscale Entanglement Renormalization ansatz (MERA)](./mera/)

[Hyper-invariant Tensor Networks](./hyperinvariant/)

