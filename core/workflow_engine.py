#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工作流引擎模块
定义常见的工具调用序列，提供智能的工作流管理功能
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

# ==================== 枚举定义 ====================

class WorkflowStatus(Enum):
    """工作流状态"""
    PENDING = "pending"          # 等待执行
    RUNNING = "running"          # 正在执行
    COMPLETED = "completed"      # 执行完成
    FAILED = "failed"           # 执行失败
    CANCELLED = "cancelled"     # 已取消
    PAUSED = "paused"           # 已暂停

class StepStatus(Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

# ==================== 数据结构定义 ====================

@dataclass
class WorkflowStep:
    """工作流步骤定义"""
    step_id: str
    step_name: str
    tool_name: str
    parameters: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)  # 依赖的步骤ID
    condition: Optional[str] = None  # 执行条件
    retry_count: int = 0
    max_retries: int = 3
    timeout: int = 30  # 超时时间（秒）
    description: str = ""
    error_recovery: Optional[str] = None  # 错误恢复策略

@dataclass
class WorkflowDefinition:
    """工作流定义"""
    workflow_id: str
    workflow_name: str
    description: str
    version: str
    category: str
    steps: List[WorkflowStep]
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    estimated_duration: str = "5-10分钟"
    difficulty_level: str = "beginner"

@dataclass
class StepExecutionResult:
    """步骤执行结果"""
    step_id: str
    success: bool
    result: Any = None
    error_message: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0

@dataclass
class WorkflowExecution:
    """工作流执行实例"""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    input_parameters: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    step_results: Dict[str, StepExecutionResult] = field(default_factory=dict)
    error_log: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

# ==================== 工作流引擎核心类 ====================

class WorkflowEngine:
    """工作流引擎 - 管理工具调用序列的执行"""
    
    def __init__(self, workflows_dir: str = "workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflow_registry: Dict[str, WorkflowDefinition] = {}
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.tool_executors: Dict[str, Callable] = {}
        
        # 确保工作流目录存在
        self.workflows_dir.mkdir(exist_ok=True)
        
        # 加载预定义工作流
        self._load_predefined_workflows()
        
        logger.info(f"工作流引擎初始化完成，加载了 {len(self.workflow_registry)} 个工作流")
    
    def _load_predefined_workflows(self):
        """加载预定义工作流"""
        # 创建文档工作流
        self._create_document_workflows()
        # 创建图片处理工作流
        self._create_image_workflows()
        # 创建表格操作工作流
        self._create_table_workflows()
        # 创建模板应用工作流
        self._create_template_workflows()
    
    def _create_document_workflows(self):
        """创建文档相关的工作流"""
        
        # 1. 创建新文档工作流
        create_doc_workflow = WorkflowDefinition(
            workflow_id="create_document",
            workflow_name="创建新文档",
            description="创建一个新的Word文档并设置基本格式",
            version="1.0",
            category="document",
            steps=[
                WorkflowStep(
                    step_id="validate_params",
                    step_name="验证参数",
                    tool_name="validate_document_params",
                    parameters={},
                    description="验证文档创建参数的有效性"
                ),
                WorkflowStep(
                    step_id="create_doc",
                    step_name="创建文档",
                    tool_name="create_document",
                    parameters={},
                    dependencies=["validate_params"],
                    description="创建新的Word文档"
                ),
                WorkflowStep(
                    step_id="set_page_settings",
                    step_name="设置页面",
                    tool_name="set_page_settings",
                    parameters={},
                    dependencies=["create_doc"],
                    condition="page_settings_provided",
                    description="设置页面格式（如果提供）"
                ),
                WorkflowStep(
                    step_id="add_title",
                    step_name="添加标题",
                    tool_name="add_heading",
                    parameters={},
                    dependencies=["create_doc"],
                    condition="title_provided",
                    description="添加文档标题（如果提供）"
                ),
                WorkflowStep(
                    step_id="save_document",
                    step_name="保存文档",
                    tool_name="save_document",
                    parameters={},
                    dependencies=["create_doc", "set_page_settings", "add_title"],
                    description="保存文档到指定路径"
                ),
                WorkflowStep(
                    step_id="upload_to_oss",
                    step_name="上传到OSS",
                    tool_name="upload_current_document_to_oss",
                    parameters={},
                    dependencies=["save_document"],
                    condition="auto_upload_enabled",
                    description="自动上传文档到OSS云存储并提供下载链接"
                )
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "文档文件名"},
                    "title": {"type": "string", "description": "文档标题（可选）"},
                    "page_settings": {
                        "type": "object",
                        "description": "页面设置（可选）",
                        "properties": {
                            "margins": {"type": "object"},
                            "orientation": {"type": "string", "enum": ["portrait", "landscape"]},
                            "size": {"type": "string"}
                        }
                    },
                    "save_locally_only": {
                        "type": "boolean",
                        "description": "是否仅保存到本地，不上传到OSS（默认false，会自动上传到OSS）",
                        "default": False
                    },
                    "custom_oss_filename": {
                        "type": "string",
                        "description": "OSS上的自定义文件名（可选）"
                    }
                },
                "required": ["filename"]
            },
            tags=["document", "creation", "basic"],
            estimated_duration="1-2分钟"
        )
        
        self.workflow_registry["create_document"] = create_doc_workflow
        
        # 2. 打开并编辑文档工作流
        edit_doc_workflow = WorkflowDefinition(
            workflow_id="edit_document",
            workflow_name="编辑现有文档",
            description="打开现有文档并进行编辑操作",
            version="1.0",
            category="document",
            steps=[
                WorkflowStep(
                    step_id="validate_file",
                    step_name="验证文件",
                    tool_name="validate_file_exists",
                    parameters={},
                    description="验证文件是否存在"
                ),
                WorkflowStep(
                    step_id="open_document",
                    step_name="打开文档",
                    tool_name="open_document",
                    parameters={},
                    dependencies=["validate_file"],
                    description="打开Word文档"
                ),
                WorkflowStep(
                    step_id="analyze_document",
                    step_name="分析文档",
                    tool_name="analyze_document_structure",
                    parameters={},
                    dependencies=["open_document"],
                    description="分析文档结构"
                ),
                WorkflowStep(
                    step_id="apply_edits",
                    step_name="应用编辑",
                    tool_name="apply_document_edits",
                    parameters={},
                    dependencies=["analyze_document"],
                    description="应用用户指定的编辑操作"
                ),
                WorkflowStep(
                    step_id="save_changes",
                    step_name="保存更改",
                    tool_name="save_document",
                    parameters={},
                    dependencies=["apply_edits"],
                    description="保存文档更改"
                ),
                WorkflowStep(
                    step_id="upload_to_oss",
                    step_name="上传到OSS",
                    tool_name="upload_current_document_to_oss",
                    parameters={},
                    dependencies=["save_changes"],
                    condition="auto_upload_enabled",
                    description="自动上传更新后的文档到OSS云存储"
                )
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "文档文件路径"},
                    "edits": {
                        "type": "array",
                        "description": "编辑操作列表",
                        "items": {
                            "type": "object",
                            "properties": {
                                "operation": {"type": "string"},
                                "parameters": {"type": "object"}
                            }
                        }
                    }
                },
                "required": ["filename", "edits"]
            },
            tags=["document", "editing", "modification"],
            estimated_duration="3-5分钟"
        )
        
        self.workflow_registry["edit_document"] = edit_doc_workflow
    
    def _create_image_workflows(self):
        """创建图片处理相关的工作流"""
        
        # 添加图片到文档工作流
        add_image_workflow = WorkflowDefinition(
            workflow_id="add_image_to_document",
            workflow_name="添加图片到文档",
            description="将图片添加到Word文档中，支持多种格式和布局选项",
            version="1.0",
            category="image",
            steps=[
                WorkflowStep(
                    step_id="validate_document",
                    step_name="验证文档",
                    tool_name="validate_document_exists",
                    parameters={},
                    description="验证目标文档是否存在"
                ),
                WorkflowStep(
                    step_id="validate_image",
                    step_name="验证图片",
                    tool_name="validate_image_file",
                    parameters={},
                    description="验证图片文件格式和大小"
                ),
                WorkflowStep(
                    step_id="process_image",
                    step_name="处理图片",
                    tool_name="process_image",
                    parameters={},
                    dependencies=["validate_image"],
                    condition="image_processing_needed",
                    description="图片预处理（调整大小、格式转换等）"
                ),
                WorkflowStep(
                    step_id="add_image",
                    step_name="添加图片",
                    tool_name="add_picture",
                    parameters={},
                    dependencies=["validate_document", "process_image"],
                    description="将图片添加到文档中"
                ),
                WorkflowStep(
                    step_id="adjust_layout",
                    step_name="调整布局",
                    tool_name="adjust_image_layout",
                    parameters={},
                    dependencies=["add_image"],
                    condition="layout_adjustment_needed",
                    description="调整图片在文档中的布局"
                ),
                WorkflowStep(
                    step_id="save_document",
                    step_name="保存文档",
                    tool_name="save_document",
                    parameters={},
                    dependencies=["add_image", "adjust_layout"],
                    description="保存包含图片的文档"
                ),
                WorkflowStep(
                    step_id="upload_to_oss",
                    step_name="上传到OSS",
                    tool_name="upload_current_document_to_oss",
                    parameters={},
                    dependencies=["save_document"],
                    condition="auto_upload_enabled",
                    description="自动上传包含图片的文档到OSS云存储"
                )
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "目标文档路径"},
                    "image_path": {"type": "string", "description": "图片文件路径"},
                    "width": {"type": "number", "description": "图片宽度（可选）"},
                    "height": {"type": "number", "description": "图片高度（可选）"},
                    "alignment": {"type": "string", "enum": ["left", "center", "right"], "description": "图片对齐方式"},
                    "caption": {"type": "string", "description": "图片标题（可选）"}
                },
                "required": ["filename", "image_path"]
            },
            tags=["image", "document", "media"],
            estimated_duration="2-3分钟"
        )
        
        self.workflow_registry["add_image_to_document"] = add_image_workflow
    
    def _create_table_workflows(self):
        """创建表格操作相关的工作流"""
        
        # 创建表格工作流
        create_table_workflow = WorkflowDefinition(
            workflow_id="create_table",
            workflow_name="创建表格",
            description="在文档中创建表格并填充数据",
            version="1.0",
            category="table",
            steps=[
                WorkflowStep(
                    step_id="validate_document",
                    step_name="验证文档",
                    tool_name="validate_document_exists",
                    parameters={},
                    description="验证目标文档是否存在"
                ),
                WorkflowStep(
                    step_id="validate_table_data",
                    step_name="验证表格数据",
                    tool_name="validate_table_data",
                    parameters={},
                    description="验证表格数据的格式和完整性"
                ),
                WorkflowStep(
                    step_id="create_table",
                    step_name="创建表格",
                    tool_name="add_table",
                    parameters={},
                    dependencies=["validate_document", "validate_table_data"],
                    description="创建表格结构"
                ),
                WorkflowStep(
                    step_id="populate_table",
                    step_name="填充数据",
                    tool_name="populate_table_data",
                    parameters={},
                    dependencies=["create_table"],
                    description="填充表格数据"
                ),
                WorkflowStep(
                    step_id="format_table",
                    step_name="格式化表格",
                    tool_name="format_table",
                    parameters={},
                    dependencies=["populate_table"],
                    condition="formatting_requested",
                    description="应用表格格式（边框、颜色等）"
                ),
                WorkflowStep(
                    step_id="save_document",
                    step_name="保存文档",
                    tool_name="save_document",
                    parameters={},
                    dependencies=["create_table", "populate_table", "format_table"],
                    description="保存包含表格的文档"
                ),
                WorkflowStep(
                    step_id="upload_to_oss",
                    step_name="上传到OSS",
                    tool_name="upload_current_document_to_oss",
                    parameters={},
                    dependencies=["save_document"],
                    condition="auto_upload_enabled",
                    description="自动上传包含表格的文档到OSS云存储"
                )
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "目标文档路径"},
                    "rows": {"type": "integer", "description": "表格行数"},
                    "cols": {"type": "integer", "description": "表格列数"},
                    "data": {
                        "type": "array",
                        "description": "表格数据",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "has_header": {"type": "boolean", "description": "是否有表头"},
                    "table_style": {
                        "type": "object",
                        "description": "表格样式设置",
                        "properties": {
                            "border_style": {"type": "string"},
                            "header_color": {"type": "string"},
                            "alternating_rows": {"type": "boolean"}
                        }
                    }
                },
                "required": ["filename", "rows", "cols"]
            },
            tags=["table", "data", "formatting"],
            estimated_duration="3-5分钟"
        )
        
        self.workflow_registry["create_table"] = create_table_workflow
    
    def _create_template_workflows(self):
        """创建模板应用相关的工作流"""
        
        # 应用模板工作流
        apply_template_workflow = WorkflowDefinition(
            workflow_id="apply_template",
            workflow_name="应用文档模板",
            description="根据模板创建文档并填充用户数据",
            version="1.0",
            category="template",
            steps=[
                WorkflowStep(
                    step_id="select_template",
                    step_name="选择模板",
                    tool_name="select_template",
                    parameters={},
                    description="根据用户需求选择合适的模板"
                ),
                WorkflowStep(
                    step_id="validate_template_data",
                    step_name="验证模板数据",
                    tool_name="validate_template_data",
                    parameters={},
                    dependencies=["select_template"],
                    description="验证用户提供的数据是否符合模板要求"
                ),
                WorkflowStep(
                    step_id="create_document",
                    step_name="创建文档",
                    tool_name="create_document",
                    parameters={},
                    description="创建新的Word文档"
                ),
                WorkflowStep(
                    step_id="apply_template",
                    step_name="应用模板",
                    tool_name="apply_template_structure",
                    parameters={},
                    dependencies=["create_document", "validate_template_data"],
                    description="将模板结构应用到文档中"
                ),
                WorkflowStep(
                    step_id="fill_template_data",
                    step_name="填充数据",
                    tool_name="fill_template_data",
                    parameters={},
                    dependencies=["apply_template"],
                    description="用用户数据填充模板"
                ),
                WorkflowStep(
                    step_id="validate_result",
                    step_name="验证结果",
                    tool_name="validate_document_result",
                    parameters={},
                    dependencies=["fill_template_data"],
                    description="验证生成的文档是否符合要求"
                ),
                WorkflowStep(
                    step_id="save_document",
                    step_name="保存文档",
                    tool_name="save_document",
                    parameters={},
                    dependencies=["validate_result"],
                    description="保存生成的文档"
                ),
                WorkflowStep(
                    step_id="upload_to_oss",
                    step_name="上传到OSS",
                    tool_name="upload_current_document_to_oss",
                    parameters={},
                    dependencies=["save_document"],
                    condition="auto_upload_enabled",
                    description="自动上传模板生成的文档到OSS云存储"
                )
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "template_id": {"type": "string", "description": "模板ID"},
                    "output_filename": {"type": "string", "description": "输出文件名"},
                    "template_data": {
                        "type": "object",
                        "description": "模板数据",
                        "additionalProperties": True
                    }
                },
                "required": ["template_id", "output_filename", "template_data"]
            },
            tags=["template", "automation", "document_generation"],
            estimated_duration="5-10分钟"
        )
        
        self.workflow_registry["apply_template"] = apply_template_workflow
        
        # 6. 自动OSS上传工作流
        auto_oss_upload_workflow = WorkflowDefinition(
            workflow_id="auto_oss_upload",
            workflow_name="自动OSS上传",
            description="自动将文档上传到OSS云存储并提供下载链接",
            version="1.0",
            category="oss",
            steps=[
                WorkflowStep(
                    step_id="validate_document",
                    step_name="验证文档",
                    tool_name="validate_document_exists",
                    parameters={},
                    description="验证当前文档是否存在"
                ),
                WorkflowStep(
                    step_id="upload_to_oss",
                    step_name="上传到OSS",
                    tool_name="upload_current_document_to_oss",
                    parameters={},
                    dependencies=["validate_document"],
                    description="上传文档到OSS云存储"
                ),
                WorkflowStep(
                    step_id="provide_download_link",
                    step_name="提供下载链接",
                    tool_name="get_download_link",
                    parameters={},
                    dependencies=["upload_to_oss"],
                    description="生成并提供下载链接"
                )
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "custom_filename": {
                        "type": "string",
                        "description": "OSS上的自定义文件名（可选）"
                    },
                    "document_path": {
                        "type": "string",
                        "description": "要上传的文档路径（可选，默认使用当前文档）"
                    }
                },
                "additionalProperties": False
            },
            tags=["oss", "upload", "cloud", "download"],
            estimated_duration="30秒-1分钟"
        )
        
        self.workflow_registry["auto_oss_upload"] = auto_oss_upload_workflow
    
    def register_tool_executor(self, tool_name: str, executor: Callable):
        """注册工具执行器"""
        self.tool_executors[tool_name] = executor
        logger.info(f"注册工具执行器: {tool_name}")
    
    def get_available_workflows(self, category: str = None) -> List[WorkflowDefinition]:
        """获取可用的工作流列表"""
        if category:
            return [wf for wf in self.workflow_registry.values() if wf.category == category]
        return list(self.workflow_registry.values())
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """获取指定工作流"""
        return self.workflow_registry.get(workflow_id)
    
    def suggest_workflows_by_intent(self, user_intent: str) -> List[Dict[str, Any]]:
        """根据用户意图推荐工作流"""
        suggestions = []
        intent_lower = user_intent.lower()
        
        for workflow in self.workflow_registry.values():
            score = 0.0
            reasons = []
            
            # 基于分类匹配
            if workflow.category in intent_lower:
                score += 0.8
                reasons.append(f"匹配{workflow.category}类别")
            
            # 基于标签匹配
            for tag in workflow.tags:
                if tag.lower() in intent_lower:
                    score += 0.3
                    reasons.append(f"匹配标签: {tag}")
            
            # 基于描述匹配
            if any(keyword in workflow.description.lower() for keyword in intent_lower.split()):
                score += 0.2
                reasons.append("描述匹配")
            
            if score > 0:
                suggestions.append({
                    "workflow_id": workflow.workflow_id,
                    "workflow_name": workflow.workflow_name,
                    "description": workflow.description,
                    "match_score": score,
                    "reasons": reasons,
                    "estimated_duration": workflow.estimated_duration,
                    "difficulty_level": workflow.difficulty_level
                })
        
        # 按匹配分数排序
        suggestions.sort(key=lambda x: x["match_score"], reverse=True)
        return suggestions[:5]  # 返回前5个建议
    
    def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> str:
        """执行工作流"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return f"工作流不存在: {workflow_id}"
        
        # 创建执行实例
        execution_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            start_time=datetime.now(),
            input_parameters=parameters
        )
        
        self.active_executions[execution_id] = execution
        
        try:
            # 执行工作流步骤
            result = self._execute_workflow_steps(workflow, execution)
            
            if result["success"]:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                return f"工作流执行成功: {execution_id}\n结果: {result['message']}"
            else:
                execution.status = WorkflowStatus.FAILED
                execution.end_time = datetime.now()
                return f"工作流执行失败: {execution_id}\n错误: {result['message']}"
                
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = datetime.now()
            execution.error_log.append(str(e))
            logger.error(f"工作流执行异常: {e}")
            return f"工作流执行异常: {str(e)}"
    
    def _execute_workflow_steps(self, workflow: WorkflowDefinition, execution: WorkflowExecution) -> Dict[str, Any]:
        """执行工作流步骤"""
        completed_steps = set()
        failed_steps = set()
        
        # 按依赖关系排序步骤
        sorted_steps = self._topological_sort_steps(workflow.steps)
        
        for step in sorted_steps:
            # 检查依赖是否满足
            if not all(dep in completed_steps for dep in step.dependencies):
                continue
            
            # 检查执行条件
            if step.condition and not self._evaluate_condition(step.condition, execution.context):
                execution.step_results[step.step_id] = StepExecutionResult(
                    step_id=step.step_id,
                    success=True,
                    result="条件不满足，跳过执行"
                )
                continue
            
            # 执行步骤
            step_result = self._execute_step(step, execution)
            execution.step_results[step.step_id] = step_result
            
            if step_result.success:
                completed_steps.add(step.step_id)
                # 更新执行上下文
                if step_result.result:
                    execution.context[step.step_id] = step_result.result
            else:
                failed_steps.add(step.step_id)
                # 处理错误恢复
                if step.error_recovery:
                    self._handle_error_recovery(step, execution)
                else:
                    return {
                        "success": False,
                        "message": f"步骤 {step.step_name} 执行失败: {step_result.error_message}"
                    }
        
        if failed_steps:
            return {
                "success": False,
                "message": f"以下步骤执行失败: {', '.join(failed_steps)}"
            }
        
        return {
            "success": True,
            "message": "所有步骤执行成功",
            "completed_steps": list(completed_steps)
        }
    
    def _topological_sort_steps(self, steps: List[WorkflowStep]) -> List[WorkflowStep]:
        """拓扑排序步骤，确保依赖关系正确"""
        # 简化的拓扑排序实现
        sorted_steps = []
        remaining_steps = steps.copy()
        
        while remaining_steps:
            # 找到没有未满足依赖的步骤
            for step in remaining_steps[:]:
                if all(dep in [s.step_id for s in sorted_steps] for dep in step.dependencies):
                    sorted_steps.append(step)
                    remaining_steps.remove(step)
                    break
            else:
                # 如果没有找到可执行的步骤，可能存在循环依赖
                logger.warning("检测到可能的循环依赖，按原始顺序执行")
                sorted_steps.extend(remaining_steps)
                break
        
        return sorted_steps
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """评估执行条件"""
        # 简化的条件评估
        if condition == "page_settings_provided":
            return "page_settings" in context
        elif condition == "title_provided":
            return "title" in context
        elif condition == "image_processing_needed":
            return "image_processing" in context
        elif condition == "layout_adjustment_needed":
            return "layout_adjustment" in context
        elif condition == "formatting_requested":
            return "table_style" in context
        elif condition == "auto_upload_enabled":
            # 默认启用自动上传，除非用户明确要求保存到本地
            return not context.get("save_locally_only", False)
        return True
    
    def _execute_step(self, step: WorkflowStep, execution: WorkflowExecution) -> StepExecutionResult:
        """执行单个步骤"""
        start_time = datetime.now()
        
        try:
            # 获取工具执行器
            executor = self.tool_executors.get(step.tool_name)
            if not executor:
                return StepExecutionResult(
                    step_id=step.step_id,
                    success=False,
                    error_message=f"工具执行器不存在: {step.tool_name}"
                )
            
            # 准备参数
            step_parameters = self._prepare_step_parameters(step, execution)
            
            # 执行工具
            result = executor(**step_parameters)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return StepExecutionResult(
                step_id=step.step_id,
                success=True,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return StepExecutionResult(
                step_id=step.step_id,
                success=False,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def _prepare_step_parameters(self, step: WorkflowStep, execution: WorkflowExecution) -> Dict[str, Any]:
        """准备步骤参数"""
        parameters = step.parameters.copy()
        
        # 从执行上下文和输入参数中解析参数
        for key, value in parameters.items():
            if isinstance(value, str) and value.startswith("$"):
                # 从上下文获取值
                context_key = value[1:]
                if context_key in execution.context:
                    parameters[key] = execution.context[context_key]
                elif context_key in execution.input_parameters:
                    parameters[key] = execution.input_parameters[context_key]
                else:
                    parameters[key] = None
            elif isinstance(value, str) and value.startswith("@"):
                # 从输入参数获取值
                input_key = value[1:]
                parameters[key] = execution.input_parameters.get(input_key)
        
        return parameters
    
    def _handle_error_recovery(self, step: WorkflowStep, execution: WorkflowExecution):
        """处理错误恢复"""
        if step.error_recovery == "retry":
            # 重试机制
            if step.retry_count < step.max_retries:
                step.retry_count += 1
                logger.info(f"重试步骤 {step.step_name}，第 {step.retry_count} 次")
            else:
                logger.error(f"步骤 {step.step_name} 重试次数已达上限")
        elif step.error_recovery == "skip":
            # 跳过步骤
            logger.warning(f"跳过步骤 {step.step_name}")
        elif step.error_recovery == "abort":
            # 中止工作流
            execution.status = WorkflowStatus.FAILED
            logger.error(f"中止工作流，因为步骤 {step.step_name} 失败")
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """获取执行状态"""
        execution = self.active_executions.get(execution_id)
        if not execution:
            return None
        
        return {
            "execution_id": execution_id,
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "start_time": execution.start_time.isoformat(),
            "end_time": execution.end_time.isoformat() if execution.end_time else None,
            "completed_steps": len([r for r in execution.step_results.values() if r.success]),
            "total_steps": len(execution.step_results),
            "error_log": execution.error_log
        }
    
    def cancel_execution(self, execution_id: str) -> bool:
        """取消执行"""
        execution = self.active_executions.get(execution_id)
        if not execution:
            return False
        
        if execution.status == WorkflowStatus.RUNNING:
            execution.status = WorkflowStatus.CANCELLED
            execution.end_time = datetime.now()
            logger.info(f"取消执行: {execution_id}")
            return True
        
        return False
