#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSON验证引擎
提供完整的JSON数据格式验证、示例模板和错误处理
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# ==================== 数据结构定义 ====================

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    corrected_data: Optional[Dict[str, Any]] = None

@dataclass
class JSONSchema:
    """JSON模式定义"""
    schema_id: str
    schema_name: str
    description: str
    schema: Dict[str, Any]
    examples: List[Dict[str, Any]] = field(default_factory=list)
    common_errors: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ValidationRule:
    """验证规则"""
    rule_id: str
    rule_name: str
    description: str
    validator: callable
    error_message: str
    fix_suggestion: Optional[str] = None

# ==================== JSON验证引擎 ====================

class JSONValidationEngine:
    """JSON验证引擎 - 提供完整的JSON数据格式验证和示例"""
    
    def __init__(self):
        self.schemas: Dict[str, JSONSchema] = {}
        self.validation_rules: Dict[str, ValidationRule] = {}
        
        # 初始化预定义模式
        self._initialize_predefined_schemas()
        self._initialize_validation_rules()
        
        logger.info("JSON验证引擎初始化完成")
    
    def _initialize_predefined_schemas(self):
        """初始化预定义的JSON模式"""
        
        # 1. 创建文档模式
        create_document_schema = JSONSchema(
            schema_id="create_document",
            schema_name="创建文档",
            description="创建Word文档的JSON数据格式",
            schema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "文档文件名",
                        "pattern": r"^[^<>:\"/\\|?*]+\.docx$",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "title": {
                        "type": "string",
                        "description": "文档标题（可选）",
                        "maxLength": 200
                    },
                    "page_settings": {
                        "type": "object",
                        "description": "页面设置（可选）",
                        "properties": {
                            "margins": {
                                "type": "object",
                                "properties": {
                                    "top": {"type": "number", "minimum": 0.5, "maximum": 5.0},
                                    "bottom": {"type": "number", "minimum": 0.5, "maximum": 5.0},
                                    "left": {"type": "number", "minimum": 0.5, "maximum": 5.0},
                                    "right": {"type": "number", "minimum": 0.5, "maximum": 5.0}
                                }
                            },
                            "orientation": {
                                "type": "string",
                                "enum": ["portrait", "landscape"],
                                "description": "页面方向"
                            },
                            "size": {
                                "type": "string",
                                "enum": ["A4", "A3", "Letter", "Legal"],
                                "description": "页面大小"
                            }
                        }
                    }
                },
                "required": ["filename"],
                "additionalProperties": False
            },
            examples=[
                {
                    "description": "基本文档创建",
                    "data": {
                        "filename": "新文档.docx"
                    }
                },
                {
                    "description": "带标题的文档创建",
                    "data": {
                        "filename": "报告.docx",
                        "title": "月度销售报告"
                    }
                },
                {
                    "description": "完整配置的文档创建",
                    "data": {
                        "filename": "正式报告.docx",
                        "title": "2024年度总结报告",
                        "page_settings": {
                            "margins": {
                                "top": 2.54,
                                "bottom": 2.54,
                                "left": 3.18,
                                "right": 3.18
                            },
                            "orientation": "portrait",
                            "size": "A4"
                        }
                    }
                }
            ],
            common_errors=[
                {
                    "error": "缺少filename参数",
                    "example": {"title": "报告标题"},
                    "fix": "添加必需的filename参数",
                    "corrected": {"filename": "报告.docx", "title": "报告标题"}
                },
                {
                    "error": "文件名格式不正确",
                    "example": {"filename": "报告.doc"},
                    "fix": "使用.docx扩展名",
                    "corrected": {"filename": "报告.docx"}
                },
                {
                    "error": "页面边距值超出范围",
                    "example": {"filename": "报告.docx", "page_settings": {"margins": {"top": 10}}},
                    "fix": "边距值应在0.5-5.0之间",
                    "corrected": {"filename": "报告.docx", "page_settings": {"margins": {"top": 2.54}}}
                }
            ]
        )
        
        self.schemas["create_document"] = create_document_schema
        
        # 2. 添加段落模式
        add_paragraph_schema = JSONSchema(
            schema_id="add_paragraph",
            schema_name="添加段落",
            description="向文档添加段落的JSON数据格式",
            schema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "目标文档文件名",
                        "pattern": r"^[^<>:\"/\\|?*]+\.docx$"
                    },
                    "text": {
                        "type": "string",
                        "description": "段落文本内容",
                        "minLength": 1,
                        "maxLength": 10000
                    },
                    "style": {
                        "type": "string",
                        "description": "段落样式（可选）",
                        "enum": ["normal", "heading1", "heading2", "heading3", "emphasis", "quote"]
                    },
                    "alignment": {
                        "type": "string",
                        "description": "文本对齐方式（可选）",
                        "enum": ["left", "center", "right", "justify"]
                    },
                    "position": {
                        "type": "string",
                        "description": "插入位置（可选）",
                        "enum": ["beginning", "end", "after_heading"]
                    }
                },
                "required": ["filename", "text"],
                "additionalProperties": False
            },
            examples=[
                {
                    "description": "基本段落添加",
                    "data": {
                        "filename": "文档.docx",
                        "text": "这是一个示例段落。"
                    }
                },
                {
                    "description": "带样式的段落",
                    "data": {
                        "filename": "文档.docx",
                        "text": "重要内容",
                        "style": "emphasis",
                        "alignment": "center"
                    }
                },
                {
                    "description": "标题段落",
                    "data": {
                        "filename": "文档.docx",
                        "text": "第一章 引言",
                        "style": "heading1",
                        "alignment": "left"
                    }
                }
            ],
            common_errors=[
                {
                    "error": "文本内容为空",
                    "example": {"filename": "文档.docx", "text": ""},
                    "fix": "提供有效的文本内容",
                    "corrected": {"filename": "文档.docx", "text": "段落内容"}
                },
                {
                    "error": "文本内容过长",
                    "example": {"filename": "文档.docx", "text": "很长的文本..."},
                    "fix": "文本长度不应超过10000字符",
                    "corrected": {"filename": "文档.docx", "text": "适当长度的文本"}
                }
            ]
        )
        
        self.schemas["add_paragraph"] = add_paragraph_schema
        
        # 3. 添加图片模式
        add_picture_schema = JSONSchema(
            schema_id="add_picture",
            schema_name="添加图片",
            description="向文档添加图片的JSON数据格式",
            schema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "目标文档文件名",
                        "pattern": r"^[^<>:\"/\\|?*]+\.docx$"
                    },
                    "image_path": {
                        "type": "string",
                        "description": "图片文件路径",
                        "pattern": r"^.+\.(jpg|jpeg|png|gif|bmp|tiff)$",
                        "minLength": 1
                    },
                    "width": {
                        "type": "number",
                        "description": "图片宽度（像素，可选）",
                        "minimum": 50,
                        "maximum": 2000
                    },
                    "height": {
                        "type": "number",
                        "description": "图片高度（像素，可选）",
                        "minimum": 50,
                        "maximum": 2000
                    },
                    "alignment": {
                        "type": "string",
                        "description": "图片对齐方式（可选）",
                        "enum": ["left", "center", "right"]
                    },
                    "caption": {
                        "type": "string",
                        "description": "图片标题（可选）",
                        "maxLength": 200
                    }
                },
                "required": ["filename", "image_path"],
                "additionalProperties": False
            },
            examples=[
                {
                    "description": "基本图片添加",
                    "data": {
                        "filename": "文档.docx",
                        "image_path": "images/photo.jpg"
                    }
                },
                {
                    "description": "带尺寸控制的图片",
                    "data": {
                        "filename": "文档.docx",
                        "image_path": "images/photo.jpg",
                        "width": 400,
                        "height": 300
                    }
                },
                {
                    "description": "带标题的图片",
                    "data": {
                        "filename": "文档.docx",
                        "image_path": "images/chart.png",
                        "width": 500,
                        "alignment": "center",
                        "caption": "图1：销售趋势图"
                    }
                }
            ],
            common_errors=[
                {
                    "error": "图片格式不支持",
                    "example": {"filename": "文档.docx", "image_path": "images/photo.pdf"},
                    "fix": "使用支持的图片格式（jpg, png, gif, bmp, tiff）",
                    "corrected": {"filename": "文档.docx", "image_path": "images/photo.jpg"}
                },
                {
                    "error": "图片尺寸过大",
                    "example": {"filename": "文档.docx", "image_path": "images/photo.jpg", "width": 5000},
                    "fix": "图片尺寸应在50-2000像素之间",
                    "corrected": {"filename": "文档.docx", "image_path": "images/photo.jpg", "width": 500}
                }
            ]
        )
        
        self.schemas["add_picture"] = add_picture_schema
        
        # 4. 添加表格模式
        add_table_schema = JSONSchema(
            schema_id="add_table",
            schema_name="添加表格",
            description="向文档添加表格的JSON数据格式",
            schema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "目标文档文件名",
                        "pattern": r"^[^<>:\"/\\|?*]+\.docx$"
                    },
                    "rows": {
                        "type": "integer",
                        "description": "表格行数",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "cols": {
                        "type": "integer",
                        "description": "表格列数",
                        "minimum": 1,
                        "maximum": 20
                    },
                    "data": {
                        "type": "array",
                        "description": "表格数据（可选）",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "has_header": {
                        "type": "boolean",
                        "description": "是否有表头"
                    },
                    "table_style": {
                        "type": "object",
                        "description": "表格样式（可选）",
                        "properties": {
                            "border_style": {
                                "type": "string",
                                "enum": ["solid", "dashed", "dotted", "none"]
                            },
                            "header_color": {
                                "type": "string",
                                "pattern": r"^#[0-9A-Fa-f]{6}$"
                            },
                            "alternating_rows": {
                                "type": "boolean"
                            }
                        }
                    }
                },
                "required": ["filename", "rows", "cols"],
                "additionalProperties": False
            },
            examples=[
                {
                    "description": "基本表格创建",
                    "data": {
                        "filename": "文档.docx",
                        "rows": 3,
                        "cols": 3
                    }
                },
                {
                    "description": "带数据的表格",
                    "data": {
                        "filename": "文档.docx",
                        "rows": 3,
                        "cols": 3,
                        "data": [
                            ["姓名", "部门", "职位"],
                            ["张三", "技术部", "工程师"],
                            ["李四", "销售部", "经理"]
                        ],
                        "has_header": True
                    }
                },
                {
                    "description": "带样式的表格",
                    "data": {
                        "filename": "文档.docx",
                        "rows": 4,
                        "cols": 4,
                        "has_header": True,
                        "table_style": {
                            "border_style": "solid",
                            "header_color": "#4472C4",
                            "alternating_rows": True
                        }
                    }
                }
            ],
            common_errors=[
                {
                    "error": "行数或列数为0",
                    "example": {"filename": "文档.docx", "rows": 0, "cols": 3},
                    "fix": "行数和列数必须大于0",
                    "corrected": {"filename": "文档.docx", "rows": 1, "cols": 3}
                },
                {
                    "error": "数据行数与指定行数不匹配",
                    "example": {"filename": "文档.docx", "rows": 3, "cols": 2, "data": [["A", "B"]]},
                    "fix": "数据行数应与指定的行数一致",
                    "corrected": {"filename": "文档.docx", "rows": 3, "cols": 2, "data": [["A", "B"], ["C", "D"], ["E", "F"]]}
                }
            ]
        )
        
        self.schemas["add_table"] = add_table_schema
        
        # 5. 工作流执行模式
        workflow_execution_schema = JSONSchema(
            schema_id="workflow_execution",
            schema_name="工作流执行",
            description="执行工作流的JSON数据格式",
            schema={
                "type": "object",
                "properties": {
                    "workflow_id": {
                        "type": "string",
                        "description": "工作流ID",
                        "enum": ["create_document", "edit_document", "add_image_to_document", "create_table", "apply_template"]
                    },
                    "parameters": {
                        "type": "object",
                        "description": "工作流参数",
                        "additionalProperties": True
                    },
                    "execution_options": {
                        "type": "object",
                        "description": "执行选项（可选）",
                        "properties": {
                            "timeout": {
                                "type": "integer",
                                "minimum": 30,
                                "maximum": 3600
                            },
                            "retry_count": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 5
                            },
                            "continue_on_error": {
                                "type": "boolean"
                            }
                        }
                    }
                },
                "required": ["workflow_id", "parameters"],
                "additionalProperties": False
            },
            examples=[
                {
                    "description": "基本工作流执行",
                    "data": {
                        "workflow_id": "create_document",
                        "parameters": {
                            "filename": "新文档.docx"
                        }
                    }
                },
                {
                    "description": "带执行选项的工作流",
                    "data": {
                        "workflow_id": "add_image_to_document",
                        "parameters": {
                            "filename": "文档.docx",
                            "image_path": "images/photo.jpg"
                        },
                        "execution_options": {
                            "timeout": 300,
                            "retry_count": 2,
                            "continue_on_error": False
                        }
                    }
                }
            ],
            common_errors=[
                {
                    "error": "工作流ID不存在",
                    "example": {"workflow_id": "invalid_workflow", "parameters": {}},
                    "fix": "使用有效的工作流ID",
                    "corrected": {"workflow_id": "create_document", "parameters": {"filename": "文档.docx"}}
                }
            ]
        )
        
        self.schemas["workflow_execution"] = workflow_execution_schema
        
        # 6. OSS上传模式
        oss_upload_schema = JSONSchema(
            schema_id="oss_upload",
            schema_name="OSS上传",
            description="上传文档到OSS云存储的JSON数据格式",
            schema={
                "type": "object",
                "properties": {
                    "custom_filename": {
                        "type": "string",
                        "description": "OSS上的自定义文件名（可选）",
                        "pattern": r"^[^<>:\"/\\|?*]+\.docx$",
                        "maxLength": 255
                    },
                    "document_path": {
                        "type": "string",
                        "description": "要上传的文档路径（可选，默认使用当前文档）",
                        "pattern": r"^.+\.docx$"
                    },
                    "auto_upload": {
                        "type": "boolean",
                        "description": "是否自动上传（默认true）",
                        "default": True
                    }
                },
                "additionalProperties": False,
                "anyOf": [
                    {"required": ["auto_upload"]},
                    {"required": ["custom_filename"]},
                    {"required": ["document_path"]}
                ]
            },
            examples=[
                {
                    "description": "基本OSS上传",
                    "data": {
                        "auto_upload": True
                    }
                },
                {
                    "description": "带自定义文件名的上传",
                    "data": {
                        "custom_filename": "月度报告_202401.docx",
                        "auto_upload": True
                    }
                },
                {
                    "description": "上传指定文档",
                    "data": {
                        "document_path": "documents/报告.docx",
                        "custom_filename": "最终报告.docx",
                        "auto_upload": True
                    }
                }
            ],
            common_errors=[
                {
                    "error": "文件名格式不正确",
                    "example": {"custom_filename": "报告.doc"},
                    "fix": "使用.docx扩展名",
                    "corrected": {"custom_filename": "报告.docx"}
                },
                {
                    "error": "文档路径不存在",
                    "example": {"document_path": "不存在的路径.docx"},
                    "fix": "确保文档路径正确且文件存在",
                    "corrected": {"document_path": "documents/报告.docx"}
                }
            ]
        )
        
        self.schemas["oss_upload"] = oss_upload_schema
    
    def _initialize_validation_rules(self):
        """初始化验证规则"""
        
        # 文件名验证规则
        self.validation_rules["filename_format"] = ValidationRule(
            rule_id="filename_format",
            rule_name="文件名格式验证",
            description="验证文件名格式是否正确",
            validator=self._validate_filename_format,
            error_message="文件名格式不正确",
            fix_suggestion="文件名应不包含特殊字符，并以.docx结尾"
        )
        
        # 图片路径验证规则
        self.validation_rules["image_path"] = ValidationRule(
            rule_id="image_path",
            rule_name="图片路径验证",
            description="验证图片路径和格式",
            validator=self._validate_image_path,
            error_message="图片路径或格式不正确",
            fix_suggestion="使用支持的图片格式（jpg, png, gif, bmp, tiff）"
        )
        
        # 数值范围验证规则
        self.validation_rules["numeric_range"] = ValidationRule(
            rule_id="numeric_range",
            rule_name="数值范围验证",
            description="验证数值是否在有效范围内",
            validator=self._validate_numeric_range,
            error_message="数值超出有效范围",
            fix_suggestion="调整数值到有效范围内"
        )
    
    def validate_json(self, schema_id: str, data: Dict[str, Any]) -> ValidationResult:
        """验证JSON数据"""
        if schema_id not in self.schemas:
            return ValidationResult(
                is_valid=False,
                errors=[f"模式不存在: {schema_id}"]
            )
        
        schema = self.schemas[schema_id]
        result = ValidationResult(is_valid=True)
        
        # 基本结构验证
        if not isinstance(data, dict):
            result.is_valid = False
            result.errors.append("数据必须是JSON对象")
            return result
        
        # 必需字段验证
        for required_field in schema.schema.get("required", []):
            if required_field not in data:
                result.is_valid = False
                result.errors.append(f"缺少必需字段: {required_field}")
        
        # 字段类型验证
        properties = schema.schema.get("properties", {})
        for field_name, field_value in data.items():
            if field_name in properties:
                field_schema = properties[field_name]
                field_result = self._validate_field(field_name, field_value, field_schema)
                if not field_result["is_valid"]:
                    result.is_valid = False
                    result.errors.extend(field_result["errors"])
                result.warnings.extend(field_result["warnings"])
        
        # 自定义规则验证（仅对相关模式应用）
        if schema_id in ["create_document", "add_picture"]:
            for rule_id, rule in self.validation_rules.items():
                if not rule.validator(data):
                    result.is_valid = False
                    result.errors.append(rule.error_message)
                    if rule.fix_suggestion:
                        result.suggestions.append(rule.fix_suggestion)
        
        # 如果验证失败，尝试提供修正建议
        if not result.is_valid:
            result.corrected_data = self._suggest_corrections(schema_id, data)
        
        return result
    
    def _validate_field(self, field_name: str, field_value: Any, field_schema: Dict[str, Any]) -> Dict[str, Any]:
        """验证单个字段"""
        result = {"is_valid": True, "errors": [], "warnings": []}
        
        # 类型验证
        expected_type = field_schema.get("type")
        if expected_type and not self._check_type(field_value, expected_type):
            result["is_valid"] = False
            result["errors"].append(f"字段 {field_name} 类型错误，期望 {expected_type}，实际 {type(field_value).__name__}")
        
        # 字符串验证
        if expected_type == "string":
            string_result = self._validate_string(field_value, field_schema)
            if not string_result["is_valid"]:
                result["is_valid"] = False
                result["errors"].extend(string_result["errors"])
            result["warnings"].extend(string_result["warnings"])
        
        # 数值验证
        elif expected_type in ["integer", "number"]:
            numeric_result = self._validate_numeric(field_value, field_schema)
            if not numeric_result["is_valid"]:
                result["is_valid"] = False
                result["errors"].extend(numeric_result["errors"])
            result["warnings"].extend(numeric_result["warnings"])
        
        # 枚举验证
        if "enum" in field_schema:
            if field_value not in field_schema["enum"]:
                result["is_valid"] = False
                result["errors"].append(f"字段 {field_name} 值不在允许的枚举值中: {field_schema['enum']}")
        
        return result
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """检查值类型"""
        type_mapping = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type:
            return isinstance(value, expected_python_type)
        
        return True
    
    def _validate_string(self, value: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
        """验证字符串"""
        result = {"is_valid": True, "errors": [], "warnings": []}
        
        if not isinstance(value, str):
            result["is_valid"] = False
            result["errors"].append("值必须是字符串")
            return result
        
        # 长度验证
        if "minLength" in schema and len(value) < schema["minLength"]:
            result["is_valid"] = False
            result["errors"].append(f"字符串长度不能少于 {schema['minLength']} 个字符")
        
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            result["is_valid"] = False
            result["errors"].append(f"字符串长度不能超过 {schema['maxLength']} 个字符")
        
        # 模式验证
        if "pattern" in schema:
            if not re.match(schema["pattern"], value):
                result["is_valid"] = False
                result["errors"].append(f"字符串格式不符合要求: {schema['pattern']}")
        
        return result
    
    def _validate_numeric(self, value: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
        """验证数值"""
        result = {"is_valid": True, "errors": [], "warnings": []}
        
        if not isinstance(value, (int, float)):
            result["is_valid"] = False
            result["errors"].append("值必须是数值")
            return result
        
        # 范围验证
        if "minimum" in schema and value < schema["minimum"]:
            result["is_valid"] = False
            result["errors"].append(f"数值不能小于 {schema['minimum']}")
        
        if "maximum" in schema and value > schema["maximum"]:
            result["is_valid"] = False
            result["errors"].append(f"数值不能大于 {schema['maximum']}")
        
        return result
    
    def _validate_filename_format(self, data: Dict[str, Any]) -> bool:
        """验证文件名格式"""
        filename = data.get("filename", "")
        if not filename:
            return False
        
        # 检查是否以.docx结尾
        if not filename.endswith(".docx"):
            return False
        
        # 检查是否包含非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        if re.search(illegal_chars, filename):
            return False
        
        return True
    
    def _validate_image_path(self, data: Dict[str, Any]) -> bool:
        """验证图片路径"""
        image_path = data.get("image_path", "")
        if not image_path:
            return False
        
        # 检查文件扩展名
        supported_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
        if not any(image_path.lower().endswith(ext) for ext in supported_extensions):
            return False
        
        return True
    
    def _validate_numeric_range(self, data: Dict[str, Any]) -> bool:
        """验证数值范围"""
        # 这里可以添加特定的数值范围验证逻辑
        return True
    
    def _suggest_corrections(self, schema_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """建议修正"""
        corrected_data = data.copy()
        schema = self.schemas[schema_id]
        
        # 基于常见错误进行修正
        common_errors = schema.common_errors
        for error_info in common_errors:
            # 这里可以实现自动修正逻辑
            pass
        
        return corrected_data
    
    def get_schema(self, schema_id: str) -> Optional[JSONSchema]:
        """获取模式"""
        return self.schemas.get(schema_id)
    
    def get_schema_examples(self, schema_id: str) -> List[Dict[str, Any]]:
        """获取模式示例"""
        schema = self.schemas.get(schema_id)
        if schema:
            return schema.examples
        return []
    
    def get_common_errors(self, schema_id: str) -> List[Dict[str, Any]]:
        """获取常见错误"""
        schema = self.schemas.get(schema_id)
        if schema:
            return schema.common_errors
        return []
    
    def generate_example_json(self, schema_id: str, example_index: int = 0) -> Optional[Dict[str, Any]]:
        """生成示例JSON"""
        examples = self.get_schema_examples(schema_id)
        if examples and 0 <= example_index < len(examples):
            return examples[example_index]["data"]
        return None
    
    def format_validation_result(self, result: ValidationResult) -> str:
        """格式化验证结果"""
        output = []
        
        if result.is_valid:
            output.append("✅ JSON数据验证通过")
        else:
            output.append("❌ JSON数据验证失败")
        
        if result.errors:
            output.append("\n错误信息:")
            for error in result.errors:
                output.append(f"  • {error}")
        
        if result.warnings:
            output.append("\n警告信息:")
            for warning in result.warnings:
                output.append(f"  ⚠️ {warning}")
        
        if result.suggestions:
            output.append("\n建议:")
            for suggestion in result.suggestions:
                output.append(f"  💡 {suggestion}")
        
        if result.corrected_data:
            output.append("\n修正后的数据:")
            output.append(json.dumps(result.corrected_data, ensure_ascii=False, indent=2))
        
        return "\n".join(output)
    
    def create_custom_schema(self, schema_id: str, schema_definition: Dict[str, Any]) -> bool:
        """创建自定义模式"""
        try:
            schema = JSONSchema(
                schema_id=schema_id,
                schema_name=schema_definition.get("name", schema_id),
                description=schema_definition.get("description", ""),
                schema=schema_definition.get("schema", {}),
                examples=schema_definition.get("examples", []),
                common_errors=schema_definition.get("common_errors", [])
            )
            
            self.schemas[schema_id] = schema
            logger.info(f"创建自定义模式: {schema_id}")
            return True
            
        except Exception as e:
            logger.error(f"创建自定义模式失败: {e}")
            return False
