#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试运行脚本
从tests目录运行所有测试文件
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """运行指定的测试文件"""
    print(f"\n🚀 运行测试: {test_file}")
    print("=" * 50)
    
    try:
        # 运行测试文件
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {test_file} 测试成功")
            print(result.stdout)
        else:
            print(f"❌ {test_file} 测试失败")
            print("错误输出:")
            print(result.stderr)
            print("标准输出:")
            print(result.stdout)
            
    except Exception as e:
        print(f"❌ 运行 {test_file} 时出错: {e}")
    
    print("=" * 50)

def main():
    """主函数"""
    print("🧪 DOCX MCP 测试套件")
    print("=" * 60)
    
    # 获取tests目录中的所有Python测试文件
    tests_dir = Path(__file__).parent
    test_files = [
        "test_image_functionality.py",
        "comprehensive_image_test.py", 
        "test_row_insertion.py",
        "verify_row_insertion.py",
        "comprehensive_test.py"
    ]
    
    # 过滤存在的测试文件
    existing_tests = [f for f in test_files if (tests_dir / f).exists()]
    
    if not existing_tests:
        print("❌ 没有找到测试文件")
        return
    
    print(f"📋 找到 {len(existing_tests)} 个测试文件:")
    for test in existing_tests:
        print(f"  - {test}")
    
    print(f"\n🎯 开始运行测试...")
    
    # 运行所有测试
    for test_file in existing_tests:
        run_test(test_file)
    
    print(f"\n🎉 所有测试完成！")
    print(f"\n📁 测试结果文件位置:")
    print(f"  - 文档文件: ../docs/")
    print(f"  - 测试图片: ../images/")
    print(f"  - 测试脚本: ./")

if __name__ == "__main__":
    main()
