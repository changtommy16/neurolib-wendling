# 🔧 Developer Guide - neurolib-wendling

> **本文件专为包开发者（你自己）准备**  
> 记录：开发流程、setup_package使用、版本发布步骤

---

## 📂 项目结构说明

```
neurolib-wendling-package/
├── neurolib_wendling/          # 主包代码
│   ├── __init__.py            # 包初始化（含auto-registration）
│   ├── register.py            # 动态注册到neurolib命名空间
│   └── models/wendling/       # Wendling模型实现
│       ├── model.py           # WendlingModel类
│       ├── loadDefaultParams.py
│       ├── timeIntegration.py
│       └── STANDARD_PARAMETERS.py
│
├── tutorials/                  # 教学Notebook
├── setup.py                   # 包配置
├── README.md                  # 用户文档
├── DEVELOPER.md               # 本文件（开发者指南）
├── test_installation.py       # 测试脚本
└── example_usage.py           # 使用示例
```

**重要文件说明：**
- `setup_package.py` - 开发者工具（已在.gitignore，不会发布）

---

## 🛠️ 开发工作流

### 第一步：在原始位置开发代码

**原始位置：**  
```
c:\Epilepsy_project\Neurolib_desktop\Neurolib_package\neurolib\models\wendling\
```

**为什么在这里开发？**
- ✅ 修改立即生效（neurolib已安装为editable）
- ✅ 可以直接在Jupyter notebook测试
- ✅ 避免在两处维护代码

**常见修改文件：**
- `model.py` - 修改WendlingModel类
- `STANDARD_PARAMETERS.py` - 调整参数集
- `timeIntegration.py` - 优化积分算法

---

### 第二步：使用 `setup_package.py` 同步代码

**作用：** 将原始位置的代码自动复制到独立包结构中

**使用方法：**
```bash
# 进入包目录
cd c:\Epilepsy_project\whole_brain_wendling\neurolib-wendling-package

# 运行同步脚本
python setup_package.py
```

**输出示例：**
```
============================================================
neurolib-wendling Package Setup
============================================================
✓ Copying wendling module...
  ✓ Copied model.py
  ✓ Copied loadDefaultParams.py
  ✓ Copied timeIntegration.py
  ✓ Copied STANDARD_PARAMETERS.py
  ✓ Copied __init__.py
✓ Copying tutorial notebook...
  ✓ Copied Wendling_Tutorial_Clean.ipynb

✅ Package structure is complete!
```

**注意事项：**
- ⚠️ 永远不要直接修改 `neurolib_wendling/models/wendling/` 内的文件
- ⚠️ 下次运行 `setup_package.py` 会覆盖所有手动修改
- ✅ 始终在原始位置开发，然后同步

---

### 第三步：测试独立包

```bash
# 安装为开发模式
pip install -e .

# 运行测试套件
python test_installation.py

# 验证两种导入方式
python example_usage.py
```

**测试通过标准：**
```
✅ All tests passed! (4/4)
- Import test
- Standard parameters test
- Model creation test
- Alternative import test (neurolib.models.wendling)
```

---

## 📦 版本发布流程

### 发布前检查清单

- [ ] 代码已从原始位置同步（`python setup_package.py`）
- [ ] 测试全部通过（`python test_installation.py`）
- [ ] 更新版本号（见下方）
- [ ] 更新 `README.md` 中的更新日志（如有重大变更）

---

### 版本号管理

**遵循语义化版本（Semantic Versioning）：**
```
版本格式: MAJOR.MINOR.PATCH (例如: 0.1.0)

- MAJOR: 重大变更，可能不向后兼容 (1.0.0)
- MINOR: 新功能，向后兼容 (0.2.0)
- PATCH: Bug修复 (0.1.1)
```

**需要修改的文件（2处）：**

1. **setup.py (第15行)**
   ```python
   version="0.1.0",  # ← 修改这里
   ```

2. **neurolib_wendling/__init__.py (第5行)**
   ```python
   __version__ = "0.1.0"  # ← 修改这里
   ```

**版本更新示例：**
```bash
# 修复bug: 0.1.0 → 0.1.1
# 新增功能: 0.1.1 → 0.2.0
# 重大变更: 0.2.0 → 1.0.0
```

---

### 发布到GitHub

#### 首次发布

1. **创建GitHub仓库**  
   - 名称: `neurolib-wendling`
   - 描述: `Wendling neural mass model extension for neurolib`
   - 可选Public或Private

2. **初始化Git并推送**
   ```bash
   cd neurolib-wendling-package
   
   # 初始化（如果尚未初始化）
   git init
   git add .
   git commit -m "Initial release: neurolib-wendling v0.1.0"
   
   # 连接到GitHub
   git branch -M main
   git remote add origin https://github.com/changtommy16/neurolib-wendling.git
   
   # 推送
   git push -u origin main
   ```

3. **创建Release（推荐）**
   - 在GitHub网站: `Releases` → `Create a new release`
   - Tag version: `v0.1.0`
   - Release title: `v0.1.0 - Initial Release`
   - Description:
     ```markdown
     ## Features
     - ✅ Wendling neural mass model implementation
     - ✅ 6 validated activity types (Type1-Type6)
     - ✅ 100% compatible with neurolib
     - ✅ Auto-registration for seamless import
     
     ## Installation
     ```bash
     pip install neurolib git+https://github.com/changtommy16/neurolib-wendling.git
     ```
     ```

---

#### 后续更新发布

```bash
# 1. 修改代码（在原始位置）
# 2. 运行同步
python setup_package.py

# 3. 更新版本号（setup.py + __init__.py）

# 4. 测试
python test_installation.py

# 5. 提交并推送
git add .
git commit -m "Update: 描述你的更新内容"
git push

# 6. 创建新的Release tag（可选）
git tag v0.1.1
git push origin v0.1.1
```

---

## 🔄 常见开发场景

### 场景1：修改模型参数

```bash
# 1. 编辑原始文件
c:\Epilepsy_project\Neurolib_desktop\Neurolib_package\neurolib\models\wendling\STANDARD_PARAMETERS.py

# 2. 在Jupyter快速测试
from neurolib.models.wendling import WendlingModel
model = WendlingModel()
# 测试你的修改...

# 3. 确认无误后同步
python setup_package.py

# 4. 测试独立包
python test_installation.py
```

---

### 场景2：修改模型核心算法

```bash
# 1. 编辑 model.py 或 timeIntegration.py

# 2. 在原始位置测试（利用editable install）
python -c "from neurolib.models.wendling import WendlingModel; ..."

# 3. 同步到独立包
python setup_package.py

# 4. 完整测试
python test_installation.py && python example_usage.py

# 5. 更新版本号（至少PATCH +1）

# 6. 发布
git add . && git commit -m "Fix: ..." && git push
```

---

### 场景3：更新教学Notebook

```bash
# 1. 编辑原始notebook
c:\Epilepsy_project\whole_brain_wendling\Validation_for_single_node\Wendling_Tutorial_Clean.ipynb

# 2. 同步到独立包
python setup_package.py

# 3. 推送更新
git add tutorials/Wendling_Tutorial_Clean.ipynb
git commit -m "Update: tutorial improvements"
git push
```

---

## 🆘 故障排除

### 问题1：`setup_package.py` 找不到源文件

**错误信息：**
```
❌ Error: Wendling source not found at c:\...\neurolib\models\wendling
```

**解决方案：**
- 检查原始neurolib安装路径是否正确
- 确认wendling文件夹存在且完整
- 修改 `setup_package.py` 中的路径常量（如有更改）

---

### 问题2：测试失败

**错误信息：**
```
✗ FAIL: Model Creation
```

**解决方案：**
```bash
# 重新安装依赖
pip uninstall neurolib-wendling
pip install -e .

# 检查neurolib版本
pip show neurolib

# 重新测试
python test_installation.py
```

---

### 问题3：导入错误

**错误信息：**
```
ModuleNotFoundError: No module named 'neurolib.models.wendling'
```

**解决方案：**
- 确保先 `import neurolib_wendling` 触发auto-registration
- 检查 `register.py` 是否被正确执行
- 验证neurolib已安装：`pip show neurolib`

---

## 📊 发布后维护

### 用户如何安装？

```bash
pip install neurolib git+https://github.com/changtommy16/neurolib-wendling.git
```

### 用户如何更新？

```bash
pip install --upgrade git+https://github.com/changtommy16/neurolib-wendling.git
```

### 监控Issues

- 定期检查GitHub Issues
- 回复用户问题
- 收集功能需求

---

## 🎯 快速参考卡

### 完整开发循环

```bash
# 1. 修改原始代码
code c:\Epilepsy_project\Neurolib_desktop\Neurolib_package\neurolib\models\wendling\model.py

# 2. 快速测试
jupyter notebook  # 在原始位置测试

# 3. 同步到包
cd neurolib-wendling-package && python setup_package.py

# 4. 完整测试
python test_installation.py

# 5. 更新版本
# 编辑 setup.py 和 __init__.py

# 6. 发布
git add . && git commit -m "描述" && git push

# 7. 创建Release（可选）
# 在GitHub网站操作
```

---

## 📚 相关文档

- `README.md` - 用户安装和使用指南
- `test_installation.py` - 测试脚本（可作为使用示例）
- `example_usage.py` - 两种导入方式演示
- `neurolib_wendling/models/wendling/README_USAGE.md` - API详细文档

---

## 💡 最佳实践

1. **代码管理**
   - ✅ 始终在原始位置开发
   - ✅ 使用 `setup_package.py` 同步
   - ❌ 不要直接编辑 `neurolib_wendling/` 内的代码

2. **版本控制**
   - ✅ 每次发布前更新版本号
   - ✅ 遵循语义化版本规范
   - ✅ 使用Git tags标记版本

3. **测试**
   - ✅ 修改后立即测试
   - ✅ 发布前运行完整测试套件
   - ✅ 验证两种导入方式都可用

4. **文档**
   - ✅ 重大变更更新README
   - ✅ 保持DEVELOPER.md同步
   - ✅ 更新教学notebook

---

**记住：** `setup_package.py` 是你的自动化助手，善用它！

---

## ⚠️ 重要：导入路径问题 (2024-12-04)

### 问题描述

独立包 (`neurolib-wendling`) 中使用**相对导入**会导致 auto-registration 失败。

**症状：**
```python
import neurolib_wendling
from neurolib.models.wendling import WendlingModel  # ModuleNotFoundError!
```

**错误信息：**
```
Warning: Could not register wendling to neurolib namespace: 
  No module named 'neurolib_wendling.utils'
ModuleNotFoundError: No module named 'neurolib.models.wendling'
```

---

### 根本原因

**包结构不同导致导入路径要求不同：**

| 位置 | 包结构 | 应使用 |
|------|--------|--------|
| **开发环境** | `neurolib/models/wendling/` | 相对导入 `from ...utils` |
| **独立包** | `neurolib_wendling/models/wendling/` | 绝对导入 `from neurolib.utils` |

**问题文件：**
1. `loadDefaultParams.py` - 第2行
2. `model.py` - 第5行

---

### 解决方案

**已修改的文件（独立包版本）：**

#### 1. `neurolib_wendling/models/wendling/loadDefaultParams.py`
```python
import numpy as np
# Use absolute import for standalone package (not relative import)
from neurolib.utils.collections import dotdict  # ← 改成绝对导入
```

#### 2. `neurolib_wendling/models/wendling/model.py`
```python
import numpy as np

from . import loadDefaultParams as dp
from . import timeIntegration as ti
# Use absolute import for standalone package (not relative import)
from neurolib.models.model import Model  # ← 改成绝对导入
```

**注意：开发环境的文件保持相对导入不变！**

---

### 为什么不用 setup_package.py 自动转换？

因为：
1. 需要转换的只有2处，手动修改简单可控
2. setup_package.py 主要用于文件复制，不做代码转换
3. 保持工具简单，避免复杂的代码解析逻辑

---

### 验证方法

测试环境中运行：
```bash
cd c:\test_wendling
.\myenv\Scripts\python.exe -c "
import neurolib_wendling
from neurolib.models.wendling import WendlingModel
import numpy as np
Cmat = np.eye(3)
Dmat = np.ones((3,3))*10
model = WendlingModel(Cmat=Cmat, Dmat=Dmat)
model.params['duration'] = 100
model.run()
print(f'✓ Success! Output: {model.y1.shape}')
"
```

**预期输出：** `✓ Success! Output: (3, 1000)`

---

### 开发工作流更新

```bash
# 1. 在开发环境修改（使用相对导入）
vim c:\Epilepsy_project\Neurolib_desktop\Neurolib_package\neurolib\models\wendling\*.py

# 2. 同步到独立包（setup_package.py 会复制文件）
cd neurolib-wendling-package
python setup_package.py

# 3. 手动检查并修正这2个文件的导入（如果被覆盖）
#    - neurolib_wendling/models/wendling/loadDefaultParams.py
#    - neurolib_wendling/models/wendling/model.py

# 4. 测试并推送
git add .
git commit -m "Fix: import paths for standalone package"
git push
```

---

最后更新：2024-12-04
