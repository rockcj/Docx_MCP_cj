#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced DOCX MCP Core Module
增强版DOCX MCP核心模块

提供完整的Word文档处理能力，包括：
- 文档生命周期管理
- 内容编辑和格式化
- 表格操作
- 图片处理
- 字体管理
- 状态持久化
"""

from .enhanced_docx_processor import EnhancedDocxProcessor
from .state_manager import StateManager
from .enhanced_state_manager import EnhancedStateManager
from .image_processor import ImageProcessor
from .font_processor import FontProcessor
from .oss_processor import OSSProcessor
from .workflow_engine import WorkflowEngine
from .smart_suggestion_engine import SmartSuggestionEngine
from .ai_guidance_enhancer import AIGuidanceEnhancer
from .json_validation_engine import JSONValidationEngine
from .ai_interface import AISmartInterface
from .models import (
    DocumentPatch,
    TableOperation,
    TableOperationType,
    CellAlignment,
    BorderStyle,
    CellFormat,
    TableFormat,
)

__version__ = "2.0.0"
__author__ = "Enhanced DOCX MCP Team"
__email__ = "support@docx-mcp.com"
__description__ = "增强版DOCX MCP处理器 - 完整的Word文档处理工具"

__all__ = [
    "EnhancedDocxProcessor",
    "StateManager",
    "EnhancedStateManager", 
    "ImageProcessor",
    "FontProcessor",
    "OSSProcessor",
    "WorkflowEngine",
    "SmartSuggestionEngine",
    "AIGuidanceEnhancer",
    "JSONValidationEngine",
    "AISmartInterface",
    "DocumentPatch",
    "TableOperation",
    "TableOperationType",
    "CellAlignment",
    "BorderStyle",
    "CellFormat",
    "TableFormat",
]

# 版本信息
VERSION_INFO = {
    "version": __version__,
    "author": __author__,
    "email": __email__,
    "description": __description__,
    "features": [
        "文档生命周期管理",
        "内容编辑和格式化", 
        "表格操作",
        "图片处理",
        "字体管理",
        "状态持久化",
        "MCP协议支持",
        "工作流引擎",
        "智能建议系统",
        "AI指导增强",
        "JSON数据验证",
        "OSS云存储集成",
        "异步处理",
        "错误处理",
        "日志记录"
    ]
}

def get_version_info():
    """获取版本信息"""
    return VERSION_INFO

def print_version_info():
    """打印版本信息"""
    print(f"Enhanced DOCX MCP v{__version__}")
    print(f"Author: {__author__}")
    print(f"Email: {__email__}")
    print(f"Description: {__description__}")
    print("\nFeatures:")
    for feature in VERSION_INFO["features"]:
        print(f"  - {feature}")
