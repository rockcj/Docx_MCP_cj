#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP增强功能测试
测试工作流引擎、状态管理、智能提示等新功能
"""

import unittest
import tempfile
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入新增的模块
from core.workflow_engine import WorkflowEngine, WorkflowStatus, StepStatus
from core.enhanced_state_manager import EnhancedStateManager, OperationType, OperationStatus
from core.smart_suggestion_engine import SmartSuggestionEngine, SuggestionType, SuggestionPriority
from core.ai_guidance_enhancer import AIGuidanceEnhancer
from core.json_validation_engine import JSONValidationEngine, ValidationResult

class TestWorkflowEngine(unittest.TestCase):
    """测试工作流引擎"""
    
    def setUp(self):
        """设置测试环境"""
        self.workflow_engine = WorkflowEngine()
        self.test_tool_called = False
        self.test_tool_result = None
        
        # 注册测试工具
        def test_tool(**kwargs):
            self.test_tool_called = True
            self.test_tool_result = kwargs
            return "测试工具执行成功"
        
        self.workflow_engine.register_tool_executor("test_tool", test_tool)
    
    def test_workflow_registration(self):
        """测试工作流注册"""
        # 检查预定义工作流是否已注册
        self.assertIn("create_document", self.workflow_engine.workflow_registry)
        self.assertIn("add_image_to_document", self.workflow_engine.workflow_registry)
        self.assertIn("create_table", self.workflow_engine.workflow_registry)
        self.assertIn("apply_template", self.workflow_engine.workflow_registry)
    
    def test_get_available_workflows(self):
        """测试获取可用工作流"""
        workflows = self.workflow_engine.get_available_workflows()
        self.assertGreater(len(workflows), 0)
        
        # 测试按分类获取
        doc_workflows = self.workflow_engine.get_available_workflows("document")
        self.assertGreater(len(doc_workflows), 0)
    
    def test_suggest_workflows_by_intent(self):
        """测试基于意图推荐工作流"""
        suggestions = self.workflow_engine.suggest_workflows_by_intent("创建文档")
        self.assertGreater(len(suggestions), 0)
        
        # 检查建议结构
        suggestion = suggestions[0]
        self.assertIn("workflow_id", suggestion)
        self.assertIn("workflow_name", suggestion)
        self.assertIn("match_score", suggestion)
    
    def test_workflow_execution(self):
        """测试工作流执行"""
        # 创建简单的工作流
        from core.workflow_engine import WorkflowDefinition, WorkflowStep
        
        simple_workflow = WorkflowDefinition(
            workflow_id="test_workflow",
            workflow_name="测试工作流",
            description="用于测试的工作流",
            version="1.0",
            category="test",
            steps=[
                WorkflowStep(
                    step_id="test_step",
                    step_name="测试步骤",
                    tool_name="test_tool",
                    parameters={"test_param": "test_value"}
                )
            ]
        )
        
        self.workflow_engine.workflow_registry["test_workflow"] = simple_workflow
        
        # 执行工作流
        result = self.workflow_engine.execute_workflow("test_workflow", {})
        
        # 验证结果
        self.assertIn("工作流执行成功", result)
        self.assertTrue(self.test_tool_called)
        self.assertEqual(self.test_tool_result["test_param"], "test_value")

class TestEnhancedStateManager(unittest.TestCase):
    """测试增强版状态管理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.state_manager = EnhancedStateManager(self.temp_dir)
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_operation_recording(self):
        """测试操作记录"""
        # 记录操作
        op_id = self.state_manager.record_operation(
            OperationType.CREATE_DOCUMENT,
            {"filename": "test.docx"}
        )
        
        self.assertIsNotNone(op_id)
        self.assertIn(op_id, self.state_manager.operation_records)
        
        # 更新操作状态
        self.state_manager.update_operation_status(
            op_id, OperationStatus.COMPLETED, "操作成功", None, 1.5
        )
        
        operation = self.state_manager.operation_records[op_id]
        self.assertEqual(operation.status, OperationStatus.COMPLETED)
        self.assertEqual(operation.result, "操作成功")
        self.assertEqual(operation.execution_time, 1.5)
    
    def test_document_state_management(self):
        """测试文档状态管理"""
        # 设置当前文档
        self.state_manager.set_current_document("test.docx", "doc_123")
        
        # 获取文档状态
        doc_state = self.state_manager.get_document_state("doc_123")
        self.assertIsNotNone(doc_state)
        self.assertEqual(doc_state.file_path, "test.docx")
        self.assertEqual(doc_state.document_id, "doc_123")
    
    def test_operation_history(self):
        """测试操作历史"""
        # 记录多个操作
        op1 = self.state_manager.record_operation(OperationType.CREATE_DOCUMENT, {"filename": "doc1.docx"})
        op2 = self.state_manager.record_operation(OperationType.ADD_PARAGRAPH, {"text": "段落内容"})
        
        # 获取操作历史
        history = self.state_manager.get_operation_history()
        self.assertGreaterEqual(len(history), 2)
        
        # 按类型过滤
        create_ops = self.state_manager.get_operation_history(operation_type=OperationType.CREATE_DOCUMENT)
        self.assertGreaterEqual(len(create_ops), 1)
    
    def test_state_snapshots(self):
        """测试状态快照"""
        # 记录一些操作
        self.state_manager.record_operation(OperationType.CREATE_DOCUMENT, {"filename": "test.docx"})
        
        # 创建快照
        snapshot_id = self.state_manager.create_state_snapshot("测试快照")
        self.assertIsNotNone(snapshot_id)
        self.assertIn(snapshot_id, self.state_manager.state_snapshots)
        
        # 获取快照列表
        snapshots = self.state_manager.get_available_snapshots()
        self.assertGreater(len(snapshots), 0)
    
    def test_session_info(self):
        """测试会话信息"""
        session_info = self.state_manager.get_current_session_info()
        self.assertIn("session_id", session_info)
        self.assertIn("start_time", session_info)
        self.assertIn("total_operations", session_info)

class TestSmartSuggestionEngine(unittest.TestCase):
    """测试智能提示引擎"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.state_manager = EnhancedStateManager(self.temp_dir)
        self.workflow_engine = WorkflowEngine()
        self.template_engine = None  # 可以创建模拟对象
        
        self.suggestion_engine = SmartSuggestionEngine(
            self.state_manager, self.workflow_engine, self.template_engine
        )
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_context_analysis(self):
        """测试上下文分析"""
        context = self.suggestion_engine.analyze_context()
        
        self.assertIn("current_state", context)
        self.assertIn("recent_operations", context)
        self.assertIn("document_info", context)
        self.assertIn("user_patterns", context)
        self.assertIn("error_patterns", context)
        self.assertIn("optimization_opportunities", context)
    
    def test_suggestion_generation(self):
        """测试建议生成"""
        # 测试基于上下文的建议
        suggestions = self.suggestion_engine.generate_suggestions()
        self.assertIsInstance(suggestions, list)
        
        # 测试基于意图的建议
        intent_suggestions = self.suggestion_engine.generate_suggestions("创建文档")
        self.assertIsInstance(intent_suggestions, list)
    
    def test_suggestion_structure(self):
        """测试建议结构"""
        suggestions = self.suggestion_engine.generate_suggestions("创建新文档")
        
        if suggestions:
            suggestion = suggestions[0]
            self.assertIn("suggestion_id", suggestion.__dict__)
            self.assertIn("suggestion_type", suggestion.__dict__)
            self.assertIn("title", suggestion.__dict__)
            self.assertIn("description", suggestion.__dict__)
            self.assertIn("priority", suggestion.__dict__)
            self.assertIn("confidence", suggestion.__dict__)

class TestAIGuidanceEnhancer(unittest.TestCase):
    """测试AI指导增强器"""
    
    def setUp(self):
        """设置测试环境"""
        self.workflow_engine = WorkflowEngine()
        self.template_engine = None  # 可以创建模拟对象
        self.suggestion_engine = None  # 可以创建模拟对象
        
        self.guidance_enhancer = AIGuidanceEnhancer(
            self.workflow_engine, self.template_engine, self.suggestion_engine
        )
    
    def test_prompt_templates(self):
        """测试提示词模板"""
        # 测试获取提示词模板
        create_doc_template = self.guidance_enhancer.get_prompt_template("create_document")
        self.assertIsNotNone(create_doc_template)
        self.assertEqual(create_doc_template.template_id, "create_document")
        
        # 测试模板结构
        self.assertIn("system_prompt", create_doc_template.__dict__)
        self.assertIn("user_prompt_template", create_doc_template.__dict__)
        self.assertIn("examples", create_doc_template.__dict__)
        self.assertIn("best_practices", create_doc_template.__dict__)
    
    def test_tool_examples(self):
        """测试工具示例"""
        # 测试获取工具示例
        create_doc_examples = self.guidance_enhancer.get_tool_examples("create_document")
        self.assertIsInstance(create_doc_examples, list)
        
        if create_doc_examples:
            example = create_doc_examples[0]
            self.assertIn("example_id", example.__dict__)
            self.assertIn("tool_name", example.__dict__)
            self.assertIn("parameters", example.__dict__)
            self.assertIn("expected_result", example.__dict__)
    
    def test_workflow_examples(self):
        """测试工作流示例"""
        # 测试获取工作流示例
        workflow_example = self.guidance_enhancer.get_workflow_example("create_document")
        self.assertIsNotNone(workflow_example)
        self.assertEqual(workflow_example.workflow_id, "create_document")
        
        # 测试示例结构
        self.assertIn("scenario", workflow_example.__dict__)
        self.assertIn("input_data", workflow_example.__dict__)
        self.assertIn("step_by_step", workflow_example.__dict__)
        self.assertIn("expected_output", workflow_example.__dict__)
    
    def test_comprehensive_guidance(self):
        """测试综合指导"""
        guidance = self.guidance_enhancer.generate_comprehensive_guidance("创建文档")
        
        self.assertIn("user_intent", guidance)
        self.assertIn("suggested_approach", guidance)
        self.assertIn("prompt_templates", guidance)
        self.assertIn("tool_examples", guidance)
        self.assertIn("workflow_examples", guidance)
        self.assertIn("best_practices", guidance)
        self.assertIn("common_mistakes", guidance)
    
    def test_custom_prompt_creation(self):
        """测试自定义提示词创建"""
        scenario = "创建商务报告"
        requirements = {
            "文档类型": "商务报告",
            "包含内容": "标题、摘要、数据表格",
            "格式要求": "公司标准格式"
        }
        
        prompt = self.guidance_enhancer.create_custom_prompt(scenario, requirements)
        self.assertIsInstance(prompt, str)
        self.assertIn(scenario, prompt)
        self.assertIn("商务报告", prompt)
    
    def test_tool_call_validation(self):
        """测试工具调用验证"""
        # 测试有效调用
        valid_result = self.guidance_enhancer.validate_tool_call(
            "create_document", {"filename": "test.docx"}
        )
        self.assertTrue(valid_result["is_valid"])
        
        # 测试无效调用
        invalid_result = self.guidance_enhancer.validate_tool_call(
            "create_document", {"title": "测试"}
        )
        self.assertFalse(invalid_result["is_valid"])
        self.assertGreater(len(invalid_result["errors"]), 0)

class TestJSONValidationEngine(unittest.TestCase):
    """测试JSON验证引擎"""
    
    def setUp(self):
        """设置测试环境"""
        self.validation_engine = JSONValidationEngine()
    
    def test_schema_registration(self):
        """测试模式注册"""
        # 检查预定义模式是否已注册
        self.assertIn("create_document", self.validation_engine.schemas)
        self.assertIn("add_paragraph", self.validation_engine.schemas)
        self.assertIn("add_picture", self.validation_engine.schemas)
        self.assertIn("add_table", self.validation_engine.schemas)
        self.assertIn("workflow_execution", self.validation_engine.schemas)
    
    def test_valid_json_validation(self):
        """测试有效JSON验证"""
        valid_data = {
            "filename": "test.docx"
        }
        
        result = self.validation_engine.validate_json("create_document", valid_data)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_invalid_json_validation(self):
        """测试无效JSON验证"""
        invalid_data = {
            "title": "测试文档"  # 缺少必需的filename字段
        }
        
        result = self.validation_engine.validate_json("create_document", invalid_data)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_filename_validation(self):
        """测试文件名验证"""
        # 测试有效文件名
        valid_data = {"filename": "test.docx"}
        result = self.validation_engine.validate_json("create_document", valid_data)
        self.assertTrue(result.is_valid)
        
        # 测试无效文件名
        invalid_data = {"filename": "test.doc"}  # 错误的扩展名
        result = self.validation_engine.validate_json("create_document", invalid_data)
        self.assertFalse(result.is_valid)
    
    def test_image_path_validation(self):
        """测试图片路径验证"""
        # 测试有效图片路径
        valid_data = {
            "filename": "test.docx",
            "image_path": "images/photo.jpg"
        }
        result = self.validation_engine.validate_json("add_picture", valid_data)
        self.assertTrue(result.is_valid)
        
        # 测试无效图片路径
        invalid_data = {
            "filename": "test.docx",
            "image_path": "images/photo.pdf"  # 不支持的格式
        }
        result = self.validation_engine.validate_json("add_picture", invalid_data)
        self.assertFalse(result.is_valid)
    
    def test_numeric_range_validation(self):
        """测试数值范围验证"""
        # 测试有效数值
        valid_data = {
            "filename": "test.docx",
            "rows": 3,
            "cols": 3
        }
        result = self.validation_engine.validate_json("add_table", valid_data)
        self.assertTrue(result.is_valid)
        
        # 测试无效数值
        invalid_data = {
            "filename": "test.docx",
            "rows": 0,  # 无效的行数
            "cols": 3
        }
        result = self.validation_engine.validate_json("add_table", invalid_data)
        self.assertFalse(result.is_valid)
    
    def test_schema_examples(self):
        """测试模式示例"""
        examples = self.validation_engine.get_schema_examples("create_document")
        self.assertGreater(len(examples), 0)
        
        example = examples[0]
        self.assertIn("description", example)
        self.assertIn("data", example)
    
    def test_common_errors(self):
        """测试常见错误"""
        errors = self.validation_engine.get_common_errors("create_document")
        self.assertGreater(len(errors), 0)
        
        error = errors[0]
        self.assertIn("error", error)
        self.assertIn("example", error)
        self.assertIn("fix", error)
    
    def test_example_json_generation(self):
        """测试示例JSON生成"""
        example_json = self.validation_engine.generate_example_json("create_document", 0)
        self.assertIsNotNone(example_json)
        self.assertIn("filename", example_json)
    
    def test_validation_result_formatting(self):
        """测试验证结果格式化"""
        result = ValidationResult(
            is_valid=False,
            errors=["测试错误"],
            warnings=["测试警告"],
            suggestions=["测试建议"]
        )
        
        formatted = self.validation_engine.format_validation_result(result)
        self.assertIsInstance(formatted, str)
        self.assertIn("❌", formatted)
        self.assertIn("测试错误", formatted)
        self.assertIn("测试警告", formatted)
        self.assertIn("测试建议", formatted)

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        
        # 初始化所有组件
        self.state_manager = EnhancedStateManager(self.temp_dir)
        self.workflow_engine = WorkflowEngine()
        self.validation_engine = JSONValidationEngine()
        self.guidance_enhancer = AIGuidanceEnhancer(
            self.workflow_engine, None, None
        )
        self.suggestion_engine = SmartSuggestionEngine(
            self.state_manager, self.workflow_engine, None
        )
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流"""
        # 1. 验证输入数据
        input_data = {"filename": "integration_test.docx"}
        validation_result = self.validation_engine.validate_json("create_document", input_data)
        self.assertTrue(validation_result.is_valid)
        
        # 2. 记录操作
        op_id = self.state_manager.record_operation(
            OperationType.CREATE_DOCUMENT, input_data
        )
        self.assertIsNotNone(op_id)
        
        # 3. 获取建议
        suggestions = self.suggestion_engine.generate_suggestions("创建文档")
        self.assertIsInstance(suggestions, list)
        
        # 4. 获取指导
        guidance = self.guidance_enhancer.generate_comprehensive_guidance("创建文档")
        self.assertIn("suggested_approach", guidance)
        
        # 5. 更新操作状态
        self.state_manager.update_operation_status(
            op_id, OperationStatus.COMPLETED, "集成测试成功"
        )
        
        # 6. 验证状态
        operation = self.state_manager.operation_records[op_id]
        self.assertEqual(operation.status, OperationStatus.COMPLETED)
    
    def test_error_recovery_workflow(self):
        """测试错误恢复工作流"""
        # 1. 记录失败的操作
        op_id = self.state_manager.record_operation(
            OperationType.CREATE_DOCUMENT, {"filename": "invalid<file>.docx"}
        )
        self.state_manager.update_operation_status(
            op_id, OperationStatus.FAILED, "文件名包含非法字符"
        )
        
        # 2. 获取错误恢复建议
        suggestions = self.suggestion_engine.generate_suggestions()
        error_recovery_suggestions = [
            s for s in suggestions 
            if s.suggestion_type.value == "error_recovery"
        ]
        
        # 应该包含错误恢复建议
        self.assertGreater(len(error_recovery_suggestions), 0)
    
    def test_state_persistence(self):
        """测试状态持久化"""
        # 1. 记录一些操作
        op_id = self.state_manager.record_operation(
            OperationType.CREATE_DOCUMENT, {"filename": "persistence_test.docx"}
        )
        self.state_manager.set_current_document("persistence_test.docx", "doc_123")
        
        # 2. 创建快照
        snapshot_id = self.state_manager.create_state_snapshot("持久化测试")
        
        # 3. 创建新的状态管理器实例（模拟重启）
        new_state_manager = EnhancedStateManager(self.temp_dir)
        
        # 4. 验证状态是否恢复
        self.assertIn(op_id, new_state_manager.operation_records)
        self.assertIn("doc_123", new_state_manager.document_states)
        self.assertIn(snapshot_id, new_state_manager.state_snapshots)

def run_all_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestWorkflowEngine,
        TestEnhancedStateManager,
        TestSmartSuggestionEngine,
        TestAIGuidanceEnhancer,
        TestJSONValidationEngine,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("开始运行MCP增强功能测试...")
    success = run_all_tests()
    
    if success:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 部分测试失败，请检查错误信息。")
