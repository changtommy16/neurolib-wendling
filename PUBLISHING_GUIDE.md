# 📦 Publishing Guide - neurolib-wendling

## 🎯 我做了什麼

### 創建的包結構
```
neurolib-wendling-package/
├── neurolib_wendling/              # 主包
│   ├── __init__.py                # 包初始化（含auto-registration）
│   ├── register.py                # 自動註冊到neurolib.models命名空間
│   └── models/
│       ├── __init__.py
│       └── wendling/              # Wendling模型實現
│           ├── __init__.py
│           ├── model.py           # WendlingModel類（繼承neurolib.Model）
│           ├── loadDefaultParams.py
│           ├── timeIntegration.py
│           ├── STANDARD_PARAMETERS.py
│           └── README_USAGE.md
│
├── tutorials/                      # 教學
│   └── Wendling_Tutorial_Clean.ipynb
│
├── setup.py                       # 包配置
├── requirements.txt               # 依賴
├── LICENSE                        # MIT授權
├── README.md                      # 主文檔
├── MANIFEST.in                    # 包含額外文件
├── .gitignore                     # Git忽略規則
│
├── test_installation.py           # 測試腳本
├── example_usage.py               # 使用示例
└── setup_package.py               # 從源頭複製文件的腳本
```

### 核心功能
1. **✅ Auto-registration機制**：可以用 `from neurolib.models.wendling import WendlingModel`
2. **✅ 100%相容性**：繼承 `neurolib.models.model.Model`，所有方法都可用
3. **✅ 獨立分發**：不需要修改原始neurolib
4. **✅ 測試通過**：4/4測試全部通過

---

## 📋 你要做什麼來發布

### 選項A：發布到GitHub（推薦開始）

#### 1. 修改setup.py中的個人資訊

```python
# 編輯 setup.py，修改這些行：
author="Your Name",          # ← 改成你的名字
author_email="your@email.com",  # ← 改成你的email
url="https://github.com/yourusername/neurolib-wendling",  # ← 改成你的repo URL
```

#### 2. 初始化Git並推送到GitHub

```bash
cd neurolib-wendling-package

# 初始化git
git init
git add .
git commit -m "Initial release: neurolib-wendling v0.1.0"

# 創建GitHub repo（在GitHub網站上創建一個新repo）
# 然後連接並推送
git branch -M main
git remote add origin https://github.com/你的用戶名/neurolib-wendling.git
git push -u origin main
```

#### 3. 創建Release（可選，但推薦）

在GitHub上：
1. 點擊 "Releases" → "Create a new release"
2. Tag version: `v0.1.0`
3. Release title: `v0.1.0 - Initial Release`
4. Description:
   ```
   # neurolib-wendling v0.1.0
   
   Initial release of Wendling neural mass model extension for neurolib.
   
   ## Features
   - ✅ Complete Wendling model implementation
   - ✅ 6 verified activity types
   - ✅ 100% compatible with neurolib
   - ✅ Auto-registration for seamless import
   - ✅ Tutorial notebook included
   
   ## Installation
   ```bash
   pip install neurolib git+https://github.com/你的用戶名/neurolib-wendling.git
   ```
   ```

#### 4. 分享給其他人

給collaborators這個指令：
```bash
pip install neurolib git+https://github.com/你的用戶名/neurolib-wendling.git
```

---

### 選項B：發布到PyPI（公開發布）

#### 準備工作

1. **註冊PyPI帳號**
   - 正式版：https://pypi.org/account/register/
   - 測試版：https://test.pypi.org/account/register/ （建議先用這個測試）

2. **安裝發布工具**
   ```bash
   pip install build twine
   ```

#### 發布步驟

##### 1. 測試本地構建

```bash
cd neurolib-wendling-package

# 構建包
python -m build

# 這會創建：
# dist/neurolib_wendling-0.1.0-py3-none-any.whl
# dist/neurolib-wendling-0.1.0.tar.gz
```

##### 2. 先發布到TestPyPI（測試）

```bash
# 上傳到TestPyPI
python -m twine upload --repository testpypi dist/*

# 輸入你的TestPyPI用戶名和密碼

# 測試安裝
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple neurolib-wendling
```

##### 3. 正式發布到PyPI

確認一切正常後：

```bash
# 上傳到正式PyPI
python -m twine upload dist/*

# 輸入你的PyPI用戶名和密碼
```

##### 4. 安裝測試

```bash
# 現在任何人都可以這樣安裝
pip install neurolib-wendling
```

---

## 📖 發布後，告訴使用者要看什麼

### 主要文檔（按順序）

1. **README.md** - 開始這裡
   - 快速了解是什麼
   - 安裝指令
   - 基本使用示例
   - 兩種導入方式

2. **tutorials/Wendling_Tutorial_Clean.ipynb** - 詳細教學
   - 完整的使用教學
   - 6種活動類型示範
   - 多節點網絡示例

3. **neurolib_wendling/models/wendling/README_USAGE.md** - API文檔
   - 詳細的參數說明
   - 所有函數用法
   - 技術細節

### 給開發者

- **test_installation.py** - 測試安裝是否成功
- **example_usage.py** - 示範兩種導入方式
- **setup_package.py** - 從源頭更新文件的腳本

---

## 🔄 更新流程

### 更新代碼

1. 修改源代碼（在原始wendling資料夾）
2. 執行 `python setup_package.py` 同步到包中
3. 更新版本號（setup.py和__init__.py）
4. 測試：`python test_installation.py`
5. 提交並推送

### 版本號規則（Semantic Versioning）

```
版本號格式：MAJOR.MINOR.PATCH (例如: 0.1.0)

- MAJOR: 重大變更，可能不向後相容（例如：1.0.0）
- MINOR: 新功能，向後相容（例如：0.2.0）
- PATCH: Bug修復（例如：0.1.1）

範例：
0.1.0 → 初始發布
0.1.1 → Bug修復
0.2.0 → 新增功能
1.0.0 → 穩定版本發布
```

---

## 🎯 快速發布檢查清單

### 發布前檢查

- [ ] 修改setup.py中的作者資訊
- [ ] 確認LICENSE中的名字和年份
- [ ] 測試通過：`python test_installation.py`
- [ ] README.md中的安裝指令正確
- [ ] .gitignore包含所有應該忽略的文件
- [ ] 版本號正確（setup.py和__init__.py一致）

### GitHub發布

- [ ] Git init並commit所有文件
- [ ] 在GitHub上創建新repo
- [ ] Push到GitHub
- [ ] 創建Release tag
- [ ] 測試從GitHub安裝

### PyPI發布（可選）

- [ ] 註冊PyPI和TestPyPI帳號
- [ ] 安裝build和twine
- [ ] 本地構建成功
- [ ] 先上傳到TestPyPI測試
- [ ] 測試安裝成功
- [ ] 正式上傳到PyPI
- [ ] 最終測試安裝

---

## 💡 推薦工作流程

### 對於研究項目（推薦）

```bash
# 1. 發布到GitHub
git init && git add . && git commit -m "Initial release"
git push origin main

# 2. 分享給collaborators
# 給他們這個指令：
pip install neurolib git+https://github.com/你的用戶名/neurolib-wendling.git
```

**優點**：
- ✅ 簡單快速
- ✅ 可以是private repo
- ✅ 容易更新
- ✅ 適合研究團隊

### 對於公開發布

```bash
# 1. 先發布到GitHub
# 2. 然後發布到PyPI
python -m build
python -m twine upload dist/*

# 3. 使用者安裝
pip install neurolib-wendling
```

**優點**：
- ✅ 最廣泛的可用性
- ✅ 標準化安裝
- ✅ 容易被發現
- ✅ 適合開源社群

---

## 🆘 常見問題

### Q: 如何更新已發布的包？

**GitHub:**
```bash
# 修改代碼後
git add .
git commit -m "Update: 描述你的更新"
git push

# 使用者更新
pip install --upgrade git+https://github.com/你的用戶名/neurolib-wendling.git
```

**PyPI:**
```bash
# 1. 更新版本號（setup.py: 0.1.0 → 0.1.1）
# 2. 重新構建
python -m build
# 3. 上傳新版本
python -m twine upload dist/*
```

### Q: 測試失敗怎麼辦？

```bash
# 重新安裝
pip uninstall neurolib-wendling
pip install -e .

# 重新測試
python test_installation.py
```

### Q: 如何讓使用者報告問題？

在README中加入：
```markdown
## Issues and Support

Found a bug or have a question? Please open an issue on [GitHub](https://github.com/你的用戶名/neurolib-wendling/issues).
```

---

## 📚 相關文檔

- **README.md** - 主要說明文檔
- **test_installation.py** - 安裝測試
- **example_usage.py** - 使用示例
- **tutorials/Wendling_Tutorial_Clean.ipynb** - 完整教學

---

**建議：從GitHub開始！** 

對於研究項目，GitHub分發是最簡單的方式：
1. 容易設置
2. 方便更新
3. 可以是private
4. 使用者只需一行指令安裝

PyPI可以等到你想公開發布時再考慮。
