#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OSS工作流演示程序
展示自动OSS上传功能的完整流程
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.workflow_engine import WorkflowEngine
from core.enhanced_state_manager import EnhancedStateManager, OperationType, OperationStatus
from core.smart_suggestion_engine import SmartSuggestionEngine
from core.ai_guidance_enhancer import AIGuidanceEnhancer
from core.json_validation_engine import JSONValidationEngine

def demo_oss_workflow_basics():
    """演示OSS工作流基础功能"""
    print("=" * 60)
    print("🚀 OSS工作流基础功能演示")
    print("=" * 60)
    
    # 初始化工作流引擎
    workflow_engine = WorkflowEngine()
    
    # 1. 查看OSS相关的工作流
    print("\n📋 OSS相关的工作流:")
    workflows = workflow_engine.get_available_workflows()
    oss_workflows = [wf for wf in workflows if "oss" in wf.workflow_id or "upload" in wf.workflow_id]
    
    for workflow in oss_workflows:
        print(f"  • {workflow.workflow_name} ({workflow.workflow_id})")
        print(f"    描述: {workflow.description}")
        print(f"    分类: {workflow.category}")
        print(f"    预计时间: {workflow.estimated_duration}")
        print()
    
    # 2. 查看所有工作流中的OSS上传步骤
    print("🔄 包含OSS上传步骤的工作流:")
    for workflow in workflows:
        oss_steps = [step for step in workflow.steps if "oss" in step.step_name.lower() or "upload" in step.step_name.lower()]
        if oss_steps:
            print(f"  • {workflow.workflow_name}")
            for step in oss_steps:
                print(f"    - {step.step_name}: {step.description}")
            print()
    
    # 3. 基于意图推荐OSS工作流
    print("🎯 基于意图推荐OSS工作流:")
    intents = [
        "上传文档到云端",
        "提供下载链接",
        "分享文档",
        "保存到OSS"
    ]
    
    for intent in intents:
        suggestions = workflow_engine.suggest_workflows_by_intent(intent)
        print(f"  意图: {intent}")
        if suggestions:
            best_suggestion = suggestions[0]
            print(f"    推荐: {best_suggestion['workflow_name']}")
            print(f"    匹配分数: {best_suggestion['match_score']:.2f}")
            print(f"    推荐理由: {best_suggestion['reasons']}")
        else:
            print("    无相关推荐")
        print()

def demo_oss_workflow_execution():
    """演示OSS工作流执行"""
    print("=" * 60)
    print("⚡ OSS工作流执行演示")
    print("=" * 60)
    
    # 初始化组件
    temp_dir = tempfile.mkdtemp()
    state_manager = EnhancedStateManager(temp_dir)
    workflow_engine = WorkflowEngine()
    
    # 模拟OSS上传工具
    def mock_upload_tool(**kwargs):
        return {
            "success": True,
            "filename": "demo_document.docx",
            "download_url": "https://ggb-lzt.oss-cn-shenzhen.aliyuncs.com/demo_document.docx",
            "file_size": 2048,
            "message": "文档已成功上传到OSS"
        }
    
    def mock_validate_tool(**kwargs):
        return "文档验证通过"
    
    def mock_link_tool(**kwargs):
        return "下载链接已生成"
    
    # 注册模拟工具
    workflow_engine.register_tool_executor("upload_current_document_to_oss", mock_upload_tool)
    workflow_engine.register_tool_executor("validate_document_exists", mock_validate_tool)
    workflow_engine.register_tool_executor("get_download_link", mock_link_tool)
    
    # 1. 执行自动OSS上传工作流
    print("\n📤 执行自动OSS上传工作流:")
    result = workflow_engine.execute_workflow("auto_oss_upload", {
        "custom_filename": "演示文档.docx"
    })
    print(f"  执行结果: {result}")
    
    # 2. 记录操作历史
    print("\n📝 记录操作历史:")
    op_id = state_manager.record_operation(
        OperationType.CREATE_DOCUMENT,
        {"filename": "演示文档.docx", "auto_upload": True}
    )
    print(f"  操作ID: {op_id}")
    
    # 更新操作状态
    state_manager.update_operation_status(
        op_id, OperationStatus.COMPLETED, "文档已上传到OSS"
    )
    print("  操作状态已更新为完成")
    
    # 3. 获取操作历史
    print("\n📚 操作历史:")
    history = state_manager.get_operation_history(limit=5)
    for op in history:
        print(f"  • {op.operation_type.value} - {op.status.value}")
        print(f"    时间: {op.timestamp.strftime('%H:%M:%S')}")
        print(f"    参数: {op.parameters}")
        print()
    
    # 清理临时目录
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

def demo_oss_validation():
    """演示OSS数据验证"""
    print("=" * 60)
    print("🔍 OSS数据验证演示")
    print("=" * 60)
    
    # 初始化验证引擎
    validation_engine = JSONValidationEngine()
    
    # 1. 测试有效数据
    print("\n✅ 有效数据验证:")
    valid_data = {
        "custom_filename": "月度报告_202401.docx",
        "auto_upload": True
    }
    
    result = validation_engine.validate_json("oss_upload", valid_data)
    print(f"  验证结果: {'通过' if result.is_valid else '失败'}")
    if result.warnings:
        print(f"  警告: {result.warnings}")
    
    # 2. 测试无效数据
    print("\n❌ 无效数据验证:")
    invalid_data = {
        "custom_filename": "报告.doc",  # 错误的扩展名
        "auto_upload": True
    }
    
    result = validation_engine.validate_json("oss_upload", invalid_data)
    print(f"  验证结果: {'通过' if result.is_valid else '失败'}")
    if result.errors:
        print("  错误信息:")
        for error in result.errors:
            print(f"    • {error}")
    if result.suggestions:
        print("  建议:")
        for suggestion in result.suggestions:
            print(f"    • {suggestion}")
    
    # 3. 获取OSS验证模式示例
    print("\n📖 OSS验证模式示例:")
    examples = validation_engine.get_schema_examples("oss_upload")
    for i, example in enumerate(examples, 1):
        print(f"  示例 {i}: {example['description']}")
        print(f"    数据: {json.dumps(example['data'], ensure_ascii=False, indent=2)}")
        print()
    
    # 4. 获取常见错误
    print("⚠️ 常见错误示例:")
    errors = validation_engine.get_common_errors("oss_upload")
    for error in errors:
        print(f"  错误: {error['error']}")
        print(f"    示例: {json.dumps(error['example'], ensure_ascii=False)}")
        print(f"    修复: {error['fix']}")
        print(f"    修正后: {json.dumps(error['corrected'], ensure_ascii=False)}")
        print()

def demo_oss_guidance():
    """演示OSS指导功能"""
    print("=" * 60)
    print("🎓 OSS指导功能演示")
    print("=" * 60)
    
    # 初始化指导增强器
    workflow_engine = WorkflowEngine()
    guidance_enhancer = AIGuidanceEnhancer(workflow_engine, None, None)
    
    # 1. 获取OSS提示词模板
    print("\n📝 OSS提示词模板:")
    template = guidance_enhancer.get_prompt_template("oss_upload")
    if template:
        print(f"  模板名称: {template.template_name}")
        print(f"  分类: {template.category}")
        print(f"  描述: {template.description}")
        print("  系统提示词片段:")
        print(f"    {template.system_prompt[:200]}...")
        print()
    
    # 2. 获取OSS工具示例
    print("🔧 OSS工具调用示例:")
    examples = guidance_enhancer.get_tool_examples("upload_current_document_to_oss")
    if examples:
        example = examples[0]
        print(f"  工具名称: {example.tool_name}")
        print(f"  描述: {example.description}")
        print(f"  参数: {json.dumps(example.parameters, ensure_ascii=False, indent=2)}")
        print(f"  预期结果: {example.expected_result}")
        print()
    
    # 3. 生成OSS综合指导
    print("📚 OSS综合指导:")
    guidance = guidance_enhancer.generate_comprehensive_guidance("上传文档到OSS")
    print(f"  建议方法: {guidance['suggested_approach']}")
    print(f"  最佳实践数量: {len(guidance['best_practices'])}")
    print(f"  常见错误数量: {len(guidance['common_mistakes'])}")
    
    # 显示最佳实践
    print("\n  最佳实践:")
    for practice in guidance['best_practices'][:3]:
        print(f"    • {practice}")
    
    # 显示常见错误
    print("\n  常见错误:")
    for mistake in guidance['common_mistakes'][:3]:
        print(f"    • {mistake}")
    print()

def demo_oss_smart_suggestions():
    """演示OSS智能建议"""
    print("=" * 60)
    print("🧠 OSS智能建议演示")
    print("=" * 60)
    
    # 初始化组件
    temp_dir = tempfile.mkdtemp()
    state_manager = EnhancedStateManager(temp_dir)
    workflow_engine = WorkflowEngine()
    suggestion_engine = SmartSuggestionEngine(state_manager, workflow_engine, None)
    
    # 1. 基于意图的OSS建议
    print("\n🎯 基于意图的OSS建议:")
    intents = [
        "提供下载链接",
        "上传文档到云端",
        "分享文档给其他人"
    ]
    
    for intent in intents:
        suggestions = suggestion_engine.generate_suggestions(intent, limit=3)
        print(f"  意图: {intent}")
        
        oss_suggestions = [s for s in suggestions if "oss" in s.title.lower() or "上传" in s.title]
        if oss_suggestions:
            for suggestion in oss_suggestions:
                print(f"    • {suggestion.title}")
                print(f"      类型: {suggestion.suggestion_type.value}")
                print(f"      置信度: {suggestion.confidence:.2f}")
                print(f"      推荐理由: {', '.join(suggestion.reasoning)}")
        else:
            print("    无OSS相关建议")
        print()
    
    # 2. 基于上下文的OSS建议
    print("🔍 基于上下文的OSS建议:")
    
    # 模拟有内容的文档状态
    state_manager.set_current_document("test.docx", "test_doc")
    
    context_suggestions = suggestion_engine.generate_suggestions()
    oss_context_suggestions = [s for s in context_suggestions if "oss" in s.title.lower() or "上传" in s.title]
    
    if oss_context_suggestions:
        for suggestion in oss_context_suggestions:
            print(f"  • {suggestion.title}")
            print(f"    类型: {suggestion.suggestion_type.value}")
            print(f"    优先级: {suggestion.priority.value}")
            print(f"    置信度: {suggestion.confidence:.2f}")
            print(f"    推荐理由: {', '.join(suggestion.reasoning)}")
            print()
    else:
        print("  无OSS相关建议")
    
    # 清理临时目录
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

def demo_oss_workflow_integration():
    """演示OSS工作流集成"""
    print("=" * 60)
    print("🔗 OSS工作流集成演示")
    print("=" * 60)
    
    # 初始化所有组件
    temp_dir = tempfile.mkdtemp()
    state_manager = EnhancedStateManager(temp_dir)
    workflow_engine = WorkflowEngine()
    validation_engine = JSONValidationEngine()
    guidance_enhancer = AIGuidanceEnhancer(workflow_engine, None, None)
    suggestion_engine = SmartSuggestionEngine(state_manager, workflow_engine, None)
    
    # 模拟工具
    def mock_upload_tool(**kwargs):
        return {
            "success": True,
            "filename": "集成测试文档.docx",
            "download_url": "https://ggb-lzt.oss-cn-shenzhen.aliyuncs.com/集成测试文档.docx",
            "file_size": 3072,
            "message": "文档已成功上传到OSS"
        }
    
    workflow_engine.register_tool_executor("upload_current_document_to_oss", mock_upload_tool)
    workflow_engine.register_tool_executor("validate_document_exists", lambda **kwargs: "文档验证通过")
    workflow_engine.register_tool_executor("get_download_link", lambda **kwargs: "下载链接已生成")
    
    print("\n🎯 端到端OSS工作流演示:")
    
    # 1. 用户意图
    user_intent = "创建文档并上传到OSS提供下载链接"
    print(f"  用户意图: {user_intent}")
    
    # 2. 数据验证
    print("\n📋 步骤1: 数据验证")
    input_data = {
        "custom_filename": "集成测试文档.docx",
        "auto_upload": True
    }
    validation_result = validation_engine.validate_json("oss_upload", input_data)
    print(f"  验证结果: {'通过' if validation_result.is_valid else '失败'}")
    
    # 3. 记录操作
    print("\n📝 步骤2: 记录操作")
    op_id = state_manager.record_operation(OperationType.CREATE_DOCUMENT, input_data)
    print(f"  操作ID: {op_id}")
    
    # 4. 获取智能建议
    print("\n💡 步骤3: 获取智能建议")
    suggestions = suggestion_engine.generate_suggestions(user_intent, limit=3)
    oss_suggestions = [s for s in suggestions if "oss" in s.title.lower() or "上传" in s.title]
    print(f"  获得 {len(oss_suggestions)} 个OSS相关建议:")
    for suggestion in oss_suggestions:
        print(f"    • {suggestion.title} (置信度: {suggestion.confidence:.2f})")
    
    # 5. 获取综合指导
    print("\n🎓 步骤4: 获取综合指导")
    guidance = guidance_enhancer.generate_comprehensive_guidance(user_intent)
    print(f"  建议方法: {guidance['suggested_approach']}")
    print(f"  最佳实践: {len(guidance['best_practices'])} 条")
    
    # 6. 执行OSS上传工作流
    print("\n🔄 步骤5: 执行OSS上传工作流")
    result = workflow_engine.execute_workflow("auto_oss_upload", input_data)
    print(f"  执行结果: {result}")
    
    # 7. 更新操作状态
    print("\n✅ 步骤6: 更新操作状态")
    state_manager.update_operation_status(
        op_id, OperationStatus.COMPLETED, "文档已上传到OSS"
    )
    print("  操作状态已更新为完成")
    
    # 8. 创建状态快照
    print("\n📸 步骤7: 创建状态快照")
    snapshot_id = state_manager.create_state_snapshot("OSS上传完成")
    print(f"  快照ID: {snapshot_id}")
    
    # 9. 获取会话总结
    print("\n📊 步骤8: 会话总结")
    session_info = state_manager.get_current_session_info()
    print(f"  会话ID: {session_info['session_id']}")
    print(f"  已完成操作: {session_info['completed_operations_count']}")
    print(f"  总操作数: {session_info['total_operations']}")
    
    # 清理临时目录
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\n🎉 OSS工作流集成演示完成！")

def main():
    """主函数"""
    print("🚀 OSS工作流演示程序")
    print("本程序将演示以下OSS相关功能:")
    print("1. OSS工作流基础功能")
    print("2. OSS工作流执行")
    print("3. OSS数据验证")
    print("4. OSS指导功能")
    print("5. OSS智能建议")
    print("6. OSS工作流集成")
    print()
    
    try:
        # 运行各个演示
        demo_oss_workflow_basics()
        demo_oss_workflow_execution()
        demo_oss_validation()
        demo_oss_guidance()
        demo_oss_smart_suggestions()
        demo_oss_workflow_integration()
        
        print("=" * 60)
        print("🎉 所有OSS工作流演示完成！")
        print("=" * 60)
        print()
        print("📚 总结:")
        print("• OSS工作流引擎提供了自动上传功能")
        print("• 所有文档操作默认会自动上传到OSS")
        print("• 智能建议系统会推荐OSS相关操作")
        print("• 数据验证确保OSS上传参数正确")
        print("• AI指导提供了完整的OSS操作指导")
        print("• 状态管理记录了完整的OSS操作历史")
        print()
        print("💡 关键改进:")
        print("• **默认自动上传**: 所有文档操作完成后自动上传到OSS")
        print("• **智能建议**: 基于用户意图推荐OSS操作")
        print("• **错误预防**: 避免忘记上传就提供下载链接的问题")
        print("• **完整流程**: 从创建到上传到提供链接的完整工作流")
        print("• **状态跟踪**: 完整的操作历史和状态管理")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
