#!/bin/bash
# direnv 自动配置脚本
# 用于配置 direnv 自动激活虚拟环境

set -e

echo "========================================================"
echo "     direnv 自动激活虚拟环境配置脚本"
echo "========================================================"
echo ""

# 1. 检查 direnv 是否已安装
if ! command -v direnv &> /dev/null; then
    echo "❌ direnv 未安装"
    echo ""
    echo "正在尝试安装 direnv..."
    echo ""
    
    # 尝试使用 brew 安装
    if command -v brew &> /dev/null; then
        echo "使用 Homebrew 安装 direnv..."
        brew install direnv
    else
        echo "⚠️  未找到 Homebrew，请手动安装 direnv:"
        echo "   macOS: brew install direnv"
        echo "   Linux: 使用系统包管理器安装"
        echo ""
        echo "安装完成后，请重新运行此脚本。"
        exit 1
    fi
else
    echo "✅ direnv 已安装: $(direnv --version)"
fi

echo ""

# 2. 配置 zsh
ZSHRC_FILE="$HOME/.zshrc"
HOOK_LINE='eval "$(direnv hook zsh)"'

if grep -q "direnv hook zsh" "$ZSHRC_FILE" 2>/dev/null; then
    echo "✅ direnv hook 已在 ~/.zshrc 中配置"
else
    echo "📝 正在配置 ~/.zshrc..."
    echo "" >> "$ZSHRC_FILE"
    echo "# direnv 配置 - 自动激活虚拟环境" >> "$ZSHRC_FILE"
    echo "$HOOK_LINE" >> "$ZSHRC_FILE"
    echo "✅ 已添加 direnv hook 到 ~/.zshrc"
fi

echo ""

# 3. 允许项目的 .envrc
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

if [ -f ".envrc" ]; then
    echo "📝 正在允许项目的 .envrc 文件..."
    direnv allow
    echo "✅ 已允许项目的 .envrc"
else
    echo "❌ 未找到 .envrc 文件"
    exit 1
fi

echo ""
echo "========================================================"
echo "✅ 配置完成！"
echo "========================================================"
echo ""
echo "下一步操作："
echo "1. 重新加载 shell 配置:"
echo "   source ~/.zshrc"
echo ""
echo "2. 或者打开新的终端窗口"
echo ""
echo "3. 进入项目目录测试:"
echo "   cd $PROJECT_DIR"
echo "   应该看到: direnv: loading .envrc"
echo "   提示符前应该有: (.venv)"
echo ""
echo "4. 离开项目目录测试:"
echo "   cd ~"
echo "   应该看到: direnv: unloading"
echo ""
