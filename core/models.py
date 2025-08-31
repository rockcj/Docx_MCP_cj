from pydantic import BaseModel
from typing import Optional, Any, List, Dict, Union
from enum import Enum

# Pydantic模型是FastAPI用于数据验证和文档生成的关键部分

class TableOperationType(str, Enum):
    """表格操作类型枚举"""
    ADD_ROW = "add_row"
    ADD_COLUMN = "add_column"
    DELETE_ROW = "delete_row"
    DELETE_COLUMN = "delete_column"
    MODIFY_CELL = "modify_cell"
    FORMAT_TABLE = "format_table"
    FORMAT_CELL = "format_cell"

class CellAlignment(str, Enum):
    """单元格对齐方式枚举"""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"

class BorderStyle(str, Enum):
    """边框样式枚举"""
    NONE = "none"
    SINGLE = "single"
    DOUBLE = "double"
    THICK = "thick"
    THIN = "thin"

class CellFormat(BaseModel):
    """单元格格式配置"""
    alignment: Optional[CellAlignment] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    font_size: Optional[int] = None
    font_name: Optional[str] = None
    background_color: Optional[str] = None  # 十六进制颜色代码，如 "#FFFFFF"
    text_color: Optional[str] = None

class TableFormat(BaseModel):
    """表格格式配置"""
    border_style: Optional[BorderStyle] = None
    border_color: Optional[str] = None  # 十六进制颜色代码
    width: Optional[str] = None  # 表格宽度，如 "100%"
    column_widths: Optional[List[str]] = None  # 列宽列表，如 ["2cm", "3cm"]

class TableOperation(BaseModel):
    """表格操作指令"""
    operation_type: TableOperationType
    table_id: str
    
    # 行/列操作相关
    row_index: Optional[int] = None
    column_index: Optional[int] = None
    cell_data: Optional[List[str]] = None  # 新增行/列时的单元格数据
    
    # 格式化相关
    cell_format: Optional[CellFormat] = None
    table_format: Optional[TableFormat] = None
    
    # 单元格修改相关
    cell_id: Optional[str] = None
    new_content: Optional[Any] = None

class DocumentPatch(BaseModel):
    """
    定义了对文档单个元素进行修改的指令结构。
    这个模型将被用于 /apply-changes/ 端点，以列表形式接收批量修改。
    """
    # 元素的唯一标识符，在提取阶段生成
    element_id: str
    
    # 新的内容，可以是简单的字符串，也可以是更复杂的结构（例如，对于表格单元格）
    new_content: Any
    
    # 表格操作指令（可选）
    table_operation: Optional[TableOperation] = None

    class Config:
        # Pydantic的配置类
        # str_strip_whitespace = True: 自动去除字符串两端的空白字符
        # from_attributes = True: 允许模型从对象的属性中读取数据
        str_strip_whitespace = True
        from_attributes = True 