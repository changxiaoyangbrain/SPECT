#!/bin/bash
# 完成 direnv 配置脚本
# 用于添加 direnv hook 到 ~/.zshrc

echo "========================================================"
echo "     完成 direnv 配置"
echo "========================================================"
echo ""

# 检查 direnv 是否已安装
if ! command -v direnv &> /dev/null; then
    echo "❌ direnv 未安装，请先运行: brew install direnv"
    exit 1
fi

echo "✅ direnv 已安装: $(direnv --version)"
echo ""

# 检查 ~/.zshrc 中是否已有 direnv hook
if grep -q "direnv hook zsh" ~/.zshrc 2>/dev/null; then
    echo "✅ direnv hook 已在 ~/.zshrc 中配置"
else
    echo "📝 正在添加 direnv hook 到 ~/.zshrc..."
    echo '' >> ~/.zshrc
    echo '# direnv 配置 - 自动激活虚拟环境' >> ~/.zshrc
    echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
    echo "✅ 已添加 direnv hook 到 ~/.zshrc"
fi

echo ""

# 允许项目的 .envrc
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
echo "4. 验证 Python 路径:"
echo "   which python"
echo "   应该显示: $PROJECT_DIR/.venv/bin/python"
echo ""
