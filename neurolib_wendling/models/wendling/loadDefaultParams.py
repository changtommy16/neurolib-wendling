import numpy as np
from neurolib.utils.collections import dotdict


def generateRandomICs(N, seed=None):
    """
    Generate random initial conditions for Wendling model.
    
    Similar to ALN's generateRandomICs() - provides different starting points
    for each node to break synchronization in whole-brain networks.
    
    :param N: Number of nodes
    :type N: int
    :param seed: Random seed
    :type seed: int, optional
    :return: Tuple of 10 initial condition arrays (N, 1)
    :rtype: tuple
    """
    np.random.seed(seed)
    
    # Membrane potentials: small random perturbations around 0
    # Range based on typical physiological values
    y0_init = np.random.uniform(-0.5, 0.5, (N, 1))  # mV
    y1_init = np.random.uniform(-0.5, 0.5, (N, 1))  # mV
    y2_init = np.random.uniform(-0.5, 0.5, (N, 1))  # mV
    y3_init = np.random.uniform(-0.5, 0.5, (N, 1))  # mV
    y4_init = np.random.uniform(-0.5, 0.5, (N, 1))  # mV
    
    # Derivatives: small random perturbations near zero
    y5_init = np.random.uniform(-0.1, 0.1, (N, 1))
    y6_init = np.random.uniform(-0.1, 0.1, (N, 1))
    y7_init = np.random.uniform(-0.1, 0.1, (N, 1))
    y8_init = np.random.uniform(-0.1, 0.1, (N, 1))
    y9_init = np.random.uniform(-0.1, 0.1, (N, 1))
    
    return (
        y0_init, y1_init, y2_init, y3_init, y4_init,
        y5_init, y6_init, y7_init, y8_init, y9_init
    )


def loadDefaultParams(Cmat=None, Dmat=None, seed=None, sigmoid_type="wendling2002", random_init=True, heterogeneity=0.0):
    """Load default parameters for the Wendling Neural Mass Model.
    
    This implements the Wendling-Chauvel model (Wendling et al., 2002)
    with 10 ODEs representing pyramidal cells, excitatory interneurons,
    slow inhibitory interneurons, and fast inhibitory interneurons.
    
    References:
    - Wendling, F., Bartolomei, F., Bellanger, J. J., & Chauvel, P. (2002). 
      Epileptic fast activity can be explained by a model of impaired GABAergic 
      dendritic inhibition. European Journal of Neuroscience, 15(9), 1499-1508.
    - Köksal Ersöz, E., et al. (2020). Neural mass modeling of slow-fast dynamics 
      of seizure initiation and abortion. PLoS Computational Biology, 16(11), e1008430.

    :param Cmat: Structural connectivity matrix (adjacency matrix), defaults to None
    :type Cmat: numpy.ndarray, optional
    :param Dmat: Fiber length matrix for delay computation, defaults to None
    :type Dmat: numpy.ndarray, optional
    :param seed: Seed for the random number generator, defaults to None
    :type seed: int, optional
    :param sigmoid_type: Sigmoid variant ("wendling2002" or "pcbi2020"), defaults to "wendling2002"
    :type sigmoid_type: str, optional
    :param random_init: Whether to use random initial conditions (True for whole-brain, False for classic waveforms), defaults to True
    :type random_init: bool, optional
    :param heterogeneity: Node heterogeneity level (0.0 = no heterogeneity, 0.1 = 10% variation, 0.2 = 20% variation), defaults to 0.0
    :type heterogeneity: float, optional
    :return: Dictionary with default parameters
    :rtype: dict
    """
    
    params = dotdict({})
    
    ### Runtime parameters (MATCHED TO WORKING CODE)
    params.dt = 0.1  # Time step (ms) = 0.0001 s (10 kHz sampling)
    params.duration = 10000  # Simulation duration (ms) - 10s
    np.random.seed(seed)
    params.seed = seed
    
    # Sigmoid type
    params.sigmoid_type = sigmoid_type
    
    # ------------------------------------------------------------------------
    # Global whole-brain network parameters
    # ------------------------------------------------------------------------
    
    params.signalV = 20.0  # Signal transmission speed (m/s)
    params.K_gl = 0.5  # Global coupling strength
    
    if Cmat is None:
        params.N = 1
        params.Cmat = np.zeros((1, 1))
        params.lengthMat = np.zeros((1, 1))
    else:
        params.Cmat = Cmat.copy()
        np.fill_diagonal(params.Cmat, 0)
        params.N = len(params.Cmat)
        params.lengthMat = Dmat if Dmat is not None else np.zeros_like(Cmat)
    
    # ------------------------------------------------------------------------
    # Local node parameters (Wendling 2002 defaults)
    # ------------------------------------------------------------------------
    
    # Base parameter values (reference values for single node or heterogeneity)
    # NOTE: Avoid Type 3 (epileptic SWD) by keeping B < 30 and G > 12
    A_base = 5.0   # Excitatory gain (mV)
    B_base = 22.0  # Slow inhibitory gain (mV) - reduced from 25 to avoid epileptic range
    G_base = 18.0  # Fast inhibitory gain (mV) - increased from 15 to stay in normal range
    p_mean_base = 90.0  # Mean input (Hz)
    
    # Node heterogeneity: vectorize parameters if requested
    if heterogeneity > 0 and params.N > 1:
        # Generate node-specific parameters with variation
        # Using seed for reproducibility
        np.random.seed(seed)
        # UPDATED: More symmetric variation for better diversity
        # While still avoiding epileptic range
        params.A = A_base * (1 + np.random.uniform(-heterogeneity, heterogeneity, params.N))
        params.B = B_base * (1 + np.random.uniform(-heterogeneity, heterogeneity, params.N))  # Full range: 15.4-28.6 @ het=0.3
        params.G = G_base * (1 + np.random.uniform(-heterogeneity, heterogeneity, params.N))  # Full range: 12.6-23.4 @ het=0.3
        params.p_mean = p_mean_base * (1 + np.random.uniform(-heterogeneity, heterogeneity, params.N))
        # Reset seed for other random operations
        np.random.seed(seed)
    else:
        # No heterogeneity or single node: use scalar (backward compatible)
        params.A = A_base
        params.B = B_base
        params.G = G_base
        params.p_mean = p_mean_base
    
    # Time constants (1/ms) - CORRECTED to match Wendling 2002 paper
    params.a = 100.0 / 1000.0  # 0.1 (1/ms) = 100 s^-1 (tau_a = 10 ms)
    params.b = 50.0 / 1000.0   # 0.05 (1/ms) = 50 s^-1 (tau_b = 20 ms) - STANDARD VALUE
    params.g = 500.0 / 1000.0  # 0.5 (1/ms) = 500 s^-1 (tau_g = 2 ms)
    
    # Connectivity constants
    params.C = 135.0  # Base connectivity constant
    params.C1 = 1.0 * 135.0   # C1 = C
    params.C2 = 0.8 * 135.0   # C2 = 0.8*C
    params.C3 = 0.25 * 135.0  # C3 = 0.25*C
    params.C4 = 0.25 * 135.0  # C4 = 0.25*C
    params.C5 = 0.3 * 135.0   # C5 = 0.3*C
    params.C6 = 0.1 * 135.0   # C6 = 0.1*C
    params.C7 = 0.8 * 135.0   # C7 = 0.8*C
    
    # External input noise parameter (not vectorized)
    params.p_sigma = 30     # Input noise std (Hz) 
    
    # External input (for input interface, similar to Hopf/ALN)
    params.p_ext = np.zeros((params.N,))  # External input to pyramidal cells (Hz)
    
    # Sigmoid parameters (Wendling 2002 form)
    params.e0 = 2.5   # Half of maximum firing rate (Hz)
    params.v0 = 6.0   # Firing threshold (mV)
    params.r = 0.56   # Sigmoid slope (1/mV)
    
    # Integration method
    params.integration_method = "euler"  # "rk4" or "euler" - using Euler to match original author's code
    
    # ------------------------------------------------------------------------
    # Initial conditions
    # ------------------------------------------------------------------------
    
    if random_init and params.N > 1:
        # Random initial conditions for whole-brain networks (to break synchronization)
        # Similar to ALN's approach
        (
            y0_init, y1_init, y2_init, y3_init, y4_init,
            y5_init, y6_init, y7_init, y8_init, y9_init
        ) = generateRandomICs(params.N, seed)
        
        params.y0_init = y0_init
        params.y1_init = y1_init
        params.y2_init = y2_init
        params.y3_init = y3_init
        params.y4_init = y4_init
        params.y5_init = y5_init
        params.y6_init = y6_init
        params.y7_init = y7_init
        params.y8_init = y8_init
        params.y9_init = y9_init
    else:
        # Zero initial conditions (for classic waveforms validation)
        # This matches the original Wendling 2002 paper and equilibrium-driven activities
        params.y0_init = np.zeros((params.N, 1))
        params.y1_init = np.zeros((params.N, 1))
        params.y2_init = np.zeros((params.N, 1))
        params.y3_init = np.zeros((params.N, 1))
        params.y4_init = np.zeros((params.N, 1))
        params.y5_init = np.zeros((params.N, 1))
        params.y6_init = np.zeros((params.N, 1))
        params.y7_init = np.zeros((params.N, 1))
        params.y8_init = np.zeros((params.N, 1))
        params.y9_init = np.zeros((params.N, 1))
    
    return params
