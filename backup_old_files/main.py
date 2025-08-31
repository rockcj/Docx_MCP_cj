import base64
import io
import json
import os
import requests
import oss2
import uuid
from datetime import datetime
from typing import List, Dict, Any

from fastmcp import FastMCP
from docx import Document

from core.docx_processor import DocxProcessor
from core.models import DocumentPatch, TableOperation, TableOperationType, CellFormat, TableFormat, CellAlignment, BorderStyle

# 实例化 FastMCP 对象，只传入服务名称，遵循 fastmcp 的正确用法
mcp = FastMCP("docx_handler")

# 阿里云OSS配置
# 注意：以下为示例配置，实际部署时请替换为真实值
# 建议通过环境变量或配置文件管理敏感信息
OSS_CONFIG = {
    "endpoint": "https://oss-cn-shenzhen.aliyuncs.com",
    "access_key": "LTAI5tEX4A49ZUeya8DCCNGd",
    "secret_key": "7uXTkPwNAE6PP3YHqHscWfKcfmx2fx",
    "bucket_name": "ggb-lzt",  # 从ALI_DOMAIN中提取的bucket名称
    "domain": "https://ggb-lzt.oss-cn-shenzhen.aliyuncs.com/"
}

def get_oss_bucket():
    """获取OSS bucket对象"""
    auth = oss2.Auth(OSS_CONFIG["access_key"], OSS_CONFIG["secret_key"])
    bucket = oss2.Bucket(auth, OSS_CONFIG["endpoint"], OSS_CONFIG["bucket_name"])
    return bucket

def _apply_modifications_core(original_file_content_base64: str, patches_json: str) -> str:
    """
    核心修改应用逻辑（内部函数）
    """
    try:
        # 解码原始文件
        decoded_original_content = base64.b64decode(original_file_content_base64)
        original_file_stream = io.BytesIO(decoded_original_content)

        # 解析JSON字符串为Python对象
        patches_data = json.loads(patches_json)
        # 将字典列表转换为DocumentPatch对象列表
        patches = [DocumentPatch(**p) for p in patches_data]

        # 创建一个新的内存流来保存修改后的文件
        modified_file_stream = io.BytesIO()

        # 调用核心逻辑来应用补丁
        DocxProcessor.apply_patches(original_file_stream, modified_file_stream, patches)

        # 将指针移到内存流的开头
        modified_file_stream.seek(0)
        # 读取修改后的文件字节
        modified_content_bytes = modified_file_stream.read()
        
        # 将修改后的字节内容编码为 Base64 字符串并返回
        return base64.b64encode(modified_content_bytes).decode('utf-8')
    except Exception as e:
        # 返回 Base64 编码的错误信息可能不是最佳实践，但作为示例
        error_message = f"Failed to apply modifications: {str(e)}"
        return base64.b64encode(error_message.encode('utf-8')).decode('utf-8')

def _upload_to_oss_core(file_bytes: bytes) -> Dict[str, Any]:
    """
    核心OSS上传逻辑（内部函数）
    """
    try:
        # 生成唯一的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"modified_document_{timestamp}_{unique_id}.docx"
        
        # 获取OSS bucket
        bucket = get_oss_bucket()
        
        # 上传文件到OSS
        result = bucket.put_object(filename, file_bytes)
        
        # 构建访问链接
        download_url = f"{OSS_CONFIG['domain']}{filename}"
        
        return {
            "success": True,
            "filename": filename,
            "download_url": download_url,
            "upload_info": {
                "etag": result.etag,
                "request_id": result.request_id
            },
            "message": "文档已成功上传到OSS，可通过返回的链接下载"
        }
        
    except oss2.exceptions.OssError as e:
        return {
            "error": f"OSS上传失败: {e.message}",
            "error_code": e.code,
            "request_id": getattr(e, 'request_id', 'unknown')
        }
    except Exception as e:
        return {"error": f"上传文件时发生错误: {str(e)}"}


@mcp.tool()
def extract_local_document_structure(file_path: str) -> Dict[str, Any]:
    """
    【本地文档结构提取工具】从本地文件路径解析.docx文件结构

    :param file_path: 本地.docx文件的完整路径，如"C:\\path\\to\\document.docx"
    :return: 包含文档结构的字典，每个元素都有唯一ID

    注意: 文件路径必须存在且可访问
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        # 检查文件扩展名
        if not file_path.lower().endswith('.docx'):
            return {"error": f"不是.docx文件: {file_path}"}
        
        # 直接从本地文件读取
        with open(file_path, 'rb') as file:
            file_stream = io.BytesIO(file.read())
        
        # 调用核心逻辑来提取结构
        structure = DocxProcessor.extract_structure_with_ids(file_stream)
        return structure
    except Exception as e:
        return {"error": f"提取文档结构失败: {str(e)}"}

@mcp.tool()
def extract_document_structure(document_url: str) -> Dict[str, Any]:
    """
    从链接下载并解析 .docx 文件的内容，并以 JSON 格式提取其结构和文本。

    这个工具接收一个 .docx 文件的URL链接，下载文件后返回一个详细描述
    文档结构（段落、表格等）的字典，并为每个元素分配一个唯一的ID。

    :param document_url: .docx 文件的URL链接。
    :return: 包含文档结构的字典。
    """
    try:
        # 发送GET请求下载文件
        response = requests.get(document_url, timeout=30)
        response.raise_for_status()  # 如果状态码不是200，抛出异常
        
        # 检查Content-Type是否为docx文件
        content_type = response.headers.get('content-type', '').lower()
        if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' not in content_type:
            # 如果Content-Type不正确，但文件可能仍然是docx，我们继续尝试处理
            pass
        
        # 使用 io.BytesIO 在内存中创建一个类文件对象
        file_stream = io.BytesIO(response.content)
        # 调用核心逻辑来提取结构
        structure = DocxProcessor.extract_structure_with_ids(file_stream)
        return structure
    except requests.exceptions.RequestException as e:
        # 处理网络请求相关的错误
        return {"error": f"Failed to download document from URL: {str(e)}"}
    except Exception as e:
        # 在MCP中，错误处理通常是通过返回一个包含错误信息的字典来完成的
        return {"error": f"Failed to extract document structure: {str(e)}"}

@mcp.tool()
def apply_modifications_to_document(
    original_file_content_base64: str,
    patches_json: str
) -> str:
    """
    将一系列修改应用到 .docx 文件，并返回修改后的文件内容。

    此工具接收原始文件的 Base64 编码内容和一个包含修改指令的 JSON 字符串。
    它会在内存中应用这些修改，并返回修改后新文件的 Base64 编码字符串。

    :param original_file_content_base64: 原始 .docx 文件的 Base64 编码字符串。
    :param patches_json: 一个JSON格式的字符串，包含一个补丁列表。
                         例如: '[{"element_id": "p_0", "new_content": "New text"}]'
    :return: 修改后的 .docx 文件内容的 Base64 编码字符串。
    """
    return _apply_modifications_core(original_file_content_base64, patches_json)

@mcp.tool()
def get_modified_document(
    original_file_content_base64: str,
    patches_json: str
) -> str:
    """
    根据原始文件和补丁，生成并返回修改后的 .docx 文件。

    这个工具是 'apply_modifications_to_document' 的一个别名，
    用于在工作流中更清晰地表达“获取最终结果”的意图。
    它接收与 'apply_modifications_to_document' 完全相同的参数。

    :param original_file_content_base64: 原始 .docx 文件的 Base64 编码字符串。
    :param patches_json: 一个JSON格式的字符串，包含一个补丁列表。
    :return: 修改后的 .docx 文件内容的 Base64 编码字符串。
    """
    # 直接调用现有工具的功能，因为它们的逻辑是相同的。
    return apply_modifications_to_document(original_file_content_base64, patches_json)


@mcp.tool()
def prepare_document_for_download(
    original_file_content_base64: str,
    patches_json: str
) -> Dict[str, Any]:
    """
    将修改后的 .docx 文件上传到阿里云OSS，并返回访问链接。

    此工具会将修改应用到文档，然后将文件上传到阿里云OSS对象存储，
    并返回可供下载的访问链接。

    :param original_file_content_base64: 原始 .docx 文件的 Base64 编码字符串。
    :param patches_json: 一个JSON格式的字符串，包含一个补丁列表。
    :return: 包含上传结果和访问链接的字典。
    """
    try:
        # 首先应用修改，获取修改后的文件内容
        modified_file_base64 = apply_modifications_to_document(original_file_content_base64, patches_json)
        
        # 检查是否是错误返回（Base64编码的错误信息）
        try:
            # 尝试解码，如果是错误信息会包含可读的错误文本
            decoded_test = base64.b64decode(modified_file_base64).decode('utf-8')
            if 'Failed to apply modifications' in decoded_test:
                return {"error": decoded_test}
        except:
            # 解码失败说明是正常的文件内容，继续处理
            pass
        
        # 解码修改后的文件内容
        modified_file_bytes = base64.b64decode(modified_file_base64)
        
        # 调用核心OSS上传逻辑
        return _upload_to_oss_core(modified_file_bytes)
        
    except Exception as e:
        return {"error": f"处理文档时发生错误: {str(e)}"}

@mcp.tool()
def process_document_from_url(
    document_url: str,
    patches_json: str
) -> Dict[str, Any]:
    """
    从URL下载文档，应用修改，然后上传到阿里云OSS。

    此工具直接从URL下载.docx文件，应用指定的修改，然后将修改后的文件
    上传到阿里云OSS对象存储，并返回可供下载的访问链接。

    :param document_url: 原始 .docx 文件的URL链接。
    :param patches_json: 一个JSON格式的字符串，包含一个补丁列表。
    :return: 包含上传结果和访问链接的字典。
    """
    try:
        # 首先下载原始文件
        response = requests.get(document_url, timeout=30)
        response.raise_for_status()
        
        # 将下载的文件内容转换为Base64
        original_file_base64 = base64.b64encode(response.content).decode('utf-8')
        
        # 应用修改
        modified_file_base64 = _apply_modifications_core(original_file_base64, patches_json)
        
        # 检查是否是错误返回（Base64编码的错误信息）
        try:
            # 尝试解码，如果是错误信息会包含可读的错误文本
            decoded_test = base64.b64decode(modified_file_base64).decode('utf-8')
            if 'Failed to apply modifications' in decoded_test:
                return {"error": decoded_test}
        except:
            # 解码失败说明是正常的文件内容，继续处理
            pass
        
        # 解码修改后的文件内容
        modified_file_bytes = base64.b64decode(modified_file_base64)
        
        # 上传到OSS
        return _upload_to_oss_core(modified_file_bytes)
        
    except requests.exceptions.RequestException as e:
        return {"error": f"下载文档失败: {str(e)}"}
    except Exception as e:
        return {"error": f"处理文档时发生错误: {str(e)}"}

@mcp.tool()
def modify_table_structure(
    document_url: str,
    table_operations_json: str
) -> Dict[str, Any]:
    """
    【表格批量操作工具】一次性执行多个表格修改操作

    支持操作: add_row, add_column, delete_row, delete_column, format_table, format_cell, modify_cell

    :param document_url: .docx文件URL链接
    :param table_operations_json: JSON操作数组，格式: '[{"operation_type": "add_row", "table_id": "tbl_0", "row_index": 1, "cell_data": ["数据1", "数据2"]}]'
    :return: 包含success状态和download_url的结果字典

    使用提示: 先用extract_document_structure获取table_id，结构操作优先于格式化操作
    """
    try:
        # 首先下载原始文件
        response = requests.get(document_url, timeout=30)
        response.raise_for_status()
        
        # 将下载的文件内容转换为Base64
        original_file_base64 = base64.b64encode(response.content).decode('utf-8')
        
        # 解析表格操作指令
        operations_data = json.loads(table_operations_json)
        
        # 创建包含表格操作的DocumentPatch列表
        patches = []
        for i, op_data in enumerate(operations_data):
            # 创建TableOperation对象
            table_op = TableOperation(**op_data)
            
            # 创建DocumentPatch对象，使用表格操作
            patch = DocumentPatch(
                element_id=f"table_operation_{i}",
                new_content="",
                table_operation=table_op
            )
            patches.append(patch)
        
        # 应用修改
        patches_json = json.dumps([patch.dict() for patch in patches])
        modified_file_base64 = _apply_modifications_core(original_file_base64, patches_json)
        
        # 检查是否是错误返回
        try:
            decoded_test = base64.b64decode(modified_file_base64).decode('utf-8')
            if 'Failed to apply modifications' in decoded_test:
                return {"error": decoded_test}
        except:
            pass
        
        # 解码修改后的文件内容并上传到OSS
        modified_file_bytes = base64.b64decode(modified_file_base64)
        return _upload_to_oss_core(modified_file_bytes)
        
    except json.JSONDecodeError as e:
        return {"error": f"JSON解析失败: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"下载文档失败: {str(e)}"}
    except Exception as e:
        return {"error": f"表格操作失败: {str(e)}"}

@mcp.tool()
def add_table_row(
    document_url: str,
    table_id: str,
    row_index: int = None,
    cell_data: List[str] = None
) -> Dict[str, Any]:
    """
    【表格行添加工具】向表格插入新行

    :param document_url: .docx文件URL链接
    :param table_id: 表格ID，格式"tbl_0"（用extract_document_structure获取）
    :param row_index: 插入位置索引，None=末尾添加，0=开头插入，正整数=指定位置
    :param cell_data: 新行数据列表，如["姓名", "年龄", "职业"]，None=空单元格
    :return: 包含success和download_url的结果字典

    注意: 新行继承表格样式，cell_data长度应匹配列数
    """
    operation = {
        "operation_type": "add_row",
        "table_id": table_id,
        "row_index": row_index,
        "cell_data": cell_data or []
    }
    
    return modify_table_structure(document_url, json.dumps([operation]))

@mcp.tool()
def add_table_column(
    document_url: str,
    table_id: str,
    column_index: int = None,
    cell_data: List[str] = None
) -> Dict[str, Any]:
    """
    【表格列添加工具】向表格插入新列

    :param document_url: .docx文件URL链接
    :param table_id: 表格ID，格式"tbl_0"（用extract_document_structure获取）
    :param column_index: 插入位置索引，None=右侧添加，0=左侧插入，正整数=指定位置
    :param cell_data: 新列数据列表，按行顺序填充，如["标题", "数据1", "数据2"]，None=空单元格
    :return: 包含success和download_url的结果字典

    注意: 新列继承表格样式，cell_data长度应匹配行数，可能影响表格宽度
    """
    operation = {
        "operation_type": "add_column",
        "table_id": table_id,
        "column_index": column_index,
        "cell_data": cell_data or []
    }
    
    return modify_table_structure(document_url, json.dumps([operation]))

@mcp.tool()
def delete_table_row(
    document_url: str,
    table_id: str,
    row_index: int
) -> Dict[str, Any]:
    """
    【表格行删除工具】删除指定表格行

    ⚠️ 不可逆操作：删除后行索引会变化，建议删除前备份重要数据

    :param document_url: .docx文件URL链接
    :param table_id: 表格ID，格式"tbl_0"（用extract_document_structure获取）
    :param row_index: 删除行索引（从0开始），0=第一行（表头请谨慎），超出范围会失败
    :return: 包含success和download_url的结果字典

    💡 删除多行时从大索引开始倒序删除，避免索引偏移
    """
    operation = {
        "operation_type": "delete_row",
        "table_id": table_id,
        "row_index": row_index
    }
    
    return modify_table_structure(document_url, json.dumps([operation]))

@mcp.tool()
def delete_table_column(
    document_url: str,
    table_id: str,
    column_index: int
) -> Dict[str, Any]:
    """
    【表格列删除工具】删除指定表格列

    ⚠️ 不可逆操作，删除后列索引会变化，可能影响表格宽度

    :param document_url: .docx文件URL链接
    :param table_id: 表格ID，格式"tbl_0"（用extract_document_structure获取）
    :param column_index: 要删除的列索引（从0开始），0=第一列（标识列请谨慎）
    :return: 包含success和download_url的结果字典

    建议: 删除多列时从大索引开始倒序删除，避免索引偏移
    """
    operation = {
        "operation_type": "delete_column",
        "table_id": table_id,
        "column_index": column_index
    }
    
    return modify_table_structure(document_url, json.dumps([operation]))

@mcp.tool()
def format_table_style(
    document_url: str,
    table_id: str,
    border_style: str = "single",
    border_color: str = "#000000",
    width: str = None,
    column_widths: List[str] = None
) -> Dict[str, Any]:
    """
    【表格样式格式化工具】设置表格整体外观样式

    :param document_url: .docx文件URL链接
    :param table_id: 表格ID，格式"tbl_0"（用extract_document_structure获取）
    :param border_style: 边框样式，支持"none"/"single"/"double"/"thick"/"thin"，默认"single"
    :param border_color: 边框颜色，十六进制格式如"#FF0000"（红色），默认"#000000"（黑色）
    :param width: 表格宽度，如"100%"（满宽）/"50%"，None=保持原宽度
    :param column_widths: 列宽列表，如["3cm", "2in", "50pt"]，支持cm/in/pt单位，None=保持原列宽
    :return: 包含success和download_url的结果字典

    建议: 正式文档用single边框，列宽设置考虑内容长度
    """
    table_format = {
        "border_style": border_style,
        "border_color": border_color
    }
    
    if width:
        table_format["width"] = width
    if column_widths:
        table_format["column_widths"] = column_widths
    
    operation = {
        "operation_type": "format_table",
        "table_id": table_id,
        "table_format": table_format
    }
    
    return modify_table_structure(document_url, json.dumps([operation]))

@mcp.tool()
def format_table_cell(
    document_url: str,
    table_id: str,
    cell_id: str,
    alignment: str = None,
    bold: bool = None,
    italic: bool = None,
    font_size: int = None,
    font_name: str = None,
    background_color: str = None,
    text_color: str = None
) -> Dict[str, Any]:
    """
    【单元格格式化工具】设置单元格外观和文本样式

    :param document_url: .docx文件URL链接
    :param table_id: 表格ID，格式"tbl_0"
    :param cell_id: 单元格ID，格式"tbl_0_r0c0"（第1行第1列），用extract_document_structure获取
    :param alignment: 对齐方式，支持"left"/"center"/"right"/"justify"，None=保持现有
    :param bold: 加粗，True/False/None，None=保持现有
    :param italic: 斜体，True/False/None，None=保持现有
    :param font_size: 字体大小（磅），常用10-12（正文），14-16（标题），None=保持现有
    :param font_name: 字体名称，如"微软雅黑"/"Arial"，None=保持现有
    :param background_color: 背景色，十六进制如"#FFFF00"（黄色高亮），None=保持现有
    :param text_color: 文字颜色，十六进制如"#FF0000"（红色），None=保持现有
    :return: 包含success和download_url的结果字典

    建议: 表头用加粗+居中+背景色，数值列右对齐，注意颜色对比度
    """
    cell_format = {}
    
    if alignment:
        cell_format["alignment"] = alignment
    if bold is not None:
        cell_format["bold"] = bold
    if italic is not None:
        cell_format["italic"] = italic
    if font_size:
        cell_format["font_size"] = font_size
    if font_name:
        cell_format["font_name"] = font_name
    if background_color:
        cell_format["background_color"] = background_color
    if text_color:
        cell_format["text_color"] = text_color
    
    operation = {
        "operation_type": "format_cell",
        "table_id": table_id,
        "cell_id": cell_id,
        "cell_format": cell_format
    }
    
    return modify_table_structure(document_url, json.dumps([operation]))

@mcp.tool()
def process_local_document(
    file_path: str,
    patches_json: str
) -> Dict[str, Any]:
    """
    【本地文档处理工具】处理本地.docx文件并上传到云端

    :param file_path: 本地.docx文件的完整路径
    :param patches_json: JSON格式的修改指令列表
    :return: 包含处理结果和下载链接的字典

    功能: 读取本地文件，应用修改，上传到阿里云OSS并返回下载链接
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        # 检查文件扩展名
        if not file_path.lower().endswith('.docx'):
            return {"error": f"不是.docx文件: {file_path}"}
        
        # 读取本地文件
        with open(file_path, 'rb') as file:
            original_file_content = file.read()
        
        # 转换为Base64
        original_file_base64 = base64.b64encode(original_file_content).decode('utf-8')
        
        # 应用修改
        modified_file_base64 = _apply_modifications_core(original_file_base64, patches_json)
        
        # 检查是否是错误返回
        try:
            decoded_test = base64.b64decode(modified_file_base64).decode('utf-8')
            if 'Failed to apply modifications' in decoded_test:
                return {"error": decoded_test}
        except:
            pass
        
        # 解码修改后的文件内容并上传到OSS
        modified_file_bytes = base64.b64decode(modified_file_base64)
        return _upload_to_oss_core(modified_file_bytes)
        
    except Exception as e:
        return {"error": f"处理本地文档失败: {str(e)}"}

@mcp.tool()
def modify_local_table_structure(
    file_path: str,
    table_operations_json: str
) -> Dict[str, Any]:
    """
    【本地表格批量操作工具】处理本地文件的表格操作

    :param file_path: 本地.docx文件的完整路径
    :param table_operations_json: JSON操作数组，格式同modify_table_structure
    :return: 包含success状态和download_url的结果字典

    功能: 读取本地文件，执行表格操作，上传到云端并返回下载链接
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        # 读取本地文件并转换为Base64
        with open(file_path, 'rb') as file:
            original_file_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        # 解析表格操作指令
        operations_data = json.loads(table_operations_json)
        
        # 创建包含表格操作的DocumentPatch列表
        patches = []
        for i, op_data in enumerate(operations_data):
            table_op = TableOperation(**op_data)
            patch = DocumentPatch(
                element_id=f"table_operation_{i}",
                new_content="",
                table_operation=table_op
            )
            patches.append(patch)
        
        # 应用修改
        patches_json = json.dumps([patch.dict() for patch in patches])
        modified_file_base64 = _apply_modifications_core(original_file_base64, patches_json)
        
        # 检查是否是错误返回
        try:
            decoded_test = base64.b64decode(modified_file_base64).decode('utf-8')
            if 'Failed to apply modifications' in decoded_test:
                return {"error": decoded_test}
        except:
            pass
        
        # 解码修改后的文件内容并上传到OSS
        modified_file_bytes = base64.b64decode(modified_file_base64)
        return _upload_to_oss_core(modified_file_bytes)
        
    except json.JSONDecodeError as e:
        return {"error": f"JSON解析失败: {str(e)}"}
    except Exception as e:
        return {"error": f"本地表格操作失败: {str(e)}"}


def main():
    """主入口点函数，用于uvx运行"""
    # 启动MCP服务
    # transport='stdio' 表示服务将通过标准输入/输出与客户端通信
    # 这是MCP的标准做法
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
