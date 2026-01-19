#!/bin/bash
# direnv 测试脚本
# 用于验证 direnv 配置是否正确

echo "========================================================"
echo "     direnv 配置测试"
echo "========================================================"
echo ""

# 1. 检查 direnv 是否已安装
if command -v direnv &> /dev/null; then
    echo "✅ direnv 已安装: $(direnv --version)"
else
    echo "❌ direnv 未安装"
    exit 1
fi

# 2. 检查 ~/.zshrc 配置
if grep -q "direnv hook zsh" ~/.zshrc 2>/dev/null; then
    echo "✅ direnv hook 已在 ~/.zshrc 中配置"
else
    echo "❌ direnv hook 未在 ~/.zshrc 中配置"
    echo "   请运行: ./完成direnv配置.sh"
    exit 1
fi

# 3. 检查 .envrc 文件
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

if [ -f ".envrc" ]; then
    echo "✅ .envrc 文件存在"
else
    echo "❌ .envrc 文件不存在"
    exit 1
fi

# 4. 检查虚拟环境
if [ -d ".venv" ]; then
    echo "✅ 虚拟环境目录存在: .venv"
elif [ -d "venv" ]; then
    echo "✅ 虚拟环境目录存在: venv"
else
    echo "❌ 虚拟环境目录不存在"
    exit 1
fi

echo ""
echo "========================================================"
echo "✅ 基本配置检查通过！"
echo "========================================================"
echo ""
echo "⚠️  重要提示："
echo "   要使 direnv 生效，您需要："
echo ""
echo "   1. 重新加载 shell 配置:"
echo "      source ~/.zshrc"
echo ""
echo "   2. 或者打开新的终端窗口"
echo ""
echo "   3. 然后进入项目目录测试:"
echo "      cd $PROJECT_DIR"
echo ""
echo "   如果配置正确，应该看到:"
echo "      direnv: loading .envrc"
echo "      提示符前显示: (.venv)"
echo ""
