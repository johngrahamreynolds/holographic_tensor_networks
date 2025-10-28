# Computational Holography: Tensor Networks, RG Flow, and Emergent Geometry

This repo is home to my broad study of holographic tensor networks as an effective, phenomenological realization of the gauge/gravity duality conjecture in theoretical physics. The most famous example of this conjecture is the AdS/CFT correspondence, which we target as an initial starting point for novel computational study. 


The aim of this robust repo is to house all resources integral to the full scientific research process. As such, this project contains a variety of different components:
- Toy/Foundational Models
- Reproduction of Interesting Results from Literature
- A List of Relevant References (far from all encompassing)
- Novel Toy Model Computation, Optimization
- Systematic Study/Comparison of Models
- Generalized ML/Tensor Net Frameworks and Tooling for reuse
- Documentation, Struggles, Failures, Questions

I can be reached for questions or comments at:

{ johngrahamreynolds [at] utexas [dot] edu } OR { johngrahamreynolds [at] gmail [dot] com }


<div align="center">
  <img src="./pics/Escher_angels_and_devils.jpg" alt="Escher A and D" width="600"/>
  <br>
  <em>Circle Limit IV (1960), M.C. Escher</em>
</div>

## Abstract

## Setup

### Environment Setup (using Conda)

**Initial setup:**
```bash
# Create the conda environment
conda env create -f environment.yml

# Activate the environment
conda activate holo_tns

# Install all requirements with exact versions
pip install -r requirements.txt
```

**Development workflow:**

As you add packages with `pip install`, update `requirements.txt` to maintain reproducibility:

```bash
# After installing new packages, export exact versions
pip freeze > requirements.txt
```

This captures all installed packages (including transitive dependencies) with exact versions, ensuring full reproducibility for research purposes.

The project uses Python 3.11 for compatibility with modern tensor network libraries. GPU support can be added later by installing appropriate packages for your hardware (CuPy, JAX, Apex, etc.).

## Overview

## Experiments

## Appendices
