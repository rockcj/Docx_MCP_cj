# 通用表格填充系统 (Universal Table Filler)

一个功能强大的Word文档表格填充系统，支持任意格式的Word表格智能分析和精确填充。基于MCP (Model Context Protocol) 协议，为AI提供完整的Word文档表格处理能力。

## ✨ 主要特性

- **🎯 坐标填充** - 基于精确坐标的表格填充（主要功能）
- **🔍 智能分析** - 自动分析表格结构和字段位置
- **🤖 AI友好** - 提供AI可直接使用的MCP工具接口
- **📄 通用支持** - 支持任意Word表格格式，无需硬编码
- **🔄 完整工作流** - AI可以自主完成整个填充过程
- **📋 文件管理** - 支持文档复制、工作副本创建
- **💾 状态管理** - 智能的文档状态管理和保存机制

## 🚀 快速开始

### 系统要求

- Python 3.8+
- Windows 10/11 (推荐)
- Microsoft Word 或兼容的docx处理库

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd docx_mcp

# 安装依赖
pip install -r requirements.txt
```

### 启动MCP服务器

```bash
python final_complete_server.py
```

服务器启动后将显示：
```
启动最终完整MCP服务器...
功能模块:
- 基础文档管理 (8个工具)
- 智能文档创建 (1个工具)
- 基础文本内容 (4个工具)
- 智能内容处理 (1个工具)
- 基础表格处理 (5个工具)
- 表格结构提取 (4个工具)
- 智能表格处理 (2个工具)
- 智能规划指导 (3个工具)
- 基础图片处理 (3个工具)
- 基础页面设置 (3个工具)
- 智能建议 (1个工具)
- 系统状态 (3个工具)

总计: 42个工具 (32个基础工具 + 10个智能工具)
```

## 🎯 核心功能

### 1. 坐标填充工作流程

这是系统的核心功能，提供精确的表格填充能力：

```python
# 1. 分析文档结构，提取坐标信息
analysis = extract_fillable_fields("实习鉴定表.docx")

# 2. 根据分析结果创建填充计划
fill_plan = {
    "张三": [1, 0, 2],           # 表格1, 行0, 列2 (姓名字段右侧)
    "2024001234": [1, 1, 2],     # 表格1, 行1, 列2 (学号字段右侧)
    "计算机学院": [1, 0, 4],      # 表格1, 行0, 列4 (学院字段右侧)
    "软件工程专业": [1, 0, 6],    # 表格1, 行0, 列6 (专业字段右侧)
    "腾讯科技有限公司": [1, 1, 4], # 表格1, 行1, 列4 (实习单位字段右侧)
    "2024年7月-9月": [1, 1, 6]    # 表格1, 行1, 列6 (实习时间字段右侧)
}

# 3. 执行精确填充
result = fill_with_coordinates("实习鉴定表.docx", fill_plan)
```

### 2. 智能分析功能

系统会自动分析文档结构，识别：
- 字段名称和位置
- 可填充的空位坐标
- 填充规则和建议
- AI判断指导信息

### 3. 文件管理功能

```python
# 创建文档副本
copy_document("原始文档.docx", "工作副本.docx")

# 创建工作副本
create_work_copy("实习鉴定表.docx", "_填写版")
```

## 📋 完整的MCP工具列表

### 基础文档管理 (8个工具)
- `create_document()` - 创建新文档
- `open_document()` - 打开现有文档
- `save_document()` - 保存当前文档
- `save_as_document()` - 另存为文档
- `copy_document()` - 复制文档文件
- `create_work_copy()` - 创建工作副本
- `close_document()` - 关闭文档
- `get_document_info()` - 获取文档信息

### 表格处理工具 (13个工具)
- `extract_fillable_fields()` - 提取可填充字段坐标
- `fill_with_coordinates()` - 执行精确坐标填充
- `basic_table_fill()` - 基础表格填充
- `intelligent_table_fill()` - 智能填充引导
- `add_table()` - 添加表格
- `add_table_row()` - 添加表格行
- `add_table_column()` - 添加表格列
- `format_table()` - 格式化表格
- `merge_table_cells()` - 合并表格单元格
- `extract_table_structure()` - 提取表格结构
- `extract_all_tables_structure()` - 提取所有表格结构

### 内容处理工具 (9个工具)
- `add_paragraph()` - 添加段落
- `add_heading()` - 添加标题
- `add_text_with_formatting()` - 添加格式化文本
- `search_and_replace()` - 搜索和替换
- `smart_add_content()` - 智能添加内容
- `intelligent_create_document()` - 智能创建文档
- `intelligent_create_table()` - 智能创建表格

### 其他工具 (12个工具)
- `add_image()` - 添加图片
- `extract_images()` - 提取图片
- `resize_image()` - 调整图片大小
- `set_page_margins()` - 设置页面边距
- `set_page_orientation()` - 设置页面方向
- `set_page_size()` - 设置页面大小
- `get_smart_suggestions()` - 获取智能建议
- `get_system_status()` - 获取系统状态
- `test_connection()` - 测试连接
- `get_server_info()` - 获取服务器信息

## 📊 系统优势

### ✅ 精确控制
- 基于3D坐标系统 `(表格索引, 行索引, 列索引)`
- 100%精确的填充位置控制
- 支持合并单元格的智能处理

### ✅ 通用性强
- 支持任意Word表格格式
- 无需硬编码字段映射
- 自动识别表格结构和字段类型

### ✅ AI友好
- 提供AI可直接使用的MCP工具接口
- 智能的填充建议和AI判断指导
- 清晰的工作流程和错误处理

### ✅ 易于使用
- 简单的三步工作流程：分析 → 规划 → 填充
- 详细的使用说明和示例
- 完善的错误处理和日志记录

### ✅ 高可靠性
- 智能的文档状态管理
- 自动的文件锁定处理
- 完整的保存和恢复机制

## 🔧 技术架构

### 核心组件

```
docx_mcp/
├── core/                                    # 核心组件
│   ├── intelligent_table_analyzer.py        # 智能表格分析器
│   ├── universal_table_filler.py            # 通用表格填充器
│   ├── table_structure_extractor.py         # 表格结构提取器
│   ├── intelligent_tool_planner.py          # 智能工具规划器
│   ├── smart_suggestion_engine.py           # 智能建议引擎
│   ├── enhanced_state_manager.py            # 增强状态管理器
│   ├── ai_guidance_enhancer.py              # AI指导增强器
│   ├── workflow_engine.py                   # 工作流引擎
│   ├── template_engine.py                   # 模板引擎
│   ├── json_validation_engine.py            # JSON验证引擎
│   ├── font_processor.py                    # 字体处理器
│   ├── image_processor.py                   # 图片处理器
│   ├── oss_processor.py                     # OSS处理器
│   ├── file_path_utils.py                   # 文件路径工具
│   ├── fixed_docx_processor.py              # 修复的docx处理器
│   ├── enhanced_docx_processor.py           # 增强docx处理器
│   ├── ai_interface.py                      # AI接口
│   ├── docx_processor.py                    # docx处理器
│   ├── state_machine.py                     # 状态机
│   ├── state_manager.py                     # 状态管理器
│   └── models.py                            # 数据模型
├── templates/                               # 模板文件
│   └── academic/                            # 学术模板
│       └── academic_paper_simple.json       # 学术论文简单模板
├── tests/                                   # 测试文件
│   ├── test_universal_table_filler.py       # 通用表格填充器测试
│   ├── test_intelligent_analyzer.py         # 智能分析器测试
│   ├── test_table_structure_extractor.py    # 表格结构提取器测试
│   ├── test_intelligent_tool_planner.py     # 智能工具规划器测试
│   ├── test_smart_suggestion_engine.py      # 智能建议引擎测试
│   ├── test_enhanced_state_manager.py       # 增强状态管理器测试
│   ├── test_ai_guidance_enhancer.py         # AI指导增强器测试
│   ├── test_workflow_engine.py              # 工作流引擎测试
│   ├── test_template_engine.py              # 模板引擎测试
│   ├── test_json_validation_engine.py       # JSON验证引擎测试
│   ├── test_font_processor.py               # 字体处理器测试
│   ├── test_image_processor.py              # 图片处理器测试
│   ├── test_oss_processor.py                # OSS处理器测试
│   └── test_integration.py                  # 集成测试
├── docs/                                    # 测试文档
│   ├── 附件7：岭南师范学院毕业（生产）实习鉴定表A3打印.docx
│   ├── 附件11：岭南师范学院专业实习优秀实习生登记表.docx
│   └── ... (其他测试文档)
├── final_complete_server.py                 # 主MCP服务器
├── requirements.txt                         # 依赖文件
├── pyproject.toml                          # 项目配置
├── README.md                               # 项目说明
├── LICENSE                                 # 许可证
└── COMPREHENSIVE_PROJECT_DOCUMENTATION.md  # 完整项目文档
```

### 数据流程

```
文档输入 → 结构分析 → 字段识别 → 坐标提取 → 填充规划 → 精确填充 → 文档保存
    ↓         ↓         ↓         ↓         ↓         ↓         ↓
   .docx → 表格结构 → 字段位置 → 3D坐标 → 填充计划 → 内容写入 → 保存完成
```

## 🎯 使用示例

### 示例1：填写实习鉴定表

```python
# 1. 打开文档
open_document("实习鉴定表.docx")

# 2. 分析文档结构
analysis = extract_fillable_fields("实习鉴定表.docx")
print("字段坐标:", analysis['field_coordinates'])
print("填充建议:", analysis['fill_suggestions'])

# 3. 创建填充计划
fill_plan = {
    "张三": [1, 0, 2],                    # 姓名
    "2024001234": [1, 1, 2],              # 学号
    "计算机学院": [1, 0, 4],               # 学院
    "软件工程专业2021级1班": [1, 0, 6],     # 专业班别
    "腾讯科技有限公司": [1, 1, 4],          # 实习单位
    "2024年7月-2024年9月": [1, 1, 6]       # 实习时间
}

# 4. 执行填充
result = fill_with_coordinates("实习鉴定表.docx", fill_plan)
print("填充结果:", result)

# 5. 保存文档
save_document()
```

### 示例2：智能填充

```python
# 使用智能填充功能（自动匹配字段）
fill_data = {
    "姓名": "张三",
    "学号": "2024001234",
    "学院": "计算机学院",
    "专业": "软件工程专业",
    "实习单位": "腾讯科技有限公司",
    "实习时间": "2024年7月-2024年9月"
}

result = basic_table_fill("实习鉴定表.docx", fill_data)
print("智能填充结果:", result)
```

### 示例3：文档管理

```python
# 创建文档副本
copy_result = copy_document(
    "原始文档.docx", 
    "工作副本.docx"
)

# 创建工作副本
work_copy = create_work_copy(
    "实习鉴定表.docx", 
    "_填写版"
)

# 打开工作副本
open_document("实习鉴定表_填写版.docx")

# 进行填充操作...

# 保存并关闭
save_document()
close_document()
```

## 🔍 坐标系统说明

### 3D坐标格式
- **格式**: `[表格索引, 行索引, 列索引]`
- **表格索引**: 从0开始，表示文档中的第几个表格
- **行索引**: 从0开始，表示表格中的第几行
- **列索引**: 从0开始，表示表格中的第几列

### 填充规则
1. **字段右侧填充**: 字段值通常填在字段名的右侧，即 `(z, x, y+1)`
2. **字段下方填充**: 某些情况下填在字段名的下方，即 `(z, x+1, y)`
3. **AI判断指导**: 系统会提供AI判断指导，帮助决定是否覆盖现有内容

### 示例坐标
```python
# 表格1的基本信息填充
"张三": [1, 0, 2],           # 姓名字段右侧
"计算机学院": [1, 0, 4],      # 学院字段右侧
"2024001234": [1, 1, 2],     # 学号字段右侧
"腾讯科技有限公司": [1, 1, 4]  # 实习单位字段右侧
```

## 🛠️ 开发指南

### 添加新的填充规则

1. 修改 `core/intelligent_table_analyzer.py` 中的 `_generate_fill_rules` 方法
2. 在 `core/universal_table_filler.py` 中添加新的填充逻辑
3. 更新测试文件验证新功能

### 扩展MCP工具

1. 在 `final_complete_server.py` 中添加新的工具函数
2. 使用 `@mcp.tool()` 装饰器注册工具
3. 更新 `available_tools` 列表

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_universal_table_filler.py
python tests/test_intelligent_analyzer.py

# 运行集成测试
python tests/test_integration.py
```

## 📚 详细文档

查看以下文档获取更多信息：

- [COMPREHENSIVE_PROJECT_DOCUMENTATION.md](COMPREHENSIVE_PROJECT_DOCUMENTATION.md) - 完整项目文档
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结
- [INTELLIGENT_PLANNING_GUIDE.md](INTELLIGENT_PLANNING_GUIDE.md) - 智能规划指南
- [TOOL_USAGE_GUIDE.md](TOOL_USAGE_GUIDE.md) - 工具使用指南

## 🐛 故障排除

### 常见问题

1. **文档被锁定**
   ```bash
   # 解决方案：关闭文档后重新打开
   close_document()
   open_document("文档.docx")
   ```

2. **填充位置错误**
   ```bash
   # 解决方案：检查坐标格式，确保使用 [表格索引, 行索引, 列索引]
   ```

3. **MCP工具未注册**
   ```bash
   # 解决方案：重启MCP服务器
   python final_complete_server.py
   ```

### 调试模式

```bash
# 启用详细日志
export LOG_LEVEL=DEBUG
python final_complete_server.py
```

## 🤝 贡献指南

### 如何贡献

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 代码规范

- 使用 Python 3.8+ 语法
- 遵循 PEP 8 代码风格
- 添加适当的类型注解
- 编写单元测试
- 更新文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [python-docx](https://github.com/python-openxml/python-docx) - Word文档处理库
- [FastMCP](https://github.com/pydantic/fastmcp) - MCP协议实现
- [pydantic](https://github.com/pydantic/pydantic) - 数据验证库

## 📞 支持

如果您遇到问题或有任何建议，请：

1. 查看 [故障排除](#-故障排除) 部分
2. 搜索现有的 [Issues](../../issues)
3. 创建新的 Issue 描述您的问题
4. 联系维护者

---

**注意**: 这是一个功能强大的表格填充系统，专为AI和自动化场景设计。请确保在使用前充分了解系统的功能和限制。