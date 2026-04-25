"""
ISB-PDE Protocol: Spatiotemporal Reaction-Diffusion on Brain Connectome
---------------------------------------------------------------------
Transforms the ISB from an ODE (Mean-Field) to a PDE (Spatial Network)
using a Graph Laplacian operator. Evaluates temporal bioenergetics 
across spatially distributed neural nodes (e.g., distinct brain regions).
"""

import numpy as np
import pandas as pd
import networkx as nx
from scipy.integrate import solve_ivp
import warnings

warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# 1. BIOPHYSICAL CONSTANTS & SPATIAL PARAMETERS
# ---------------------------------------------------------
V_MAX_BASE = 5.0   
K_ATP = 0.5        
K_M = 1.0          
C_BASAL = 0.2      
DIFFUSION_COEFF = 0.1 # Novel Parameter: Inter-nodal glutamate diffusion coefficient

# Cohort Parameterization (Modeling East Asian / EAS cohort with elevated R_stress)
PaCO2_ENV = 39.2

# ---------------------------------------------------------
# 2. SPATIAL MATRIX EXTRACTION & LAPLACIAN OPERATOR
# ---------------------------------------------------------
print("1. Constructing Spatial Connectome Architecture...")

NUM_NODES = 100 # Represents 100 distinct parcellated cortical/subcortical regions

# APPROACH 1: EMPIRICAL DTI INTEGRATION (Nilearn/Nibabel Pipeline)
# Intended for future implementation with empirical HCP DTI datasets:
# from nilearn import datasets, connectome
# dataset = datasets.fetch_atlas_destrieux_2009()
# adjacency_matrix = load_your_dti_tractography_here()

# APPROACH 2: MATHEMATICAL PROXY (Watts-Strogatz Small-World Topology)
# Simulates empirical structural connectome properties (high clustering, short characteristic path length)
brain_graph = nx.watts_strogatz_graph(n=NUM_NODES, k=10, p=0.1, seed=42)

# Extract Adjacency Matrix (A)
A_matrix = nx.to_numpy_array(brain_graph)

# Compute Degree Matrix (D)
degree_array = np.sum(A_matrix, axis=1)
D_matrix = np.diag(degree_array)

# DERIVE GRAPH LAPLACIAN OPERATOR (L = D - A)
# Functions as the spatial discrete diffusion operator (PDE equivalent)
Laplacian_L = D_matrix - A_matrix

print("Laplacian Operator successfully derived. Initializing spatial genetic parameterization...")

# ---------------------------------------------------------
# 3. SPATIAL DISTRIBUTION OF GENETIC PARAMETERS (GWAS)
# ---------------------------------------------------------
np.random.seed(42)
# Heterogeneous distribution of P_basal and R_stress capacities across 100 nodes
# Reflects theoretical asymmetric transcriptomic expression across varying brain regions
P_basal_spatial = np.random.normal(8.0, 0.2, NUM_NODES) 
R_stress_spatial = np.random.normal(1.0, 0.15, NUM_NODES) # EAS Scenario

# ---------------------------------------------------------
# 4. PDE SYSTEM (REACTION-DIFFUSION COUPLED SYSTEM)
# ---------------------------------------------------------
def spatiotemporal_bioenergetics(t, state_vector, L, P_basal, R_stress, PaCO2):
    """
    Spatiotemporal Reaction-Diffusion System. State vector contains 2x NUM_NODES:
    First half = ATP across all localized regions.
    Second half = Glutamate across all localized regions.
    """
    # Bifurcate state vector into spatial ATP (A) and Glutamate (G) arrays
    A = state_vector[:NUM_NODES]
    G = state_vector[NUM_NODES:]
    
    # Boundary constraint (precluding non-physiological negative arithmetic limits)
    A = np.clip(A, 1e-5, None)
    G = np.clip(G, 1e-5, None)
    
    # Non-linear oxygenation limitation functions (Reaction Kinetics)
    k_v, beta = 7.0 / 200.0, 1.0 / 10.0
    phi_vaso = np.exp(k_v * (PaCO2 - 40.0))
    phi_bohr = 1.0 / (1.0 + 10**(beta * (40.0 - PaCO2)))
    
    # Localized ATP production vector per spatial node
    P_ATP_current = P_basal * phi_vaso * phi_bohr
    
    # Localized ATP-Dependent Michaelis-Menten Clearance Kinetics
    V_GLT1 = V_MAX_BASE * (A / (K_ATP + A)) * (G / (K_M + G))
    
    # EQUATION 1: ATP Dynamics (Purely reactive; assuming intracellular ATP does not undergo inter-nodal diffusion)
    dA_dt = P_ATP_current - C_BASAL - (4.0 * V_GLT1)
    
    # EQUATION 2: Glutamate Dynamics (REACTION + PDE SPATIAL DIFFUSION)
    # Critical mechanism: Diffusion operator acting on spatial glutamate gradient
    # Glutamate accumulates locally prior to propagating to adjacent topological nodes
    diffusion_term = -DIFFUSION_COEFF * np.dot(L, G)
    dG_dt = diffusion_term + R_stress - V_GLT1 
    
    # Concatenate arrays into a 1D vector for numerical integration
    return np.concatenate([dA_dt, dG_dt])

# ---------------------------------------------------------
# 5. NUMERICAL INTEGRATION AND SPATIOTEMPORAL TRACKING
# ---------------------------------------------------------
print("Executing spatiotemporal numerical integration. Network diffusion underway...")

# Baseline Initialization (Homeostatic Equilibrium)
A_initial = np.full(NUM_NODES, 3.0)
G_initial = np.full(NUM_NODES, 0.2)

# SIMULATED LOCALIZED EXCITOTOXIC INJECTION (Spatiotemporal Target)
# Introducing concentrated glutamate load exclusively at Node 0 (e.g., theoretically representing the Amygdala)
# Designed to observe the spatiotemporal propagation of the excitotoxic wave across the network
G_initial[0] = 5.0  

initial_state = np.concatenate([A_initial, G_initial])
time_span = (0, 100)
t_eval = np.linspace(0, 100, 200) # Tracking across 200 temporal frames

# Utilizing solve_ivp for enhanced stability in stiff PDE/Reaction-Diffusion systems
solution = solve_ivp(
    fun=spatiotemporal_bioenergetics,
    t_span=time_span,
    y0=initial_state,
    t_eval=t_eval,
    args=(Laplacian_L, P_basal_spatial, R_stress_spatial, PaCO2_ENV),
    method='Radau' # Radau method selected for handling stiff differential equations
)

# ---------------------------------------------------------
# 6. WAVE PROPAGATION ANALYSIS
# ---------------------------------------------------------
print("\n--- SPATIOTEMPORAL DYNAMICS OUTPUT (WAVE PROPAGATION) ---")
# Extract terminal glutamate coordinates for focal point (Node 0), adjacent (Node 1), and distal nodes (Node 99)
final_G_node_0 = solution.y[NUM_NODES + 0, -1]
final_G_node_1 = solution.y[NUM_NODES + 1, -1]
final_G_node_99 = solution.y[NUM_NODES + 99, -1]

# Extract terminal ATP coordinates to evaluate whether excitotoxic diffusion induced bioenergetic collapse in adjacent nodes
final_ATP_node_1 = solution.y[1, -1]

print(f"Focal Glutamate Injection (Node 0)        : {final_G_node_0:.4f} mM")
print(f"Adjacent Propagated Area (Node 1)         : {final_G_node_1:.4f} mM")
print(f"Distal Theoretical Area (Node 99)         : {final_G_node_99:.4f} mM")
print(f"\nTerminal ATP at Adjacent Area (Node 1)    : {final_ATP_node_1:.4f} mM (Bifurcation threshold < 0.5)")

print("\nSpatiotemporal Reaction-Diffusion Simulation Complete.")
