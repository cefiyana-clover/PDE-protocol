"""
ISB-PDE Protocol: The Grand Assembly (Operation 2C)
---------------------------------------------------------------------
Executes the unified Spatiotemporal Reaction-Diffusion system.
Integrates the empirical Graph Laplacian (Operation 2A) and localized 
transcriptomic parameters (Operation 2B) to evaluate theoretical 
systemic excitotoxicity across 148 anatomical brain regions.
"""

import numpy as np
from scipy.integrate import solve_ivp
import warnings

warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# 1. BIOPHYSICAL CONSTANTS & BOUNDARY INITIALIZATION
# ---------------------------------------------------------
print("1. Initializing thermodynamic constants and boundary conditions...")
V_MAX_BASE = 5.0   
K_ATP = 0.5        
K_M = 1.0          
C_BASAL = 0.2      
DIFFUSION_COEFF = 0.1 
PaCO2_ENV = 39.2

# Retrieving spatial dimensions established in Op 2A/2B
NUM_NODES = Laplacian_L.shape[0] # Should be exactly 148

# ---------------------------------------------------------
# 2. PDE ENGINE (SPATIOTEMPORAL THERMODYNAMICS)
# ---------------------------------------------------------
def empirical_spatiotemporal_bioenergetics(t, state_vector, L, P_basal, R_stress, PaCO2):
    """
    Evaluates reaction-diffusion kinetics across MNI152 parcellated space.
    State vector: [ATP_0...ATP_147, Glutamate_0...Glutamate_147]
    """
    # Bifurcating the 296-dimensional state vector
    A = np.clip(state_vector[:NUM_NODES], 1e-5, None)
    G = np.clip(state_vector[NUM_NODES:], 1e-5, None)
    
    # Oxygenation kinetics (Vascular constraints)
    k_v, beta = 7.0 / 200.0, 1.0 / 10.0
    phi_vaso = np.exp(k_v * (PaCO2 - 40.0))
    phi_bohr = 1.0 / (1.0 + 10**(beta * (40.0 - PaCO2)))
    
    # Localized bioenergetic production (utilizing transcriptomic P_basal)
    P_ATP_current = P_basal * phi_vaso * phi_bohr
    
    # Michaelis-Menten Clearance Kinetics
    V_GLT1 = V_MAX_BASE * (A / (K_ATP + A)) * (G / (K_M + G))
    
    # EXPLICIT ASSUMPTION (Rule 10): Intracellular ATP remains localized; Glutamate diffuses.
    dA_dt = P_ATP_current - C_BASAL - (4.0 * V_GLT1)
    
    # The PDE Core: Network diffusion term via empirical Graph Laplacian
    diffusion_term = -DIFFUSION_COEFF * np.dot(L, G)
    dG_dt = diffusion_term + R_stress - V_GLT1 
    
    return np.concatenate([dA_dt, dG_dt])

# ---------------------------------------------------------
# 3. SPATIOTEMPORAL INTEGRATION EXECUTION
# ---------------------------------------------------------
print(f"\n2. Priming localized initial states across {NUM_NODES} anatomical regions...")
# Homeostatic baseline
A_initial = np.full(NUM_NODES, 3.0)
G_initial = np.full(NUM_NODES, 0.2)

# IN SILICO PERTURBATION (Rule 12): Inducing an isolated excitotoxic load
# Injecting concentrated glutamate strictly into Node 0 to observe spatiotemporal propagation
G_initial[0] = 5.0  

initial_state = np.concatenate([A_initial, G_initial])
time_span = (0, 100)
t_eval = np.linspace(0, 100, 200) 

print("3. Executing stiff PDE integration (Radau method) over MNI152 coordinate space. Matrix diffusion underway...")

solution = solve_ivp(
    fun=empirical_spatiotemporal_bioenergetics,
    t_span=time_span,
    y0=initial_state,
    t_eval=t_eval,
    args=(Laplacian_L, P_basal_spatial, R_stress_spatial, PaCO2_ENV),
    method='Radau' 
)

# ---------------------------------------------------------
# 4. TERMINAL STATE ANALYSIS (SYSTEMIC COLLAPSE EVALUATION)
# ---------------------------------------------------------
print("\n--- SPATIOTEMPORAL BIFURCATION OUTPUT (IN SILICO) ---")
# Evaluating the focal point (Node 0), an adjacent region (Node 1), and a highly distal cortical region (Node 147)
final_G_node_0 = solution.y[NUM_NODES + 0, -1]
final_G_node_1 = solution.y[NUM_NODES + 1, -1]
final_G_node_147 = solution.y[NUM_NODES + 147, -1]

final_ATP_node_1 = solution.y[1, -1]
final_ATP_node_147 = solution.y[147, -1]

print(f"Focal Injection Region (Node 0)      : Terminal Glutamate = {final_G_node_0:.4f} mM")
print(f"Adjacent Anatomical Region (Node 1)  : Terminal Glutamate = {final_G_node_1:.4f} mM | ATP = {final_ATP_node_1:.4f} mM")
print(f"Distal Cortical Region (Node 147)    : Terminal Glutamate = {final_G_node_147:.4f} mM | ATP = {final_ATP_node_147:.4f} mM")
print("\nAnalysis: Indicates whether theoretical topological diffusion is sufficient to induce systemic astrocytic bifurcation (ATP < 0.5 mM) across distal anatomical nodes.")
print("ISB-PDE Empirical Pipeline Execution Complete.")
