#!/usr/bin/env python3
"""
测试虚拟环境自动激活脚本
用于验证虚拟环境是否正确激活
"""

import sys
import os

def test_venv_activation():
    """测试虚拟环境是否已激活"""
    print("=" * 60)
    print("虚拟环境激活测试")
    print("=" * 60)
    print()
    
    # 检查 Python 路径
    python_path = sys.executable
    print(f"📍 Python 路径: {python_path}")
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ 虚拟环境已激活")
        if '.venv' in python_path or 'venv' in python_path:
            print("✅ Python 路径指向项目虚拟环境")
        else:
            print("⚠️  Python 路径不在项目虚拟环境中")
    else:
        print("❌ 虚拟环境未激活")
        print("   请运行: source scripts/activate.sh")
        return False
    
    # 检查项目路径（tests 的父目录）
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"📂 项目路径: {project_path}")
    
    # 检查虚拟环境路径
    if '.venv' in python_path:
        venv_path = os.path.join(project_path, '.venv')
        if os.path.exists(venv_path):
            print(f"✅ 虚拟环境目录存在: {venv_path}")
        else:
            print(f"❌ 虚拟环境目录不存在: {venv_path}")
            return False
    
    # 检查关键依赖
    print()
    print("📦 检查关键依赖包:")
    required_packages = {
        'numpy': 'numpy',
        'pandas': 'pandas',
        'scipy': 'scipy',
        'matplotlib': 'matplotlib',
        'skimage': 'scikit-image',
        'docx': 'python-docx',
        'pptx': 'python-pptx',
    }
    
    all_ok = True
    for module_name, package_name in required_packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {package_name}: {version}")
        except ImportError:
            print(f"  ❌ {package_name}: 未安装")
            all_ok = False
    
    print()
    print("=" * 60)
    if in_venv and all_ok:
        print("✅ 所有检查通过！虚拟环境配置正确。")
        return True
    else:
        print("❌ 检查未通过，请检查配置。")
        return False

if __name__ == '__main__':
    success = test_venv_activation()
    sys.exit(0 if success else 1)
