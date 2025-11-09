# Questions

A running list of questions related to this program. Comments and Extensions gladly accepted.

## Mathematical Foundations

1. What can the field of Geometric Deep Learning tell us about the relationship between tensor networks and quantum state representations? 
    - Can different tensor networks (MERA, hyper-invariant TNs, etc.) come to be best understood in a foundational, geometric manner in the same way Geometric Deep Learning has attempted to generally unify the foundations of different neural architectures (Transformers, Convolutions, etc.)? 
    - Can this generalized understanding teach us something about the connection between tensor networks (+ more general structures) and holography?

2. Can we do tensor network state emulation of nontrivial quantum states known to describe black holes? 
    - Maldacena raises this question explicitly in [Maldacena_simple_quantum_bh](../references/Maldacena_Quantum_BH.pdf).
    - This paper [Rinaldi_quantum_simulation](../references/Rinaldi_Matrix_Model_Simulation.pdf) likewise attempts to address this question with quantum Monte Carlo, deep learning, and more. 
    - Another interesting but more complicated attempt in the framework of M-theory is the [MCSMC_lattice_gg](../references/MCSMC_lattice_gauge_gravity.pdf).

3. In the literature beyond strings, can we combine variational methods from both quantum physics and ML to simulate other models of quantum gravity (spin foams, loop quantum gravity, etc.)?

4. The *convolutions* of Convolutional Neural Networks (CNNs) use locality to optimally learn information about some dense tensor-like structure (images, videos, and other types of high-dimensional, pixelated data) with a minimal number free parameters where naive, fully connected linear layers are suboptimal, requiring a total number of parameters that is often many orders of magnitude larger. Furthermore, CNNs are more invariant (than other models) to symmetry transformations like rotations, shifts, resaclings, etc. that we recognize as valuable in physics. Can one apply these notion to physical (quantum) systems obeying locality in order to optimize computational simulations? 
    - Is there some deeper connection here to locality in spacetime that can be uncovered?
    - Recent work has proposed that bulk spacetime emerges from boundary quantum systems attempting to optimize their dynamics. See [Carrasco, et al.](../references/Carrasco_Gravitation_from_Computation.pdf)
    - There is an obvious connection here to QCNNs


## Computational Foundations

1. Tensor networks currently dominate research interest in algorithmic quantum many-body problem wavefunction emulation. How can modified Neural Tensor Networks improve this program?