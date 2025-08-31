#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP增强功能演示
展示工作流引擎、状态管理、智能提示等新功能的使用方法
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from core.workflow_engine import WorkflowEngine
from core.enhanced_state_manager import EnhancedStateManager, OperationType, OperationStatus
from core.smart_suggestion_engine import SmartSuggestionEngine
from core.ai_guidance_enhancer import AIGuidanceEnhancer
from core.json_validation_engine import JSONValidationEngine

def demo_workflow_engine():
    """演示工作流引擎功能"""
    print("=" * 60)
    print("🚀 工作流引擎演示")
    print("=" * 60)
    
    # 初始化工作流引擎
    workflow_engine = WorkflowEngine()
    
    # 1. 查看可用工作流
    print("\n📋 可用工作流列表:")
    workflows = workflow_engine.get_available_workflows()
    for workflow in workflows[:3]:  # 只显示前3个
        print(f"  • {workflow.workflow_name} ({workflow.workflow_id})")
        print(f"    描述: {workflow.description}")
        print(f"    分类: {workflow.category}")
        print(f"    预计时间: {workflow.estimated_duration}")
        print()
    
    # 2. 基于意图推荐工作流
    print("🎯 基于意图推荐工作流:")
    intent = "创建商务报告文档"
    suggestions = workflow_engine.suggest_workflows_by_intent(intent)
    
    for suggestion in suggestions[:2]:  # 只显示前2个
        print(f"  • {suggestion['workflow_name']}")
        print(f"    匹配分数: {suggestion['match_score']:.2f}")
        print(f"    推荐理由: {suggestion['reasons']}")
        print(f"    预计时间: {suggestion['estimated_duration']}")
        print()
    
    # 3. 获取工作流详情
    print("📖 工作流详情示例:")
    workflow = workflow_engine.get_workflow("create_document")
    if workflow:
        print(f"  工作流名称: {workflow.workflow_name}")
        print(f"  步骤数量: {len(workflow.steps)}")
        print("  执行步骤:")
        for i, step in enumerate(workflow.steps[:3], 1):  # 只显示前3个步骤
            print(f"    {i}. {step.step_name} ({step.tool_name})")
            if step.dependencies:
                print(f"       依赖: {', '.join(step.dependencies)}")
        print()

def demo_state_manager():
    """演示状态管理器功能"""
    print("=" * 60)
    print("💾 增强版状态管理器演示")
    print("=" * 60)
    
    # 初始化状态管理器
    temp_dir = tempfile.mkdtemp()
    state_manager = EnhancedStateManager(temp_dir)
    
    # 1. 记录操作
    print("\n📝 记录操作示例:")
    op_id = state_manager.record_operation(
        OperationType.CREATE_DOCUMENT,
        {"filename": "演示文档.docx", "title": "MCP增强功能演示"}
    )
    print(f"  操作ID: {op_id}")
    
    # 2. 更新操作状态
    print("\n✅ 更新操作状态:")
    state_manager.update_operation_status(
        op_id, OperationStatus.COMPLETED, "文档创建成功", None, 2.5
    )
    print("  操作状态已更新为完成")
    
    # 3. 设置文档状态
    print("\n📄 设置文档状态:")
    state_manager.set_current_document("演示文档.docx", "demo_doc_001")
    print("  当前文档已设置")
    
    # 4. 获取会话信息
    print("\n📊 会话信息:")
    session_info = state_manager.get_current_session_info()
    print(f"  会话ID: {session_info['session_id']}")
    print(f"  开始时间: {session_info['start_time']}")
    print(f"  当前文档: {session_info['current_document']}")
    print(f"  已完成操作: {session_info['completed_operations_count']}")
    print(f"  总操作数: {session_info['total_operations']}")
    
    # 5. 创建状态快照
    print("\n📸 创建状态快照:")
    snapshot_id = state_manager.create_state_snapshot("演示快照")
    print(f"  快照ID: {snapshot_id}")
    
    # 6. 获取操作历史
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

def demo_smart_suggestions():
    """演示智能提示功能"""
    print("=" * 60)
    print("🧠 智能提示引擎演示")
    print("=" * 60)
    
    # 初始化组件
    temp_dir = tempfile.mkdtemp()
    state_manager = EnhancedStateManager(temp_dir)
    workflow_engine = WorkflowEngine()
    
    suggestion_engine = SmartSuggestionEngine(
        state_manager, workflow_engine, None
    )
    
    # 1. 分析上下文
    print("\n🔍 上下文分析:")
    context = suggestion_engine.analyze_context()
    print(f"  当前状态: {context.current_state}")
    print(f"  最近操作: {context.recent_operations}")
    print(f"  用户模式: {list(context.user_patterns.keys())}")
    print(f"  错误模式: {context.error_patterns}")
    print(f"  优化机会: {context.optimization_opportunities}")
    
    # 2. 生成建议
    print("\n💡 智能建议:")
    suggestions = suggestion_engine.generate_suggestions("创建文档", limit=3)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion.title}")
        print(f"     类型: {suggestion.suggestion_type.value}")
        print(f"     优先级: {suggestion.priority.value}")
        print(f"     置信度: {suggestion.confidence:.2f}")
        print(f"     描述: {suggestion.description}")
        print(f"     推荐理由: {', '.join(suggestion.reasoning)}")
        if suggestion.estimated_time:
            print(f"     预计时间: {suggestion.estimated_time}")
        print()
    
    # 3. 基于意图的建议
    print("🎯 基于特定意图的建议:")
    intent_suggestions = suggestion_engine.generate_suggestions("添加图片到文档")
    
    for suggestion in intent_suggestions[:2]:
        print(f"  • {suggestion.title}")
        print(f"    操作类型: {suggestion.action_type}")
        print(f"    参数: {suggestion.parameters}")
        print()
    
    # 清理临时目录
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

def demo_ai_guidance():
    """演示AI指导功能"""
    print("=" * 60)
    print("🎓 AI指导增强器演示")
    print("=" * 60)
    
    # 初始化组件
    workflow_engine = WorkflowEngine()
    guidance_enhancer = AIGuidanceEnhancer(workflow_engine, None, None)
    
    # 1. 获取提示词模板
    print("\n📝 提示词模板示例:")
    template = guidance_enhancer.get_prompt_template("create_document")
    if template:
        print(f"  模板名称: {template.template_name}")
        print(f"  分类: {template.category}")
        print(f"  描述: {template.description}")
        print("  系统提示词片段:")
        print(f"    {template.system_prompt[:100]}...")
        print()
    
    # 2. 获取工具示例
    print("🔧 工具调用示例:")
    examples = guidance_enhancer.get_tool_examples("create_document")
    if examples:
        example = examples[0]
        print(f"  工具名称: {example.tool_name}")
        print(f"  描述: {example.description}")
        print(f"  参数: {json.dumps(example.parameters, ensure_ascii=False, indent=2)}")
        print(f"  预期结果: {example.expected_result}")
        print()
    
    # 3. 获取工作流示例
    print("🔄 工作流示例:")
    workflow_example = guidance_enhancer.get_workflow_example("create_document")
    if workflow_example:
        print(f"  场景: {workflow_example.scenario}")
        print(f"  输入数据: {json.dumps(workflow_example.input_data, ensure_ascii=False, indent=2)}")
        print("  执行步骤:")
        for step in workflow_example.step_by_step[:3]:  # 只显示前3个步骤
            print(f"    {step['step']}. {step['action']} ({step['tool']})")
        print(f"  预期输出: {workflow_example.expected_output}")
        print()
    
    # 4. 生成综合指导
    print("📚 综合指导示例:")
    guidance = guidance_enhancer.generate_comprehensive_guidance("创建商务报告")
    print(f"  建议方法: {guidance['suggested_approach']}")
    print(f"  最佳实践数量: {len(guidance['best_practices'])}")
    print(f"  常见错误数量: {len(guidance['common_mistakes'])}")
    print(f"  故障排除数量: {len(guidance['troubleshooting'])}")
    print()
    
    # 5. 创建自定义提示词
    print("✍️ 自定义提示词示例:")
    custom_prompt = guidance_enhancer.create_custom_prompt(
        "创建产品手册",
        {
            "文档类型": "产品手册",
            "包含内容": "产品介绍、功能说明、使用指南",
            "格式要求": "专业排版，包含图片和表格"
        }
    )
    print(f"  自定义提示词长度: {len(custom_prompt)} 字符")
    print(f"  包含场景: {'产品手册' in custom_prompt}")
    print()
    
    # 6. 工具调用验证
    print("✅ 工具调用验证:")
    valid_result = guidance_enhancer.validate_tool_call(
        "create_document", {"filename": "test.docx"}
    )
    print(f"  有效调用验证: {'通过' if valid_result['is_valid'] else '失败'}")
    
    invalid_result = guidance_enhancer.validate_tool_call(
        "create_document", {"title": "测试"}
    )
    print(f"  无效调用验证: {'通过' if invalid_result['is_valid'] else '失败'}")
    if not invalid_result['is_valid']:
        print(f"  错误信息: {invalid_result['errors']}")

def demo_json_validation():
    """演示JSON验证功能"""
    print("=" * 60)
    print("🔍 JSON验证引擎演示")
    print("=" * 60)
    
    # 初始化验证引擎
    validation_engine = JSONValidationEngine()
    
    # 1. 查看可用模式
    print("\n📋 可用验证模式:")
    schemas = list(validation_engine.schemas.keys())
    for schema_id in schemas:
        schema = validation_engine.schemas[schema_id]
        print(f"  • {schema.schema_name} ({schema_id})")
        print(f"    描述: {schema.description}")
    print()
    
    # 2. 有效数据验证
    print("✅ 有效数据验证示例:")
    valid_data = {
        "filename": "演示文档.docx",
        "title": "MCP增强功能演示",
        "page_settings": {
            "margins": {"top": 2.54, "bottom": 2.54, "left": 3.18, "right": 3.18},
            "orientation": "portrait",
            "size": "A4"
        }
    }
    
    result = validation_engine.validate_json("create_document", valid_data)
    print(f"  验证结果: {'通过' if result.is_valid else '失败'}")
    if result.warnings:
        print(f"  警告: {result.warnings}")
    print()
    
    # 3. 无效数据验证
    print("❌ 无效数据验证示例:")
    invalid_data = {
        "title": "测试文档",  # 缺少必需的filename字段
        "page_settings": {
            "margins": {"top": 10}  # 边距值超出范围
        }
    }
    
    result = validation_engine.validate_json("create_document", invalid_data)
    print(f"  验证结果: {'通过' if result.is_valid else '失败'}")
    if result.errors:
        print("  错误信息:")
        for error in result.errors:
            print(f"    • {error}")
    if result.suggestions:
        print("  建议:")
        for suggestion in result.suggestions:
            print(f"    • {suggestion}")
    print()
    
    # 4. 获取模式示例
    print("📖 模式示例:")
    examples = validation_engine.get_schema_examples("create_document")
    for i, example in enumerate(examples[:2], 1):
        print(f"  示例 {i}: {example['description']}")
        print(f"    数据: {json.dumps(example['data'], ensure_ascii=False, indent=2)}")
        print()
    
    # 5. 获取常见错误
    print("⚠️ 常见错误示例:")
    errors = validation_engine.get_common_errors("create_document")
    for error in errors[:2]:
        print(f"  错误: {error['error']}")
        print(f"    示例: {json.dumps(error['example'], ensure_ascii=False)}")
        print(f"    修复: {error['fix']}")
        print(f"    修正后: {json.dumps(error['corrected'], ensure_ascii=False)}")
        print()
    
    # 6. 生成示例JSON
    print("🎯 生成示例JSON:")
    example_json = validation_engine.generate_example_json("create_document", 0)
    print(f"  示例数据: {json.dumps(example_json, ensure_ascii=False, indent=2)}")

def demo_integration():
    """演示集成功能"""
    print("=" * 60)
    print("🔗 集成功能演示")
    print("=" * 60)
    
    # 初始化所有组件
    temp_dir = tempfile.mkdtemp()
    state_manager = EnhancedStateManager(temp_dir)
    workflow_engine = WorkflowEngine()
    validation_engine = JSONValidationEngine()
    guidance_enhancer = AIGuidanceEnhancer(workflow_engine, None, None)
    suggestion_engine = SmartSuggestionEngine(state_manager, workflow_engine, None)
    
    print("\n🎯 端到端工作流演示:")
    
    # 1. 用户意图
    user_intent = "创建一个包含图片和表格的产品手册"
    print(f"  用户意图: {user_intent}")
    
    # 2. 数据验证
    print("\n📋 步骤1: 数据验证")
    input_data = {
        "filename": "产品手册.docx",
        "title": "智能产品使用手册"
    }
    validation_result = validation_engine.validate_json("create_document", input_data)
    print(f"  验证结果: {'通过' if validation_result.is_valid else '失败'}")
    
    # 3. 记录操作
    print("\n📝 步骤2: 记录操作")
    op_id = state_manager.record_operation(OperationType.CREATE_DOCUMENT, input_data)
    print(f"  操作ID: {op_id}")
    
    # 4. 获取智能建议
    print("\n💡 步骤3: 获取智能建议")
    suggestions = suggestion_engine.generate_suggestions(user_intent, limit=3)
    print(f"  获得 {len(suggestions)} 个建议:")
    for suggestion in suggestions:
        print(f"    • {suggestion.title} (置信度: {suggestion.confidence:.2f})")
    
    # 5. 获取综合指导
    print("\n🎓 步骤4: 获取综合指导")
    guidance = guidance_enhancer.generate_comprehensive_guidance(user_intent)
    print(f"  建议方法: {guidance['suggested_approach']}")
    print(f"  最佳实践: {len(guidance['best_practices'])} 条")
    
    # 6. 推荐工作流
    print("\n🔄 步骤5: 推荐工作流")
    workflow_suggestions = workflow_engine.suggest_workflows_by_intent(user_intent)
    if workflow_suggestions:
        best_workflow = workflow_suggestions[0]
        print(f"  推荐工作流: {best_workflow['workflow_name']}")
        print(f"  匹配分数: {best_workflow['match_score']:.2f}")
    
    # 7. 更新操作状态
    print("\n✅ 步骤6: 更新操作状态")
    state_manager.update_operation_status(
        op_id, OperationStatus.COMPLETED, "产品手册创建成功"
    )
    print("  操作状态已更新为完成")
    
    # 8. 创建状态快照
    print("\n📸 步骤7: 创建状态快照")
    snapshot_id = state_manager.create_state_snapshot("产品手册创建完成")
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
    
    print("\n🎉 集成演示完成！")

def main():
    """主函数"""
    print("🚀 MCP增强功能演示程序")
    print("本程序将演示以下功能:")
    print("1. 工作流引擎 - 定义和执行工具调用序列")
    print("2. 增强版状态管理器 - 操作历史和状态持久化")
    print("3. 智能提示引擎 - 基于上下文的智能建议")
    print("4. AI指导增强器 - 完整的提示词和调用示例")
    print("5. JSON验证引擎 - 数据格式验证和示例模板")
    print("6. 集成功能 - 端到端工作流演示")
    print()
    
    try:
        # 运行各个演示
        demo_workflow_engine()
        demo_state_manager()
        demo_smart_suggestions()
        demo_ai_guidance()
        demo_json_validation()
        demo_integration()
        
        print("=" * 60)
        print("🎉 所有演示完成！")
        print("=" * 60)
        print()
        print("📚 总结:")
        print("• 工作流引擎提供了预定义的工具调用序列")
        print("• 状态管理器实现了完整的操作历史记录")
        print("• 智能提示引擎能够根据上下文推荐操作")
        print("• AI指导增强器提供了详细的提示词和示例")
        print("• JSON验证引擎确保了数据格式的正确性")
        print("• 所有组件可以无缝集成，提供完整的MCP增强体验")
        print()
        print("💡 这些功能大大减少了AI工具调用时的问题:")
        print("• 避免了工具调用顺序错误")
        print("• 提供了参数验证和错误处理")
        print("• 实现了状态持久化和错误恢复")
        print("• 给出了智能的操作建议")
        print("• 提供了完整的调用示例和最佳实践")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
