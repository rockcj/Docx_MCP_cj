#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试表格行指定位置插入功能
"""

import os
import sys

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.enhanced_docx_processor import EnhancedDocxProcessor

def test_row_insertion():
    """测试行插入功能"""
    
    print("🧪 测试表格行指定位置插入功能")
    print("=" * 50)
    
    # 创建处理器实例
    processor = EnhancedDocxProcessor()
    
    # 打开文档
    print("\n📂 1. 打开测试文档")
    result = processor.open_document("C:\\Users\\26818\\Desktop\\docx_mcp\\202308764104+陈杰.docx")
    print(f"结果: {result}")
    
    # 获取文档信息
    print("\n📊 2. 获取文档信息")
    info = processor.get_document_info()
    print(f"文档信息: {info}")
    
    # 标记现有行
    print("\n📝 3. 标记现有行")
    processor.edit_table_cell(0, 0, 0, "🏷️ 测试-原第1行")
    processor.edit_table_cell(0, 1, 0, "🏷️ 测试-原第2行")
    processor.edit_table_cell(0, 2, 0, "🏷️ 测试-原第3行")
    print("标记完成")
    
    # 测试在第1、2行之间插入新行
    print("\n🆕 4. 在第1、2行之间插入新行（row_index=1）")
    result = processor.add_table_row(
        table_index=0,
        data=["🎯 新插入的行", "数据A", "数据B"],
        row_index=1  # 在索引1位置插入，即第1行和第2行之间
    )
    print(f"插入结果: {result}")
    
    # 验证插入结果
    print("\n✅ 5. 验证插入结果")
    processor.edit_table_cell(0, 1, 1, "✅ 这是新插入的行的第2列")
    print("验证完成")
    
    # 测试在表格开头插入
    print("\n🏆 6. 在表格开头插入新行（row_index=0）")
    result = processor.add_table_row(
        table_index=0,
        data=["🚀 新的第1行", "开头数据1", "开头数据2"],
        row_index=0  # 在索引0位置插入，即表格开头
    )
    print(f"插入结果: {result}")
    
    # 验证开头插入
    print("\n✅ 7. 验证开头插入")
    processor.edit_table_cell(0, 0, 1, "✅ 这是新的第1行")
    print("验证完成")
    
    # 测试末尾添加（保持兼容性）
    print("\n📎 8. 在末尾添加行（保持兼容性）")
    result = processor.add_table_row(
        table_index=0,
        data=["📋 末尾新行", "末尾数据1", "末尾数据2"]
        # 不传row_index，使用默认行为
    )
    print(f"添加结果: {result}")
    
    # 保存文档
    print("\n💾 9. 保存测试结果")
    save_result = processor.save_document()
    print(f"保存结果: {save_result}")
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")
    
    # 显示最终结果
    print("\n📋 预期结果:")
    print("表格行顺序应该是:")
    print("- 第1行: 🚀 新的第1行 (row_index=0插入)")
    print("- 第2行: 🏷️ 测试-原第1行 (原第1行)")
    print("- 第3行: 🎯 新插入的行 (row_index=1插入)")
    print("- 第4行: 🏷️ 测试-原第2行 (原第2行)")
    print("- 第5行: 🏷️ 测试-原第3行 (原第3行)")
    print("- 第6行: 📍 新添加的第4行（末尾）(之前的测试)")
    print("- 第7行: 📋 末尾新行 (末尾添加)")

if __name__ == "__main__":
    try:
        test_row_insertion()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
