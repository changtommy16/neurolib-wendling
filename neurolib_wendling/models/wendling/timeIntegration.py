import numpy as np
import numba
from numba import njit

from neurolib.utils import model_utils as mu


def timeIntegration(params):
    """Time integration for Wendling Neural Mass Model.
    
    Implements the 10-ODE Wendling-Chauvel model with RK4 or Euler integration.
    Supports both single node and whole-brain network simulations.
    
    :param params: Parameter dictionary of the model
    :type params: dict
    :return: Integrated activity variables (t, y0, y1, ..., y9)
    :rtype: tuple of numpy.ndarray
    """
    
    dt = params["dt"]  # Time step (ms)
    duration = params["duration"]  # Simulation duration (ms)
    RNGseed = params["seed"]  # Random seed
    
    # Set random seed if provided
    if RNGseed is not None:
        np.random.seed(RNGseed)
    
    # ------------------------------------------------------------------------
    # Local parameters
    # ------------------------------------------------------------------------
    A = params["A"]
    B = params["B"]
    G = params["G"]
    a = params["a"]
    b = params["b"]
    g = params["g"]
    C1 = params["C1"]
    C2 = params["C2"]
    C3 = params["C3"]
    C4 = params["C4"]
    C5 = params["C5"]
    C6 = params["C6"]
    C7 = params["C7"]
    p_mean = params["p_mean"]
    p_sigma = params["p_sigma"]
    e0 = params["e0"]
    v0 = params["v0"]
    r = params["r"]
    sigmoid_type = params.get("sigmoid_type", "wendling2002")
    integration_method = params.get("integration_method", "rk4")
    
    # ------------------------------------------------------------------------
    # Global coupling parameters
    # ------------------------------------------------------------------------
    Cmat = params["Cmat"]
    N = len(Cmat)  # Number of nodes
    K_gl = params["K_gl"]  # Global coupling strength
    lengthMat = params["lengthMat"]
    signalV = params["signalV"]
    
    if N == 1:
        Dmat = np.zeros((N, N))
    else:
        # Compute delay matrix
        Dmat = mu.computeDelayMatrix(lengthMat, signalV)
        Dmat[np.eye(len(Dmat)) == 1] = np.zeros(len(Dmat))
    
    Dmat_ndt = np.around(Dmat / dt).astype(int)  # Delay matrix in multiples of dt
    
    # ------------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------------
    t = np.arange(1, round(duration, 6) / dt + 1) * dt  # Time vector (ms)
    
    max_global_delay = int(np.max(Dmat_ndt))
    startind = max_global_delay + 1  # Start index after initial conditions
    
    # State variable arrays
    y0_arr = np.zeros((N, startind + len(t)))
    y1_arr = np.zeros((N, startind + len(t)))
    y2_arr = np.zeros((N, startind + len(t)))
    y3_arr = np.zeros((N, startind + len(t)))
    y4_arr = np.zeros((N, startind + len(t)))
    y5_arr = np.zeros((N, startind + len(t)))
    y6_arr = np.zeros((N, startind + len(t)))
    y7_arr = np.zeros((N, startind + len(t)))
    y8_arr = np.zeros((N, startind + len(t)))
    y9_arr = np.zeros((N, startind + len(t)))
    
    # Set initial conditions
    if np.shape(params["y0_init"])[1] == 1:
        y0_arr[:, :startind] = np.dot(params["y0_init"], np.ones((1, startind)))
        y1_arr[:, :startind] = np.dot(params["y1_init"], np.ones((1, startind)))
        y2_arr[:, :startind] = np.dot(params["y2_init"], np.ones((1, startind)))
        y3_arr[:, :startind] = np.dot(params["y3_init"], np.ones((1, startind)))
        y4_arr[:, :startind] = np.dot(params["y4_init"], np.ones((1, startind)))
        y5_arr[:, :startind] = np.dot(params["y5_init"], np.ones((1, startind)))
        y6_arr[:, :startind] = np.dot(params["y6_init"], np.ones((1, startind)))
        y7_arr[:, :startind] = np.dot(params["y7_init"], np.ones((1, startind)))
        y8_arr[:, :startind] = np.dot(params["y8_init"], np.ones((1, startind)))
        y9_arr[:, :startind] = np.dot(params["y9_init"], np.ones((1, startind)))
    else:
        y0_arr[:, :startind] = params["y0_init"][:, -startind:]
        y1_arr[:, :startind] = params["y1_init"][:, -startind:]
        y2_arr[:, :startind] = params["y2_init"][:, -startind:]
        y3_arr[:, :startind] = params["y3_init"][:, -startind:]
        y4_arr[:, :startind] = params["y4_init"][:, -startind:]
        y5_arr[:, :startind] = params["y5_init"][:, -startind:]
        y6_arr[:, :startind] = params["y6_init"][:, -startind:]
        y7_arr[:, :startind] = params["y7_init"][:, -startind:]
        y8_arr[:, :startind] = params["y8_init"][:, -startind:]
        y9_arr[:, :startind] = params["y9_init"][:, -startind:]
    
    # Normalize connectivity matrix
    if N > 1:
        Cmat_normalized = Cmat / np.max(Cmat) if np.max(Cmat) > 0 else Cmat
    else:
        Cmat_normalized = Cmat
    
    # ------------------------------------------------------------------------
    # Integration (Unified Euler-Maruyama only)
    # ------------------------------------------------------------------------
    if integration_method == "rk4":
        raise ValueError("RK4 integration has been removed. Use integration_method='euler' instead.")
    
    # Use unified Euler-Maruyama integration (same core as _integrate_wendling_simple)
    # Convert units
    dt_s = dt / 1000.0  # ms to seconds
    a_s = a * 1000.0    # 1/ms to 1/s
    b_s = b * 1000.0
    g_s = g * 1000.0
    n_steps = len(t)
    
    # Prepare initial conditions (N, 10)
    y0_init_arr = np.zeros((N, 10), dtype=np.float64)
    for i in range(N):
        y0_init_arr[i, 0] = y0_arr[i, startind-1]
        y0_init_arr[i, 1] = y1_arr[i, startind-1]
        y0_init_arr[i, 2] = y2_arr[i, startind-1]
        y0_init_arr[i, 3] = y3_arr[i, startind-1]
        y0_init_arr[i, 4] = y4_arr[i, startind-1]
        y0_init_arr[i, 5] = y5_arr[i, startind-1]
        y0_init_arr[i, 6] = y6_arr[i, startind-1]
        y0_init_arr[i, 7] = y7_arr[i, startind-1]
        y0_init_arr[i, 8] = y8_arr[i, startind-1]
        y0_init_arr[i, 9] = y9_arr[i, startind-1]
    
    # Vectorize parameters (convert scalar to array if needed)
    # This must be done before calling JIT function to avoid numba issues
    A_vec = np.atleast_1d(A).astype(np.float64)
    B_vec = np.atleast_1d(B).astype(np.float64)
    G_vec = np.atleast_1d(G).astype(np.float64)
    p_mean_vec = np.atleast_1d(p_mean).astype(np.float64)
    
    # If scalar (length 1), expand to N nodes
    if len(A_vec) == 1 and N > 1:
        A_vec = np.full(N, A_vec[0], dtype=np.float64)
        B_vec = np.full(N, B_vec[0], dtype=np.float64)
        G_vec = np.full(N, G_vec[0], dtype=np.float64)
        p_mean_vec = np.full(N, p_mean_vec[0], dtype=np.float64)
    
    # Call unified integration
    result = _integrate_wendling_unified(
        y0_init_arr, n_steps, dt_s, N,
        A_vec, a_s, B_vec, b_s, G_vec, g_s,
        params["C"], C1, C2, C3, C4, C5, C6, C7,
        e0, v0, r, p_mean_vec, p_sigma,
        Cmat_normalized, K_gl, Dmat_ndt, max_global_delay
    )
    
    # Convert result (N, 10, n_steps) to separate arrays
    for i in range(N):
        y0_arr[i, startind:] = result[i, 0, :]
        y1_arr[i, startind:] = result[i, 1, :]
        y2_arr[i, startind:] = result[i, 2, :]
        y3_arr[i, startind:] = result[i, 3, :]
        y4_arr[i, startind:] = result[i, 4, :]
        y5_arr[i, startind:] = result[i, 5, :]
        y6_arr[i, startind:] = result[i, 6, :]
        y7_arr[i, startind:] = result[i, 7, :]
        y8_arr[i, startind:] = result[i, 8, :]
        y9_arr[i, startind:] = result[i, 9, :]
    
    return_arrays = (y0_arr, y1_arr, y2_arr, y3_arr, y4_arr,
                    y5_arr, y6_arr, y7_arr, y8_arr, y9_arr)
    
    # Return time vector and all state variables (including initial conditions)
    return (t,) + return_arrays


# ==================== Unified Euler-Maruyama Integration ====================
# Direct computation without intermediate function calls

@njit(cache=True, fastmath=True)
def _sigm_fast(v, e0, v0, r):
    """Fast sigmoid for numba."""
    return 2.0 * e0 / (1.0 + np.exp(r * (v0 - v)))


@njit(cache=True, fastmath=True)
def _integrate_wendling_unified(y0_arr, n_steps, dt, N,
                                 A, a, B, b, G, g,
                                 C, C1, C2, C3, C4, C5, C6, C7,
                                 e0, v0, r, p_mean, p_sigma,
                                 Cmat, K_gl, Dmat_ndt, max_delay):
    """
    Unified Euler-Maruyama integration for Wendling model.
    Handles both single node (N=1) and whole-brain network (N>1).
    Supports node-specific parameters (A, B, G, p_mean are arrays of length N).
    
    Units: dt in seconds, a/b/g in 1/s (not 1/ms).
    
    Args:
        y0_arr: Initial conditions (N, 10)
        N: Number of nodes
        A, B, G, p_mean: Arrays of length N (node-specific parameters)
        Cmat: Connectivity matrix (N, N) - set to zeros for single node
        K_gl: Global coupling strength - set to 0 for single node
        max_delay: Maximum delay steps - set to 0 for single node
    
    Returns:
        ys: State trajectories (N, 10, n_steps)
    """
    # Allocate arrays with delay buffer
    total_steps = n_steps + max_delay
    ys = np.zeros((N, 10, total_steps), dtype=np.float64)
    
    # Initialize
    for node in range(N):
        for i in range(10):
            ys[node, i, :max_delay] = y0_arr[node, i]
    
    # Time integration
    for k in range(n_steps):
        idx = max_delay + k
        
        for node in range(N):
            # Get node-specific parameters (A, B, G, p_mean are already arrays)
            A_node = A[node]
            B_node = B[node]
            G_node = G[node]
            p_mean_node = p_mean[node]
            
            # Current state
            y0_ = ys[node, 0, idx-1]
            y1 = ys[node, 1, idx-1]
            y2 = ys[node, 2, idx-1]
            y3 = ys[node, 3, idx-1]
            y4 = ys[node, 4, idx-1]
            y5 = ys[node, 5, idx-1]
            y6 = ys[node, 6, idx-1]
            y7 = ys[node, 7, idx-1]
            y8 = ys[node, 8, idx-1]
            y9 = ys[node, 9, idx-1]
            
            # Noise (use node-specific p_mean)
            xi_t = np.random.normal(0.0, 1.0)
            p_t = p_mean_node + p_sigma * xi_t * np.sqrt(dt) #Euler–Maruyama（with sqrt(dt))decreases the amplitude of output. \
            # if you want exact amplitude (larger) as in some papers, you can remove sqrt(dt).            
            # Coupling input
            coupling_input = 0.0
            for j in range(N):
                if Cmat[node, j] > 0:
                    delay_idx = idx - 1 - Dmat_ndt[node, j]
                    if delay_idx >= 0:
                        v_j = ys[j, 1, delay_idx] - ys[j, 2, delay_idx] - ys[j, 3, delay_idx]
                        coupling_input += K_gl * Cmat[node, j] * _sigm_fast(v_j, e0, v0, r)
            
            # Derivatives (use node-specific A, B, G)
            dy0 = y5
            dy5 = A_node * a * (_sigm_fast(y1 - y2 - y3, e0, v0, r) + coupling_input) - 2.0 * a * y5 - a * a * y0_
            
            dy1 = y6
            dy6 = A_node * a * (C2 * _sigm_fast(C1 * y0_, e0, v0, r) + p_t) - 2.0 * a * y6 - a * a * y1
            
            dy2 = y7
            dy7 = B_node * b * (C4 * _sigm_fast(C3 * y0_, e0, v0, r)) - 2.0 * b * y7 - b * b * y2
            
            dy3 = y8
            dy8 = G_node * g * (C7 * _sigm_fast((C5 * y0_ - C6 * y4), e0, v0, r)) - 2.0 * g * y8 - g * g * y3
            
            dy4 = y9
            dy9 = B_node * b * (_sigm_fast(C3 * y0_, e0, v0, r)) - 2.0 * b * y9 - b * b * y4
            
            # Euler update
            ys[node, 0, idx] = y0_ + dt * dy0
            ys[node, 1, idx] = y1 + dt * dy1
            ys[node, 2, idx] = y2 + dt * dy2
            ys[node, 3, idx] = y3 + dt * dy3
            ys[node, 4, idx] = y4 + dt * dy4
            ys[node, 5, idx] = y5 + dt * dy5
            ys[node, 6, idx] = y6 + dt * dy6
            ys[node, 7, idx] = y7 + dt * dy7
            ys[node, 8, idx] = y8 + dt * dy8
            ys[node, 9, idx] = y9 + dt * dy9
    
    # Return without delay buffer
    return ys[:, :, max_delay:]
