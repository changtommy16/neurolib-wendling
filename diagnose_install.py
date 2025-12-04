"""
诊断 neurolib-wendling 安装问题
"""
import sys
import os

print("=" * 70)
print("neurolib-wendling 安装诊断")
print("=" * 70)

# 1. 检查Python版本
print(f"\n[1] Python版本: {sys.version}")
print(f"    可执行文件: {sys.executable}")

# 2. 检查neurolib版本
print("\n[2] 检查neurolib...")
try:
    import neurolib
    print(f"    ✓ neurolib已安装")
    print(f"    位置: {neurolib.__file__}")
    
    # 检查computeDelayMatrix
    from neurolib.utils import model_utils as mu
    if hasattr(mu, 'computeDelayMatrix'):
        print(f"    ✓ computeDelayMatrix 存在")
        print(f"    位置: {mu.__file__}")
    else:
        print(f"    ✗ computeDelayMatrix 不存在！")
        print(f"    可用函数: {[x for x in dir(mu) if not x.startswith('_')]}")
except Exception as e:
    print(f"    ✗ 错误: {e}")

# 3. 检查neurolib-wendling
print("\n[3] 检查neurolib-wendling...")
try:
    import neurolib_wendling
    print(f"    ✓ neurolib_wendling已安装")
    print(f"    版本: {neurolib_wendling.__version__}")
    print(f"    位置: {neurolib_wendling.__file__}")
except Exception as e:
    print(f"    ✗ 错误: {e}")

# 4. 检查timeIntegration
print("\n[4] 检查timeIntegration模块...")
try:
    from neurolib_wendling.models.wendling import timeIntegration
    import inspect
    source_file = inspect.getsourcefile(timeIntegration.timeIntegration)
    print(f"    ✓ timeIntegration已加载")
    print(f"    源文件: {source_file}")
    
    # 读取前30行检查是否有向后兼容补丁
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:30]
        has_patch = any('Backward compatibility' in line for line in lines)
        if has_patch:
            print(f"    ✓ 包含向后兼容补丁")
        else:
            print(f"    ✗ 缺少向后兼容补丁！")
            
except Exception as e:
    print(f"    ✗ 错误: {e}")
    import traceback
    traceback.print_exc()

# 5. 测试导入WendlingModel
print("\n[5] 测试WendlingModel导入...")
try:
    from neurolib_wendling.models.wendling import WendlingModel
    print(f"    ✓ WendlingModel导入成功")
except Exception as e:
    print(f"    ✗ 错误: {e}")
    import traceback
    traceback.print_exc()

# 6. 测试多节点创建
print("\n[6] 测试多节点模型创建...")
try:
    import numpy as np
    from neurolib_wendling.models.wendling import WendlingModel
    
    Cmat = np.eye(3)
    Dmat = np.ones((3, 3)) * 10
    model = WendlingModel(Cmat=Cmat, Dmat=Dmat, seed=42)
    print(f"    ✓ 模型创建成功")
    print(f"    节点数: {len(model.params['Cmat'])}")
except Exception as e:
    print(f"    ✗ 错误: {e}")
    import traceback
    traceback.print_exc()

# 7. 测试运行
print("\n[7] 测试短时运行...")
try:
    model.params['duration'] = 100
    model.run()
    print(f"    ✓ 运行成功")
    print(f"    输出形状: {model.y1.shape}")
except Exception as e:
    print(f"    ✗ 错误: {e}")
    import traceback
    traceback.print_exc()

# 总结
print("\n" + "=" * 70)
print("诊断完成")
print("=" * 70)
print("\n如果看到任何 ✗ 标记，请将完整输出发送给开发者")
