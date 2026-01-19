#!/bin/bash
# SPECT 项目虚拟环境设置脚本
# 用于 macOS/Linux 系统

set -e  # 遇到错误立即退出

echo "========================================================"
echo "     SPECT Project Virtual Environment Setup"
echo "========================================================"
echo ""

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 未安装或不在 PATH 中。"
    echo "请安装 Python 3.8+ 后重试。"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "[INFO] 检测到: $PYTHON_VERSION"
echo ""

# 2. 创建虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "[INFO] 正在创建虚拟环境 '.venv'..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] 创建虚拟环境失败。"
        exit 1
    fi
    echo "[INFO] 虚拟环境创建成功。"
else
    echo "[INFO] 虚拟环境 '.venv' 已存在。"
fi

# 3. 激活虚拟环境并安装依赖
echo ""
echo "[INFO] 正在安装/更新依赖..."
source .venv/bin/activate
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] 依赖安装失败。"
    exit 1
fi

echo ""
echo "========================================================"
echo "[SUCCESS] 虚拟环境设置完成！"
echo "========================================================"
echo ""
echo "使用方法："
echo "  激活虚拟环境: source .venv/bin/activate"
echo "  退出虚拟环境: deactivate"
echo "  运行项目:     python main_pipeline.py"
echo ""
