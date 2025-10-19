# 🔐 PyPI 认证配置指南

## 📊 当前状态

✅ **包已准备好上传！**
- 本地测试：通过 ✅
- 包含42个MCP工具 ✅
- 入口点配置正确 ✅
- Wheel包和源码包都已构建 ✅

❌ **需要配置认证**
- 上传失败原因：缺少有效的PyPI API令牌

---

## 🔑 获取PyPI API令牌

### 步骤1：登录PyPI

访问：https://pypi.org/account/login/

如果还没有账号，需要先注册：https://pypi.org/account/register/

### 步骤2：创建API令牌

1. 登录后，访问：https://pypi.org/manage/account/token/
2. 点击 **"Add API token"** 按钮
3. 填写令牌信息：
   - **Token name**: 例如 "docx-mcp-upload"
   - **Scope**: 
     - 推荐选择 **"Project: docx-mcp"**（首次上传需要先用整个账号权限上传一次）
     - 或者选择 **"Entire account"**（所有项目）
4. 点击 **"Add token"**
5. **重要**：复制生成的令牌（格式：`pypi-AgEIc...`）
   - ⚠️ 这个令牌只会显示一次！
   - 立即保存到安全的地方

### 步骤3：配置.pypirc文件

有两种方式：

#### 方式A：创建/编辑 .pypirc 文件（推荐）

创建或编辑文件：`C:\Users\26818\.pypirc`

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE
```

⚠️ **注意**：将 `pypi-YOUR-API-TOKEN-HERE` 替换为你复制的完整令牌

#### 方式B：使用环境变量

在PowerShell中设置（临时）：
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR-API-TOKEN-HERE"
```

---

## 🚀 上传到PyPI

### 配置完成后，执行上传：

```bash
# 方式1：使用配置文件
python -m twine upload dist/*

# 方式2：交互式输入令牌
python -m twine upload dist/* --username __token__
# 然后输入密码（粘贴你的令牌）

# 方式3：使用脚本
upload_to_pypi.bat
# 选择选项2（上传到PyPI）
```

---

## ✅ 验证上传成功

### 1. 查看PyPI页面
上传成功后，访问：
- https://pypi.org/project/docx-mcp/
- https://pypi.org/project/docx-mcp/0.1.5/

### 2. 测试安装
```bash
# 创建虚拟环境测试
python -m venv test_env
test_env\Scripts\activate

# 安装
pip install docx-mcp==0.1.5

# 验证工具数量
python -c "from final_complete_server import mcp; print(f'工具数量: {len(mcp._tools)}')"
# 应该输出: 工具数量: 42
```

### 3. 验证命令行工具
```bash
# 查看已安装的包
pip show docx-mcp

# 检查入口点
docx-mcp --help
```

---

## 📋 快速操作清单

- [ ] 登录PyPI账号（https://pypi.org/account/login/）
- [ ] 创建API令牌（https://pypi.org/manage/account/token/）
- [ ] 复制令牌（格式：pypi-AgEIc...）
- [ ] 创建/编辑 `C:\Users\26818\.pypirc` 文件
- [ ] 粘贴令牌到配置文件
- [ ] 运行上传命令：`python -m twine upload dist/*`
- [ ] 验证PyPI页面
- [ ] 测试安装：`pip install docx-mcp==0.1.5`
- [ ] 验证工具数量（应该是42个）

---

## 🐛 常见问题

### Q1: 上传失败 - 403 Forbidden
**原因**: API令牌无效或未配置
**解决**: 重新生成令牌，确保正确粘贴到 `.pypirc`

### Q2: 上传失败 - 400 Bad Request (File already exists)
**原因**: 版本0.1.5已经存在
**解决**: 更新版本号（在setup.py和pyproject.toml中）然后重新构建

### Q3: .pypirc文件在哪里？
**Windows**: `C:\Users\你的用户名\.pypirc`
**Linux/Mac**: `~/.pypirc`

### Q4: 如何检查令牌是否正确？
使用verbose模式查看详细信息：
```bash
python -m twine upload dist/* --verbose
```

---

## 📝 .pypirc 文件示例

完整的 `.pypirc` 配置示例（包含TestPyPI和正式PyPI）：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJGFiY2RlZmc...（你的正式PyPI令牌）

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwIkYWJjZGVm...（你的TestPyPI令牌）
```

⚠️ **安全提示**：
- 不要将 `.pypirc` 提交到Git
- 不要分享你的API令牌
- 如果令牌泄露，立即在PyPI上撤销

---

## ✨ 配置完成后的上传命令

```bash
# 上传到正式PyPI
python -m twine upload dist/*

# 如果上传成功，会看到：
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading docx_mcp-0.1.5-py3-none-any.whl
# 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Uploading docx_mcp-0.1.5.tar.gz
# 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# View at:
# https://pypi.org/project/docx-mcp/0.1.5/
```

---

## 🎉 预期结果

上传成功后，全世界的用户都可以：

```bash
# 安装你的包
pip install docx-mcp

# 使用42个MCP工具
python -c "from final_complete_server import mcp; print(mcp._tools.keys())"

# 使用命令行工具
docx-mcp
docx-interactive
```

**本地42个工具 = PyPI 42个工具** ✅

---

需要帮助？
- PyPI帮助文档：https://pypi.org/help/
- Twine文档：https://twine.readthedocs.io/
- 问题反馈：https://github.com/rockcj/Docx_MCP_cj/issues

