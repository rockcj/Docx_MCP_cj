#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试通用表格填充系统
验证新的智能表格分析和填充功能
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.intelligent_table_analyzer import IntelligentTableAnalyzer
from core.universal_table_filler import UniversalTableFiller

def test_table_analyzer():
    """测试表格分析器"""
    print("🔍 测试智能表格分析器...")
    
    # 测试文档路径
    test_doc = r"docs\附件7：岭南师范学院毕业（生产）实习鉴定表A3打印.docx"
    
    if not os.path.exists(test_doc):
        print(f"❌ 测试文档不存在: {test_doc}")
        return False
    
    try:
        analyzer = IntelligentTableAnalyzer()
        
        # 分析文档
        print(f"📄 分析文档: {test_doc}")
        result = analyzer.analyze_document(test_doc)
        
        if 'error' in result:
            print(f"❌ 分析失败: {result['error']}")
            return False
        
        print("✅ 文档分析成功!")
        
        # 显示分析结果摘要
        doc_info = result.get('document_info', {})
        print(f"📊 文档信息:")
        print(f"   - 总表格数: {doc_info.get('total_tables', 0)}")
        print(f"   - 字段总数: {result.get('total_fields', 0)}")
        print(f"   - 空位总数: {result.get('total_empty_positions', 0)}")
        print(f"   - 填充规则数: {result.get('total_fill_rules', 0)}")
        
        # 显示字段位置
        field_positions = result.get('field_positions', {})
        if field_positions:
            print(f"\n🏷️  发现的字段:")
            for field_name, position in field_positions.items():
                print(f"   - '{field_name}': {position}")
        
        # 显示填充规则
        fill_rules = result.get('fill_rules', [])
        if fill_rules:
            print(f"\n📋 填充规则:")
            for rule in fill_rules:
                print(f"   - {rule['field']} → {rule['fill_position']} ({rule['rule_type']})")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_universal_filler():
    """测试通用表格填充器"""
    print("\n🔧 测试通用表格填充器...")
    
    # 测试文档路径
    test_doc = r"docs\附件7：岭南师范学院毕业（生产）实习鉴定表A3打印.docx"
    
    if not os.path.exists(test_doc):
        print(f"❌ 测试文档不存在: {test_doc}")
        return False
    
    try:
        filler = UniversalTableFiller()
        
        # 测试文档分析（不填充）
        print(f"📄 分析文档结构...")
        analysis_result = filler.get_document_analysis(test_doc)
        
        if "失败" in analysis_result:
            print(f"❌ 分析失败: {analysis_result}")
            return False
        
        print("✅ 文档结构分析成功!")
        
        # 解析分析结果
        try:
            analysis_data = json.loads(analysis_result)
            print(f"📊 分析摘要:")
            print(f"   - 字段数: {len(analysis_data.get('field_positions', {}))}")
            print(f"   - 空位数: {len(analysis_data.get('empty_positions', {}))}")
            print(f"   - 规则数: {len(analysis_data.get('fill_rules', []))}")
        except json.JSONDecodeError:
            print("⚠️  无法解析分析结果JSON")
        
        # 测试智能填充
        print(f"\n🎯 测试智能填充...")
        test_data = {
            "姓名": "张三",
            "学号": "2023001234",
            "学院": "计算机学院",
            "专业": "计算机科学与技术"
        }
        
        # 创建测试文档副本
        import shutil
        test_doc_copy = test_doc.replace(".docx", "_test_copy.docx")
        shutil.copy2(test_doc, test_doc_copy)
        
        fill_result = filler.analyze_and_fill(test_doc_copy, test_data)
        
        if "失败" in fill_result:
            print(f"❌ 填充失败: {fill_result}")
            # 清理测试文件
            if os.path.exists(test_doc_copy):
                os.remove(test_doc_copy)
            return False
        
        print("✅ 智能填充成功!")
        print(f"📋 填充结果: {fill_result}")
        
        # 测试坐标填充
        print(f"\n🎯 测试坐标填充...")
        coordinate_data = {
            "李四": (1, 1, 3),
            "2024005678": (1, 2, 3),
            "软件学院": (1, 1, 5)
        }
        
        coord_result = filler.fill_with_coordinates(test_doc_copy, coordinate_data)
        
        if "失败" in coord_result:
            print(f"❌ 坐标填充失败: {coord_result}")
            # 清理测试文件
            if os.path.exists(test_doc_copy):
                os.remove(test_doc_copy)
            return False
        
        print("✅ 坐标填充成功!")
        print(f"📋 坐标填充结果: {coord_result}")
        
        # 清理测试文件
        if os.path.exists(test_doc_copy):
            print(f"🗑️  清理测试文件: {test_doc_copy}")
            os.remove(test_doc_copy)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_field_detection():
    """测试字段检测功能"""
    print("\n🔍 测试字段检测功能...")
    
    try:
        analyzer = IntelligentTableAnalyzer()
        
        # 测试各种字段名
        test_fields = [
            "姓名", "姓  名", "学生姓名",
            "学号", "学  号", "学生学号",
            "学院", "所在学院", "就读学院",
            "专业", "专业名称", "专业、班别",
            "实习单位", "实习公司",
            "实习时间", "实习期间",
            "指导教师", "指导老师",
            "联系方式", "联系电话",
            "成绩", "分数", "得分",
            "评价", "评语",
            "日期", "时间",
            "签名", "签字",
            "盖章", "印章"
        ]
        
        print("🧪 测试字段识别:")
        for field in test_fields:
            field_type = analyzer._identify_field_type(field)
            confidence = analyzer._calculate_field_confidence(field, field_type) if field_type else 0.0
            status = "✅" if field_type else "❌"
            print(f"   {status} '{field}' → {field_type} (置信度: {confidence:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ 字段检测测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试通用表格填充系统")
    print("=" * 50)
    
    test_results = []
    
    # 测试字段检测
    test_results.append(test_field_detection())
    
    # 测试表格分析器
    test_results.append(test_table_analyzer())
    
    # 测试通用填充器
    test_results.append(test_universal_filler())
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！通用表格填充系统工作正常！")
        return True
    else:
        print("⚠️  部分测试失败，请检查系统配置")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
