"""
Standard Parameter Sets for Wendling Model

These parameters have been verified through single-node validation 
Source: Validation_for_single_node/test_six_types_strict.py
Verification plot: results/validation/single_vs_multi_verification.png

Use cases:
1. Standard reference for single-node testing
2. Ground truth for multi-node verification
3. Baseline parameters for research and debugging

Usage:
    from STANDARD_PARAMETERS import WENDLING_STANDARD_PARAMS
    params = WENDLING_STANDARD_PARAMS['Type4']
    model.params['B'] = params['B']
    model.params['G'] = params['G']
"""

# ============================================================================
# VERIFIED WENDLING PARAMETERS (Single-Node Validation)
# ============================================================================
# Important Update (2025-10-14):
# Testing confirms p_sigma=2.0 produces correct waveforms for all 6 types
# Previously thought Type1, 2, 4, 5 needed p_sigma=30.0, but p_sigma=2.0 works better
# All types now uniformly use p_sigma=2.0 (low noise, reveals intrinsic dynamics)
WENDLING_STANDARD_PARAMS = {
    'Type1': {
        'name': 'Type 1: Background activity',
        'description': 'Normal background activity, slow waves (1-7 Hz)',
        'params': {
            'A': 5.0,      # Excitatory gain (mV)
            'B': 50,       # Slow inhibitory gain (mV)
            'G': 15,       # Fast inhibitory gain (mV)
            'p_mean': 90,  # Mean input (Hz)
            'p_sigma': 2.0  # Input noise (Hz)
        },
        'expected': {
            'freq_range': (1, 7),   # Hz
            'pattern': 'background',
            'amplitude': 'low',
            'description': 'Slow background waves, low amplitude'
        }
    },
    
    'Type2': {
        'name': 'Type 2: Sporadic spikes',
        'description': 'Sporadic spikes (1-5 Hz)',
        'params': {
            'A': 5.0,
            'B': 40,
            'G': 15,
            'p_mean': 90,
            'p_sigma': 2.0
        },
        'expected': {
            'freq_range': (1, 5),
            'pattern': 'sporadic_spikes',
            'amplitude': 'medium-high',
            'description': 'Occasional spikes with irregular timing'
        }
    },
    
    'Type3': {
        'name': 'Type 3: Sustained SWD (Spike-Wave Discharge)',
        'description': 'Sustained spike-wave, epileptic activity (3-6 Hz)',
        'params': {
            'A': 5.0,
            'B': 25,
            'G': 15,
            'p_mean': 90,
            'p_sigma': 2.0  # Low noise for sustained oscillations
        },
        'expected': {
            'freq_range': (3, 6),
            'pattern': 'sustained_SWD',
            'amplitude': 'high',
            'description': 'Epileptic spike-and-wave discharges, regular ~3-4 Hz'
        }
    },
    
    'Type4': {
        'name': 'Type 4: Alpha-like rhythm',
        'description': 'Slow rhythmic activity, alpha-like (8-13 Hz)',
        'params': {
            'A': 5.0,
            'B': 10,       # Low B for alpha rhythm
            'G': 15,
            'p_mean': 90,
            'p_sigma': 2.0
        },
        'expected': {
            'freq_range': (8, 13),
            'pattern': 'alpha-like',
            'amplitude': 'medium',
            'description': 'Regular alpha rhythm, typical resting state'
        }
    },
    
    'Type5': {
        'name': 'Type 5: Low-voltage fast activity (LVFA)',
        'description': 'Low-voltage fast activity (10-20 Hz)',
        'params': {
            'A': 5.0,
            'B': 5,        # Very low B
            'G': 25,       # High G
            'p_mean': 90,
            'p_sigma': 2.0
        },
        'expected': {
            'freq_range': (10, 20),
            'pattern': 'LVFA',
            'amplitude': 'low',
            'description': 'Low amplitude, high frequency, desynchronized'
        }
    },
    
    'Type6': {
        'name': 'Type 6: Quasi-sinusoidal',
        'description': 'Slow quasi-sinusoidal activity (9-13 Hz)',
        'params': {
            'A': 5.0,
            'B': 15,
            'G': 0,        # No fast inhibition!
            'p_mean': 90,
            'p_sigma': 2.0  # Low noise
        },
        'expected': {
            'freq_range': (9, 13),
            'pattern': 'quasi-sinusoidal',
            'amplitude': 'medium',
            'description': 'Smooth, regular oscillations, sinusoidal-like'
        }
    }
}

# ============================================================================
# PARAMETER RANGES SUMMARY
# ============================================================================

PARAMETER_RANGES = {
    'B': {
        'min': 5,    # Type 5 (LVFA)
        'max': 50,   # Type 1 (Background)
        'normal': (10, 30),  # Most common range
        'epileptic': (30, 50),  # Risk of Type 3 SWD
    },
    'G': {
        'min': 0,    # Type 6 (no fast inhibition)
        'max': 25,   # Type 5 (LVFA)
        'normal': (12, 20),  # Most common range
    },
    'A': {
        'standard': 5.0,  # Fixed in most cases
    },
    'p_mean': {
        'standard': 90,  # Fixed in most cases
    },
    'p_sigma': {
        'standard': 2.0,  # All types uniformly use 2.0 (verified)
        'note': 'Low noise (p_sigma=2.0) allows system to show intrinsic dynamics',
        # 'high_noise': 30.0,  # Not recommended: disrupts regularity
    }
}

# ============================================================================
# RECOMMENDED PARAMETERS FOR WHOLE-BRAIN NETWORKS
# ============================================================================

WHOLE_BRAIN_RECOMMENDATIONS = {
    'conservative': {
        'B_base': 22.0,
        'G_base': 18.0,
        'heterogeneity': 0.20,
        'K_gl': 0.15,
        'description': 'Safe, minimal Type 3 risk, moderate diversity'
    },
    
    'balanced': {
        'B_base': 23.0,
        'G_base': 17.0,
        'heterogeneity': 0.30,
        'K_gl': 0.15,
        'description': 'Good diversity, low Type 3 risk, recommended default'
    },
    
    'diverse': {
        'B_base': 25.0,
        'G_base': 17.0,
        'heterogeneity': 0.50,
        'K_gl': 0.10,
        'description': 'High diversity, includes Type 1 and Type 3, monitor closely'
    },
    
    'six_types': {
        'description': 'Assign each node a different activity type manually',
        'example': {
            'Node 0': WENDLING_STANDARD_PARAMS['Type1']['params'],
            'Node 1': WENDLING_STANDARD_PARAMS['Type2']['params'],
            'Node 2': WENDLING_STANDARD_PARAMS['Type3']['params'],
            'Node 3': WENDLING_STANDARD_PARAMS['Type4']['params'],
            'Node 4': WENDLING_STANDARD_PARAMS['Type5']['params'],
            'Node 5': WENDLING_STANDARD_PARAMS['Type6']['params'],
        }
    }
}

# ============================================================================
# VALIDATION STATUS
# ============================================================================

VALIDATION_INFO = {
    'single_node_verified': True,
    'multi_node_verified': True,
    'verification_file': 'tests/validation/VERIFY_MULTINODE_CORRECT.py',
    'verification_result': 'results/validation/single_vs_multi_verification.png',
    'validation_date': '2025-10-14',
    'last_updated': '2025-10-14',
    'status': 'All 6 types verified with p_sigma=2.0 ✅',
    'notes': [
        'All 6 types use p_sigma=2.0 (low noise)',
        'p_sigma=2.0 allows intrinsic dynamics to dominate',
        'All parameters produce expected waveforms in single-node',
        'Multi-node (het=0, K_gl=0) matches single-node exactly',
        'Frequency differences < 0.5 Hz',
        'Amplitude differences < 5%',
        '⚠️ All types now compatible in multi-node networks (same p_sigma)',
    ]
}

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print("WENDLING MODEL - STANDARD PARAMETERS")
    print("="*80)
    
    print("\n📋 Verified Parameter Sets:\n")
    for type_name, type_info in WENDLING_STANDARD_PARAMS.items():
        params = type_info['params']
        expected = type_info['expected']
        print(f"{type_name}: {type_info['name']}")
        print(f"  B={params['B']:<4.0f} G={params['G']:<4.0f} | "
              f"Freq: {expected['freq_range'][0]}-{expected['freq_range'][1]} Hz | "
              f"{type_info['description']}")
    
    print("\n" + "="*80)
    print("WHOLE-BRAIN NETWORK RECOMMENDATIONS")
    print("="*80)
    
    for profile_name, profile_info in WHOLE_BRAIN_RECOMMENDATIONS.items():
        if profile_name == 'six_types':
            continue
        print(f"\n{profile_name.upper()}:")
        print(f"  B_base: {profile_info['B_base']}")
        print(f"  G_base: {profile_info['G_base']}")
        print(f"  heterogeneity: {profile_info['heterogeneity']}")
        print(f"  K_gl: {profile_info['K_gl']}")
        print(f"  → {profile_info['description']}")
    
    print("\n" + "="*80)
    print("VALIDATION STATUS")
    print("="*80)
    print(f"✅ Single-node: {VALIDATION_INFO['single_node_verified']}")
    print(f"✅ Multi-node: {VALIDATION_INFO['multi_node_verified']}")
    print(f"📅 Validated: {VALIDATION_INFO['validation_date']}")
    print(f"📊 Verification: {VALIDATION_INFO['verification_result']}")
    print("="*80)
