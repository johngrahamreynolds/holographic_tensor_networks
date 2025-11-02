# Quantum Algorithms

## Overview

This directory houses example implementations of foundational quantum algorithms. The unifying perspective of this repository is that quantum circuits are naturally represented as tensor networks: gates correspond to tensors, wires to contracted indices, and full circuits to tensor network diagrams. This lens connects algorithmic quantum computing to the broader study of efficient tensor contractions, renormalization ideas, and emergent geometry explored elsewhere in the repo.

For background on tensor networks and their expressivity, see [Orús_intro](../../references/Orus_TensorNetworksIntro.pdf) and related materials in `references/`.

## Contents

- Deutsch–Jozsa: `deutsch–jozsa.ipynb`
  - Implements the Deutsch–Jozsa algorithm and highlights how the circuit maps to a small tensor network where the final measurement statistics arise from structured contractions.

## How to Use

1. Ensure the project environment is set up (see the root `README.md` for `conda` and `pip` instructions).
2. Open the notebooks in this directory with Jupyter or VS Code:
   - `jupyter lab` or `jupyter notebook`
3. Run cells top-to-bottom. Where relevant, notes will point out the tensor network interpretation (e.g., mapping gates to tensors and contractions along wires).

## Roadmap

Planned additions to broaden coverage and deepen tensor network connections:

- Grover's search (amplitude amplification as structured contractions)
- Quantum Fourier Transform (QFT) and phase estimation
- Simon's problem and hidden subgroup structure
- Variational algorithms (VQE/QAOA) and tensor network ansätze

Contributions that extend examples or add tensor-network-centric visualizations are welcome.

