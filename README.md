# DOCX MCP Service

A powerful Word document processing MCP service that provides document structure extraction, content modification, cloud storage integration and other complete document processing solutions. Supports downloading documents from URLs, batch content modification, automatic upload to Alibaba Cloud OSS, and is fully compatible with the MCP protocol for seamless integration into various AI assistants.

## 🚀 Service Features

- **📄 Document Structure Extraction**: Intelligently parse .docx files, extract structured content such as paragraphs and tables, and assign unique IDs to each element
- **✏️ Batch Content Modification**: Support precise text replacement and content updates based on element IDs
- **📊 Advanced Table Operations**: Comprehensive table manipulation including adding/deleting rows/columns, formatting styles, and cell customization
- **🎨 Table Formatting**: Support table border styles, colors, column widths, cell alignment, fonts, and background colors
- **☁️ Cloud Storage Integration**: Automatically upload modified documents to Alibaba Cloud OSS with convenient download links
- **🔗 URL Document Processing**: Directly download, process and re-upload documents from network URLs
- **🛠️ MCP Standard Compliance**: Fully compliant with Model Context Protocol specifications, supporting standard MCP clients

## 📋 System Requirements

- Python 3.13+
- uvx (Python package manager, recommended)

## 🔧 Service Configuration

### Server config

```json
{
  "command": "uvx",
  "args": ["docx-mcp"]
}
```

> **⚠️ Deployment Requirements**: 
> - Package must be published to PyPI before deployment on third-party platforms
> - Use `python publish.py` to publish package to PyPI
> - After publishing, third-party platforms can automatically download and deploy the service

### Local Development Configuration

For local development or testing, you can use:

```json
{
  "command": "uvx",
  "args": ["--from", ".", "docx-mcp"]
}
```

## 🛠️ Available Tools

### Basic Document Operations

#### 1. extract_document_structure
Download and parse .docx file structure from URL

**Parameters:**
- `document_url` (string): URL link to the .docx file

**Returns:** Dictionary containing document structure with each element having a unique ID

#### 2. apply_modifications_to_document  
Apply modifications to .docx files

**Parameters:**
- `original_file_content_base64` (string): Base64 encoding of the original file
- `patches_json` (string): JSON format modification instruction list

**Returns:** Base64 encoding of the modified file

#### 3. get_modified_document
Get modified document (alias for apply_modifications_to_document)

**Parameters:** Same as apply_modifications_to_document

#### 4. prepare_document_for_download
Upload modified document to Alibaba Cloud OSS

**Parameters:**
- `original_file_content_base64` (string): Base64 encoding of the original file  
- `patches_json` (string): JSON format modification instructions

**Returns:** Dictionary containing upload results and download links

#### 5. process_document_from_url
Complete workflow to download document from URL, apply modifications, and upload to OSS

**Parameters:**
- `document_url` (string): URL of the original document
- `patches_json` (string): JSON format modification instructions

**Returns:** Dictionary containing processing results and download links

### Advanced Table Operations

#### 6. modify_table_structure
Comprehensive table structure modification operations

**Parameters:**
- `document_url` (string): URL of the original document
- `table_operations_json` (string): JSON array of table operation instructions

**Returns:** Dictionary containing processing results and download links

#### 7. add_table_row
Add new row to specified table

**Parameters:**
- `document_url` (string): Document URL
- `table_id` (string): Table ID (e.g., "tbl_0")
- `row_index` (int, optional): Insert position, null for append
- `cell_data` (List[str], optional): Cell data for new row

#### 8. add_table_column
Add new column to specified table

**Parameters:**
- `document_url` (string): Document URL
- `table_id` (string): Table ID (e.g., "tbl_0")
- `column_index` (int, optional): Insert position, null for append
- `cell_data` (List[str], optional): Cell data for new column

#### 9. delete_table_row
Delete specified table row

**Parameters:**
- `document_url` (string): Document URL
- `table_id` (string): Table ID (e.g., "tbl_0")
- `row_index` (int): Row index to delete

#### 10. delete_table_column
Delete specified table column

**Parameters:**
- `document_url` (string): Document URL
- `table_id` (string): Table ID (e.g., "tbl_0")
- `column_index` (int): Column index to delete

#### 11. format_table_style
Format table appearance and layout

**Parameters:**
- `document_url` (string): Document URL
- `table_id` (string): Table ID (e.g., "tbl_0")
- `border_style` (string): Border style ("none", "single", "double", "thick", "thin")
- `border_color` (string): Border color (hex code, e.g., "#000000")
- `width` (string, optional): Table width (e.g., "100%")
- `column_widths` (List[str], optional): Column widths (e.g., ["2cm", "3cm"])

#### 12. format_table_cell
Format individual cell appearance

**Parameters:**
- `document_url` (string): Document URL
- `table_id` (string): Table ID (e.g., "tbl_0")
- `cell_id` (string): Cell ID (e.g., "tbl_0_r0c1")
- `alignment` (string, optional): Text alignment ("left", "center", "right", "justify")
- `bold` (bool, optional): Bold text
- `italic` (bool, optional): Italic text
- `font_size` (int, optional): Font size
- `font_name` (string, optional): Font family
- `background_color` (string, optional): Background color (hex code)
- `text_color` (string, optional): Text color (hex code)

## 📝 Usage Examples

### Basic Content Modification Format

```json
[
  {
    "element_id": "p_0",
    "new_content": "New paragraph content"
  },
  {
    "element_id": "tbl_0_r0c0", 
    "new_content": "New table cell content"
  }
]
```

### Table Operations Format

```json
[
  {
    "operation_type": "add_row",
    "table_id": "tbl_0",
    "row_index": 1,
    "cell_data": ["New Row Data 1", "New Row Data 2", "New Row Data 3"]
  },
  {
    "operation_type": "format_table",
    "table_id": "tbl_0",
    "table_format": {
      "border_style": "double",
      "border_color": "#FF0000",
      "column_widths": ["3cm", "4cm", "5cm"]
    }
  },
  {
    "operation_type": "format_cell",
    "table_id": "tbl_0",
    "cell_id": "tbl_0_r0c0",
    "cell_format": {
      "alignment": "center",
      "bold": true,
      "font_size": 14,
      "background_color": "#FFFF00",
      "text_color": "#FF0000"
    }
  }
]
```

### Typical Workflows

#### Basic Document Processing
1. **Extract Document Structure**: Use `extract_document_structure` to get IDs of all elements in the document
2. **Prepare Modification Instructions**: Create modification instruction JSON based on element IDs
3. **Process Document**: Use `process_document_from_url` to complete download, modification, and upload in one step
4. **Get Results**: Retrieve the processed document from the returned download link

#### Advanced Table Operations
1. **Extract Document Structure**: Get table IDs and current structure
2. **Plan Table Modifications**: Determine what rows/columns to add/delete and formatting to apply
3. **Execute Table Operations**: Use table operation tools like `add_table_row`, `format_table_style`, etc.
4. **Download Results**: Get the modified document from the returned download link

#### Complex Table Restructuring
```json
// Example: Comprehensive table modification
[
  {
    "operation_type": "add_column",
    "table_id": "tbl_0",
    "column_index": 2,
    "cell_data": ["New Column", "Data 1", "Data 2"]
  },
  {
    "operation_type": "delete_row",
    "table_id": "tbl_0",
    "row_index": 3
  },
  {
    "operation_type": "format_table",
    "table_id": "tbl_0",
    "table_format": {
      "border_style": "thick",
      "border_color": "#0000FF"
    }
  }
]
```

## 🚀 Quick Start

### Run via uvx (Recommended)

```bash
# Direct run (published to PyPI)
uvx docx-mcp

# Run from local project
uvx --from . docx-mcp
```

### Configure to MCP Client

Add the following configuration to MCP-compatible clients:

```json
{
  "mcpServers": {
      "docx_filler_service": {
        "command": "uvx",
        "args": ["docx-mcp"]
    }
  }
}
```

## ✨ Deployment Advantages

- **🚀 Zero-Config Deployment**: No need to configure environment variables, ready to use out of the box
- **📦 One-Click Installation**: Run directly through uvx with automatic dependency handling
- **🔒 Built-in Configuration**: OSS storage configuration is built-in, simplifying deployment process
- **⚡ Instant Ready**: Immediately ready to process documents after installation

## 📁 Project Structure

```
docx_mcp/
├── core/                    # Core functionality modules
│   ├── docx_processor.py   # Document processor
│   └── models.py           # Data model definitions
├── main.py                 # MCP service main entry point
├── pyproject.toml         # Project configuration and dependency definitions
├── requirements.txt       # Dependency list
├── LICENSE               # MIT license
└── README.md             # Project documentation
```

## 🔧 Technology Stack

- **MCP Framework**: FastMCP - High-performance MCP service framework
- **Document Processing**: python-docx - Office document manipulation library
- **Cloud Storage**: Alibaba Cloud OSS Python SDK
- **Package Management**: uvx/uv - Modern Python package management tools

## 📊 Performance Features

- **Memory Efficient**: Stream processing for large documents, avoiding memory overflow
- **Concurrency Safe**: Support multiple clients accessing simultaneously
- **Error Recovery**: Comprehensive exception handling and error recovery mechanisms
- **Format Compatible**: Support Office 2007+ .docx format
- **Zero Configuration**: Built-in cloud storage configuration, no additional setup required

## 🤝 Contributing Guidelines

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/pydantic/fastmcp)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [Alibaba Cloud OSS Python SDK](https://help.aliyun.com/document_detail/32026.html)

## ❓ Frequently Asked Questions

**Q: Do I need to configure any environment variables?**
A: No! OSS configuration is built into the service, ready to use out of the box.

**Q: What document formats are supported?**
A: Currently only supports .docx format (Office 2007+ format).

**Q: What are the document size limits?**
A: Recommend single documents not exceed 50MB for optimal performance.

**Q: How do I get started?**
A: Simply run `uvx docx-mcp` to start the service, no configuration needed.

**Q: Where are documents stored?**
A: Processed documents are automatically uploaded to pre-configured Alibaba Cloud OSS storage with download links provided.

---

💡 **Tip**: If you have questions or suggestions, welcome to submit Issues or Pull Requests!
