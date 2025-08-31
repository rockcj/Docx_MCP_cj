#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OSS处理模块
负责文档的云存储上传和下载操作
"""

import os
import logging
import requests
import uuid
from datetime import datetime
from typing import Dict, Any, Union
from io import BytesIO

try:
    import oss2
    OSS_AVAILABLE = True
except ImportError:
    OSS_AVAILABLE = False

logger = logging.getLogger(__name__)

# 复用main.py中的OSS配置
OSS_CONFIG = {
    "endpoint": "https://oss-cn-shenzhen.aliyuncs.com",
    "access_key": "LTAI5tEX4A49ZUeya8DCCNGd",
    "secret_key": "7uXTkPwNAE6PP3YHqHscWfKcfmx2fx",
    "bucket_name": "ggb-lzt",
    "domain": "https://ggb-lzt.oss-cn-shenzhen.aliyuncs.com/"
}

class OSSProcessor:
    """OSS处理器，提供云存储上传下载功能"""
    
    def __init__(self):
        """初始化OSS处理器"""
        if not OSS_AVAILABLE:
            logger.warning("OSS2 library not available. OSS features will be disabled.")
    
    def get_oss_bucket(self):
        """获取OSS bucket对象"""
        if not OSS_AVAILABLE:
            raise Exception("OSS2 library not installed. Please install with: pip install oss2")
        
        auth = oss2.Auth(OSS_CONFIG["access_key"], OSS_CONFIG["secret_key"])
        bucket = oss2.Bucket(auth, OSS_CONFIG["endpoint"], OSS_CONFIG["bucket_name"])
        return bucket
    
    def upload_file_to_oss(self, file_path: str, custom_filename: str = None) -> Dict[str, Any]:
        """
        上传本地文件到OSS
        
        Parameters:
        - file_path: 本地文件路径
        - custom_filename: 自定义文件名，None则自动生成
        
        Returns:
        - 包含上传结果的字典
        """
        try:
            if not OSS_AVAILABLE:
                return {"error": "OSS功能不可用，请安装oss2库: pip install oss2"}
            
            if not os.path.exists(file_path):
                return {"error": f"文件不存在: {file_path}"}
            
            # 生成文件名
            if custom_filename:
                filename = custom_filename
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                file_ext = os.path.splitext(file_path)[1]
                filename = f"document_{timestamp}_{unique_id}{file_ext}"
            
            # 读取文件
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            
            return self._upload_bytes_to_oss(file_bytes, filename)
            
        except Exception as e:
            logger.error(f"Upload file to OSS failed: {e}")
            return {"error": f"上传文件失败: {str(e)}"}
    
    def upload_bytes_to_oss(self, file_bytes: bytes, filename: str = None) -> Dict[str, Any]:
        """
        上传字节数据到OSS
        
        Parameters:
        - file_bytes: 文件字节数据
        - filename: 文件名，None则自动生成
        
        Returns:
        - 包含上传结果的字典
        """
        try:
            if not OSS_AVAILABLE:
                return {"error": "OSS功能不可用，请安装oss2库: pip install oss2"}
            
            # 生成文件名
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                filename = f"document_{timestamp}_{unique_id}.docx"
            
            return self._upload_bytes_to_oss(file_bytes, filename)
            
        except Exception as e:
            logger.error(f"Upload bytes to OSS failed: {e}")
            return {"error": f"上传数据失败: {str(e)}"}
    
    def _upload_bytes_to_oss(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        核心OSS上传逻辑
        
        Parameters:
        - file_bytes: 文件字节数据
        - filename: 文件名
        
        Returns:
        - 包含上传结果的字典
        """
        try:
            # 获取OSS bucket
            bucket = self.get_oss_bucket()
            
            # 上传文件到OSS
            result = bucket.put_object(filename, file_bytes)
            
            # 构建访问链接
            download_url = f"{OSS_CONFIG['domain']}{filename}"
            
            return {
                "success": True,
                "filename": filename,
                "download_url": download_url,
                "file_size": len(file_bytes),
                "upload_info": {
                    "etag": result.etag,
                    "request_id": result.request_id
                },
                "message": "文档已成功上传到OSS，可通过返回的链接下载"
            }
            
        except Exception as e:
            if OSS_AVAILABLE and hasattr(e, 'code'):
                return {
                    "error": f"OSS上传失败: {e.message}",
                    "error_code": e.code,
                    "request_id": getattr(e, 'request_id', 'unknown')
                }
            else:
                return {"error": f"上传文件时发生错误: {str(e)}"}
    
    def download_file_from_oss(self, filename: str, local_path: str = None) -> Dict[str, Any]:
        """
        从OSS下载文件
        
        Parameters:
        - filename: OSS上的文件名
        - local_path: 本地保存路径，None则保存到临时目录
        
        Returns:
        - 包含下载结果的字典
        """
        try:
            if not OSS_AVAILABLE:
                return {"error": "OSS功能不可用，请安装oss2库: pip install oss2"}
            
            # 确定本地保存路径
            if not local_path:
                import tempfile
                local_path = os.path.join(tempfile.gettempdir(), filename)
            
            # 获取OSS bucket
            bucket = self.get_oss_bucket()
            
            # 下载文件
            result = bucket.get_object(filename)
            
            # 保存到本地
            with open(local_path, 'wb') as f:
                f.write(result.read())
            
            return {
                "success": True,
                "filename": filename,
                "local_path": local_path,
                "file_size": os.path.getsize(local_path),
                "message": f"文件已下载到: {local_path}"
            }
            
        except Exception as e:
            logger.error(f"Download file from OSS failed: {e}")
            if OSS_AVAILABLE and hasattr(e, 'code'):
                return {
                    "error": f"OSS下载失败: {e.message}",
                    "error_code": e.code,
                    "request_id": getattr(e, 'request_id', 'unknown')
                }
            else:
                return {"error": f"下载文件失败: {str(e)}"}
    
    def download_file_from_url(self, url: str, local_path: str = None) -> Dict[str, Any]:
        """
        从网络URL下载文件
        
        Parameters:
        - url: 文件URL
        - local_path: 本地保存路径，None则保存到临时目录
        
        Returns:
        - 包含下载结果的字典
        """
        try:
            # 从URL获取文件名
            filename = os.path.basename(url.split('?')[0])
            if not filename or '.' not in filename:
                filename = f"downloaded_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            
            # 确定本地保存路径
            if not local_path:
                import tempfile
                local_path = os.path.join(tempfile.gettempdir(), filename)
            
            # 下载文件
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 保存到本地
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            return {
                "success": True,
                "url": url,
                "local_path": local_path,
                "file_size": len(response.content),
                "message": f"文件已从URL下载到: {local_path}"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download from URL failed: {e}")
            return {"error": f"从URL下载失败: {str(e)}"}
        except Exception as e:
            logger.error(f"Download from URL failed: {e}")
            return {"error": f"下载文件失败: {str(e)}"}
    
    def list_oss_files(self, prefix: str = "", max_keys: int = 100) -> Dict[str, Any]:
        """
        列出OSS中的文件
        
        Parameters:
        - prefix: 文件名前缀过滤
        - max_keys: 最大返回数量
        
        Returns:
        - 包含文件列表的字典
        """
        try:
            if not OSS_AVAILABLE:
                return {"error": "OSS功能不可用，请安装oss2库: pip install oss2"}
            
            # 获取OSS bucket
            bucket = self.get_oss_bucket()
            
            # 列出文件
            files = []
            for obj in oss2.ObjectIterator(bucket, prefix=prefix, max_keys=max_keys):
                files.append({
                    "filename": obj.key,
                    "size": obj.size,
                    "last_modified": obj.last_modified,
                    "download_url": f"{OSS_CONFIG['domain']}{obj.key}"
                })
            
            return {
                "success": True,
                "files": files,
                "count": len(files),
                "message": f"找到 {len(files)} 个文件"
            }
            
        except Exception as e:
            logger.error(f"List OSS files failed: {e}")
            return {"error": f"列出文件失败: {str(e)}"}
    
    def delete_oss_file(self, filename: str) -> Dict[str, Any]:
        """
        删除OSS中的文件
        
        Parameters:
        - filename: 要删除的文件名
        
        Returns:
        - 包含删除结果的字典
        """
        try:
            if not OSS_AVAILABLE:
                return {"error": "OSS功能不可用，请安装oss2库: pip install oss2"}
            
            # 获取OSS bucket
            bucket = self.get_oss_bucket()
            
            # 删除文件
            bucket.delete_object(filename)
            
            return {
                "success": True,
                "filename": filename,
                "message": f"文件已删除: {filename}"
            }
            
        except Exception as e:
            logger.error(f"Delete OSS file failed: {e}")
            return {"error": f"删除文件失败: {str(e)}"}
