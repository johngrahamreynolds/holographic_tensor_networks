# Loop Quantum Gravity

## Overview

This directory contains implementations and studies related to spin networks and spin foams in loop quantum gravity (LQG). LQG is a background-independent approach to quantum gravity that quantizes geometry itself, rather than quantizing fundamentally extended objects (strings, branes, etc.) around a fixed background spacetime (and other fixed background fields). 

It's worth noting that many string theorists still argue that string theory, particularly string *field* theory, proposes a truly background-independent theory of quantum gravity; see [Tomasiello (2016), page 8](../../references/non_pdf_references.md#string-theory). While string theory remains the most popular framework for understanding a UV-complete theory of gravity, LQG and its constituent spin networks/foams can likely be studied more directly in this tensor network optimization approach, whereas connections to strings and branes are more implicit through AdS/CFT and holographic geometry.

## Connection to Tensor Networks

Spin networks and spin foams share deep mathematical connections with tensor networks:

- **Spin networks** are graphs with edges labeled by group representations (typically SU(2)) and vertices by intertwiners. They can be viewed as tensor networks where tensors are placed at vertices and contracted along edges.

- **Spin foams** are 2-complexes that provide a history or evolution of spin networks, similar to how tensor network renormalization provides flow between different scales.

- Both structures involve:
  - Graphical representations of quantum states
  - Entanglement and geometric interpretation
  - Renormalization and scale transformations
  - Connections to holographic principles

The study of spin networks and spin foams through tensor network methods offers promising avenues for:
- Efficient simulation of LQG states
- Understanding the emergence of classical geometry
- Connections to holographic tensor networks and AdS/CFT
- Variational methods for quantum gravity

## Directory Structure

- **`spin_networks/`**: Implementation of spin networks and related structures
  - Basis states and intertwiners
  - Spin network states as tensor networks
  - Geometric operators and observables

- **`spin_foams/`**: Implementation of spin foam models
  - Spin foam amplitudes
  - Path integrals and transition amplitudes
  - Connection to tensor network renormalization

## See Also

- Tensor networks: [`../tensor_networks/`](../tensor_networks/)
- Holographic geometry: [`../tensor_networks/mera/`](../tensor_networks/mera/), [`../tensor_networks/hyperinvariant/`](../tensor_networks/hyperinvariant/)
- Research questions: [`../../docs/questions.md`](../../docs/questions.md) (see question #3)
- Background literature: [`../../references/`](../../references/)

## References

Key papers on spin networks, spin foams, and their connection to tensor networks can be found in the `references/` directory. See also the broader literature on loop quantum gravity and its computational aspects.

### Textbooks
- **Tomasiello (2016)**: A. Tomasiello, *Geometry of String Theory Compactifications*. Cambridge University Press, 2016. See [`../../references/non_pdf_references.md#string-theory`](../../references/non_pdf_references.md#string-theory) for full reference.

