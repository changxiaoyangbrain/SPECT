#!/bin/bash
# 手动激活虚拟环境的便捷脚本
# 使用方法: source activate.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ 虚拟环境已激活: $(which python)"
    echo "📦 Python 版本: $(python --version)"
    echo "📂 工作目录: $(pwd)"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活: $(which python)"
    echo "📦 Python 版本: $(python --version)"
    echo "📂 工作目录: $(pwd)"
else
    echo "❌ 错误: 未找到虚拟环境目录 (.venv 或 venv)"
    echo "请先运行: ./scripts/setup_venv.sh"
    return 1
fi
