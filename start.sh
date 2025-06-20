#!/bin/bash

# AI多功能工具平台启动脚本
echo "🚀 正在启动 AI多功能工具平台..."
echo "📅 时间: $(date)"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查依赖包
echo "📦 检查依赖包..."
if ! python3 -c "import gradio" &> /dev/null; then
    echo "📥 正在安装依赖包..."
    pip install -r requirements.txt
fi

# 启动应用
echo "🌐 启动Gradio应用..."
python3 app.py

echo "✅ 应用已启动"
echo "🔗 本地访问: http://localhost:7860"
echo "🌍 公网访问: 请查看控制台输出的公网链接"
