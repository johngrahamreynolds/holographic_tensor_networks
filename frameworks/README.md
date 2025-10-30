# Frameworks

This directory houses internal tooling and frameworks for reuse across different tensor network methods.

## Purpose

- Share utilities across `tensor_networks/`, `quantum_algorithms/`, and `geometric_deep_learning/`
- Avoid duplication of data structures, contractions, visualization helpers, and training loops

## Suggested Use

- Import utilities here from examples and experiments rather than re-implementing
- Keep modules small and focused (e.g., I/O, tensor ops, plotting)

## Related

- Implementations: `../tensor_networks/`
- Algorithms as tensor networks: `../quantum_algorithms/`