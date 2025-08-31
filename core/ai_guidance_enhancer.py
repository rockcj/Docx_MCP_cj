#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI指导增强器
提供完整的提示词、调用示例和最佳实践指导
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .workflow_engine import WorkflowEngine, WorkflowDefinition
from .template_engine import DocumentTemplateEngine
from .smart_suggestion_engine import SmartSuggestionEngine

logger = logging.getLogger(__name__)

# ==================== 数据结构定义 ====================

@dataclass
class AIPromptTemplate:
    """AI提示词模板"""
    template_id: str
    template_name: str
    category: str
    description: str
    system_prompt: str
    user_prompt_template: str
    examples: List[Dict[str, Any]] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    best_practices: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)

@dataclass
class ToolCallExample:
    """工具调用示例"""
    example_id: str
    tool_name: str
    description: str
    parameters: Dict[str, Any]
    expected_result: str
    error_cases: List[Dict[str, Any]] = field(default_factory=list)
    alternatives: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class WorkflowExample:
    """工作流示例"""
    workflow_id: str
    scenario: str
    input_data: Dict[str, Any]
    step_by_step: List[Dict[str, Any]]
    expected_output: str
    troubleshooting: List[Dict[str, Any]] = field(default_factory=list)

# ==================== AI指导增强器 ====================

class AIGuidanceEnhancer:
    """AI指导增强器 - 提供完整的提示词和调用示例"""
    
    def __init__(self, workflow_engine: WorkflowEngine, 
                 template_engine: DocumentTemplateEngine,
                 suggestion_engine: SmartSuggestionEngine):
        self.workflow_engine = workflow_engine
        self.template_engine = template_engine
        self.suggestion_engine = suggestion_engine
        
        # 提示词模板库
        self.prompt_templates: Dict[str, AIPromptTemplate] = {}
        
        # 工具调用示例库
        self.tool_examples: Dict[str, List[ToolCallExample]] = {}
        
        # 工作流示例库
        self.workflow_examples: Dict[str, WorkflowExample] = {}
        
        # 初始化指导内容
        self._initialize_prompt_templates()
        self._initialize_tool_examples()
        self._initialize_workflow_examples()
        
        logger.info("AI指导增强器初始化完成")
    
    def _initialize_prompt_templates(self):
        """初始化提示词模板"""
        
        # 1. 文档创建提示词
        create_doc_prompt = AIPromptTemplate(
            template_id="create_document",
            template_name="创建文档",
            category="document_creation",
            description="指导AI创建Word文档的完整提示词",
            system_prompt="""你是一个专业的Word文档处理助手。你的任务是帮助用户创建、编辑和管理Word文档。

核心原则：
1. 始终验证参数的有效性
2. 按照正确的顺序调用工具
3. 提供清晰的错误处理和恢复建议
4. 使用中文进行所有交互
5. **重要：默认自动上传文档到OSS云存储并提供下载链接**

工具调用顺序：
1. 首先验证文档参数
2. 创建或打开文档
3. 应用格式和内容
4. 保存文档
5. **自动上传到OSS云存储（除非用户明确要求仅保存到本地）**
6. 提供下载链接给用户
7. 验证结果

OSS上传规则：
- 默认情况下，所有文档操作完成后都会自动上传到OSS
- 只有在用户明确要求"仅保存到本地"或"不要上传"时才跳过OSS上传
- 上传成功后必须提供下载链接
- 如果用户要求下载链接但没有先上传，必须先执行上传操作""",
            user_prompt_template="""请帮我{action}一个Word文档。

具体要求：
- 文件名：{filename}
- 文档类型：{document_type}
- 内容要求：{content_requirements}
- 格式要求：{format_requirements}

请按照以下步骤执行：
1. 验证参数的有效性
2. 选择合适的工具序列
3. 执行文档创建/编辑操作
4. 验证结果并提供反馈""",
            examples=[
                {
                    "scenario": "创建商务报告",
                    "parameters": {
                        "action": "创建",
                        "filename": "月度销售报告.docx",
                        "document_type": "商务报告",
                        "content_requirements": "包含标题、摘要、数据表格和结论",
                        "format_requirements": "使用公司标准格式，包含页眉页脚"
                    }
                },
                {
                    "scenario": "创建学术论文",
                    "parameters": {
                        "action": "创建",
                        "filename": "研究论文.docx",
                        "document_type": "学术论文",
                        "content_requirements": "包含摘要、引言、方法、结果、讨论和参考文献",
                        "format_requirements": "符合学术规范，使用标准引用格式"
                    }
                }
            ],
            best_practices=[
                "始终检查文件名是否已存在",
                "使用描述性的文件名",
                "在创建前验证所有必需参数",
                "提供清晰的错误信息",
                "建议使用模板以提高效率",
                "**默认自动上传文档到OSS云存储**",
                "**上传成功后必须提供下载链接**",
                "只有在用户明确要求时才跳过OSS上传"
            ],
            common_mistakes=[
                "忘记验证文件路径",
                "使用无效的文件名",
                "跳过参数验证步骤",
                "不处理文件已存在的情况",
                "忘记保存文档",
                "**忘记上传文档到OSS就提供下载链接**",
                "**没有自动上传文档到云存储**",
                "**提供下载链接但没有先上传文件**"
            ]
        )
        
        self.prompt_templates["create_document"] = create_doc_prompt
        
        # 2. 图片处理提示词
        image_processing_prompt = AIPromptTemplate(
            template_id="image_processing",
            template_name="图片处理",
            category="image_handling",
            description="指导AI处理图片的完整提示词",
            system_prompt="""你是一个专业的图片处理助手。你的任务是帮助用户在Word文档中添加、编辑和管理图片。

核心原则：
1. 验证图片文件的存在和格式
2. 检查图片大小和分辨率
3. 提供合适的布局建议
4. 处理图片格式转换
5. 优化图片质量

处理流程：
1. 验证图片文件
2. 检查图片属性
3. 处理图片（如需要）
4. 添加到文档
5. 调整布局""",
            user_prompt_template="""请帮我在文档中{action}图片。

图片信息：
- 图片路径：{image_path}
- 目标文档：{target_document}
- 布局要求：{layout_requirements}
- 尺寸要求：{size_requirements}

请执行以下步骤：
1. 验证图片文件的有效性
2. 检查图片格式和大小
3. 处理图片（如需要调整大小或格式）
4. 将图片添加到文档
5. 调整图片在文档中的位置和大小""",
            examples=[
                {
                    "scenario": "添加产品图片",
                    "parameters": {
                        "action": "添加",
                        "image_path": "images/product.jpg",
                        "target_document": "产品手册.docx",
                        "layout_requirements": "居中显示，与文字环绕",
                        "size_requirements": "宽度不超过页面宽度的50%"
                    }
                }
            ],
            best_practices=[
                "检查图片文件是否存在",
                "验证图片格式是否支持",
                "考虑图片大小对文档的影响",
                "提供合适的图片说明",
                "保持图片与文字的比例协调"
            ],
            common_mistakes=[
                "不检查图片文件路径",
                "忽略图片格式兼容性",
                "不处理大图片的优化",
                "忘记添加图片说明",
                "不考虑页面布局"
            ]
        )
        
        self.prompt_templates["image_processing"] = image_processing_prompt
        
        # 3. 表格操作提示词
        table_operation_prompt = AIPromptTemplate(
            template_id="table_operation",
            template_name="表格操作",
            category="table_handling",
            description="指导AI操作表格的完整提示词",
            system_prompt="""你是一个专业的表格处理助手。你的任务是帮助用户在Word文档中创建、编辑和格式化表格。

核心原则：
1. 验证表格数据的完整性
2. 选择合适的表格结构
3. 应用适当的格式
4. 确保数据对齐
5. 提供清晰的表头

操作流程：
1. 验证表格参数
2. 创建表格结构
3. 填充数据
4. 应用格式
5. 验证结果""",
            user_prompt_template="""请帮我{action}表格。

表格信息：
- 行数：{rows}
- 列数：{cols}
- 数据内容：{data}
- 格式要求：{format_requirements}
- 表头设置：{header_settings}

请按以下步骤执行：
1. 验证表格参数的有效性
2. 创建表格结构
3. 填充表格数据
4. 应用表格格式
5. 验证表格显示效果""",
            examples=[
                {
                    "scenario": "创建员工信息表",
                    "parameters": {
                        "action": "创建",
                        "rows": 5,
                        "cols": 4,
                        "data": [["姓名", "部门", "职位", "入职日期"], ["张三", "技术部", "工程师", "2023-01-15"]],
                        "format_requirements": "使用边框，表头加粗，数据居中对齐",
                        "header_settings": "第一行作为表头，使用深色背景"
                    }
                }
            ],
            best_practices=[
                "确保数据行数与指定行数一致",
                "使用清晰的表头",
                "保持数据格式一致",
                "应用适当的边框和颜色",
                "考虑表格在页面中的位置"
            ],
            common_mistakes=[
                "数据行数与表格行数不匹配",
                "忘记设置表头格式",
                "数据格式不统一",
                "表格超出页面宽度",
                "忘记保存表格更改"
            ]
        )
        
        self.prompt_templates["table_operation"] = table_operation_prompt
        
        # 4. OSS上传提示词
        oss_upload_prompt = AIPromptTemplate(
            template_id="oss_upload",
            template_name="OSS云存储上传",
            category="oss_upload",
            description="指导AI进行OSS云存储上传的完整提示词",
            system_prompt="""你是一个专业的文档云存储助手。你的任务是帮助用户将文档上传到OSS云存储并提供下载链接。

核心原则：
1. **默认自动上传所有文档到OSS云存储**
2. 上传成功后必须提供下载链接
3. 只有在用户明确要求时才跳过上传
4. 使用中文进行所有交互
5. 提供清晰的上传状态和结果

上传流程：
1. 验证文档是否存在
2. 上传文档到OSS云存储
3. 获取上传结果和下载链接
4. 向用户提供下载链接
5. 记录上传信息

重要提醒：
- 用户要求下载链接时，必须先确保文档已上传到OSS
- 如果文档未上传，必须先执行上传操作
- 上传失败时要提供清晰的错误信息
- 成功上传后必须提供可用的下载链接""",
            user_prompt_template="""请帮我{action}文档到OSS云存储。

文档信息：
- 文档路径：{document_path}
- 自定义文件名：{custom_filename}
- 上传要求：{upload_requirements}

请按以下步骤执行：
1. 验证文档文件的有效性
2. 上传文档到OSS云存储
3. 获取上传结果和下载链接
4. 提供下载链接给用户
5. 确认上传成功""",
            examples=[
                {
                    "scenario": "上传当前文档",
                    "parameters": {
                        "action": "上传",
                        "document_path": "当前文档",
                        "custom_filename": "月度报告_202401.docx",
                        "upload_requirements": "自动上传并提供下载链接"
                    }
                },
                {
                    "scenario": "上传指定文档",
                    "parameters": {
                        "action": "上传",
                        "document_path": "documents/报告.docx",
                        "custom_filename": "最终报告.docx",
                        "upload_requirements": "上传到OSS并获取下载链接"
                    }
                }
            ],
            best_practices=[
                "**默认自动上传所有文档到OSS**",
                "**上传成功后必须提供下载链接**",
                "验证文档文件存在性",
                "使用描述性的文件名",
                "处理上传失败的情况",
                "提供清晰的上传状态反馈",
                "记录上传结果信息"
            ],
            common_mistakes=[
                "**忘记上传文档就提供下载链接**",
                "**没有自动上传到OSS云存储**",
                "**提供无效的下载链接**",
                "不验证文档文件存在性",
                "不处理上传失败的情况",
                "不提供上传状态反馈"
            ]
        )
        
        self.prompt_templates["oss_upload"] = oss_upload_prompt
    
    def _initialize_tool_examples(self):
        """初始化工具调用示例"""
        
        # 文档创建工具示例
        self.tool_examples["create_document"] = [
            ToolCallExample(
                example_id="create_basic_doc",
                tool_name="create_document",
                description="创建基本Word文档",
                parameters={
                    "filename": "新文档.docx"
                },
                expected_result="成功创建名为'新文档.docx'的Word文档",
                error_cases=[
                    {
                        "error": "文件已存在",
                        "solution": "使用不同的文件名或确认覆盖",
                        "parameters": {"filename": "新文档_副本.docx"}
                    },
                    {
                        "error": "路径无效",
                        "solution": "检查文件路径是否正确",
                        "parameters": {"filename": "./documents/新文档.docx"}
                    }
                ],
                alternatives=[
                    {
                        "description": "使用模板创建文档",
                        "tool": "create_document_from_template",
                        "parameters": {"filename": "报告.docx", "template_id": "business_report"}
                    }
                ]
            )
        ]
        
        # 添加段落工具示例
        self.tool_examples["add_paragraph"] = [
            ToolCallExample(
                example_id="add_simple_paragraph",
                tool_name="add_paragraph",
                description="添加简单段落",
                parameters={
                    "filename": "文档.docx",
                    "text": "这是一个示例段落。"
                },
                expected_result="在文档末尾添加指定文本段落",
                error_cases=[
                    {
                        "error": "文档不存在",
                        "solution": "先创建或打开文档",
                        "prerequisite": "create_document"
                    },
                    {
                        "error": "文本为空",
                        "solution": "提供有效的文本内容",
                        "parameters": {"text": "有效的段落内容"}
                    }
                ],
                alternatives=[
                    {
                        "description": "添加带格式的段落",
                        "tool": "add_paragraph",
                        "parameters": {
                            "filename": "文档.docx",
                            "text": "重要内容",
                            "style": "emphasis"
                        }
                    }
                ]
            )
        ]
        
        # 添加图片工具示例
        self.tool_examples["add_picture"] = [
            ToolCallExample(
                example_id="add_image_basic",
                tool_name="add_picture",
                description="添加图片到文档",
                parameters={
                    "filename": "文档.docx",
                    "image_path": "images/example.jpg"
                },
                expected_result="在文档中添加指定图片",
                error_cases=[
                    {
                        "error": "图片文件不存在",
                        "solution": "检查图片路径是否正确",
                        "parameters": {"image_path": "correct/path/image.jpg"}
                    },
                    {
                        "error": "图片格式不支持",
                        "solution": "使用支持的图片格式（jpg, png, gif, bmp）",
                        "parameters": {"image_path": "images/example.png"}
                    }
                ],
                alternatives=[
                    {
                        "description": "添加带尺寸控制的图片",
                        "tool": "add_picture",
                        "parameters": {
                            "filename": "文档.docx",
                            "image_path": "images/example.jpg",
                            "width": 300,
                            "height": 200
                        }
                    }
                ]
            )
        ]
        
        # 添加表格工具示例
        self.tool_examples["add_table"] = [
            ToolCallExample(
                example_id="create_basic_table",
                tool_name="add_table",
                description="创建基本表格",
                parameters={
                    "filename": "文档.docx",
                    "rows": 3,
                    "cols": 3
                },
                expected_result="在文档中创建3x3的表格",
                error_cases=[
                    {
                        "error": "行数或列数为0",
                        "solution": "提供有效的行数和列数",
                        "parameters": {"rows": 2, "cols": 2}
                    },
                    {
                        "error": "表格过大",
                        "solution": "减少行数或列数",
                        "parameters": {"rows": 10, "cols": 5}
                    }
                ],
                alternatives=[
                    {
                        "description": "创建带数据的表格",
                        "tool": "add_table",
                        "parameters": {
                            "filename": "文档.docx",
                            "rows": 3,
                            "cols": 3,
                            "data": [["A1", "A2", "A3"], ["B1", "B2", "B3"], ["C1", "C2", "C3"]]
                        }
                    }
                ]
            )
        ]
        
        # OSS上传工具示例
        self.tool_examples["upload_current_document_to_oss"] = [
            ToolCallExample(
                example_id="upload_current_doc",
                tool_name="upload_current_document_to_oss",
                description="上传当前文档到OSS",
                parameters={
                    "custom_filename": "月度报告_202401.docx"
                },
                expected_result="文档已上传到OSS，返回下载链接",
                error_cases=[
                    {
                        "error": "没有当前文档",
                        "solution": "先创建或打开文档",
                        "prerequisite": "create_document 或 open_document"
                    },
                    {
                        "error": "OSS服务不可用",
                        "solution": "检查OSS配置和网络连接",
                        "parameters": {"custom_filename": "backup_report.docx"}
                    }
                ],
                alternatives=[
                    {
                        "description": "使用默认文件名上传",
                        "tool": "upload_current_document_to_oss",
                        "parameters": {}
                    }
                ]
            )
        ]
        
        self.tool_examples["upload_file_to_oss"] = [
            ToolCallExample(
                example_id="upload_specific_file",
                tool_name="upload_file_to_oss",
                description="上传指定文件到OSS",
                parameters={
                    "file_path": "documents/报告.docx",
                    "custom_filename": "最终报告.docx"
                },
                expected_result="指定文件已上传到OSS，返回下载链接",
                error_cases=[
                    {
                        "error": "文件不存在",
                        "solution": "检查文件路径是否正确",
                        "parameters": {"file_path": "correct/path/report.docx"}
                    },
                    {
                        "error": "文件权限不足",
                        "solution": "检查文件读取权限",
                        "parameters": {"file_path": "accessible/path/report.docx"}
                    }
                ],
                alternatives=[
                    {
                        "description": "使用原文件名上传",
                        "tool": "upload_file_to_oss",
                        "parameters": {"file_path": "documents/报告.docx"}
                    }
                ]
            )
        ]
    
    def _initialize_workflow_examples(self):
        """初始化工作流示例"""
        
        # 创建文档工作流示例
        create_doc_workflow_example = WorkflowExample(
            workflow_id="create_document",
            scenario="创建商务报告文档",
            input_data={
                "filename": "月度销售报告.docx",
                "title": "2024年1月销售报告",
                "page_settings": {
                    "margins": {"top": 2.54, "bottom": 2.54, "left": 3.18, "right": 3.18},
                    "orientation": "portrait"
                }
            },
            step_by_step=[
                {
                    "step": 1,
                    "action": "验证参数",
                    "tool": "validate_document_params",
                    "parameters": {"filename": "月度销售报告.docx"},
                    "expected_result": "参数验证通过"
                },
                {
                    "step": 2,
                    "action": "创建文档",
                    "tool": "create_document",
                    "parameters": {"filename": "月度销售报告.docx"},
                    "expected_result": "文档创建成功"
                },
                {
                    "step": 3,
                    "action": "设置页面",
                    "tool": "set_page_settings",
                    "parameters": {
                        "filename": "月度销售报告.docx",
                        "margins": {"top": 2.54, "bottom": 2.54, "left": 3.18, "right": 3.18}
                    },
                    "expected_result": "页面设置应用成功"
                },
                {
                    "step": 4,
                    "action": "添加标题",
                    "tool": "add_heading",
                    "parameters": {
                        "filename": "月度销售报告.docx",
                        "text": "2024年1月销售报告",
                        "level": 1
                    },
                    "expected_result": "标题添加成功"
                },
                {
                    "step": 5,
                    "action": "保存文档",
                    "tool": "save_document",
                    "parameters": {"filename": "月度销售报告.docx"},
                    "expected_result": "文档保存成功"
                }
            ],
            expected_output="成功创建包含标题和正确页面设置的销售报告文档",
            troubleshooting=[
                {
                    "problem": "文件已存在",
                    "solution": "使用不同的文件名或确认覆盖现有文件",
                    "alternative_parameters": {"filename": "月度销售报告_202401.docx"}
                },
                {
                    "problem": "页面设置失败",
                    "solution": "检查页面设置参数是否有效",
                    "alternative_parameters": {"margins": {"top": 2.0, "bottom": 2.0, "left": 2.0, "right": 2.0}}
                }
            ]
        )
        
        self.workflow_examples["create_document"] = create_doc_workflow_example
        
        # 添加图片工作流示例
        add_image_workflow_example = WorkflowExample(
            workflow_id="add_image_to_document",
            scenario="向文档添加产品图片",
            input_data={
                "filename": "产品手册.docx",
                "image_path": "images/product_photo.jpg",
                "width": 400,
                "alignment": "center"
            },
            step_by_step=[
                {
                    "step": 1,
                    "action": "验证文档",
                    "tool": "validate_document_exists",
                    "parameters": {"filename": "产品手册.docx"},
                    "expected_result": "文档存在且可访问"
                },
                {
                    "step": 2,
                    "action": "验证图片",
                    "tool": "validate_image_file",
                    "parameters": {"image_path": "images/product_photo.jpg"},
                    "expected_result": "图片文件有效"
                },
                {
                    "step": 3,
                    "action": "添加图片",
                    "tool": "add_picture",
                    "parameters": {
                        "filename": "产品手册.docx",
                        "image_path": "images/product_photo.jpg",
                        "width": 400
                    },
                    "expected_result": "图片添加成功"
                },
                {
                    "step": 4,
                    "action": "调整布局",
                    "tool": "adjust_image_layout",
                    "parameters": {
                        "filename": "产品手册.docx",
                        "alignment": "center"
                    },
                    "expected_result": "图片布局调整成功"
                },
                {
                    "step": 5,
                    "action": "保存文档",
                    "tool": "save_document",
                    "parameters": {"filename": "产品手册.docx"},
                    "expected_result": "文档保存成功"
                }
            ],
            expected_output="成功将产品图片添加到文档中，并调整了布局",
            troubleshooting=[
                {
                    "problem": "图片文件不存在",
                    "solution": "检查图片路径是否正确，确保文件存在",
                    "alternative_parameters": {"image_path": "correct/path/product_photo.jpg"}
                },
                {
                    "problem": "图片格式不支持",
                    "solution": "使用支持的图片格式（jpg, png, gif, bmp）",
                    "alternative_parameters": {"image_path": "images/product_photo.png"}
                },
                {
                    "problem": "图片过大",
                    "solution": "调整图片尺寸或使用较小的图片",
                    "alternative_parameters": {"width": 200, "height": 150}
                }
            ]
        )
        
        self.workflow_examples["add_image_to_document"] = add_image_workflow_example
    
    def get_prompt_template(self, template_id: str) -> Optional[AIPromptTemplate]:
        """获取提示词模板"""
        return self.prompt_templates.get(template_id)
    
    def get_tool_examples(self, tool_name: str) -> List[ToolCallExample]:
        """获取工具调用示例"""
        return self.tool_examples.get(tool_name, [])
    
    def get_workflow_example(self, workflow_id: str) -> Optional[WorkflowExample]:
        """获取工作流示例"""
        return self.workflow_examples.get(workflow_id)
    
    def generate_comprehensive_guidance(self, user_intent: str) -> Dict[str, Any]:
        """生成综合指导信息"""
        guidance = {
            "user_intent": user_intent,
            "suggested_approach": "",
            "prompt_templates": [],
            "tool_examples": [],
            "workflow_examples": [],
            "best_practices": [],
            "common_mistakes": [],
            "troubleshooting": []
        }
        
        # 分析用户意图
        intent_lower = user_intent.lower()
        
        # 推荐方法
        if any(keyword in intent_lower for keyword in ["创建", "新建", "制作"]):
            guidance["suggested_approach"] = "使用工作流方式创建文档，确保步骤完整"
            guidance["prompt_templates"].append(self.get_prompt_template("create_document"))
        elif any(keyword in intent_lower for keyword in ["图片", "image", "照片"]):
            guidance["suggested_approach"] = "使用图片处理工作流，注意验证文件格式"
            guidance["prompt_templates"].append(self.get_prompt_template("image_processing"))
        elif any(keyword in intent_lower for keyword in ["表格", "table", "数据"]):
            guidance["suggested_approach"] = "使用表格操作工作流，注意数据格式"
            guidance["prompt_templates"].append(self.get_prompt_template("table_operation"))
        
        # 添加相关工具示例
        if "创建" in intent_lower:
            guidance["tool_examples"].extend(self.get_tool_examples("create_document"))
            guidance["tool_examples"].extend(self.get_tool_examples("add_paragraph"))
        if "图片" in intent_lower:
            guidance["tool_examples"].extend(self.get_tool_examples("add_picture"))
        if "表格" in intent_lower:
            guidance["tool_examples"].extend(self.get_tool_examples("add_table"))
        
        # 添加工作流示例
        if "创建" in intent_lower:
            guidance["workflow_examples"].append(self.get_workflow_example("create_document"))
        if "图片" in intent_lower:
            guidance["workflow_examples"].append(self.get_workflow_example("add_image_to_document"))
        
        # 收集最佳实践和常见错误
        for template in guidance["prompt_templates"]:
            if template:
                guidance["best_practices"].extend(template.best_practices)
                guidance["common_mistakes"].extend(template.common_mistakes)
        
        # 收集故障排除信息
        for workflow_example in guidance["workflow_examples"]:
            if workflow_example:
                guidance["troubleshooting"].extend(workflow_example.troubleshooting)
        
        return guidance
    
    def create_custom_prompt(self, scenario: str, requirements: Dict[str, Any]) -> str:
        """创建自定义提示词"""
        base_template = """你是一个专业的Word文档处理助手。请根据以下场景和要求，提供准确、高效的工具调用建议。

场景：{scenario}

具体要求：
{requirements}

请按照以下原则执行：
1. 验证所有参数的有效性
2. 按照正确的顺序调用工具
3. 提供清晰的错误处理
4. 使用中文进行交互
5. 提供详细的执行步骤

工具调用示例格式：
```json
{{
    "tool_name": "工具名称",
    "parameters": {{
        "参数名": "参数值"
    }},
    "expected_result": "预期结果"
}}
```

请提供完整的执行方案。"""
        
        requirements_text = "\n".join([f"- {key}: {value}" for key, value in requirements.items()])
        
        return base_template.format(
            scenario=scenario,
            requirements=requirements_text
        )
    
    def validate_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """验证工具调用参数"""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        # 获取工具示例
        examples = self.get_tool_examples(tool_name)
        if not examples:
            validation_result["warnings"].append(f"没有找到工具 {tool_name} 的示例")
            return validation_result
        
        # 使用第一个示例作为参考
        example = examples[0]
        
        # 检查必需参数
        for param_name in example.parameters.keys():
            if param_name not in parameters:
                validation_result["errors"].append(f"缺少必需参数: {param_name}")
                validation_result["is_valid"] = False
        
        # 检查参数值
        for param_name, param_value in parameters.items():
            if param_name in example.parameters:
                expected_type = type(example.parameters[param_name])
                if not isinstance(param_value, expected_type):
                    validation_result["warnings"].append(
                        f"参数 {param_name} 类型不匹配，期望 {expected_type.__name__}，实际 {type(param_value).__name__}"
                    )
        
        # 提供建议
        if not validation_result["is_valid"]:
            validation_result["suggestions"].append("请参考以下正确示例：")
            validation_result["suggestions"].append(json.dumps(example.parameters, ensure_ascii=False, indent=2))
        
        return validation_result
    
    def get_quick_reference(self) -> Dict[str, Any]:
        """获取快速参考指南"""
        return {
            "common_tools": {
                "create_document": {
                    "description": "创建新文档",
                    "required_params": ["filename"],
                    "example": {"filename": "新文档.docx"}
                },
                "add_paragraph": {
                    "description": "添加段落",
                    "required_params": ["filename", "text"],
                    "example": {"filename": "文档.docx", "text": "段落内容"}
                },
                "add_picture": {
                    "description": "添加图片",
                    "required_params": ["filename", "image_path"],
                    "example": {"filename": "文档.docx", "image_path": "images/photo.jpg"}
                },
                "add_table": {
                    "description": "添加表格",
                    "required_params": ["filename", "rows", "cols"],
                    "example": {"filename": "文档.docx", "rows": 3, "cols": 3}
                }
            },
            "workflow_sequences": {
                "create_document": ["validate_params", "create_document", "add_content", "save_document"],
                "add_image": ["validate_document", "validate_image", "add_picture", "save_document"],
                "create_table": ["validate_document", "validate_data", "add_table", "format_table", "save_document"]
            },
            "error_handling": {
                "file_not_found": "检查文件路径是否正确",
                "invalid_parameters": "验证参数类型和值",
                "permission_denied": "检查文件权限",
                "format_not_supported": "使用支持的格式"
            }
        }
