#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP增强版DOCX处理器 - 综合功能测试
测试所有功能，特别关注：
1. 表格行列的中间位置插入
2. 图片编辑功能
3. 其他核心功能
"""

import sys
import os

def test_mcp_functions():
    """测试所有MCP功能"""
    
    print("🚀 开始MCP增强版DOCX处理器综合测试")
    print("=" * 60)
    
    # 1. 打开文档
    print("\n📂 1. 打开测试文档")
    try:
        from mcp_enhanced_docx_processor_open_document import mcp_enhanced_docx_processor_open_document
        result = mcp_enhanced_docx_processor_open_document("202308764104+陈杰.docx")
        print(f"✅ 打开文档: {result}")
    except Exception as e:
        print(f"❌ 打开文档失败: {e}")
        return False
    
    # 2. 获取文档信息
    print("\n📊 2. 获取文档信息")
    try:
        from mcp_enhanced_docx_processor_get_document_info import mcp_enhanced_docx_processor_get_document_info
        result = mcp_enhanced_docx_processor_get_document_info("dummy")
        print(f"✅ 文档信息: {result}")
    except Exception as e:
        print(f"❌ 获取文档信息失败: {e}")
    
    # 3. 测试图片功能
    print("\n🖼️ 3. 测试图片功能")
    
    # 3.1 列出现有图片
    print("\n📋 3.1 列出文档中的图片")
    try:
        from mcp_enhanced_docx_processor_list_images import mcp_enhanced_docx_processor_list_images
        result = mcp_enhanced_docx_processor_list_images("dummy")
        print(f"✅ 图片列表: {result}")
    except Exception as e:
        print(f"❌ 列出图片失败: {e}")
    
    # 3.2 测试图片大小调整
    print("\n📏 3.2 测试图片大小调整")
    try:
        from mcp_enhanced_docx_processor_resize_image import mcp_enhanced_docx_processor_resize_image
        result = mcp_enhanced_docx_processor_resize_image(0, "3cm", "2cm", True)
        print(f"✅ 调整图片大小: {result}")
    except Exception as e:
        print(f"❌ 调整图片大小失败: {e}")
    
    # 3.3 添加新图片（如果有图片文件）
    print("\n➕ 3.3 测试添加图片")
    # 检查是否有可用的图片文件
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']:
        import glob
        image_files.extend(glob.glob(ext))
    
    if image_files:
        try:
            from mcp_enhanced_docx_processor_add_image import mcp_enhanced_docx_processor_add_image
            result = mcp_enhanced_docx_processor_add_image(
                image_files[0], "4cm", "3cm", "center", None
            )
            print(f"✅ 添加图片: {result}")
        except Exception as e:
            print(f"❌ 添加图片失败: {e}")
    else:
        print("⚠️ 未找到可用的图片文件，跳过图片添加测试")
    
    # 4. 测试表格功能
    print("\n📋 4. 测试表格功能")
    
    # 4.1 添加新表格
    print("\n➕ 4.1 添加新表格")
    try:
        from mcp_enhanced_docx_processor_add_table import mcp_enhanced_docx_processor_add_table
        result = mcp_enhanced_docx_processor_add_table(
            3, 3, [
                ["标题1", "标题2", "标题3"],
                ["数据1", "数据2", "数据3"],
                ["数据4", "数据5", "数据6"]
            ]
        )
        print(f"✅ 添加表格: {result}")
    except Exception as e:
        print(f"❌ 添加表格失败: {e}")
    
    # 4.2 测试表格行操作
    print("\n📝 4.2 测试表格行操作")
    try:
        from mcp_enhanced_docx_processor_add_table_row import mcp_enhanced_docx_processor_add_table_row
        # 添加行到第一个表格
        result = mcp_enhanced_docx_processor_add_table_row(0, ["新行1", "新行2", "新行3"])
        print(f"✅ 添加表格行: {result}")
        
        # 编辑新添加的行
        from mcp_enhanced_docx_processor_edit_table_cell import mcp_enhanced_docx_processor_edit_table_cell
        result = mcp_enhanced_docx_processor_edit_table_cell(0, -1, 0, "🆕 最新添加的行")
        print(f"✅ 编辑表格单元格: {result}")
    except Exception as e:
        print(f"❌ 表格行操作失败: {e}")
    
    # 4.3 测试表格列操作
    print("\n📝 4.3 测试表格列操作")
    try:
        from mcp_enhanced_docx_processor_add_table_column import mcp_enhanced_docx_processor_add_table_column
        # 添加列到第一个表格的中间位置（索引1）
        result = mcp_enhanced_docx_processor_add_table_column(
            0, 1, ["新列标题", "新列数据1", "新列数据2", "新列数据3"]
        )
        print(f"✅ 在中间位置添加表格列: {result}")
    except Exception as e:
        print(f"❌ 表格列操作失败: {e}")
    
    # 5. 测试文本格式功能
    print("\n🎨 5. 测试文本格式功能")
    
    # 5.1 添加格式化段落
    print("\n➕ 5.1 添加格式化段落")
    try:
        from mcp_enhanced_docx_processor_add_paragraph import mcp_enhanced_docx_processor_add_paragraph
        result = mcp_enhanced_docx_processor_add_paragraph(
            "🎉 这是一个测试段落，展示各种格式效果！", 
            True, True, True, 16, "Arial", "#FF0000", "center"
        )
        print(f"✅ 添加格式化段落: {result}")
    except Exception as e:
        print(f"❌ 添加段落失败: {e}")
    
    # 5.2 添加标题
    print("\n📝 5.2 添加标题")
    try:
        from mcp_enhanced_docx_processor_add_heading import mcp_enhanced_docx_processor_add_heading
        result = mcp_enhanced_docx_processor_add_heading("🔥 测试功能完成报告", 2)
        print(f"✅ 添加标题: {result}")
    except Exception as e:
        print(f"❌ 添加标题失败: {e}")
    
    # 6. 测试搜索和替换功能
    print("\n🔍 6. 测试搜索和替换功能")
    
    # 6.1 搜索文本
    print("\n🔎 6.1 搜索文本")
    try:
        from mcp_enhanced_docx_processor_search_text import mcp_enhanced_docx_processor_search_text
        result = mcp_enhanced_docx_processor_search_text("测试")
        print(f"✅ 搜索结果: {result}")
    except Exception as e:
        print(f"❌ 搜索文本失败: {e}")
    
    # 6.2 查找替换
    print("\n🔄 6.2 查找替换")
    try:
        from mcp_enhanced_docx_processor_find_and_replace import mcp_enhanced_docx_processor_find_and_replace
        result = mcp_enhanced_docx_processor_find_and_replace("测试", "✅测试成功")
        print(f"✅ 查找替换: {result}")
    except Exception as e:
        print(f"❌ 查找替换失败: {e}")
    
    # 7. 测试页面设置
    print("\n📄 7. 测试页面设置")
    try:
        from mcp_enhanced_docx_processor_set_page_margins import mcp_enhanced_docx_processor_set_page_margins
        result = mcp_enhanced_docx_processor_set_page_margins(2.5, 2.5, 2.0, 2.0)
        print(f"✅ 设置页边距: {result}")
    except Exception as e:
        print(f"❌ 设置页边距失败: {e}")
    
    # 8. 保存文档
    print("\n💾 8. 保存文档")
    try:
        from mcp_enhanced_docx_processor_save_document import mcp_enhanced_docx_processor_save_document
        result = mcp_enhanced_docx_processor_save_document("dummy")
        print(f"✅ 保存文档: {result}")
    except Exception as e:
        print(f"❌ 保存文档失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎊 综合功能测试完成！")
    return True

if __name__ == "__main__":
    # 尝试通过MCP工具直接调用
    print("🧪 使用MCP工具进行测试...")
    
    # 由于无法直接导入MCP工具，我们将使用执行代码的方式
    print("注意：这个脚本需要在MCP环境中运行MCP工具")
    print("请在支持MCP的环境中逐一测试各项功能")
