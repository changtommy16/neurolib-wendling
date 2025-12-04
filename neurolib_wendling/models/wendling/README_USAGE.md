# Wendling Model Usage Guide

## ⚡ Quick Reference

| Parameter | What it does | When to use |
|-----------|--------------|-------------|
| `heterogeneity` | 0 = scalar params<br>>0 = vector params + random variation | **Scenario A**: Use 0.3 for automatic diversity<br>**Scenario B**: Use 0.01 as hack to enable manual setting |
| `random_init` | False = zero initial conditions<br>True = random initial conditions | Use True for multi-node networks |
| `seed` | Random seed for reproducibility | Set to 42 for consistent results |

**Key insight**: 
- `heterogeneity` generates initial random variation during model creation
- **If you DON'T set parameters manually** → The random variation is used (Scenario A)
- **If you DO set parameters manually** → Your values overwrite the random variation (Scenario B)
- Once set (either way), parameters stay **fixed** during `model.run()`

---

## 📌 Basic Usage

```python
from neurolib.models.wendling import WendlingModel
import numpy as np

# Create connectivity matrices
N = 6
Cmat = np.eye(N)  # Structural connectivity matrix
Dmat = np.zeros((N, N))  # Distance matrix

# Create model
model = WendlingModel(Cmat=Cmat, Dmat=Dmat)
model.params['duration'] = 10000  # 10 seconds
model.params['dt'] = 0.1  # Time step
model.params['K_gl'] = 0.15  # Global coupling strength

# Run simulation
model.run()

# Extract signals
signals = model.y1 - model.y2 - model.y3  # PSP (pyramidal neuron output)
```

---

## 🎛️ Key Parameters

### 1. heterogeneity (Node Heterogeneity)

**Purpose**: Generates random parameter variation during initialization

**What happens**:
1. When `heterogeneity > 0`: Parameters become vectors with random variation
2. **If you don't set parameters** → Uses the random values (intended use)
3. **If you set parameters manually** → Your values overwrite the random values

#### Use Case A: Automatic diversity (INTENDED)
```python
# For whole-brain modeling
model = WendlingModel(Cmat, Dmat, heterogeneity=0.30)
# → Generates: B = [25.3, 18.7, 22.1, ...] (random)
# → Don't overwrite! Use these values directly ✅
model.run()
```

#### Use Case B: Manual control (HACK)
```python
# For manual type assignment
model = WendlingModel(Cmat, Dmat, heterogeneity=0.01)
# → Generates: B = [22.04, 21.85, ...] (random, but we don't want)
# → Overwrite with exact values ✅
model.params['B'] = np.array([50, 25, 15, ...])
# → Now: B = [50, 25, 15, ...] (our values!)
model.run()
```

**Value Range**: 0.0 ~ 1.0
- `0.0` = Scalar mode (cannot set different values per node)
- `0.01` = Minimal variation (hack to enable vectorization)
- `0.3` = 30% variation (realistic diversity)
- `0.5` = 50% variation (high diversity)

**Why is this confusing?**
- The design mixes two concepts: "vectorization" + "variation"
- Ideally, there should be a separate `vectorize_params=True` parameter
- We exploit the side effect for manual control

---

### 2. random_init (Initial Condition Type)

**Purpose**: Controls the initial values of state variables

**Values**: `True` or `False`
- `False` = Zero initial conditions (all states start from 0)
- `True` = Random initial conditions (start from random(-0.1, 0.1))

**Usage Recommendations**:

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Single-node testing | `False` | Reproduce classic Wendling 2002 waveforms |
| Multi-node networks | `True` | Avoid decay to steady state for certain parameter combinations |
| Whole-brain simulation | `True` | More realistic brain state |

**Example**:
```python
# Single-node
model = WendlingModel(Cmat, Dmat, random_init=False)

# Multi-node
model = WendlingModel(Cmat, Dmat, random_init=True)
```

---

### 3. seed (Random Seed)

**Purpose**: Ensures reproducible results

```python
model = WendlingModel(Cmat, Dmat, heterogeneity=0.3, seed=42)
# Every run produces the same random parameters and initial conditions
```

---

## 🎯 Common Use Cases

### Scenario 1: Single-node classic waveform reproduction

```python
# Reproduce the 6 activity types from Wendling 2002
Cmat = np.array([[0]])
Dmat = np.array([[0]])

model = WendlingModel(
    Cmat=Cmat, 
    Dmat=Dmat,
    heterogeneity=0.0,   # Scalar mode
    random_init=False,   # Zero initial conditions
    seed=42
)

# Set Type3 (SWD) parameters
model.params['B'] = 25
model.params['G'] = 15
model.params['A'] = 5
model.params['p_mean'] = 90
model.params['p_sigma'] = 2.0
model.params['duration'] = 10000
model.params['dt'] = 0.1
model.params['K_gl'] = 0.0

model.run()
signal = model.y1[0, :] - model.y2[0, :] - model.y3[0, :]
```

---

### Scenario 2: Multi-node with manually specified types for each node

```python
# Goal: Set different Wendling types for each node
N = 6
NODE_TYPES = ['Type1', 'Type3', 'Type6', 'Type6', 'Type1', 'Type1']

Cmat = np.eye(N)
Dmat = np.zeros((N, N))

# Hack: Use tiny heterogeneity to trigger vector mode
model = WendlingModel(
    Cmat=Cmat, 
    Dmat=Dmat,
    heterogeneity=0.01,  # Triggers vector mode (parameters become arrays)
    random_init=True,    # MUST use True for multi-node
    seed=42
)

# Check: Parameters are now vectors (but random)
print(model.params['B'])  # → [22.04, 21.85, 21.85, 21.85, 22.04, 22.04]

# Manually overwrite with exact values for each type
model.params['B'] = np.array([50, 25, 15, 15, 50, 50])  # Type1, Type3, Type6...
model.params['G'] = np.array([15, 15, 0, 0, 15, 15])
model.params['A'] = np.array([5, 5, 5, 5, 5, 5])
model.params['p_mean'] = np.array([90, 90, 90, 90, 90, 90])
model.params['p_sigma'] = 2.0  # Scalar (shared by all nodes)

# Verify: Parameters are now fixed
print(model.params['B'])  # → [50, 25, 15, 15, 50, 50] ✅

model.params['duration'] = 10000
model.params['dt'] = 0.1
model.params['K_gl'] = 0.0  # or 0.15 for coupling

# Run simulation
model.run()

# Check again: Parameters stayed fixed!
print(model.params['B'])  # → [50, 25, 15, 15, 50, 50] ✅ (unchanged)
```

**Key takeaway**: 
- `heterogeneity` only sets the **initial** random values
- Your manual assignment **overrides** them completely
- During `model.run()`, parameters **stay fixed** at your values

---

### Scenario 3: Whole-brain network modeling (automatic random parameters)

**This is the INTENDED use of heterogeneity!**

```python
# 80-node whole-brain network
N = 80
Cmat = load_structural_connectivity()  # Real SC matrix
Dmat = load_distance_matrix()

model = WendlingModel(
    Cmat=Cmat, 
    Dmat=Dmat,
    heterogeneity=0.30,  # 30% parameter variation
    random_init=True,    # Random initial conditions
    seed=42
)

# ⚠️ IMPORTANT: Do NOT overwrite parameters here!
# The purpose of heterogeneity is to USE these random values
# They represent realistic brain diversity

# Check the generated diversity
print(f"B range: {model.params['B'].min():.1f} - {model.params['B'].max():.1f}")
# → B range: 15.4 - 28.6 (diverse!)

model.params['duration'] = 10000
model.params['dt'] = 0.1
model.params['K_gl'] = 0.15  # Global coupling strength

model.run()

# Extract signals from all nodes
signals = model.y1 - model.y2 - model.y3  # shape: (80, 100000)
```

**Key difference from Scenario 2**:
- Scenario 2: Use heterogeneity as a **hack** → overwrite values
- Scenario 3: Use heterogeneity as **intended** → keep random values

---

## 📊 Summary: When is the random variation useful?

| Scenario | heterogeneity | Manual override? | Random variation used? | Purpose |
|----------|---------------|------------------|------------------------|---------|
| **Single-node** | 0.0 | Set manually | N/A (scalar mode) | Testing specific types |
| **Manual types** | 0.01 | ✅ Override | ❌ No (overwritten) | We need vectorization only |
| **Whole-brain** | 0.30 | ❌ Keep random | ✅ **YES!** | Realistic brain diversity |

**The key logic**:
- `heterogeneity > 0` always generates random variation during initialization
- **Without manual override** → Random variation is used (intended for whole-brain)
- **With manual override** → Your values replace the random variation (hack for manual types)

---

## ⚠️ Important Notes

### 1. heterogeneity has a dual role

```python
# heterogeneity controls both variation AND vectorization!

# heterogeneity = 0
# → B, G, A, p_mean are SCALARS
# → Cannot set different values for each node

# heterogeneity > 0
# → B, G, A, p_mean are VECTORS
# → Can manually overwrite with any values
```

**Decision flow**:
```python
model = WendlingModel(heterogeneity=0.01, seed=42)
# At this point: B = [22.04, 21.85, ...] (random values from heterogeneity)

# Path A: Don't set parameters manually
model.run()
# → Uses the random values: B = [22.04, 21.85, ...]

# Path B: Set parameters manually
model.params['B'] = np.array([50, 25, 15, ...])
# → Your values overwrite: B = [50, 25, 15, ...]
model.run()
# → Uses your values: B = [50, 25, 15, ...]
```

**Key points**:
- ✅ heterogeneity generates initial random values during `__init__()`
- ✅ If you don't set manually → random values are used
- ✅ If you set manually → your values overwrite the random values
- ✅ Once set (either way), parameters stay fixed during `model.run()`

---

### 2. random_init is critical for multi-node networks

```python
# ❌ Wrong: multi-node + random_init=False
model = WendlingModel(Cmat, Dmat, random_init=False)
model.params['B'] = np.array([50, 50, 50])  # high-B type
model.run()
# → Signals decay to flat line!

# ✅ Correct: multi-node + random_init=True
model = WendlingModel(Cmat, Dmat, random_init=True)
model.params['B'] = np.array([50, 50, 50])
model.run()
# → Normal oscillations
```

**Reason**: Zero initial conditions + multi-node + high-B parameters → System falls into steady-state attractor

---

### 3. p_sigma 未向量化

```python
# 限制：p_sigma 始终是标量
model.params['p_sigma'] = 2.0  # 所有节点共用

# ❌ 无法这样做：
model.params['p_sigma'] = np.array([2.0, 30.0, 2.0, ...])  # 不支持
```

**影响**：不能在同一网络中混用需要不同 p_sigma 的 Wendling types
- Type3, Type6 需要 `p_sigma = 2.0`（低噪声）
- Type1, Type2, Type4, Type5 需要 `p_sigma = 30.0`（高噪声）

**变通方案**：只混用需要相同 p_sigma 的 types

---

## 📊 Parameter Vectorization Status

| Parameter | Vectorized? | Condition | Manual Override |
|-----------|-------------|-----------|-----------------|
| B | ✅ | heterogeneity > 0 | ✅ Yes |
| G | ✅ | heterogeneity > 0 | ✅ Yes |
| A | ✅ | heterogeneity > 0 | ✅ Yes |
| p_mean | ✅ | heterogeneity > 0 | ✅ Yes |
| p_sigma | ❌ | Always scalar | ❌ No |
| K_gl | ❌ | Always scalar | ✅ Yes |
| duration | ❌ | Always scalar | ✅ Yes |
| dt | ❌ | Always scalar | ✅ Yes |

---

## 🔧 Wendling 2002 Six Activity Types

### Standard Parameters (STANDARD_PARAMETERS.py)

**⚠️ Important Update (2025-10-14)**:  
All 6 types now use **`p_sigma=2.0`** (verified through single-node testing).  
This shows intrinsic dynamics without excessive noise.

| Type | B | G | A | p_mean | p_sigma | Frequency | Description |
|------|---|---|---|--------|---------|-----------|-------------|
| Type1 | 50 | 15 | 5 | 90 | **2.0** | 1-7 Hz | Background activity |
| Type2 | 40 | 15 | 5 | 90 | **2.0** | 1-5 Hz | Sporadic spikes |
| Type3 | 25 | 15 | 5 | 90 | **2.0** | 3-6 Hz | SWD (epileptic) |
| Type4 | 10 | 15 | 5 | 90 | **2.0** | 8-13 Hz | Alpha rhythm |
| Type5 | 5 | 25 | 5 | 90 | **2.0** | 10-20 Hz | LVFA |
| Type6 | 15 | 0 | 5 | 90 | **2.0** | 9-13 Hz | Quasi-sinusoidal |

**Notes**:
- Original Wendling 2002 paper suggested different p_sigma values
- Verified testing shows `p_sigma=2.0` produces correct waveforms for all types
- See `STANDARD_PARAMETERS.py` for verified parameter sets

---

## 📚 Related Documentation

- `STANDARD_PARAMETERS.py` - Standard parameter definitions
- `HETEROGENEITY_AND_RANDOM_INIT.md` - Detailed parameter explanation
- Wendling et al. (2002) - Original paper

---

## 🐛 FAQ

### Q1: Why do my signals decay to a flat line?
**A**: Multi-node networks MUST use `random_init=True`

### Q2: Why can't I set different B values for each node?
**A**: You need to set `heterogeneity > 0` to trigger vector mode

### Q3: Can I mix different activity types in one network?
**A**: **YES!** All 6 types now use `p_sigma=2.0` (verified), so you can freely mix them. Just set different B and G values for each node.

### Q4: How to ensure reproducible results?
**A**: Set the `seed` parameter: `WendlingModel(..., seed=42)`

### Q5: Can I fix parameters after setting heterogeneity > 0?
**A**: **YES!** `heterogeneity` only affects initialization. Your manual values will stay fixed during `model.run()`

### Q6: If I'm going to overwrite the random values, what's the point of heterogeneity?
**A**: It depends on your use case:
- **Don't overwrite (whole-brain)**: The random variation IS the point - simulates realistic brain diversity
- **Do overwrite (manual types)**: The random variation is useless, but we need `heterogeneity>0` to trigger vectorization. It's a hack.

### Q7: When does heterogeneity generate the random values?
**A**: Only during `__init__()` (model creation). The values are then:
- Used directly if you don't set parameters manually, OR
- Overwritten if you do set parameters manually

---

**Last Updated**: 2025-10-14  
**Version**: neurolib wendling model (custom implementation)
