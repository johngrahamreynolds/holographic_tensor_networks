# Geometric Deep Learning

Recent work in the mathematical foundations of machine learning has classified many deep learning architectures by their underlying network geometry. This field, known as *geometric deep learning*, may prove fruitful for studying emergent holographic geometry in tensor networks.  

<p align="center">
  <img src="../pics/Abstract_Composition_LeCorbusier.jpg" alt="Abstract Composition by Le Corbusier" width="320">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../pics/Transformer.png" alt="Transformer" width="320"><br>
  <sub>Abstract Composition (1927), Le Corbusier (Charles-Édouard Jeanneret)</sub>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <sub>Transformer Architecture (2017), Vaswani, et al.</sub>
</p>

## Non-Euclidean Optimization

Traditional machine learning methods typically perform (ideally convex) optimization to find extrema in high-dimensional, *Euclidean* latent spaces learned from labeled datasets. Neural networks are designed to efficiently discover features within this Euclidean framework. A key insight of geometric deep learning is extending optimization to more general, non-Euclidean manifolds—typically *Riemannian* or *pseudo-Riemannian*—with nontrivial metrics. By transforming the data space into these curved geometric spaces, hidden features and intrinsic characteristics of the dataset can be more naturally and effectively uncovered.

## Connections

- Tensor networks and geometry: see `../tensor_networks/`
- Quantum circuits as tensor networks: see `../quantum_algorithms/`


