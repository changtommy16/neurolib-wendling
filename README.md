# neurolib-wendling

Wendling neural mass model extension for [neurolib](https://github.com/neurolib-dev/neurolib).

## Features

- 🧠 Complete Wendling neural mass model implementation
- 📊 6 verified activity types (background, alpha, beta, gamma, spike-wave, sustained)
- 📚 Tutorial notebook with examples
- 🔧 Easy integration with neurolib framework

## Installation

### Install from source (recommended for now)

```bash
# Install original neurolib first
pip install neurolib

# Clone and install this extension
git clone https://github.com/changtommy16/neurolib-wendling.git
cd neurolib-wendling-package
pip install -e .
```


## Quick Start

### ✨ Two Ways to Import (Both Work!)

```python
# Method 1: Import as if it's part of neurolib (recommended)
import neurolib_wendling  # Enable auto-registration
from neurolib.models.wendling import WendlingModel

# Method 2: Direct import from extension package
from neurolib_wendling.models.wendling import WendlingModel
```

### Basic Usage

```python
from neurolib.models.wendling import WendlingModel
from neurolib.models.wendling.STANDARD_PARAMETERS import WENDLING_STANDARD_PARAMS

# Create model with default parameters
model = WendlingModel()

# Update with standard parameters (e.g., Type1 activity)
std_params = WENDLING_STANDARD_PARAMS['Type1']['params']
for key, value in std_params.items():
    model.params[key] = value

# Run simulation
model.run()

# Get output signal
signal = model.get_output_signal()  # v_pyr = y1 - y2 - y3

# Plot results
import matplotlib.pyplot as plt
plt.plot(model.t, signal[0])
plt.xlabel('Time (ms)')
plt.ylabel('Pyramidal Output (mV)')
plt.show()
```

## Tutorials

Check out the [Wendling Tutorial notebook](tutorials/Wendling_Tutorial_Clean.ipynb) for:
- Basic setup and single node simulation
- All 6 activity types demonstration
- Multi-node network examples
- Parameter effects analysis

## Full Compatibility with neurolib

This extension is **100% compatible** with neurolib. After installation:

✅ **Same import syntax** as native neurolib models:
```python
import neurolib_wendling  # Trigger auto-registration
from neurolib.models.wendling import WendlingModel  # Just like native models!
```

✅ **Same API** as other neurolib models:
```python
model = WendlingModel()  # Inherits from neurolib.models.model.Model
model.run()              # All Model methods available
model.params             # Parameter dictionary
model.t                  # Time array
```

✅ **Works with neurolib tools**:
```python
from neurolib.utils.collections import dotdict
from neurolib.optimize.evolution import Evolution
# All neurolib utilities work with WendlingModel
```

**Key Point:** This extension registers itself to `neurolib.models` namespace, so you can import it exactly like native neurolib models!

## Documentation

See [README_USAGE.md](neurolib_wendling/models/wendling/README_USAGE.md) for detailed API documentation.

## Requirements

- Python >= 3.9
- neurolib >= 0.6.0
- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0

## License

MIT License (same as neurolib)

## Citation

If you use this model in your research, please cite:
- Chang, H. (2025). neurolib-wendling: neurolib implementation of the Wendling neural mass model [Computer software]. https://doi.org/10.5281/zenodo.17810152

You should also cite the original model and framework:
```
- Wendling F, Bellanger JJ, Bartolomei F, Chauvel P (2000).
  Relevance of nonlinear lumped-parameter models in the analysis of depth-EEG epileptic signals.
  *Biological Cybernetics*, 83(4), 367–378.
- Cakan C, Jajcay N, Obermayer K (2023).
  neurolib: A Simulation Framework for Whole-Brain Neural Mass Modeling.
  *Cognitive Computation*, 15, 1132–1152.
```

## Developer Guide

For package development, version control, and publishing workflow, see **[DEVELOPER.md](DEVELOPER.md)**.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
