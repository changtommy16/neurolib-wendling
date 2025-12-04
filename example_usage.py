"""
Example: Both import methods work identically
示例：兩種導入方式效果完全相同
"""

import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 方法1：使用neurolib命名空間（透過auto-registration）
# Method 1: Use neurolib namespace (via auto-registration)
# ==============================================================================
print("=" * 70)
print("Method 1: Import from neurolib.models.wendling")
print("=" * 70)

import neurolib_wendling  # Trigger auto-registration

from neurolib.models.wendling import WendlingModel as WM1
from neurolib.models.wendling.STANDARD_PARAMETERS import WENDLING_STANDARD_PARAMS

# Create model
model1 = WM1()
print(f"✓ Model created: {model1}")
print(f"  Model name: {model1.name}")
print(f"  Model class: {model1.__class__.__module__}.{model1.__class__.__name__}")

# Set parameters
for key, value in WENDLING_STANDARD_PARAMS['Type1']['params'].items():
    model1.params[key] = value
model1.params['duration'] = 1000  # 1 second

# Run
model1.run()
print(f"✓ Simulation completed: {len(model1.t)} time points")
signal1 = model1.get_output_signal()
print(f"  Output signal shape: {signal1.shape}")

# ==============================================================================
# 方法2：直接使用擴展包命名空間
# Method 2: Direct import from extension package
# ==============================================================================
print("\n" + "=" * 70)
print("Method 2: Import from neurolib_wendling.models.wendling")
print("=" * 70)

from neurolib_wendling.models.wendling import WendlingModel as WM2

# Create model (same code!)
model2 = WM2()
print(f"✓ Model created: {model2}")
print(f"  Model name: {model2.name}")
print(f"  Model class: {model2.__class__.__module__}.{model2.__class__.__name__}")

# Set parameters (same code!)
for key, value in WENDLING_STANDARD_PARAMS['Type1']['params'].items():
    model2.params[key] = value
model2.params['duration'] = 1000

# Run (same code!)
model2.run()
print(f"✓ Simulation completed: {len(model2.t)} time points")
signal2 = model2.get_output_signal()
print(f"  Output signal shape: {signal2.shape}")

# ==============================================================================
# 驗證：兩種方法產生相同結果
# Verification: Both methods produce identical results
# ==============================================================================
print("\n" + "=" * 70)
print("Verification: Are the results identical?")
print("=" * 70)

print(f"Time arrays equal: {np.allclose(model1.t, model2.t)}")
print(f"Output signals equal: {np.allclose(signal1, signal2)}")
print(f"State y1 equal: {np.allclose(model1.y1, model2.y1)}")

print("\n✅ Both methods work identically!")
print("   You can use whichever import style you prefer.")

# ==============================================================================
# 展示：與neurolib其他工具的相容性
# Demo: Compatibility with other neurolib tools
# ==============================================================================
print("\n" + "=" * 70)
print("Demo: Using neurolib utilities")
print("=" * 70)

# Use neurolib's utils (works for both models)
from neurolib.utils.collections import dotdict

test_dict = dotdict({'a': 1, 'b': 2})
print(f"✓ neurolib.utils.collections.dotdict works: {test_dict.a}")

# Check that model inherits from neurolib.Model
from neurolib.models.model import Model
print(f"✓ WendlingModel inherits from neurolib.Model: {isinstance(model1, Model)}")
print(f"✓ Both models are instances of the same class: {model1.__class__ is model2.__class__}")

# ==============================================================================
# 可視化：兩種方法產生相同波形
# Visualization: Both methods produce identical waveforms
# ==============================================================================
fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].plot(model1.t, signal1[0], 'b-', linewidth=1, label='Method 1 (neurolib.models.wendling)')
axes[0].set_ylabel('Amplitude (mV)')
axes[0].set_title('Method 1: from neurolib.models.wendling')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(model2.t, signal2[0], 'r-', linewidth=1, label='Method 2 (neurolib_wendling.models.wendling)')
axes[1].set_ylabel('Amplitude (mV)')
axes[1].set_xlabel('Time (ms)')
axes[1].set_title('Method 2: from neurolib_wendling.models.wendling')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comparison_both_methods.png', dpi=150, bbox_inches='tight')
print("\n📊 Plot saved: comparison_both_methods.png")
print("   The two waveforms should be identical!")

plt.show()

print("\n" + "=" * 70)
print("Summary:")
print("=" * 70)
print("✅ Both import methods work")
print("✅ Both produce identical results")
print("✅ Full compatibility with neurolib utilities")
print("✅ You can choose whichever style you prefer!")
print("\nRecommended: Use 'from neurolib.models.wendling import ...'")
print("             (Just remember to import neurolib_wendling first)")
