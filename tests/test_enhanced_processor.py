#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced DOCX Processor Tests
增强版DOCX处理器测试
"""

import os
import tempfile
import unittest
from pathlib import Path

from core.enhanced_docx_processor import EnhancedDocxProcessor


class TestEnhancedDocxProcessor(unittest.TestCase):
    """增强版DOCX处理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = EnhancedDocxProcessor()
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.docx")
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        # 关闭文档
        try:
            self.processor.close_document()
        except:
            pass
    
    def test_create_document(self):
        """测试创建文档"""
        result = self.processor.create_document(self.test_file)
        self.assertIn("成功", result)
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_add_paragraph(self):
        """测试添加段落"""
        # 先创建文档
        self.processor.create_document(self.test_file)
        
        # 添加段落
        result = self.processor.add_paragraph("测试段落")
        self.assertIn("成功", result)
    
    def test_add_heading(self):
        """测试添加标题"""
        # 先创建文档
        self.processor.create_document(self.test_file)
        
        # 添加标题
        result = self.processor.add_heading("测试标题", 1)
        self.assertIn("标题", result)
    
    def test_add_table(self):
        """测试添加表格"""
        # 先创建文档
        self.processor.create_document(self.test_file)
        
        # 添加表格
        result = self.processor.add_table(3, 3)
        self.assertIn("表格", result)
    
    def test_search_text(self):
        """测试搜索文本"""
        # 先创建文档并添加内容
        self.processor.create_document(self.test_file)
        self.processor.add_paragraph("这是一个测试段落")
        
        # 搜索文本
        result = self.processor.search_text("测试")
        self.assertIn("段落 0", result)
    
    def test_document_info(self):
        """测试获取文档信息"""
        # 先创建文档
        self.processor.create_document(self.test_file)
        
        # 获取文档信息
        result = self.processor.get_document_info()
        self.assertIn("文档路径", result)
    
    def test_no_document_error(self):
        """测试没有打开文档时的错误处理"""
        result = self.processor.add_paragraph("测试")
        self.assertIn("没有打开的文档", result)


if __name__ == "__main__":
    unittest.main()
