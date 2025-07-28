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
from core.models import DocumentPatch

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


def main():
    """主入口点函数，用于uvx运行"""
    # 启动MCP服务
    # transport='stdio' 表示服务将通过标准输入/输出与客户端通信
    # 这是MCP的标准做法
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
