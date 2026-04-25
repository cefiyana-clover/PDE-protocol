# Bioenergetic Stability Index (ISB): Spatiotemporal Reaction-Diffusion Architecture

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview
This repository contains the computational Python codebase for the **Bioenergetic Stability Index (ISB)** spatiotemporal framework. The protocol reconstructs severe psychiatric phenotypes (e.g., Major Depressive Disorder) as an emergent property of systemic bioenergetic instability, bridging localized temporal dynamics with connectome-wide spatial propagation. 

The mathematical framework advances from temporally isolated Coupled Ordinary Differential Equations (ODEs) to a Spatiotemporal Partial Differential Equation (PDE) system, utilizing a Graph Laplacian operator mapped onto the 148-node Destrieux Atlas.

This architecture explicitly operates as a **theoretical, mathematically tractable blueprint** intended for hypothesis generation and future prospective validation via *in vivo* high-resolution 1H-MRS imaging.

## Core Computational Modules

The codebase is structured into three primary operational phases to ensure multi-scale bridging and methodological transparency:

### 1. Empirical Connectome Mapping
* Extracts human structural brain parcellation (Destrieux Atlas, 2009 release, MNI152 coordinate space) utilizing `nilearn`.
* Computes absolute physical distances to derive an empirically grounded spatial adjacency matrix.
* Derives the explicit Graph Laplacian operator ($L = D - A$) to simulate inter-nodal glutamate diffusion, applying an exponential decay heuristic over physical distance.

### 2. Spatial Parameter Mapping
* Interfaces with the Allen Human Brain Atlas (AHBA) API via the `abagen` pipeline.
* Translates regional microarray expression data for key bioenergetic genes (e.g., *COX4I1* for mitochondrial capacity, *SLC1A2* for EAAT2 clearance) into anatomically localized thermodynamic parameters ($P_{basal}$ and $R_{stress}$).

### 3. System-Wide Reaction-Diffusion Integration
* Executes the coupled PDE system integrating the Laplacian matrix and spatial transcriptomics.
* Simulates a focal excitotoxic load (parameterized heuristically as $\Delta G = +5.0$ mM) at a localized seed region (Node 0).
* Evaluates the network using an implicit Radau solver (optimized for stiff spatiotemporal equations) to track the spatial propagation of excitotoxicity and the potential for a localized Saddle-Node Bifurcation to induce connectome-wide bioenergetic failure.

## Installation and Requirements

This codebase requires standard scientific computing libraries and specific neuroinformatics tools.

```bash
# Core dependencies
pip install numpy pandas scipy matplotlib networkx

# Neuroinformatics interfaces
pip install nilearn abagen

## Methodological Boundaries and Explicit Assumptions
​To ensure rigorous interpretation within the limits of computational biology, users of this protocol must acknowledge the following boundary conditions:
* ​Topological Limitations: The mathematical clearance capacity is strictly bounded. The model only operates up to the point of a theoretical Saddle-Node Bifurcation (ATP < 0.5 mM). It does not model cellular necrosis, apoptosis, or elastic rescue mechanisms post-bifurcation.
​* System Isolation: The reaction-diffusion framework explicitly isolates localized thermodynamic variables. It inherently excludes concurrent neuroendocrine feedback loops (e.g., HPA axis dynamics) and systemic inflammatory cascade effects.
* ​Transcriptomic Assumptions: The architecture parsimoniously assumes that regional mRNA expression correlates linearly with functional enzyme kinetics (V_{MAX}) at the astrocytic membrane, obscuring complex in vivo parameters such as localized cellular density and glial-neuronal stoichiometric ratios.
* ​AHBA Donor Cohort: The spatial parameters are derived from the AHBA, which utilizes a highly restricted donor cohort (N=6, predominantly Caucasian demographics). Extrapolating these spatial vectors to pan-ancestry population variances carries inherent structural biases.

## ​Reproducibility and Usage
​To reproduce the simulated spatiotemporal trajectory (as detailed in the manuscript's primary figures):
1. ​Ensure all dependencies are installed.
2. ​Execute the primary PDE execution script.
3. ​The console will output the terminal state analysis across the seed node (Node 0), adjacent nodes, and the most distal connectome node (Node 147), identifying whether the excitotoxic wave mathematically breached the bifurcation threshold.
​Note: Initializing the AHBA microarray extraction requires significant memory and may take several minutes to download localized gene expression data.
## ​Future Directions: The Stochastic Expansion
​The current codebase is deterministic. As outlined in the primary manuscript (Appendix A), future iterations of the ISB protocol will transcend these absolute boundaries by integrating Stochastic Differential Equations (SDEs) and Langevin dynamics. This expansion will model biological noise derived from continuous functional 1H-MRS, enabling the quantification of Critical Slowing Down prior to terminal collapse.
## ​License
​This research code is distributed under a Creative Commons Attribution-NonCommercial (CC BY-NC 4.0) license. It is openly accessible for academic review, replication, and non-commercial theoretical expansion.
## ​Contact
​For methodological inquiries or collaborative empirical validation utilizing in vivo neurometabolic imaging:
* ​Author: Cefiyana
* ​Email: leafcloverfive@gmail.com
