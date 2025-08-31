#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DOCX MCP处理器主入口（兼容性版本）
保持与原有版本的兼容性，同时支持增强功能

使用建议:
- 新项目请使用: python enhanced_main.py
- 原有项目可继续使用: python main.py
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数 - 兼容性入口"""
    print("🔄 DOCX MCP处理器 (兼容性模式)")
    print("💡 建议使用增强版: python enhanced_main.py")
    print("📖 查看帮助: python enhanced_main.py --help")
    print()
    
    # 检查是否有命令行参数要求增强功能
    if len(sys.argv) > 1 and any(arg in sys.argv for arg in ['--enhanced', '--interactive', '--help']):
        print("🚀 切换到增强模式...")
        from enhanced_main import main as enhanced_main
        return enhanced_main()
    
    # 原有功能保持不变
    try:
        from fastmcp import FastMCP
        from core.docx_processor import DocxProcessor
        from core.models import DocumentPatch, TableOperation, TableOperationType, CellFormat, TableFormat, CellAlignment, BorderStyle
        
        # 创建原有的MCP服务
        mcp = FastMCP("docx_handler")
        
        # 这里可以添加原有的工具定义...
        print("启动原有MCP服务器...")
        mcp.run(transport='stdio')
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("📦 请安装依赖: pip install -r requirements.txt")
        print("🚀 或使用增强版: python enhanced_main.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
