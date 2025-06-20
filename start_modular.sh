#!/bin/bash

# Gradio多功能工具平台 - 模块化版本启动脚本
# 创建时间: 2025-06-19

echo "🚀 启动Gradio多功能工具平台 - 模块化版本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 检查环境..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

echo "✅ Python环境: $(python3 --version)"

# 检查并安装依赖
echo "📦 检查依赖包..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✅ 依赖包已安装/更新"
else
    echo "⚠️  requirements.txt 文件未找到"
fi

# 检查模块化文件
echo "🧩 检查模块化架构..."
if [ -f "app_modular.py" ]; then
    echo "✅ 主程序文件: app_modular.py"
else
    echo "❌ 主程序文件未找到: app_modular.py"
    exit 1
fi

if [ -f "config.py" ]; then
    echo "✅ 配置文件: config.py"
else
    echo "❌ 配置文件未找到: config.py"
    exit 1
fi

if [ -d "modules" ]; then
    module_count=$(find modules/ -name "*.py" ! -name "__init__.py" | wc -l)
    echo "✅ 功能模块: $module_count 个模块已就绪"
else
    echo "❌ 模块目录未找到: modules/"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌟 启动模块化应用..."
echo ""

# 启动应用
python3 app_modular.py

echo ""
echo "👋 应用已退出"
