#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI友好的智能接口
为AI提供智能化的文档操作接口，集成状态机和模板系统
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime

from .state_machine import IntelligentStateManager, GlobalDocumentState
from .template_engine import DocumentTemplateEngine, TemplateSuggestion, ValidationResult

logger = logging.getLogger(__name__)

# ==================== 数据结构定义 ====================

@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    suggestions: List[str] = None
    error_details: Optional[str] = None

@dataclass
class SmartOperationRequest:
    """智能操作请求"""
    user_intent: str
    context: Dict[str, Any]
    operation_type: str  # template, direct, batch
    parameters: Dict[str, Any]

# ==================== AI智能接口类 ====================

class AISmartInterface:
    """AI智能接口 - 为AI提供智能化的操作接口"""
    
    def __init__(self, state_manager: IntelligentStateManager, template_engine: DocumentTemplateEngine):
        self.state_manager = state_manager
        self.template_engine = template_engine
        self.operation_history: List[SmartOperationRequest] = []
        
        logger.info("AI智能接口初始化完成")
    
    def smart_execute(self, user_intent: str, context: Dict[str, Any] = None) -> ExecutionResult:
        """智能执行 - 基于用户意图和上下文自动选择最佳操作"""
        try:
            if context is None:
                context = {}
            
            # 分析用户意图
            intent_analysis = self._analyze_user_intent(user_intent)
            
            # 根据意图类型选择执行策略
            if intent_analysis["type"] == "template_based":
                return self._execute_template_based_operation(user_intent, context, intent_analysis)
            elif intent_analysis["type"] == "direct_operation":
                return self._execute_direct_operation(user_intent, context, intent_analysis)
            elif intent_analysis["type"] == "batch_operation":
                return self._execute_batch_operation(user_intent, context, intent_analysis)
            else:
                return ExecutionResult(
                    success=False,
                    message="无法理解用户意图",
                    suggestions=self._get_contextual_suggestions()
                )
                
        except Exception as e:
            logger.error(f"智能执行失败: {e}")
            return ExecutionResult(
                success=False,
                message=f"执行失败: {str(e)}",
                error_details=str(e)
            )
    
    def _analyze_user_intent(self, user_intent: str) -> Dict[str, Any]:
        """分析用户意图"""
        intent_lower = user_intent.lower()
        
        # 模板相关意图
        template_keywords = ["创建", "生成", "制作", "写", "模板", "格式"]
        if any(keyword in intent_lower for keyword in template_keywords):
            return {
                "type": "template_based",
                "confidence": 0.8,
                "suggested_templates": self._suggest_templates_by_intent(user_intent)
            }
        
        # 直接操作意图
        direct_keywords = ["添加", "删除", "修改", "编辑", "保存", "打开"]
        if any(keyword in intent_lower for keyword in direct_keywords):
            return {
                "type": "direct_operation",
                "confidence": 0.7,
                "suggested_operations": self._suggest_direct_operations(user_intent)
            }
        
        # 批量操作意图
        batch_keywords = ["批量", "全部", "所有", "格式化", "统一"]
        if any(keyword in intent_lower for keyword in batch_keywords):
            return {
                "type": "batch_operation",
                "confidence": 0.6,
                "suggested_batch_operations": self._suggest_batch_operations(user_intent)
            }
        
        return {
            "type": "unknown",
            "confidence": 0.0,
            "suggestions": self._get_contextual_suggestions()
        }
    
    def _execute_template_based_operation(self, user_intent: str, context: Dict[str, Any], intent_analysis: Dict[str, Any]) -> ExecutionResult:
        """执行基于模板的操作"""
        try:
            # 获取模板建议
            template_suggestions = intent_analysis.get("suggested_templates", [])
            
            if not template_suggestions:
                return ExecutionResult(
                    success=False,
                    message="未找到合适的模板",
                    suggestions=["请尝试更具体的描述，如'创建商务书信'或'生成学术论文'"]
                )
            
            # 选择最佳模板
            best_template = template_suggestions[0]
            
            # 获取模板填写指导
            guidance = self.template_engine.get_template_filling_guidance(best_template.template_id)
            
            return ExecutionResult(
                success=True,
                message=f"建议使用模板: {best_template.template_name}",
                data={
                    "template_id": best_template.template_id,
                    "template_name": best_template.template_name,
                    "match_reason": best_template.reason,
                    "filling_guidance": guidance,
                    "required_variables": guidance.get("required_variables", []),
                    "suggested_prompts": guidance.get("suggested_prompts", [])
                },
                suggestions=[
                    f"请提供模板所需的变量: {', '.join(guidance.get('required_variables', []))}",
                    "您可以使用 'fill_template' 命令来填写模板数据"
                ]
            )
            
        except Exception as e:
            logger.error(f"模板操作执行失败: {e}")
            return ExecutionResult(
                success=False,
                message=f"模板操作失败: {str(e)}",
                error_details=str(e)
            )
    
    def _execute_direct_operation(self, user_intent: str, context: Dict[str, Any], intent_analysis: Dict[str, Any]) -> ExecutionResult:
        """执行直接操作"""
        try:
            # 获取建议的操作
            suggested_operations = intent_analysis.get("suggested_operations", [])
            
            if not suggested_operations:
                return ExecutionResult(
                    success=False,
                    message="无法确定具体操作",
                    suggestions=self._get_contextual_suggestions()
                )
            
            # 检查当前状态是否允许操作
            current_state = self.state_manager.get_current_state_summary()
            available_operations = self.state_manager.get_available_operations()
            
            # 过滤可用的操作
            valid_operations = [op for op in suggested_operations if op in available_operations]
            
            if not valid_operations:
                return ExecutionResult(
                    success=False,
                    message=f"当前状态不允许执行这些操作。当前状态: {current_state['global']}",
                    suggestions=[
                        "请先打开或创建文档",
                        "可用的操作: " + ", ".join(available_operations)
                    ]
                )
            
            return ExecutionResult(
                success=True,
                message=f"建议执行操作: {valid_operations[0]}",
                data={
                    "suggested_operation": valid_operations[0],
                    "all_suggestions": valid_operations,
                    "current_state": current_state
                },
                suggestions=[
                    f"您可以使用 '{valid_operations[0]}' 命令来执行操作",
                    f"其他可用操作: {', '.join(valid_operations[1:3])}"
                ]
            )
            
        except Exception as e:
            logger.error(f"直接操作执行失败: {e}")
            return ExecutionResult(
                success=False,
                message=f"直接操作失败: {str(e)}",
                error_details=str(e)
            )
    
    def _execute_batch_operation(self, user_intent: str, context: Dict[str, Any], intent_analysis: Dict[str, Any]) -> ExecutionResult:
        """执行批量操作"""
        try:
            # 获取批量操作建议
            batch_operations = intent_analysis.get("suggested_batch_operations", [])
            
            if not batch_operations:
                return ExecutionResult(
                    success=False,
                    message="无法确定批量操作内容",
                    suggestions=["请提供更具体的批量操作描述"]
                )
            
            return ExecutionResult(
                success=True,
                message="建议执行批量操作",
                data={
                    "batch_operations": batch_operations,
                    "estimated_time": "5-10分钟"
                },
                suggestions=[
                    "批量操作将按顺序执行多个命令",
                    "您可以使用 'execute_batch' 命令来执行批量操作"
                ]
            )
            
        except Exception as e:
            logger.error(f"批量操作执行失败: {e}")
            return ExecutionResult(
                success=False,
                message=f"批量操作失败: {str(e)}",
                error_details=str(e)
            )
    
    def fill_template(self, template_id: str, variables: Dict[str, Any]) -> ExecutionResult:
        """填写模板数据"""
        try:
            # 验证模板数据
            validation_result = self.template_engine.validate_template_data(template_id, variables)
            
            if not validation_result.is_valid:
                return ExecutionResult(
                    success=False,
                    message="模板数据验证失败",
                    data={
                        "missing_variables": validation_result.missing_variables,
                        "error_messages": validation_result.error_messages
                    },
                    suggestions=[
                        f"请提供缺少的变量: {', '.join(validation_result.missing_variables)}",
                        "请检查数据格式是否正确"
                    ]
                )
            
            # 渲染模板
            document_structure = self.template_engine.template_renderer.render_template_to_document(template_id, variables)
            
            return ExecutionResult(
                success=True,
                message="模板填写成功",
                data={
                    "template_id": template_id,
                    "document_structure": document_structure,
                    "warnings": validation_result.warnings
                },
                suggestions=[
                    "模板已准备就绪，可以使用 'render_document' 命令生成文档",
                    "您还可以使用 'modify_template_content' 命令修改特定内容"
                ]
            )
            
        except Exception as e:
            logger.error(f"模板填写失败: {e}")
            return ExecutionResult(
                success=False,
                message=f"模板填写失败: {str(e)}",
                error_details=str(e)
            )
    
    def get_contextual_suggestions(self) -> List[str]:
        """获取上下文相关的操作建议"""
        current_state = self.state_manager.get_current_state_summary()
        available_operations = self.state_manager.get_available_operations()
        
        suggestions = []
        
        if current_state["global"] == "no_document":
            suggestions = [
                "请先创建或打开文档",
                "使用 'create_document' 创建新文档",
                "使用 'open_document' 打开现有文档"
            ]
        elif current_state["global"] == "document_ready":
            suggestions = [
                "可以开始编辑文档内容",
                "使用 'add_paragraph' 添加段落",
                "使用 'add_table' 添加表格",
                "使用 'add_image' 添加图片"
            ]
        elif current_state["global"] == "document_editing":
            suggestions = [
                "继续编辑文档内容",
                "使用 'save_document' 保存文档",
                "使用 'set_paragraph_font' 设置格式"
            ]
        
        # 添加模板建议
        template_categories = self.template_engine.get_template_categories()
        if template_categories:
            suggestions.append(f"可以使用模板: {', '.join(template_categories)}")
        
        return suggestions
    
    def _suggest_templates_by_intent(self, user_intent: str) -> List[TemplateSuggestion]:
        """基于意图建议模板"""
        return self.template_engine.suggest_templates_by_intent(user_intent)
    
    def _suggest_direct_operations(self, user_intent: str) -> List[str]:
        """基于意图建议直接操作"""
        intent_lower = user_intent.lower()
        suggestions = []
        
        if "段落" in intent_lower or "文字" in intent_lower:
            suggestions.extend(["add_paragraph", "add_heading"])
        if "表格" in intent_lower:
            suggestions.extend(["add_table", "edit_table_cell", "add_table_row"])
        if "图片" in intent_lower:
            suggestions.extend(["add_image", "resize_image", "list_images"])
        if "保存" in intent_lower:
            suggestions.append("save_document")
        if "搜索" in intent_lower:
            suggestions.extend(["search_text", "find_and_replace"])
        if "格式" in intent_lower:
            suggestions.extend(["set_paragraph_font", "batch_format_paragraphs"])
        
        return suggestions
    
    def _suggest_batch_operations(self, user_intent: str) -> List[str]:
        """基于意图建议批量操作"""
        intent_lower = user_intent.lower()
        suggestions = []
        
        if "格式化" in intent_lower:
            suggestions.append("batch_format_paragraphs")
        if "删除" in intent_lower:
            suggestions.extend(["delete_paragraph", "delete_table_row"])
        if "添加" in intent_lower:
            suggestions.extend(["add_paragraph", "add_table_row", "add_image"])
        
        return suggestions
    
    def get_operation_statistics(self) -> Dict[str, Any]:
        """获取操作统计信息"""
        state_stats = self.state_manager.get_operation_statistics()
        
        return {
            "state_statistics": state_stats,
            "template_count": len(self.template_engine.template_registry),
            "template_categories": self.template_engine.get_template_categories(),
            "operation_history_count": len(self.operation_history)
        }
