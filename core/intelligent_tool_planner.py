#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能工具规划器 - 为AI提供智能的工具选择和规划能力
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class TaskType(Enum):
    """任务类型枚举"""
    DOCUMENT_CREATION = "document_creation"
    TABLE_PROCESSING = "table_processing"
    CONTENT_EDITING = "content_editing"
    FORMAT_PRESERVATION = "format_preservation"
    STRUCTURE_EXTRACTION = "structure_extraction"
    IMAGE_PROCESSING = "image_processing"
    BATCH_PROCESSING = "batch_processing"
    COMPLEX_WORKFLOW = "complex_workflow"

@dataclass
class ToolInfo:
    """工具信息"""
    name: str
    description: str
    parameters: Dict[str, Any]
    use_cases: List[str]
    prerequisites: List[str]
    output_format: str
    examples: List[Dict[str, Any]]

@dataclass
class WorkflowStep:
    """工作流步骤"""
    step_id: int
    tool_name: str
    parameters: Dict[str, Any]
    description: str
    expected_output: str
    validation_criteria: List[str]

@dataclass
class IntelligentPlan:
    """智能规划结果"""
    task_type: TaskType
    total_steps: int
    estimated_time: str
    workflow_steps: List[WorkflowStep]
    parallel_opportunities: List[List[int]]
    risk_factors: List[str]
    optimization_suggestions: List[str]

class IntelligentToolPlanner:
    """智能工具规划器"""
    
    def __init__(self):
        self.tools_registry = self._build_tools_registry()
        self.workflow_patterns = self._build_workflow_patterns()
        
    def _build_tools_registry(self) -> Dict[str, ToolInfo]:
        """构建工具注册表"""
        return {
            # 基础文档管理
            "create_document": ToolInfo(
                name="create_document",
                description="创建新的Word文档",
                parameters={"file_path": "文档保存路径", "title": "文档标题"},
                use_cases=["新建文档", "初始化工作"],
                prerequisites=[],
                output_format="成功创建文档路径",
                examples=[
                    {"file_path": "docs/新文档.docx", "title": "项目报告"}
                ]
            ),
            
            "open_document": ToolInfo(
                name="open_document", 
                description="打开现有Word文档",
                parameters={"file_path": "文档路径"},
                use_cases=["编辑现有文档", "查看文档内容"],
                prerequisites=["文档文件存在"],
                output_format="文档已打开",
                examples=[
                    {"file_path": "docs/报告.docx"}
                ]
            ),
            
            "save_document": ToolInfo(
                name="save_document",
                description="保存当前文档",
                parameters={"file_path": "保存路径"},
                use_cases=["保存更改", "另存为新文件"],
                prerequisites=["有打开的文档"],
                output_format="文档已保存",
                examples=[
                    {"file_path": "docs/修改后的报告.docx"}
                ]
            ),
            
            # 智能表格处理
            "intelligent_table_fill": ToolInfo(
                name="intelligent_table_fill",
                description="智能表格填充 - 在保持格式的前提下智能填充表格内容",
                parameters={
                    "file_path": "文档文件路径",
                    "table_index": "表格索引(从0开始)",
                    "fill_data": "填充数据字典"
                },
                use_cases=["空白表格填充", "批量数据录入", "表格内容更新"],
                prerequisites=["文档已打开", "表格结构已分析"],
                output_format="填充成功统计",
                examples=[
                    {
                        "file_path": "docs/学生信息表.docx",
                        "table_index": 0,
                        "fill_data": {"姓名": "张三", "学号": "2023001", "班级": "计算机1班"}
                    }
                ]
            ),
            
            # 表格结构提取
            "extract_table_structure": ToolInfo(
                name="extract_table_structure",
                description="提取表格的详细结构信息",
                parameters={
                    "file_path": "文档路径",
                    "table_index": "表格索引"
                },
                use_cases=["分析表格布局", "理解表格结构", "为智能填充做准备"],
                prerequisites=["文档存在且包含表格"],
                output_format="JSON格式的表格结构信息",
                examples=[
                    {"file_path": "docs/评价表.docx", "table_index": 0}
                ]
            ),
            
            # 智能内容处理
            "intelligent_content_enhancement": ToolInfo(
                name="intelligent_content_enhancement",
                description="智能内容增强 - 自动优化文档内容",
                parameters={
                    "file_path": "文档路径",
                    "enhancement_type": "增强类型",
                    "content_requirements": "内容要求"
                },
                use_cases=["内容优化", "格式统一", "结构改进"],
                prerequisites=["文档已打开"],
                output_format="增强完成报告",
                examples=[
                    {
                        "file_path": "docs/报告.docx",
                        "enhancement_type": "格式统一",
                        "content_requirements": "统一字体和段落格式"
                    }
                ]
            ),
            
            # 基础文本操作
            "add_paragraph": ToolInfo(
                name="add_paragraph",
                description="添加段落到文档",
                parameters={
                    "text": "段落文本",
                    "style": "段落样式",
                    "position": "插入位置"
                },
                use_cases=["添加新内容", "插入文本"],
                prerequisites=["文档已打开"],
                output_format="段落已添加",
                examples=[
                    {"text": "这是新添加的段落", "style": "Normal", "position": "end"}
                ]
            ),
            
            "replace_text": ToolInfo(
                name="replace_text",
                description="替换文档中的文本",
                parameters={
                    "old_text": "要替换的文本",
                    "new_text": "新文本",
                    "replace_all": "是否全部替换"
                },
                use_cases=["内容修改", "批量替换"],
                prerequisites=["文档已打开"],
                output_format="替换完成统计",
                examples=[
                    {"old_text": "旧内容", "new_text": "新内容", "replace_all": True}
                ]
            )
        }
    
    def _build_workflow_patterns(self) -> Dict[TaskType, List[str]]:
        """构建工作流模式"""
        return {
            TaskType.DOCUMENT_CREATION: [
                "create_document",
                "add_paragraph", 
                "add_table",
                "save_document"
            ],
            
            TaskType.TABLE_PROCESSING: [
                "open_document",
                "extract_table_structure",
                "intelligent_table_fill",
                "save_document"
            ],
            
            TaskType.CONTENT_EDITING: [
                "open_document",
                "replace_text",
                "add_paragraph",
                "save_document"
            ],
            
            TaskType.STRUCTURE_EXTRACTION: [
                "open_document",
                "extract_table_structure",
                "extract_all_tables_structure"
            ],
            
            TaskType.COMPLEX_WORKFLOW: [
                "create_document",
                "add_paragraph",
                "add_table", 
                "intelligent_table_fill",
                "intelligent_content_enhancement",
                "save_document"
            ]
        }
    
    def analyze_user_request(self, user_request: str) -> TaskType:
        """分析用户请求，确定任务类型"""
        request_lower = user_request.lower()
        
        # 关键词映射
        if any(keyword in request_lower for keyword in ["创建", "新建", "生成", "制作", "create", "generate"]):
            if any(keyword in request_lower for keyword in ["表格", "table", "数据"]):
                return TaskType.DOCUMENT_CREATION
            return TaskType.DOCUMENT_CREATION
            
        elif any(keyword in request_lower for keyword in ["表格", "table", "填充", "填写", "fill"]):
            return TaskType.TABLE_PROCESSING
            
        elif any(keyword in request_lower for keyword in ["编辑", "修改", "更新", "edit", "modify", "update"]):
            return TaskType.CONTENT_EDITING
            
        elif any(keyword in request_lower for keyword in ["提取", "分析", "extract", "analyze", "结构"]):
            return TaskType.STRUCTURE_EXTRACTION
            
        elif any(keyword in request_lower for keyword in ["图片", "图像", "image", "photo"]):
            return TaskType.IMAGE_PROCESSING
            
        elif any(keyword in request_lower for keyword in ["批量", "batch", "多个", "many"]):
            return TaskType.BATCH_PROCESSING
            
        else:
            return TaskType.COMPLEX_WORKFLOW
    
    def create_intelligent_plan(self, user_request: str, context: Dict[str, Any] = None) -> IntelligentPlan:
        """创建智能规划"""
        task_type = self.analyze_user_request(user_request)
        workflow_steps = []
        
        # 获取基础工作流
        base_workflow = self.workflow_patterns.get(task_type, [])
        
        # 根据用户请求调整工作流
        if task_type == TaskType.TABLE_PROCESSING:
            workflow_steps = [
                WorkflowStep(
                    step_id=1,
                    tool_name="open_document",
                    parameters={"file_path": "待处理文档路径"},
                    description="打开包含表格的文档",
                    expected_output="文档成功打开",
                    validation_criteria=["文档存在", "包含表格"]
                ),
                WorkflowStep(
                    step_id=2,
                    tool_name="extract_table_structure", 
                    parameters={"file_path": "文档路径", "table_index": 0},
                    description="分析表格结构，了解字段布局",
                    expected_output="表格结构信息JSON",
                    validation_criteria=["成功提取结构", "包含字段映射"]
                ),
                WorkflowStep(
                    step_id=3,
                    tool_name="intelligent_table_fill",
                    parameters={
                        "file_path": "文档路径",
                        "table_index": 0,
                        "fill_data": "用户提供的数据字典"
                    },
                    description="智能填充表格数据",
                    expected_output="填充成功统计",
                    validation_criteria=["数据成功填充", "格式保持完整"]
                ),
                WorkflowStep(
                    step_id=4,
                    tool_name="save_document",
                    parameters={"file_path": "保存路径"},
                    description="保存修改后的文档",
                    expected_output="文档已保存",
                    validation_criteria=["保存成功", "文件可访问"]
                )
            ]
        
        elif task_type == TaskType.DOCUMENT_CREATION:
            workflow_steps = [
                WorkflowStep(
                    step_id=1,
                    tool_name="create_document",
                    parameters={"file_path": "新文档路径", "title": "文档标题"},
                    description="创建新文档",
                    expected_output="文档创建成功",
                    validation_criteria=["文档创建", "路径有效"]
                ),
                WorkflowStep(
                    step_id=2,
                    tool_name="add_paragraph",
                    parameters={"text": "初始内容", "style": "Normal"},
                    description="添加初始内容",
                    expected_output="段落已添加",
                    validation_criteria=["内容添加成功"]
                ),
                WorkflowStep(
                    step_id=3,
                    tool_name="save_document",
                    parameters={"file_path": "保存路径"},
                    description="保存新文档",
                    expected_output="文档已保存",
                    validation_criteria=["保存成功"]
                )
            ]
        
        # 识别并行机会
        parallel_opportunities = []
        if len(workflow_steps) > 2:
            # 分析哪些步骤可以并行执行
            for i in range(1, len(workflow_steps) - 1):
                if "extract" in workflow_steps[i].tool_name:
                    parallel_opportunities.append([i, i+1])
        
        # 评估风险因素
        risk_factors = []
        if task_type == TaskType.TABLE_PROCESSING:
            risk_factors.extend([
                "表格结构复杂可能导致字段识别失败",
                "数据格式不匹配可能影响填充效果",
                "文档格式特殊可能影响保存"
            ])
        
        # 生成优化建议
        optimization_suggestions = []
        if task_type == TaskType.TABLE_PROCESSING:
            optimization_suggestions.extend([
                "建议先提取表格结构确认字段映射",
                "建议使用智能填充工具保持格式",
                "建议在填充前备份原文档"
            ])
        
        return IntelligentPlan(
            task_type=task_type,
            total_steps=len(workflow_steps),
            estimated_time=f"{len(workflow_steps) * 2}分钟",
            workflow_steps=workflow_steps,
            parallel_opportunities=parallel_opportunities,
            risk_factors=risk_factors,
            optimization_suggestions=optimization_suggestions
        )
    
    def get_tool_guidance(self, tool_name: str) -> str:
        """获取特定工具的详细指导"""
        tool_info = self.tools_registry.get(tool_name)
        if not tool_info:
            return f"工具 {tool_name} 未找到"
        
        guidance = f"""
🔧 工具详细指导: {tool_info.name}
═══════════════════════════════════════════════════════════════

📋 功能描述:
{tool_info.description}

📝 参数说明:
"""
        for param, desc in tool_info.parameters.items():
            guidance += f"  - {param}: {desc}\n"
        
        guidance += f"""
🎯 适用场景:
"""
        for use_case in tool_info.use_cases:
            guidance += f"  - {use_case}\n"
        
        guidance += f"""
⚠️ 前置条件:
"""
        for prereq in tool_info.prerequisites:
            guidance += f"  - {prereq}\n"
        
        guidance += f"""
📤 输出格式:
{tool_info.output_format}

💡 使用示例:
"""
        for example in tool_info.examples:
            guidance += f"  {json.dumps(example, ensure_ascii=False, indent=2)}\n"
        
        guidance += "\n═══════════════════════════════════════════════════════════════\n"
        
        return guidance
    
    def get_all_tools_summary(self) -> str:
        """获取所有工具的摘要"""
        summary = """
🎯 智能工具规划器 - 工具总览
═══════════════════════════════════════════════════════════════

📚 工具分类:

🔹 基础文档管理:
"""
        doc_tools = ["create_document", "open_document", "save_document", "close_document"]
        for tool in doc_tools:
            if tool in self.tools_registry:
                summary += f"  - {tool}: {self.tools_registry[tool].description}\n"
        
        summary += """
🔹 智能表格处理:
"""
        table_tools = ["intelligent_table_fill", "extract_table_structure", "extract_all_tables_structure"]
        for tool in table_tools:
            if tool in self.tools_registry:
                summary += f"  - {tool}: {self.tools_registry[tool].description}\n"
        
        summary += """
🔹 基础文本操作:
"""
        text_tools = ["add_paragraph", "replace_text", "delete_paragraph"]
        for tool in text_tools:
            if tool in self.tools_registry:
                summary += f"  - {tool}: {self.tools_registry[tool].description}\n"
        
        summary += """
🔹 智能内容处理:
"""
        smart_tools = ["intelligent_content_enhancement", "intelligent_create_table"]
        for tool in smart_tools:
            if tool in self.tools_registry:
                summary += f"  - {tool}: {self.tools_registry[tool].description}\n"
        
        summary += """
🎯 智能规划建议:
═══════════════════════════════════════════════════════════════

1. 📋 任务分析:
   - 首先分析用户请求，确定任务类型
   - 识别关键信息：文档路径、表格索引、数据内容等
   - 评估任务复杂度和风险

2. 🔄 工作流规划:
   - 按照逻辑顺序规划工具调用
   - 识别可以并行执行的步骤
   - 考虑错误处理和回滚策略

3. ⚡ 优化执行:
   - 优先使用智能工具（如intelligent_table_fill）
   - 利用缓存机制提高效率
   - 批量处理相似任务

4. ✅ 质量保证:
   - 每个步骤后验证结果
   - 保持文档格式完整性
   - 提供详细的执行报告

═══════════════════════════════════════════════════════════════
"""
        
        return summary

# 全局规划器实例
intelligent_planner = IntelligentToolPlanner()
