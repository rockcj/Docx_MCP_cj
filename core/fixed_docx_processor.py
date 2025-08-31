#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复版DOCX处理器
解决SSE和HTTP模式下文件保存问题
"""

import os
import logging
from typing import Optional
from docx import Document

from .enhanced_docx_processor import EnhancedDocxProcessor
from .file_path_utils import get_safe_file_path, get_file_info, validate_file_path

logger = logging.getLogger(__name__)

class FixedDocxProcessor(EnhancedDocxProcessor):
    """修复版DOCX处理器，解决文件保存问题"""
    
    def __init__(self):
        super().__init__()
        logger.info("FixedDocxProcessor initialized with file save fixes")
    
    def create_document(self, file_path: str) -> str:
        """创建新文档 - 修复版"""
        try:
            # 获取当前工作目录信息
            current_dir = os.getcwd()
            logger.info(f"Current working directory: {current_dir}")
            
            # 获取文件信息
            file_info = get_file_info(file_path)
            logger.info(f"File info: {file_info}")
            
            # 获取安全的文件路径
            safe_path = get_safe_file_path(file_path, ".docx")
            logger.info(f"Safe path: {safe_path}")
            
            # 验证路径
            is_valid, error_msg = validate_file_path(safe_path)
            if not is_valid:
                return f"文件路径无效: {error_msg}"
            
            # 创建文档
            document = Document()
            
            # 设置当前文档
            self.state_manager.set_current_document(safe_path, document)
            
            # 保存文档
            document.save(safe_path)
            
            # 验证文件是否真的保存成功
            if os.path.exists(safe_path):
                file_size = os.path.getsize(safe_path)
                logger.info(f"Document successfully created: {safe_path} (size: {file_size} bytes)")
                return f"文档创建成功: {safe_path} (大小: {file_size} 字节)"
            else:
                logger.error(f"File was not created despite successful save call: {safe_path}")
                return f"文档创建失败: 文件未成功保存到 {safe_path}"
                
        except Exception as e:
            logger.error(f"Failed to create document: {e}")
            return f"创建文档失败: {str(e)}"
    
    def save_as_document(self, new_file_path: str) -> str:
        """另存为新文件 - 修复版"""
        try:
            if not self.state_manager.has_current_document():
                return "没有打开的文档"
            
            # 获取安全的文件路径
            safe_path = get_safe_file_path(new_file_path, ".docx")
            logger.info(f"Saving document as: {safe_path}")
            
            # 验证路径
            is_valid, error_msg = validate_file_path(safe_path)
            if not is_valid:
                return f"文件路径无效: {error_msg}"
            
            # 获取当前文档
            document = self.state_manager.get_current_document()
            
            # 保存文档
            document.save(safe_path)
            
            # 更新状态管理器
            self.state_manager.set_current_document(safe_path, document)
            
            # 验证文件是否真的保存成功
            if os.path.exists(safe_path):
                file_size = os.path.getsize(safe_path)
                logger.info(f"Document successfully saved as: {safe_path} (size: {file_size} bytes)")
                return f"文档另存为成功: {safe_path} (大小: {file_size} 字节)"
            else:
                logger.error(f"File was not saved despite successful save call: {safe_path}")
                return f"文档另存为失败: 文件未成功保存到 {safe_path}"
                
        except Exception as e:
            logger.error(f"Failed to save document as: {e}")
            return f"另存文档失败: {str(e)}"
    
    def save_document(self) -> str:
        """保存当前文档 - 修复版"""
        try:
            if not self.state_manager.has_current_document():
                return "没有打开的文档"
            
            current_path = self.state_manager.get_current_file_path()
            if not current_path:
                return "当前文档未设置保存路径"
            
            logger.info(f"Saving document to: {current_path}")
            
            # 获取当前文档
            document = self.state_manager.get_current_document()
            
            # 保存文档
            document.save(current_path)
            
            # 验证文件是否真的保存成功
            if os.path.exists(current_path):
                file_size = os.path.getsize(current_path)
                logger.info(f"Document successfully saved: {current_path} (size: {file_size} bytes)")
                return f"文档保存成功: {current_path} (大小: {file_size} 字节)"
            else:
                logger.error(f"File was not saved despite successful save call: {current_path}")
                return f"文档保存失败: 文件未成功保存到 {current_path}"
                
        except Exception as e:
            logger.error(f"Failed to save document: {e}")
            return f"保存文档失败: {str(e)}"
    
    def get_debug_info(self) -> str:
        """获取调试信息"""
        try:
            info = []
            
            # 工作目录信息
            info.append(f"当前工作目录: {os.getcwd()}")
            info.append(f"用户主目录: {os.path.expanduser('~')}")
            info.append(f"桌面目录: {os.path.join(os.path.expanduser('~'), 'Desktop')}")
            
            # 当前文档信息
            if self.state_manager.has_current_document():
                current_path = self.state_manager.get_current_file_path()
                info.append(f"当前文档路径: {current_path}")
                if current_path:
                    file_info = get_file_info(current_path)
                    info.append(f"文件信息: {file_info}")
            else:
                info.append("当前没有打开的文档")
            
            # 临时目录信息
            import tempfile
            info.append(f"临时目录: {tempfile.gettempdir()}")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"获取调试信息失败: {str(e)}"
