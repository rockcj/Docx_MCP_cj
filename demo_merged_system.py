#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并后的表格填充系统演示
展示坐标填充为重点的新架构
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.universal_table_filler import UniversalTableFiller

def demo_coordinate_workflow():
    """演示坐标填充工作流程"""
    print("🎯 坐标填充工作流程演示（主要功能）")
    print("=" * 60)
    
    # 测试文档路径
    test_doc = r"docs\附件7：岭南师范学院毕业（生产）实习鉴定表A3打印.docx"
    
    if not os.path.exists(test_doc):
        print(f"❌ 演示文档不存在: {test_doc}")
        return False
    
    try:
        filler = UniversalTableFiller()
        
        print("步骤1: 📍 分析文档坐标结构")
        print("-" * 40)
        
        # 分析文档坐标
        analysis_result = filler.analyze_and_get_coordinates(test_doc)
        
        if "失败" in analysis_result:
            print(f"❌ 坐标分析失败: {analysis_result}")
            return False
        
        # 解析分析结果
        data = json.loads(analysis_result)
        
        print("✅ 坐标分析成功!")
        print(f"📊 发现 {len(data.get('field_coordinates', {}))} 个字段坐标")
        print(f"🕳️  发现 {len(data.get('empty_positions', []))} 个空位")
        print(f"💡 生成 {len(data.get('fill_suggestions', []))} 个填充建议")
        
        # 显示关键字段坐标
        field_coordinates = data.get('field_coordinates', {})
        key_fields = ['姓  名', '学  号', '所在学院', '专业、班别', '实习单位', '实习时间']
        
        print(f"\n🏷️  关键字段坐标:")
        for field in key_fields:
            if field in field_coordinates:
                position = field_coordinates[field]
                print(f"   - '{field}': 表格{position[0]}, 行{position[1]}, 列{position[2]}")
        
        # 显示填充建议
        fill_suggestions = data.get('fill_suggestions', [])
        key_suggestions = [s for s in fill_suggestions if s['field_name'] in key_fields]
        
        print(f"\n💡 关键填充建议:")
        for suggestion in key_suggestions:
            pos = suggestion['suggested_position']
            print(f"   - {suggestion['field_name']} → 表格{pos[0]}, 行{pos[1]}, 列{pos[2]} ({suggestion['rule_type']})")
        
        print(f"\n步骤2: 🤖 AI创建填充计划")
        print("-" * 40)
        
        # 模拟AI基于分析结果创建填充计划
        fill_plan = {
            "张三": [1, 1, 2],      # 姓名位置
            "2024001234": [1, 2, 2], # 学号位置
            "计算机学院": [1, 1, 4],  # 学院位置
            "软件工程": [1, 1, 6],    # 专业位置
            "腾讯科技": [1, 2, 4],    # 实习单位位置
            "2024年7月-9月": [1, 2, 6]  # 实习时间位置
        }
        
        print("✅ AI基于坐标分析创建填充计划:")
        for data, coord in fill_plan.items():
            print(f"   - '{data}' → 表格{coord[0]}, 行{coord[1]}, 列{coord[2]}")
        
        print(f"\n步骤3: 🎯 执行坐标填充")
        print("-" * 40)
        
        # 创建测试文档副本
        import shutil
        test_doc_copy = test_doc.replace(".docx", "_coordinate_demo.docx")
        shutil.copy2(test_doc, test_doc_copy)
        
        # 转换格式
        coordinate_data = {}
        for data, coord_list in fill_plan.items():
            coordinate_data[data] = tuple(coord_list)
        
        # 执行坐标填充
        fill_result = filler.fill_with_coordinates(test_doc_copy, coordinate_data)
        
        if "失败" in fill_result:
            print(f"❌ 坐标填充失败: {fill_result}")
            if os.path.exists(test_doc_copy):
                os.remove(test_doc_copy)
            return False
        
        print("✅ 坐标填充成功!")
        print(f"📋 填充结果: {fill_result}")
        
        print(f"\n步骤4: 📁 保存结果")
        print("-" * 40)
        print(f"✅ 文档已保存为: {test_doc_copy}")
        
        return test_doc_copy
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_simplified_intelligent_fill():
    """演示简化的智能填充功能"""
    print("\n\n🤖 简化的智能填充功能演示（辅助功能）")
    print("=" * 60)
    
    test_doc = r"docs\附件7：岭南师范学院毕业（生产）实习鉴定表A3打印.docx"
    
    try:
        filler = UniversalTableFiller()
        
        print("📝 尝试使用简化的智能填充功能...")
        
        fill_data = {
            "姓名": "李四",
            "学号": "2024005678",
            "学院": "软件学院"
        }
        
        print(f"📊 填充数据: {fill_data}")
        
        # 模拟智能填充的简化响应
        suggestion = f"""
智能填充功能已简化。建议使用更精确的坐标填充方式：

1. 首先调用 extract_fillable_fields('{test_doc}') 获取坐标信息
2. 根据返回的坐标信息创建填充计划
3. 调用 fill_with_coordinates() 执行精确填充

这样可以获得更好的填充效果和更精确的控制。
        """
        
        print(f"\n📋 智能填充响应:")
        print(suggestion)
        
        print("\n✅ 智能填充功能已正确简化为辅助功能")
        print("🎯 系统引导用户使用更精确的坐标填充方式")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_ai_workflow():
    """演示AI工作流程"""
    print("\n\n🤖 AI工作流程演示")
    print("=" * 60)
    
    print("""
🔄 合并后的AI工作流程（坐标填充为重点）：

1️⃣  AI接收用户请求: "帮我填充这个表格"
   ↓
2️⃣  AI调用 extract_fillable_fields() 分析文档坐标
   ↓
3️⃣  AI获得详细的坐标信息:
      {
        "field_coordinates": {
          "姓  名": [1, 0, 1],
          "学  号": [1, 1, 1],
          "所在学院": [1, 0, 3],
          ...
        },
        "empty_positions": [
          {"index": 1, "position": [1, 2, 3], "description": "空位1"},
          {"index": 2, "position": [1, 2, 5], "description": "空位2"}
        ],
        "fill_suggestions": [
          {"field_name": "姓  名", "suggested_position": [1, 1, 1], "rule_type": "field_below"},
          ...
        ],
        "usage_instructions": [
          "1. 使用 field_coordinates 查看字段位置",
          "2. 使用 empty_positions 查看可填充的空位",
          "3. 返回格式: {\"数据内容\": [表格索引, 行索引, 列索引]}"
        ]
      }
   ↓
4️⃣  AI基于坐标信息创建精确的填充计划:
      {
        "张三": [1, 1, 1],
        "2024001234": [1, 2, 1],
        "计算机学院": [1, 1, 3],
        ...
      }
   ↓
5️⃣  AI调用 fill_with_coordinates() 执行精确填充
   ↓
6️⃣  AI返回详细的填充结果给用户

✨ 新架构优势：
   - 🎯 坐标填充为主要功能，提供精确控制
   - 🔍 坐标分析为重点功能，提供详细结构信息
   - 🤖 智能填充简化为辅助功能，引导用户使用坐标填充
   - 📍 完全基于坐标的精确填充，避免智能匹配的不确定性
   - 🔄 清晰的工作流程，AI可以自主完成整个填充过程
""")

def cleanup_demo_files():
    """清理演示文件"""
    print("\n\n🗑️  清理演示文件...")
    
    demo_files = [
        r"docs\附件7：岭南师范学院毕业（生产）实习鉴定表A3打印_coordinate_demo.docx"
    ]
    
    cleaned_count = 0
    for file_path in demo_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"   ✅ 已删除: {file_path}")
                cleaned_count += 1
            except Exception as e:
                print(f"   ❌ 删除失败: {file_path} - {e}")
    
    if cleaned_count > 0:
        print(f"🗑️  清理完成，共删除 {cleaned_count} 个演示文件")
    else:
        print("🗑️  没有需要清理的演示文件")

def main():
    """主演示函数"""
    print("🚀 合并后的表格填充系统演示")
    print("🎯 坐标填充为重点的新架构")
    print("=" * 80)
    
    try:
        # 演示坐标填充工作流程（主要功能）
        coordinate_result = demo_coordinate_workflow()
        if not coordinate_result:
            print("❌ 演示终止：坐标填充演示失败")
            return False
        
        # 演示简化的智能填充（辅助功能）
        intelligent_result = demo_simplified_intelligent_fill()
        if not intelligent_result:
            print("❌ 演示终止：智能填充演示失败")
            return False
        
        # AI工作流程演示
        demo_ai_workflow()
        
        print("\n" + "=" * 80)
        print("🎉 演示完成！")
        print("✨ 合并后系统的主要特点：")
        print("   1. 🎯 坐标填充为主要功能 - 提供精确的位置控制")
        print("   2. 🔍 坐标分析为重点功能 - 提供详细的结构信息")
        print("   3. 🤖 智能填充简化为辅助功能 - 引导用户使用坐标填充")
        print("   4. 📍 完全基于坐标的精确填充 - 避免智能匹配的不确定性")
        print("   5. 🔄 清晰的工作流程 - AI可以自主完成整个填充过程")
        print("   6. 💡 智能建议系统 - 提供填充建议和使用指导")
        
        # 询问是否清理演示文件
        print(f"\n📁 演示过程中创建的文件:")
        if coordinate_result and isinstance(coordinate_result, str):
            print(f"   - {coordinate_result}")
        
        cleanup_demo_files()
        
        return True
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        cleanup_demo_files()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
