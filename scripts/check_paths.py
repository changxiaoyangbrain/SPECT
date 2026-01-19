#!/usr/bin/env python3
"""
路径检查脚本
验证目录优化后所有路径是否正确
"""

import os
import sys

def check_paths():
    """检查所有关键路径"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("路径检查报告")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # 1. 检查数据目录
    print("📊 数据目录检查:")
    data_input = os.path.join(base_dir, "data", "input")
    data_ref = os.path.join(base_dir, "data", "reference")
    
    required_input = ["Proj.dat", "orbit.xlsx"]
    required_ref = ["OSEMReconed.dat", "Filtered.dat"]
    
    for f in required_input:
        path = os.path.join(data_input, f)
        if os.path.exists(path):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} - 未找到")
            errors.append(f"输入数据文件缺失: {f}")
    
    for f in required_ref:
        path = os.path.join(data_ref, f)
        if os.path.exists(path):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} - 未找到")
            errors.append(f"参考数据文件缺失: {f}")
    
    print()
    
    # 2. 检查输出目录
    print("📤 输出目录检查:")
    outputs_dir = os.path.join(base_dir, "outputs")
    if os.path.exists(outputs_dir):
        print(f"  ✅ outputs/ 目录存在")
    else:
        print(f"  ⚠️  outputs/ 目录不存在（程序运行时会自动创建）")
        warnings.append("outputs/ 目录不存在")
    
    print()
    
    # 3. 检查图片目录
    print("🖼️  图片目录检查:")
    pictures_dir = os.path.join(base_dir, "pictures")
    if os.path.exists(pictures_dir):
        print(f"  ✅ pictures/ 目录存在")
        png_files = [f for f in os.listdir(pictures_dir) if f.endswith('.png')]
        print(f"  📁 包含 {len(png_files)} 个 PNG 文件")
    else:
        print(f"  ⚠️  pictures/ 目录不存在（程序运行时会自动创建）")
        warnings.append("pictures/ 目录不存在")
    
    print()
    
    # 4. 检查核心模块
    print("📦 核心模块检查:")
    spect_dir = os.path.join(base_dir, "spect")
    required_modules = ["__init__.py", "data_loader.py", "system_matrix.py", 
                       "reconstruction.py", "evaluate.py"]
    
    for module in required_modules:
        path = os.path.join(spect_dir, module)
        if os.path.exists(path):
            print(f"  ✅ {module}")
        else:
            print(f"  ❌ {module} - 未找到")
            errors.append(f"核心模块缺失: {module}")
    
    print()
    
    # 5. 测试导入（需要虚拟环境）
    print("🔍 模块导入测试:")
    try:
        sys.path.insert(0, base_dir)
        from spect import SPECTDataLoader, OSEMReconstructor, Evaluator, SystemMatrix
        print("  ✅ 核心模块导入成功")
    except ImportError as e:
        print(f"  ⚠️  导入失败（需要激活虚拟环境）: {e}")
        print("  💡 提示: 请先激活虚拟环境: source .venv/bin/activate")
        warnings.append(f"模块导入需要虚拟环境: {e}")
    except Exception as e:
        print(f"  ⚠️  导入警告: {e}")
        warnings.append(f"模块导入警告: {e}")
    
    print()
    
    # 6. 检查报告生成脚本路径
    print("📄 报告生成脚本路径检查:")
    scripts_dir = os.path.join(base_dir, "scripts")
    pics_dir = os.path.join(base_dir, "pictures")
    
    # 模拟报告脚本的路径计算
    test_script_path = os.path.join(scripts_dir, "generate_refined_report.py")
    if os.path.exists(test_script_path):
        # 计算脚本中使用的路径
        script_base = os.path.dirname(os.path.dirname(test_script_path))
        test_pic_path = os.path.join(script_base, "pictures", "viz_compare_raw_axial.png")
        if os.path.exists(test_pic_path):
            print("  ✅ 报告脚本图片路径正确")
        else:
            print(f"  ⚠️  图片路径可能有问题: {test_pic_path}")
            warnings.append("报告脚本图片路径可能不正确")
    else:
        print("  ⚠️  无法验证报告脚本路径")
    
    print()
    print("=" * 60)
    
    # 总结
    if errors:
        print("❌ 发现错误:")
        for error in errors:
            print(f"  - {error}")
        print()
    
    if warnings:
        print("⚠️  警告:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    if not errors and not warnings:
        print("✅ 所有路径检查通过！")
        return True
    elif not errors:
        print("✅ 路径检查通过（有警告但不影响运行）")
        return True
    else:
        print("❌ 发现错误，请修复后重试")
        return False

if __name__ == "__main__":
    success = check_paths()
    sys.exit(0 if success else 1)
