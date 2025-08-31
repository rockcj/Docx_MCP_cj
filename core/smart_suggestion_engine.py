#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能提示引擎
根据当前状态和上下文智能推荐下一步操作
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re

from .enhanced_state_manager import EnhancedStateManager, OperationType, OperationStatus
from .workflow_engine import WorkflowEngine, WorkflowDefinition
from .template_engine import DocumentTemplateEngine

logger = logging.getLogger(__name__)

# ==================== 枚举定义 ====================

class SuggestionType(Enum):
    """建议类型"""
    WORKFLOW = "workflow"              # 工作流建议
    OPERATION = "operation"            # 操作建议
    TEMPLATE = "template"              # 模板建议
    ERROR_RECOVERY = "error_recovery"  # 错误恢复建议
    OPTIMIZATION = "optimization"      # 优化建议
    NEXT_STEP = "next_step"           # 下一步建议

class SuggestionPriority(Enum):
    """建议优先级"""
    HIGH = "high"      # 高优先级
    MEDIUM = "medium"  # 中等优先级
    LOW = "low"        # 低优先级

# ==================== 数据结构定义 ====================

@dataclass
class SmartSuggestion:
    """智能建议"""
    suggestion_id: str
    suggestion_type: SuggestionType
    title: str
    description: str
    priority: SuggestionPriority
    confidence: float  # 置信度 0-1
    action_type: str   # 建议的操作类型
    parameters: Dict[str, Any] = field(default_factory=dict)
    reasoning: List[str] = field(default_factory=list)  # 推荐理由
    prerequisites: List[str] = field(default_factory=list)  # 前置条件
    estimated_time: str = ""
    examples: List[Dict[str, Any]] = field(default_factory=list)  # 示例

@dataclass
class ContextAnalysis:
    """上下文分析结果"""
    current_state: str
    recent_operations: List[str]
    document_info: Dict[str, Any]
    user_patterns: Dict[str, Any]
    error_patterns: List[str]
    optimization_opportunities: List[str]

# ==================== 智能提示引擎 ====================

class SmartSuggestionEngine:
    """智能提示引擎 - 根据当前状态推荐下一步操作"""
    
    def __init__(self, state_manager: EnhancedStateManager, 
                 workflow_engine: WorkflowEngine, 
                 template_engine: DocumentTemplateEngine):
        self.state_manager = state_manager
        self.workflow_engine = workflow_engine
        self.template_engine = template_engine
        
        # 用户行为模式分析
        self.user_patterns = {}
        self.operation_patterns = {}
        
        # 建议规则库
        self.suggestion_rules = self._initialize_suggestion_rules()
        
        logger.info("智能提示引擎初始化完成")
    
    def _initialize_suggestion_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """初始化建议规则库"""
        return {
            "document_creation": [
                {
                    "condition": "no_current_document",
                    "suggestions": [
                        {
                            "type": SuggestionType.WORKFLOW,
                            "action": "create_document",
                            "title": "创建新文档",
                            "description": "开始创建一个新的Word文档",
                            "priority": SuggestionPriority.HIGH,
                            "confidence": 0.9
                        },
                        {
                            "type": SuggestionType.TEMPLATE,
                            "action": "browse_templates",
                            "title": "浏览文档模板",
                            "description": "查看可用的文档模板，快速开始",
                            "priority": SuggestionPriority.MEDIUM,
                            "confidence": 0.8
                        }
                    ]
                }
            ],
            "document_editing": [
                {
                    "condition": "has_current_document",
                    "suggestions": [
                        {
                            "type": SuggestionType.OPERATION,
                            "action": "add_content",
                            "title": "添加内容",
                            "description": "向文档添加段落、标题或表格",
                            "priority": SuggestionPriority.HIGH,
                            "confidence": 0.8
                        },
                        {
                            "type": SuggestionType.OPERATION,
                            "action": "format_document",
                            "title": "格式化文档",
                            "description": "调整文档格式和样式",
                            "priority": SuggestionPriority.MEDIUM,
                            "confidence": 0.7
                        }
                    ]
                }
            ],
            "error_recovery": [
                {
                    "condition": "recent_failures",
                    "suggestions": [
                        {
                            "type": SuggestionType.ERROR_RECOVERY,
                            "action": "retry_operation",
                            "title": "重试操作",
                            "description": "重试最近失败的操作",
                            "priority": SuggestionPriority.HIGH,
                            "confidence": 0.9
                        },
                        {
                            "type": SuggestionType.ERROR_RECOVERY,
                            "action": "restore_snapshot",
                            "title": "恢复快照",
                            "description": "从之前的状态快照恢复",
                            "priority": SuggestionPriority.MEDIUM,
                            "confidence": 0.8
                        }
                    ]
                }
            ],
            "workflow_optimization": [
                {
                    "condition": "repetitive_operations",
                    "suggestions": [
                        {
                            "type": SuggestionType.OPTIMIZATION,
                            "action": "create_workflow",
                            "title": "创建工作流",
                            "description": "将重复操作转换为自动化工作流",
                            "priority": SuggestionPriority.MEDIUM,
                            "confidence": 0.8
                        }
                    ]
                }
            ]
        }
    
    def analyze_context(self) -> ContextAnalysis:
        """分析当前上下文"""
        session_info = self.state_manager.get_current_session_info()
        recent_operations = self.state_manager.get_operation_history(limit=10)
        
        # 分析当前状态
        current_state = "idle"
        if session_info.get("current_document"):
            current_state = "document_open"
        if session_info.get("active_operations_count", 0) > 0:
            current_state = "operation_running"
        
        # 分析最近操作
        recent_op_types = [op.operation_type.value for op in recent_operations]
        
        # 分析文档信息
        document_info = {}
        if session_info.get("current_document"):
            doc_state = self.state_manager.get_document_state(session_info["current_document"])
            if doc_state:
                document_info = {
                    "file_path": doc_state.file_path,
                    "last_modified": doc_state.last_modified.isoformat(),
                    "structure": doc_state.structure_info,
                    "operation_count": len(doc_state.operation_history)
                }
        
        # 分析用户模式
        user_patterns = self._analyze_user_patterns(recent_operations)
        
        # 分析错误模式
        error_patterns = self._analyze_error_patterns(recent_operations)
        
        # 分析优化机会
        optimization_opportunities = self._analyze_optimization_opportunities(recent_operations)
        
        return ContextAnalysis(
            current_state=current_state,
            recent_operations=recent_op_types,
            document_info=document_info,
            user_patterns=user_patterns,
            error_patterns=error_patterns,
            optimization_opportunities=optimization_opportunities
        )
    
    def generate_suggestions(self, user_intent: str = None, limit: int = 5) -> List[SmartSuggestion]:
        """生成智能建议"""
        context = self.analyze_context()
        suggestions = []
        
        # 基于上下文的建议
        context_suggestions = self._generate_context_based_suggestions(context)
        suggestions.extend(context_suggestions)
        
        # 基于用户意图的建议
        if user_intent:
            intent_suggestions = self._generate_intent_based_suggestions(user_intent, context)
            suggestions.extend(intent_suggestions)
        
        # 基于错误恢复的建议
        error_suggestions = self._generate_error_recovery_suggestions(context)
        suggestions.extend(error_suggestions)
        
        # 基于优化的建议
        optimization_suggestions = self._generate_optimization_suggestions(context)
        suggestions.extend(optimization_suggestions)
        
        # 去重和排序
        suggestions = self._deduplicate_and_rank_suggestions(suggestions)
        
        return suggestions[:limit]
    
    def _generate_context_based_suggestions(self, context: ContextAnalysis) -> List[SmartSuggestion]:
        """基于上下文生成建议"""
        suggestions = []
        
        # 根据当前状态生成建议
        if context.current_state == "idle":
            suggestions.append(SmartSuggestion(
                suggestion_id="create_document_suggestion",
                suggestion_type=SuggestionType.WORKFLOW,
                title="创建新文档",
                description="开始创建一个新的Word文档，支持多种模板和格式",
                priority=SuggestionPriority.HIGH,
                confidence=0.9,
                action_type="workflow",
                parameters={"workflow_id": "create_document"},
                reasoning=["当前没有打开的文档", "创建文档是常见的起始操作"],
                estimated_time="1-2分钟",
                examples=[
                    {
                        "description": "创建空白文档",
                        "parameters": {"filename": "新文档.docx"}
                    },
                    {
                        "description": "使用模板创建文档",
                        "parameters": {"filename": "报告.docx", "template_id": "business_report"}
                    }
                ]
            ))
        
        elif context.current_state == "document_open":
            # 分析文档内容，提供针对性建议
            if context.document_info.get("structure", {}).get("paragraphs_count", 0) == 0:
                suggestions.append(SmartSuggestion(
                    suggestion_id="add_content_suggestion",
                    suggestion_type=SuggestionType.OPERATION,
                    title="添加文档内容",
                    description="向空白文档添加段落、标题或列表",
                    priority=SuggestionPriority.HIGH,
                    confidence=0.9,
                    action_type="operation",
                    parameters={"operation": "add_paragraph"},
                    reasoning=["文档为空", "需要添加内容"],
                    estimated_time="2-3分钟"
                ))
            
            if context.document_info.get("structure", {}).get("tables_count", 0) == 0:
                suggestions.append(SmartSuggestion(
                    suggestion_id="add_table_suggestion",
                    suggestion_type=SuggestionType.OPERATION,
                    title="添加表格",
                    description="在文档中添加表格来组织数据",
                    priority=SuggestionPriority.MEDIUM,
                    confidence=0.7,
                    action_type="operation",
                    parameters={"operation": "add_table"},
                    reasoning=["文档中没有表格", "表格有助于数据展示"],
                    estimated_time="3-5分钟"
                ))
            
            # 如果文档有内容，推荐上传到OSS
            if (context.document_info.get("structure", {}).get("paragraphs_count", 0) > 0 or 
                context.document_info.get("structure", {}).get("tables_count", 0) > 0):
                suggestions.append(SmartSuggestion(
                    suggestion_id="auto_oss_upload_suggestion",
                    suggestion_type=SuggestionType.WORKFLOW,
                    title="上传到OSS云存储",
                    description="将文档上传到OSS云存储并提供下载链接",
                    priority=SuggestionPriority.HIGH,
                    confidence=0.8,
                    action_type="workflow",
                    parameters={"workflow_id": "auto_oss_upload"},
                    reasoning=["文档已有内容", "默认自动上传到OSS"],
                    estimated_time="30秒-1分钟"
                ))
        
        return suggestions
    
    def _generate_intent_based_suggestions(self, user_intent: str, context: ContextAnalysis) -> List[SmartSuggestion]:
        """基于用户意图生成建议"""
        suggestions = []
        intent_lower = user_intent.lower()
        
        # 分析意图关键词
        if any(keyword in intent_lower for keyword in ["创建", "新建", "制作", "生成"]):
            # 推荐工作流
            workflow_suggestions = self.workflow_engine.suggest_workflows_by_intent(user_intent)
            for wf_suggestion in workflow_suggestions[:3]:
                suggestions.append(SmartSuggestion(
                    suggestion_id=f"workflow_{wf_suggestion['workflow_id']}",
                    suggestion_type=SuggestionType.WORKFLOW,
                    title=wf_suggestion["workflow_name"],
                    description=wf_suggestion["description"],
                    priority=SuggestionPriority.HIGH,
                    confidence=wf_suggestion["match_score"],
                    action_type="workflow",
                    parameters={"workflow_id": wf_suggestion["workflow_id"]},
                    reasoning=wf_suggestion["reasons"],
                    estimated_time=wf_suggestion["estimated_duration"]
                ))
        
        elif any(keyword in intent_lower for keyword in ["模板", "格式", "样式"]):
            # 推荐模板
            template_suggestions = self.template_engine.suggest_templates_by_intent(user_intent)
            for tmpl_suggestion in template_suggestions[:3]:
                suggestions.append(SmartSuggestion(
                    suggestion_id=f"template_{tmpl_suggestion.template_id}",
                    suggestion_type=SuggestionType.TEMPLATE,
                    title=tmpl_suggestion.template_name,
                    description=tmpl_suggestion.reason,
                    priority=SuggestionPriority.HIGH,
                    confidence=tmpl_suggestion.match_score,
                    action_type="template",
                    parameters={"template_id": tmpl_suggestion.template_id},
                    reasoning=[tmpl_suggestion.reason],
                    estimated_time=tmpl_suggestion.estimated_time
                ))
        
        elif any(keyword in intent_lower for keyword in ["添加", "插入", "放入"]):
            # 推荐具体操作
            if "图片" in intent_lower or "image" in intent_lower:
                suggestions.append(SmartSuggestion(
                    suggestion_id="add_image_suggestion",
                    suggestion_type=SuggestionType.OPERATION,
                    title="添加图片",
                    description="向文档添加图片，支持多种格式和布局",
                    priority=SuggestionPriority.HIGH,
                    confidence=0.9,
                    action_type="operation",
                    parameters={"operation": "add_picture"},
                    reasoning=["用户明确提到添加图片"],
                    estimated_time="2-3分钟"
                ))
            
            if "表格" in intent_lower or "table" in intent_lower:
                suggestions.append(SmartSuggestion(
                    suggestion_id="add_table_suggestion",
                    suggestion_type=SuggestionType.OPERATION,
                    title="添加表格",
                    description="创建表格并填充数据",
                    priority=SuggestionPriority.HIGH,
                    confidence=0.9,
                    action_type="operation",
                    parameters={"operation": "add_table"},
                    reasoning=["用户明确提到添加表格"],
                    estimated_time="3-5分钟"
                ))
        
        elif any(keyword in intent_lower for keyword in ["下载", "链接", "分享", "上传", "云端", "oss"]):
            # 推荐OSS上传操作
            suggestions.append(SmartSuggestion(
                suggestion_id="oss_upload_suggestion",
                suggestion_type=SuggestionType.WORKFLOW,
                title="上传到OSS云存储",
                description="将文档上传到OSS云存储并提供下载链接",
                priority=SuggestionPriority.HIGH,
                confidence=0.9,
                action_type="workflow",
                parameters={"workflow_id": "auto_oss_upload"},
                reasoning=["用户提到下载链接或云端存储"],
                estimated_time="30秒-1分钟"
            ))
        
        return suggestions
    
    def _generate_error_recovery_suggestions(self, context: ContextAnalysis) -> List[SmartSuggestion]:
        """生成错误恢复建议"""
        suggestions = []
        
        if context.error_patterns:
            # 检查最近的失败操作
            recent_failures = self.state_manager.get_operation_history(limit=5)
            failed_operations = [op for op in recent_failures if op.status == OperationStatus.FAILED]
            
            if failed_operations:
                latest_failure = failed_operations[0]
                suggestions.append(SmartSuggestion(
                    suggestion_id="retry_failed_operation",
                    suggestion_type=SuggestionType.ERROR_RECOVERY,
                    title="重试失败的操作",
                    description=f"重试最近失败的操作: {latest_failure.operation_type.value}",
                    priority=SuggestionPriority.HIGH,
                    confidence=0.8,
                    action_type="retry",
                    parameters={"operation_id": latest_failure.operation_id},
                    reasoning=["检测到最近的操作失败", "重试可能解决问题"],
                    estimated_time="1-2分钟"
                ))
                
                # 检查是否有可用的快照
                snapshots = self.state_manager.get_available_snapshots()
                if snapshots:
                    latest_snapshot = snapshots[0]
                    suggestions.append(SmartSuggestion(
                        suggestion_id="restore_snapshot",
                        suggestion_type=SuggestionType.ERROR_RECOVERY,
                        title="恢复状态快照",
                        description=f"从快照恢复: {latest_snapshot['timestamp']}",
                        priority=SuggestionPriority.MEDIUM,
                        confidence=0.7,
                        action_type="restore",
                        parameters={"snapshot_id": latest_snapshot["snapshot_id"]},
                        reasoning=["有可用的状态快照", "可以恢复到之前的工作状态"],
                        estimated_time="1分钟"
                    ))
        
        return suggestions
    
    def _generate_optimization_suggestions(self, context: ContextAnalysis) -> List[SmartSuggestion]:
        """生成优化建议"""
        suggestions = []
        
        if context.optimization_opportunities:
            for opportunity in context.optimization_opportunities:
                if "repetitive_operations" in opportunity:
                    suggestions.append(SmartSuggestion(
                        suggestion_id="create_workflow_optimization",
                        suggestion_type=SuggestionType.OPTIMIZATION,
                        title="创建工作流",
                        description="将重复的操作序列转换为自动化工作流",
                        priority=SuggestionPriority.MEDIUM,
                        confidence=0.8,
                        action_type="create_workflow",
                        parameters={},
                        reasoning=["检测到重复操作模式", "工作流可以提高效率"],
                        estimated_time="5-10分钟"
                    ))
        
        return suggestions
    
    def _analyze_user_patterns(self, recent_operations: List) -> Dict[str, Any]:
        """分析用户行为模式"""
        patterns = {
            "frequent_operations": {},
            "operation_sequences": [],
            "time_patterns": {},
            "error_patterns": []
        }
        
        # 统计操作频率
        for op in recent_operations:
            op_type = op.operation_type.value
            patterns["frequent_operations"][op_type] = patterns["frequent_operations"].get(op_type, 0) + 1
        
        # 分析操作序列
        if len(recent_operations) >= 2:
            sequences = []
            for i in range(len(recent_operations) - 1):
                seq = f"{recent_operations[i].operation_type.value} -> {recent_operations[i+1].operation_type.value}"
                sequences.append(seq)
            patterns["operation_sequences"] = sequences
        
        return patterns
    
    def _analyze_error_patterns(self, recent_operations: List) -> List[str]:
        """分析错误模式"""
        error_patterns = []
        
        failed_operations = [op for op in recent_operations if op.status == OperationStatus.FAILED]
        
        if len(failed_operations) >= 2:
            error_patterns.append("recent_failures")
        
        # 分析特定错误类型
        for op in failed_operations:
            if "file" in op.error_message.lower() if op.error_message else False:
                error_patterns.append("file_access_errors")
            if "permission" in op.error_message.lower() if op.error_message else False:
                error_patterns.append("permission_errors")
        
        return list(set(error_patterns))
    
    def _analyze_optimization_opportunities(self, recent_operations: List) -> List[str]:
        """分析优化机会"""
        opportunities = []
        
        # 检查重复操作
        operation_counts = {}
        for op in recent_operations:
            op_type = op.operation_type.value
            operation_counts[op_type] = operation_counts.get(op_type, 0) + 1
        
        # 如果某个操作重复3次以上，建议创建工作流
        for op_type, count in operation_counts.items():
            if count >= 3:
                opportunities.append("repetitive_operations")
                break
        
        return opportunities
    
    def _deduplicate_and_rank_suggestions(self, suggestions: List[SmartSuggestion]) -> List[SmartSuggestion]:
        """去重和排序建议"""
        # 去重
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            key = (suggestion.suggestion_type, suggestion.action_type)
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(suggestion)
        
        # 排序：优先级 > 置信度 > 类型
        def sort_key(suggestion):
            priority_score = {"high": 3, "medium": 2, "low": 1}[suggestion.priority.value]
            type_score = {"workflow": 3, "operation": 2, "template": 2, "error_recovery": 4, "optimization": 1}[suggestion.suggestion_type.value]
            return (priority_score, suggestion.confidence, type_score)
        
        unique_suggestions.sort(key=sort_key, reverse=True)
        return unique_suggestions
    
    def get_suggestion_details(self, suggestion_id: str) -> Optional[Dict[str, Any]]:
        """获取建议的详细信息"""
        # 这里可以根据suggestion_id返回更详细的信息
        # 包括具体的参数示例、使用说明等
        return {
            "suggestion_id": suggestion_id,
            "detailed_examples": [],
            "usage_instructions": "",
            "related_suggestions": []
        }
    
    def provide_feedback(self, suggestion_id: str, feedback: str, rating: int):
        """提供建议反馈"""
        # 记录用户对建议的反馈，用于改进建议质量
        logger.info(f"建议反馈: {suggestion_id} - {feedback} (评分: {rating})")
        
        # 这里可以更新建议的权重或调整推荐算法
        pass
