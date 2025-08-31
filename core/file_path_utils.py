#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件路径工具模块
提供跨平台的文件路径处理和验证功能
"""

import os
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def normalize_file_path(file_path: str, default_extension: str = ".docx") -> str:
    """
    标准化文件路径处理
    
    Parameters:
    - file_path: 原始文件路径
    - default_extension: 默认文件扩展名
    
    Returns:
    - 标准化后的绝对路径
    """
    try:
        # 转换为 Path 对象以便更好地处理
        path = Path(file_path)
        
        # 如果是相对路径，转换为绝对路径
        if not path.is_absolute():
            path = path.resolve()
        
        # 确保有正确的扩展名
        if not path.suffix.lower() == default_extension.lower():
            path = path.with_suffix(default_extension)
        
        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        normalized_path = str(path)
        logger.info(f"Path normalized: '{file_path}' -> '{normalized_path}'")
        
        return normalized_path
        
    except Exception as e:
        logger.error(f"Failed to normalize path '{file_path}': {e}")
        raise ValueError(f"无效的文件路径: {file_path}")

def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """
    验证文件路径的有效性
    
    Parameters:
    - file_path: 要验证的文件路径
    
    Returns:
    - (是否有效, 错误信息)
    """
    try:
        path = Path(file_path)
        
        # 检查路径是否为空
        if not file_path.strip():
            return False, "文件路径不能为空"
        
        # 检查路径长度
        if len(file_path) > 260:  # Windows 路径长度限制
            return False, "文件路径过长"
        
        # 检查目录是否可写
        parent_dir = path.parent
        if not parent_dir.exists():
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                return False, f"没有权限创建目录: {parent_dir}"
        
        if not os.access(parent_dir, os.W_OK):
            return False, f"没有写入权限: {parent_dir}"
        
        # 检查文件名是否有效
        filename = path.name
        invalid_chars = '<>:"|?*'
        if any(char in filename for char in invalid_chars):
            return False, f"文件名包含无效字符: {invalid_chars}"
        
        return True, ""
        
    except Exception as e:
        return False, f"路径验证失败: {str(e)}"

def get_safe_file_path(file_path: str, default_extension: str = ".docx") -> str:
    """
    获取安全的文件路径，处理各种边界情况
    
    Parameters:
    - file_path: 原始文件路径
    - default_extension: 默认文件扩展名
    
    Returns:
    - 安全的文件路径
    """
    try:
        # 标准化路径
        normalized_path = normalize_file_path(file_path, default_extension)
        
        # 验证路径
        is_valid, error_msg = validate_file_path(normalized_path)
        if not is_valid:
            raise ValueError(error_msg)
        
        return normalized_path
        
    except Exception as e:
        logger.error(f"Failed to get safe file path: {e}")
        raise

def ensure_file_directory(file_path: str) -> bool:
    """
    确保文件目录存在
    
    Parameters:
    - file_path: 文件路径
    
    Returns:
    - 是否成功创建目录
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory for {file_path}: {e}")
        return False

def get_relative_to_desktop(file_path: str) -> str:
    """
    获取相对于桌面的路径
    
    Parameters:
    - file_path: 原始文件路径
    
    Returns:
    - 相对于桌面的路径
    """
    try:
        desktop = Path.home() / "Desktop"
        path = Path(file_path)
        
        if not path.is_absolute():
            # 如果是相对路径，假设相对于桌面
            return str(desktop / path)
        else:
            return file_path
            
    except Exception as e:
        logger.error(f"Failed to get desktop relative path: {e}")
        return file_path

def get_file_info(file_path: str) -> dict:
    """
    获取文件信息
    
    Parameters:
    - file_path: 文件路径
    
    Returns:
    - 包含文件信息的字典
    """
    try:
        path = Path(file_path)
        
        info = {
            "original_path": file_path,
            "absolute_path": str(path.resolve()),
            "directory": str(path.parent),
            "filename": path.name,
            "extension": path.suffix,
            "exists": path.exists(),
            "is_file": path.is_file() if path.exists() else False,
            "size": path.stat().st_size if path.exists() else 0,
            "parent_exists": path.parent.exists(),
            "parent_writable": os.access(path.parent, os.W_OK) if path.parent.exists() else False,
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Failed to get file info: {e}")
        return {
            "original_path": file_path,
            "error": str(e)
        }
