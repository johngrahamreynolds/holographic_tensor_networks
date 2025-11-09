# Quantum Machine Learning

## Overview

This directory houses implementations and examples of quantum machine learning algorithms. While related to the canonical quantum algorithms in [`../quantum_algorithms/`](../quantum_algorithms/), QML focuses on learning and optimization tasks rather than computational complexity advantages.

Quantum machine learning algorithms can be broadly categorized as either hybrid quantum-classical or purely quantum approaches. The hybrid paradigm leverages quantum circuits as parameterized models within classical optimization loops, while purely quantum approaches (still largely theoretical) aim for end-to-end quantum processing.

## Directory Structure

- **`hybrid/`**: Hybrid quantum-classical machine learning algorithms
  - Quantum Convolutional Neural Networks (QCNNs)
  - Variational Quantum Eigensolvers (VQE)
  - Quantum Approximate Optimization Algorithm (QAOA)
  - Quantum Neural Networks (QNNs)
  - Other variational quantum algorithms with ML applications

- **`purely_quantum/`**: Purely quantum machine learning approaches
  - Quantum kernel methods
  - Quantum support vector machines
  - Other fully quantum learning algorithms

## Connection to Tensor Networks

Many quantum machine learning algorithms can be understood through the lens of tensor networks:
- Parameterized quantum circuits are naturally represented as tensor networks
- The optimization landscape of variational algorithms relates to tensor network contraction complexity
- Quantum neural networks can be viewed as structured tensor networks with trainable parameters

For background on tensor networks and their geometric structure, see [`../tensor_networks/`](../tensor_networks/).

## See Also

- Canonical quantum algorithms: [`../quantum_algorithms/`](../quantum_algorithms/)
- Tensor network implementations: [`../tensor_networks/`](../tensor_networks/)
- Background literature: [`../../references/`](../../references/)

