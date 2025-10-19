from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docx-mcp",
    version="0.1.6",
    author="rockcj",
    author_email="support@docx-mcp.com",
    description="DOCX MCP处理器 - 完整的Word文档处理工具，支持图片编辑和表格操作",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rockcj/Docx_MCP_cj",
    project_urls={
        "Homepage": "https://github.com/rockcj/Docx_MCP_cj",
        "Documentation": "https://github.com/rockcj/Docx_MCP_cj/blob/main/README_Enhanced.md",
        "Repository": "https://github.com/rockcj/Docx_MCP_cj.git",
        "Issues": "https://github.com/rockcj/Docx_MCP_cj/issues",
        "Changelog": "https://github.com/rockcj/Docx_MCP_cj/blob/main/CHANGELOG.md",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="docx, word, document, mcp, ai-tools, document-processing, image-processing, font-management",
    packages=find_packages(exclude=["tests*", "backup_old_files", "__pycache__*"]),
    python_requires=">=3.8",
    install_requires=[
        "python-docx>=1.1.0",
        "mcp>=1.0.0",
        "fastmcp>=0.5.0",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "pydantic>=2.5.0",
        "typing-extensions>=4.8.0",
    ],
    extras_require={
        "cloud": [
            "oss2>=2.18.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
            "colorlog>=6.7.0",
        ],
        "all": [
            "oss2>=2.18.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
            "colorlog>=6.7.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "docx-mcp=final_complete_server:main",
            "docx-interactive=final_complete_server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)