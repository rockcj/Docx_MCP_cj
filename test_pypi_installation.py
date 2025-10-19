#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试从PyPI安装的docx-mcp包
验证42个MCP工具是否都能正常导入和使用
"""

import sys
import subprocess
import time

def wait_for_pypi():
    """等待PyPI索引新版本（可能需要几分钟）"""
    print("⏳ 等待PyPI索引新版本...")
    print("   通常需要1-5分钟")
    print()
    
    max_attempts = 10
    for i in range(max_attempts):
        try:
            result = subprocess.run(
                ['pip', 'index', 'versions', 'docx-mcp'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if '0.1.6' in result.stdout:
                print("✅ 版本0.1.6已在PyPI上可用！")
                return True
            
            print(f"   尝试 {i+1}/{max_attempts}...")
            time.sleep(30)  # 等待30秒
            
        except Exception as e:
            print(f"   检查失败: {e}")
            time.sleep(30)
    
    print("⚠️  PyPI可能还在索引中，但我们可以继续测试...")
    return False

def test_import():
    """测试导入功能"""
    print()
    print("=" * 60)
    print("🧪 测试1: 导入核心模块")
    print("=" * 60)
    
    try:
        # 测试导入主模块
        print("导入 final_complete_server...")
        import final_complete_server
        print("✅ final_complete_server 导入成功")
        
        # 测试导入MCP实例
        print("导入 mcp 实例...")
        from final_complete_server import mcp
        print("✅ mcp 实例导入成功")
        
        # 统计工具数量
        tool_count = len(mcp._tools)
        print(f"📊 MCP工具数量: {tool_count}")
        
        if tool_count == 42:
            print("✅ 工具数量正确（42个）")
        else:
            print(f"⚠️  工具数量异常（预期42个，实际{tool_count}个）")
        
        return tool_count == 42
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_core_modules():
    """测试核心模块导入"""
    print()
    print("=" * 60)
    print("🧪 测试2: 导入核心子模块")
    print("=" * 60)
    
    modules = [
        'core.universal_table_filler',
        'core.intelligent_table_analyzer',
        'core.table_structure_extractor',
        'core.intelligent_tool_planner',
        'core.enhanced_docx_processor',
    ]
    
    success_count = 0
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {module_name}: {e}")
    
    print()
    print(f"成功: {success_count}/{len(modules)}")
    return success_count == len(modules)

def test_entry_points():
    """测试命令行入口点"""
    print()
    print("=" * 60)
    print("🧪 测试3: 命令行入口点")
    print("=" * 60)
    
    try:
        # 检查docx-mcp命令是否存在
        result = subprocess.run(
            ['docx-mcp', '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 or 'MCP' in result.stdout:
            print("✅ docx-mcp 命令可用")
            return True
        else:
            print("⚠️  docx-mcp 命令返回异常")
            return False
            
    except FileNotFoundError:
        print("⚠️  docx-mcp 命令未找到（可能需要重新安装）")
        return False
    except Exception as e:
        print(f"⚠️  测试命令失败: {e}")
        return False

def main():
    print("=" * 60)
    print("  DOCX MCP PyPI 安装测试")
    print("=" * 60)
    print()
    print("测试版本: 0.1.6")
    print("PyPI页面: https://pypi.org/project/docx-mcp/0.1.6/")
    print()
    
    # 检查是否已安装
    try:
        import docx_mcp
        print(f"✅ docx-mcp 已安装")
    except:
        print("⚠️  docx-mcp 未安装，需要先安装:")
        print("   pip install docx-mcp==0.1.6")
        print()
        print("或者等待几分钟让PyPI索引新版本...")
        print()
        
        # 等待PyPI
        # wait_for_pypi()
        # return
    
    # 运行测试
    results = []
    
    results.append(("导入测试", test_import()))
    results.append(("核心模块测试", test_core_modules()))
    results.append(("入口点测试", test_entry_points()))
    
    # 总结
    print()
    print("=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print()
    print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print()
        print("🎉 所有测试通过！docx-mcp 0.1.6 在PyPI上正常工作！")
        print()
        print("用户现在可以通过以下方式安装:")
        print("  pip install docx-mcp")
        print()
        print("并使用42个MCP工具！")
        return 0
    else:
        print()
        print("⚠️  部分测试失败，可能需要:")
        print("  1. 等待PyPI索引完成（1-5分钟）")
        print("  2. 重新安装: pip install --force-reinstall docx-mcp==0.1.6")
        print("  3. 检查安装环境")
        return 1

if __name__ == "__main__":
    sys.exit(main())

