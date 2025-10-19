#!/bin/bash
# 上传到PyPI的脚本

echo "📦 DOCX MCP 上传到PyPI"
echo "================================"
echo ""

# 检查dist目录是否存在
if [ ! -d "dist" ]; then
    echo "❌ 错误: dist目录不存在，请先运行构建命令"
    echo "   python -m build"
    exit 1
fi

# 检查是否有构建文件
if [ ! -f "dist/docx_mcp-0.1.5-py3-none-any.whl" ]; then
    echo "❌ 错误: 找不到wheel文件，请先运行构建命令"
    echo "   python -m build"
    exit 1
fi

echo "✅ 找到构建文件:"
ls -lh dist/

echo ""
echo "📋 上传选项:"
echo "1. 上传到 TestPyPI (测试环境，推荐)"
echo "2. 上传到 PyPI (正式环境)"
echo "3. 退出"
echo ""

read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🧪 上传到 TestPyPI..."
        echo "================================"
        python -m twine upload --repository testpypi dist/*
        echo ""
        echo "✅ 上传完成！"
        echo ""
        echo "测试安装命令:"
        echo "pip install --index-url https://test.pypi.org/simple/ docx-mcp==0.1.5"
        ;;
    2)
        echo ""
        echo "⚠️  警告: 即将上传到正式PyPI环境"
        read -p "确认上传? (yes/no): " confirm
        if [ "$confirm" == "yes" ]; then
            echo ""
            echo "🚀 上传到 PyPI..."
            echo "================================"
            python -m twine upload dist/*
            echo ""
            echo "✅ 上传完成！"
            echo ""
            echo "安装命令:"
            echo "pip install docx-mcp==0.1.5"
        else
            echo "❌ 取消上传"
        fi
        ;;
    3)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

