#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能状态机模块
提供细化的状态管理和智能操作控制
"""

import os
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# ==================== 状态定义 ====================

class GlobalDocumentState(Enum):
    """全局文档状态 - 最高层级"""
    NO_DOCUMENT = "no_document"
    DOCUMENT_LOADING = "document_loading"
    DOCUMENT_READY = "document_ready"
    DOCUMENT_EDITING = "document_editing"
    DOCUMENT_SAVING = "document_saving"
    DOCUMENT_ERROR = "document_error"
    DOCUMENT_CLOSED = "document_closed"

class ContentEditingState(Enum):
    """内容编辑状态"""
    IDLE = "idle"
    ADDING_PARAGRAPH = "adding_paragraph"
    ADDING_HEADING = "adding_heading"
    DELETING_CONTENT = "deleting_content"
    FORMATTING_TEXT = "formatting_text"
    SEARCHING_TEXT = "searching_text"
    REPLACING_TEXT = "replacing_text"

class TableOperationState(Enum):
    """表格操作状态"""
    IDLE = "idle"
    CREATING_TABLE = "creating_table"
    ADDING_ROW = "adding_row"
    ADDING_COLUMN = "adding_column"
    DELETING_ROW = "deleting_row"
    DELETING_COLUMN = "deleting_column"
    EDITING_CELL = "editing_cell"
    MERGING_CELLS = "merging_cells"
    FORMATTING_TABLE = "formatting_table"

class ImageProcessingState(Enum):
    """图片处理状态"""
    IDLE = "idle"
    ADDING_IMAGE = "adding_image"
    RESIZING_IMAGE = "resizing_image"
    DELETING_IMAGE = "deleting_image"
    EXTRACTING_IMAGE = "extracting_image"
    MOVING_IMAGE = "moving_image"
    COPYING_IMAGE = "copying_image"
    LISTING_IMAGES = "listing_images"

class FontProcessingState(Enum):
    """字体处理状态"""
    IDLE = "idle"
    SETTING_PARAGRAPH_FONT = "setting_paragraph_font"
    SETTING_TEXT_RANGE_FONT = "setting_text_range_font"
    BATCH_FORMATTING = "batch_formatting"
    GETTING_FONT_INFO = "getting_font_info"

class CloudStorageState(Enum):
    """云存储状态"""
    IDLE = "idle"
    UPLOADING_DOCUMENT = "uploading_document"
    DOWNLOADING_FILE = "downloading_file"
    LISTING_FILES = "listing_files"
    DELETING_FILE = "deleting_file"
    PROCESSING_URL = "processing_url"

class TemplateState(Enum):
    """模板相关状态"""
    IDLE = "idle"
    TEMPLATE_SELECTED = "template_selected"
    TEMPLATE_DATA_FILLING = "template_data_filling"
    TEMPLATE_RENDERING = "template_rendering"
    TEMPLATE_MODIFYING = "template_modifying"
    TEMPLATE_COMPLETED = "template_completed"

class OperationContext(Enum):
    """操作上下文状态"""
    # 表格操作上下文
    TABLE_INDEX_SELECTED = "table_index_selected"
    ROW_INDEX_SELECTED = "row_index_selected"
    COLUMN_INDEX_SELECTED = "column_index_selected"
    CELL_POSITION_SELECTED = "cell_position_selected"
    
    # 图片操作上下文
    IMAGE_INDEX_SELECTED = "image_index_selected"
    IMAGE_PATH_PROVIDED = "image_path_provided"
    IMAGE_DIMENSIONS_SET = "image_dimensions_set"
    
    # 文本操作上下文
    PARAGRAPH_INDEX_SELECTED = "paragraph_index_selected"
    TEXT_RANGE_SELECTED = "text_range_selected"
    SEARCH_KEYWORD_SET = "search_keyword_set"
    
    # 格式化上下文
    FONT_STYLE_SELECTED = "font_style_selected"
    ALIGNMENT_SET = "alignment_set"
    COLOR_SCHEME_SET = "color_scheme_set"

# ==================== 数据结构 ====================

@dataclass
class OperationRecord:
    """操作记录"""
    operation: str
    timestamp: datetime
    parameters: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

@dataclass
class StateTransition:
    """状态转换记录"""
    from_state: str
    to_state: str
    operation: str
    timestamp: datetime
    success: bool

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    error_messages: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

# ==================== 状态转换规则 ====================

class StateTransitionRules:
    """状态转换规则"""
    
    # 全局状态转换规则
    GLOBAL_TRANSITIONS = {
        GlobalDocumentState.NO_DOCUMENT: [
            GlobalDocumentState.DOCUMENT_LOADING
        ],
        GlobalDocumentState.DOCUMENT_LOADING: [
            GlobalDocumentState.DOCUMENT_READY,
            GlobalDocumentState.DOCUMENT_ERROR
        ],
        GlobalDocumentState.DOCUMENT_READY: [
            GlobalDocumentState.DOCUMENT_EDITING,
            GlobalDocumentState.DOCUMENT_CLOSED
        ],
        GlobalDocumentState.DOCUMENT_EDITING: [
            GlobalDocumentState.DOCUMENT_SAVING,
            GlobalDocumentState.DOCUMENT_READY,
            GlobalDocumentState.DOCUMENT_ERROR
        ],
        GlobalDocumentState.DOCUMENT_SAVING: [
            GlobalDocumentState.DOCUMENT_READY,
            GlobalDocumentState.DOCUMENT_ERROR
        ],
        GlobalDocumentState.DOCUMENT_ERROR: [
            GlobalDocumentState.DOCUMENT_READY,
            GlobalDocumentState.NO_DOCUMENT
        ]
    }
    
    # 功能域状态转换规则
    CONTENT_EDITING_TRANSITIONS = {
        ContentEditingState.IDLE: [
            ContentEditingState.ADDING_PARAGRAPH,
            ContentEditingState.ADDING_HEADING,
            ContentEditingState.SEARCHING_TEXT,
            ContentEditingState.FORMATTING_TEXT
        ],
        ContentEditingState.ADDING_PARAGRAPH: [
            ContentEditingState.FORMATTING_TEXT,
            ContentEditingState.IDLE
        ],
        ContentEditingState.ADDING_HEADING: [
            ContentEditingState.IDLE
        ],
        ContentEditingState.SEARCHING_TEXT: [
            ContentEditingState.REPLACING_TEXT,
            ContentEditingState.IDLE
        ],
        ContentEditingState.REPLACING_TEXT: [
            ContentEditingState.IDLE
        ]
    }
    
    TABLE_OPERATION_TRANSITIONS = {
        TableOperationState.IDLE: [
            TableOperationState.CREATING_TABLE,
            TableOperationState.ADDING_ROW,
            TableOperationState.ADDING_COLUMN,
            TableOperationState.EDITING_CELL
        ],
        TableOperationState.CREATING_TABLE: [
            TableOperationState.ADDING_ROW,
            TableOperationState.FORMATTING_TABLE,
            TableOperationState.IDLE
        ],
        TableOperationState.ADDING_ROW: [
            TableOperationState.EDITING_CELL,
            TableOperationState.IDLE
        ],
        TableOperationState.EDITING_CELL: [
            TableOperationState.FORMATTING_TABLE,
            TableOperationState.IDLE
        ]
    }

# ==================== 智能状态管理器 ====================

class IntelligentStateManager:
    """智能状态管理器"""
    
    def __init__(self):
        # 初始化所有状态
        self.global_state = GlobalDocumentState.NO_DOCUMENT
        self.content_state = ContentEditingState.IDLE
        self.table_state = TableOperationState.IDLE
        self.image_state = ImageProcessingState.IDLE
        self.font_state = FontProcessingState.IDLE
        self.cloud_state = CloudStorageState.IDLE
        self.template_state = TemplateState.IDLE
        
        # 上下文和历史记录
        self.context_stack: List[OperationContext] = []
        self.operation_history: List[OperationRecord] = []
        self.transition_history: List[StateTransition] = []
        self.pending_operations: List[str] = []
        
        # 状态转换规则
        self.transition_rules = StateTransitionRules()
        
        logger.info("智能状态管理器初始化完成")
    
    def get_current_state_summary(self) -> Dict[str, str]:
        """获取当前状态摘要"""
        return {
            "global": self.global_state.value,
            "content": self.content_state.value,
            "table": self.table_state.value,
            "image": self.image_state.value,
            "font": self.font_state.value,
            "cloud": self.cloud_state.value,
            "template": self.template_state.value,
            "context_count": len(self.context_stack)
        }
    
    def validate_state_transition(self, target_state: str, operation: str) -> ValidationResult:
        """验证状态转换的有效性"""
        errors = []
        warnings = []
        
        # 检查全局状态转换
        if hasattr(GlobalDocumentState, target_state.upper()):
            target_global_state = GlobalDocumentState[target_state.upper()]
            if target_global_state not in self.transition_rules.GLOBAL_TRANSITIONS.get(self.global_state, []):
                errors.append(f"无法从 {self.global_state.value} 转换到 {target_state}")
        
        # 检查操作依赖
        if self.global_state == GlobalDocumentState.NO_DOCUMENT:
            if operation not in ["open_document", "create_document"]:
                errors.append(f"在无文档状态下无法执行 {operation} 操作")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            error_messages=errors,
            warnings=warnings
        )
    
    def execute_state_transition(self, operation: str, **kwargs) -> bool:
        """执行状态转换"""
        try:
            # 记录操作
            operation_record = OperationRecord(
                operation=operation,
                timestamp=datetime.now(),
                parameters=kwargs,
                success=False
            )
            
            # 根据操作类型更新状态
            if operation == "open_document" or operation == "create_document":
                if self.global_state == GlobalDocumentState.NO_DOCUMENT:
                    self.global_state = GlobalDocumentState.DOCUMENT_LOADING
                    # 模拟加载完成
                    self.global_state = GlobalDocumentState.DOCUMENT_READY
                    operation_record.success = True
            
            elif operation == "add_paragraph":
                if self.global_state == GlobalDocumentState.DOCUMENT_READY:
                    self.global_state = GlobalDocumentState.DOCUMENT_EDITING
                    self.content_state = ContentEditingState.ADDING_PARAGRAPH
                    operation_record.success = True
            
            elif operation == "add_table":
                if self.global_state == GlobalDocumentState.DOCUMENT_READY:
                    self.global_state = GlobalDocumentState.DOCUMENT_EDITING
                    self.table_state = TableOperationState.CREATING_TABLE
                    operation_record.success = True
            
            elif operation == "save_document":
                if self.global_state == GlobalDocumentState.DOCUMENT_EDITING:
                    self.global_state = GlobalDocumentState.DOCUMENT_SAVING
                    # 模拟保存完成
                    self.global_state = GlobalDocumentState.DOCUMENT_READY
                    operation_record.success = True
            
            elif operation == "close_document":
                self.global_state = GlobalDocumentState.DOCUMENT_CLOSED
                self._reset_all_states()
                operation_record.success = True
            
            # 记录操作历史
            self.operation_history.append(operation_record)
            
            # 记录状态转换
            transition = StateTransition(
                from_state=self.global_state.value,
                to_state=self.global_state.value,
                operation=operation,
                timestamp=datetime.now(),
                success=operation_record.success
            )
            self.transition_history.append(transition)
            
            logger.info(f"状态转换执行: {operation} -> {self.global_state.value}")
            return operation_record.success
            
        except Exception as e:
            logger.error(f"状态转换失败: {operation}, 错误: {e}")
            return False
    
    def get_available_operations(self) -> List[str]:
        """获取当前状态下可用的操作列表"""
        available_ops = []
        
        if self.global_state == GlobalDocumentState.NO_DOCUMENT:
            available_ops = ["open_document", "create_document"]
        
        elif self.global_state == GlobalDocumentState.DOCUMENT_READY:
            available_ops = [
                "add_paragraph", "add_heading", "add_table", "add_image",
                "search_text", "save_document", "close_document", "get_document_info"
            ]
        
        elif self.global_state == GlobalDocumentState.DOCUMENT_EDITING:
            available_ops = [
                "add_paragraph", "add_heading", "add_table", "add_image",
                "edit_table_cell", "set_paragraph_font", "search_text",
                "save_document", "close_document"
            ]
        
        return available_ops
    
    def suggest_next_operation(self, user_intent: str) -> List[str]:
        """基于用户意图建议下一步操作"""
        suggestions = []
        
        if "创建" in user_intent or "新建" in user_intent:
            if self.global_state == GlobalDocumentState.NO_DOCUMENT:
                suggestions = ["create_document"]
            else:
                suggestions = ["add_paragraph", "add_heading"]
        
        elif "表格" in user_intent:
            suggestions = ["add_table", "edit_table_cell", "add_table_row"]
        
        elif "图片" in user_intent:
            suggestions = ["add_image", "resize_image", "list_images"]
        
        elif "保存" in user_intent:
            suggestions = ["save_document"]
        
        elif "格式化" in user_intent or "样式" in user_intent:
            suggestions = ["set_paragraph_font", "batch_format_paragraphs"]
        
        return suggestions
    
    def _reset_all_states(self):
        """重置所有状态到初始状态"""
        self.content_state = ContentEditingState.IDLE
        self.table_state = TableOperationState.IDLE
        self.image_state = ImageProcessingState.IDLE
        self.font_state = FontProcessingState.IDLE
        self.cloud_state = CloudStorageState.IDLE
        self.template_state = TemplateState.IDLE
        self.context_stack.clear()
    
    def get_operation_statistics(self) -> Dict[str, Any]:
        """获取操作统计信息"""
        total_operations = len(self.operation_history)
        successful_operations = sum(1 for op in self.operation_history if op.success)
        
        return {
            "total_operations": total_operations,
            "successful_operations": successful_operations,
            "success_rate": successful_operations / total_operations if total_operations > 0 else 0,
            "current_session_duration": (datetime.now() - self.operation_history[0].timestamp).total_seconds() if self.operation_history else 0
        }
