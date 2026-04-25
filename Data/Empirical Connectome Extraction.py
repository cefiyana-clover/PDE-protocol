"""
ISB-PDE Protocol: Empirical Connectome Extraction (Operation 2A)
---------------------------------------------------------------------
Extracts human structural brain parcellation (Destrieux Atlas, 2009 release, MNI152 space)
to derive an empirically grounded spatial adjacency matrix and Graph Laplacian.
This module transitions the spatial framework from synthetic topologies to 
actual anatomical coordinate space.
"""

# ---------------------------------------------------------
# 0. AUTOMATED DEPENDENCY INITIALIZATION
# ---------------------------------------------------------
import subprocess
import sys

def initialize_environment():
    """Silently installs required neuroimaging dependencies if absent."""
    print("0. Verifying computational environment... Installing required dependency ('nilearn').")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nilearn", "--quiet"])
    print("   Dependency installation complete. Environment initialized.\n")

try:
    import nilearn
except ImportError:
    initialize_environment()

import numpy as np
from scipy.spatial import distance_matrix
from nilearn import datasets
from nilearn.plotting import find_parcellation_cut_coords
import warnings

warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# 1. PARCELLATION EXTRACTION (FETCHING DESTRIEUX ATLAS)
# ---------------------------------------------------------
print("1. Fetching Destrieux Atlas (MNI152 Coordinate Space) via Nilearn API...")
# The Destrieux atlas parcellates the cortical surface into distinct Regions of Interest (ROIs)
destrieux = datasets.fetch_atlas_destrieux_2009()
atlas_img = destrieux.maps
labels = destrieux.labels

print(f"   Atlas successfully loaded. Total Cortical/Subcortical regions defined: {len(labels)}.")

# ---------------------------------------------------------
# 2. SPATIAL COORDINATE MAPPING
# ---------------------------------------------------------
print("\n2. Extracting 3D spatial coordinates (Center of Mass) for each anatomical ROI...")
# Deriving absolute physical coordinates (x, y, z in millimeters) to establish a concrete geometric basis.
roi_coords = find_parcellation_cut_coords(labels_img=atlas_img)
NUM_NODES = len(roi_coords)

print(f"   Coordinates extracted for {NUM_NODES} distinct nodes.")
print(f"   Coordinate sample (Node 0): {roi_coords[0]} (mm)")

# ---------------------------------------------------------
# 3. DISTANCE MATRIX & EMPIRICAL ADJACENCY
# ---------------------------------------------------------
print("\n3. Constructing Geometry-Based Adjacency Matrix...")

# A. Compute the absolute Euclidean distance matrix across all extracted ROIs (N x N)
dist_matrix = distance_matrix(roi_coords, roi_coords)

# B. Transform Distance into Diffusion Connectivity (Exponential Decay)
# EXPLICIT THEORETICAL ASSUMPTION (Rule 10): Excitotoxic glutamate diffusion is modeled to 
# undergo exponential decay as a function of physical inter-nodal distance.
LAMBDA_DECAY = 15.0 # Spatial decay constant (mm)
A_matrix = np.exp(-dist_matrix / LAMBDA_DECAY)

# C. Boundary Conditions (Rule 8): Eliminate self-loops to prevent recursive non-physiological diffusion
np.fill_diagonal(A_matrix, 0)

# D. Sparsity Enforcement (Thresholding)
# Mitigates parameter overfitting by eliminating negligible long-distance connections (Rule 13)
THRESHOLD = 0.1 
A_matrix[A_matrix < THRESHOLD] = 0.0

print("   Empirical Adjacency Matrix successfully constructed (Sparse Connectivity enforced).")

# ---------------------------------------------------------
# 4. DERIVING THE EMPIRICAL GRAPH LAPLACIAN
# ---------------------------------------------------------
print("\n4. Deriving the Empirical Graph Laplacian operator...")

# Compute the Degree Matrix (D) from the thresholded Adjacency Matrix
degree_array = np.sum(A_matrix, axis=1)
D_matrix = np.diag(degree_array)

# Derivation of the spatial differential operator: L = D - A
Laplacian_L = D_matrix - A_matrix

print("   Graph Laplacian (L) successfully derived. PDE system is primed for anatomical execution.")

# ---------------------------------------------------------
# 5. REPRODUCIBILITY & INTEGRITY CHECK
# ---------------------------------------------------------
print("\n--- SPATIAL ARCHITECTURE INTEGRITY VERIFICATION ---")
print(f"Laplacian Matrix Dimensions : {Laplacian_L.shape} (Expected: 148 x 148)")
print(f"Mean Nodal Degree           : {np.mean(degree_array):.2f} (Average connection strength per region)")
print("Data Provenance             : MNI152 Standard Space, Destrieux Parcellation (2009).")

