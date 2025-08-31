#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片提取和移动功能测试脚本
测试DOCX文档中的图片提取到本地和移动到另一个文档的功能
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.enhanced_docx_processor import EnhancedDocxProcessor

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_source_document():
    """创建包含多张图片的源文档"""
    print("📝 创建包含多张图片的源文档...")
    
    processor = EnhancedDocxProcessor()
    
    # 创建新文档
    doc_path = "../docs/source_document_with_images.docx"
    processor.create_document(doc_path)
    
    # 添加标题
    processor.add_heading("源文档 - 包含多张图片", 1)
    processor.add_paragraph("这个文档包含多张图片，用于测试提取和移动功能")
    
    # 插入第一张图片
    print("📸 插入第一张图片...")
    if os.path.exists("../images/test_image.jpg"):
        result = processor.add_image("../images/test_image.jpg", width="2in", height="1.5in")
        print(f"第一张图片插入结果: {result}")
    else:
        print("⚠️ test_image.jpg 不存在")
    
    # 添加一些文字
    processor.add_paragraph("这是第一张图片下方的文字说明")
    
    # 插入第二张图片
    print("📸 插入第二张图片...")
    if os.path.exists("../images/test_image.png"):
        result = processor.add_image("../images/test_image.png", width="2.5in", height="2in", alignment="center")
        print(f"第二张图片插入结果: {result}")
    else:
        print("⚠️ test_image.png 不存在")
    
    # 添加更多文字
    processor.add_paragraph("这是第二张图片下方的文字说明")
    
    # 插入第三张图片
    print("📸 插入第三张图片...")
    if os.path.exists("../images/test_image.bmp"):
        result = processor.add_image("../images/test_image.bmp", width="3in", height="2.5in")
        print(f"第三张图片插入结果: {result}")
    else:
        print("⚠️ test_image.bmp 不存在")
    
    # 添加结尾文字
    processor.add_paragraph("源文档创建完成")
    
    # 保存文档
    processor.save_document()
    print(f"✅ 源文档已创建: {doc_path}")
    
    return doc_path

def test_image_extraction():
    """测试图片提取功能"""
    print("\n📤 开始测试图片提取功能...")
    
    processor = EnhancedDocxProcessor()
    
    # 打开源文档
    doc_path = "../docs/source_document_with_images.docx"
    if not os.path.exists(doc_path):
        print(f"❌ 源文档不存在: {doc_path}")
        return
    
    processor.open_document(doc_path)
    
    # 检查图片数量
    print("\n🔍 检查源文档中的图片...")
    result = processor.list_images()
    print(f"图片列表: {result}")
    
    # 测试1: 提取单张图片
    print("\n📸 测试1: 提取第一张图片 (索引0)")
    result = processor.extract_image_to_local(0, "../extracted_images", "first_image.jpg")
    print(f"提取结果: {result}")
    
    # 测试2: 提取第二张图片
    print("\n📸 测试2: 提取第二张图片 (索引1)")
    result = processor.extract_image_to_local(1, "../extracted_images", "second_image.png")
    print(f"提取结果: {result}")
    
    # 测试3: 提取第三张图片
    print("\n📸 测试3: 提取第三张图片 (索引2)")
    result = processor.extract_image_to_local(2, "../extracted_images", "third_image.bmp")
    print(f"提取结果: {result}")
    
    # 测试4: 提取所有图片
    print("\n📸 测试4: 提取所有图片")
    result = processor.extract_all_images_to_local("../extracted_images/all_images")
    print(f"提取结果: {result}")
    
    # 检查提取的文件
    print("\n📁 检查提取的文件...")
    extracted_dir = "../extracted_images"
    if os.path.exists(extracted_dir):
        files = os.listdir(extracted_dir)
        print(f"提取目录中的文件: {files}")
        
        # 检查子目录
        all_images_dir = "../extracted_images/all_images"
        if os.path.exists(all_images_dir):
            all_files = os.listdir(all_images_dir)
            print(f"all_images子目录中的文件: {all_files}")

def test_image_movement():
    """测试图片移动功能"""
    print("\n🔄 开始测试图片移动功能...")
    
    processor = EnhancedDocxProcessor()
    
    # 打开源文档
    doc_path = "../docs/source_document_with_images.docx"
    if not os.path.exists(doc_path):
        print(f"❌ 源文档不存在: {doc_path}")
        return
    
    processor.open_document(doc_path)
    
    # 创建目标文档
    print("\n📝 创建目标文档...")
    target_processor = EnhancedDocxProcessor()
    target_doc_path = "../docs/target_document_for_images.docx"
    target_processor.create_document(target_doc_path)
    
    # 添加标题
    target_processor.add_heading("目标文档 - 接收移动的图片", 1)
    target_processor.add_paragraph("这个文档将接收从源文档移动过来的图片")
    
    # 保存目标文档
    target_processor.save_document()
    
    # 测试1: 移动第一张图片
    print("\n📸 测试1: 移动第一张图片 (索引0)")
    result = processor.move_image_to_another_document(
        target_doc_path, 0, width="2.5in", height="2in", alignment="center"
    )
    print(f"移动结果: {result}")
    
    # 测试2: 复制第二张图片（保留在源文档中）
    print("\n📸 测试2: 复制第二张图片 (索引1)")
    result = processor.copy_image_to_another_document(
        target_doc_path, 1, width="3in", height="2.5in", alignment="right"
    )
    print(f"复制结果: {result}")
    
    # 检查源文档是否还有图片
    print("\n🔍 检查源文档中的图片...")
    result = processor.list_images()
    print(f"源文档图片列表: {result}")
    
    # 检查目标文档中的图片
    print("\n🔍 检查目标文档中的图片...")
    target_processor.open_document(target_doc_path)
    result = target_processor.list_images()
    print(f"目标文档图片列表: {result}")
    
    # 保存目标文档
    target_processor.save_document()
    print("✅ 目标文档已保存")

def test_image_copy_without_source():
    """测试在没有源文档的情况下复制图片"""
    print("\n📋 测试在没有源文档的情况下复制图片...")
    
    # 创建一个新的处理器实例
    processor = EnhancedDocxProcessor()
    
    # 尝试复制图片（应该失败）
    print("\n📸 尝试在没有源文档的情况下复制图片...")
    result = processor.copy_image_to_another_document(
        "../docs/test_copy_without_source.docx", 0
    )
    print(f"复制结果: {result}")
    
    # 尝试移动图片（应该失败）
    print("\n📸 尝试在没有源文档的情况下移动图片...")
    result = processor.move_image_to_another_document(
        "../docs/test_move_without_source.docx", 0
    )
    print(f"移动结果: {result}")

def verify_extracted_files():
    """验证提取的文件"""
    print("\n🔬 验证提取的文件...")
    
    # 检查提取的图片文件
    extracted_dirs = ["../extracted_images", "../extracted_images/all_images"]
    
    for dir_path in extracted_dirs:
        if os.path.exists(dir_path):
            print(f"\n📁 目录: {dir_path}")
            files = os.listdir(dir_path)
            for file in files:
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"  📄 {file}: {file_size} 字节")
        else:
            print(f"⚠️ 目录不存在: {dir_path}")

def main():
    """主函数"""
    print("🚀 图片提取和移动功能测试开始")
    print("=" * 70)
    
    # 创建源文档
    doc_path = create_source_document()
    
    # 测试图片提取功能
    test_image_extraction()
    
    # 测试图片移动功能
    test_image_movement()
    
    # 测试边界情况
    test_image_copy_without_source()
    
    # 验证提取的文件
    verify_extracted_files()
    
    print("\n" + "=" * 70)
    print("🎯 图片提取和移动功能测试完成！")
    print("\n📋 生成的文件:")
    print("- ../docs/source_document_with_images.docx (源文档)")
    print("- ../docs/target_document_for_images.docx (目标文档)")
    print("- ../extracted_images/ (提取的图片目录)")
    print("- ../extracted_images/all_images/ (批量提取的图片目录)")
    
    print("\n💡 测试要点:")
    print("1. 图片提取功能应能正确提取各种格式的图片")
    print("2. 图片移动功能应能正确移动图片到目标文档")
    print("3. 图片复制功能应能复制图片而不删除源文档中的图片")
    print("4. 提取的图片应保持原始格式和质量")
    print("5. 边界情况应被正确处理")

if __name__ == "__main__":
    main()
