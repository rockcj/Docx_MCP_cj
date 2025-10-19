# 🔧 上传问题排查指南

## ❌ 当前问题

**错误信息**: `403 Invalid API Token: signatures do not match`

**原因**: PyPI API令牌签名验证失败

## 🔍 可能的原因

1. **令牌不完整**
   - 复制时可能遗漏了开头或结尾的字符
   - 令牌应该很长（通常200+字符）

2. **令牌已过期或被撤销**
   - 检查PyPI账号中令牌是否仍然有效

3. **令牌范围不正确**
   - 如果是首次上传，需要使用"Entire account"范围
   - 项目已存在后可以使用"Project: docx-mcp"范围

## ✅ 解决步骤

### 步骤1：重新生成令牌

1. **登录PyPI**
   - 访问：https://pypi.org/account/login/

2. **删除旧令牌**（如果存在）
   - 访问：https://pypi.org/manage/account/token/
   - 找到 "docx-mcp" 相关的令牌
   - 点击 "Remove" 删除

3. **创建新令牌**
   - 点击 "Add API token"
   - **Token name**: docx-mcp-upload
   - **Scope**: 
     - ✅ 首次上传：选择 "Entire account (all projects)"
     - 📦 已有项目：选择 "Project: docx-mcp"
   - 点击 "Add token"

4. **复制完整令牌**
   - ⚠️ 令牌只显示一次！
   - 从 `pypi-` 开始复制
   - 确保复制到最后一个字符
   - 令牌通常很长（200-250字符）
   - 不要有空格或换行

### 步骤2：配置令牌

有三种方式：

#### 方式A：修改.pypirc文件

编辑 `C:\Users\26818\.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = 你的完整令牌（从pypi-开始）
```

#### 方式B：使用环境变量（推荐临时使用）

在PowerShell中：
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "你的完整令牌"
python -m twine upload dist/*
```

#### 方式C：交互式输入（最安全）

```bash
python -m twine upload dist/*
# 会提示输入:
# Enter your username: __token__
# Enter your password: [粘贴你的完整令牌]
```

### 步骤3：重新上传

```bash
python -m twine upload dist/*
```

## 📋 令牌格式检查清单

- [ ] 令牌以 `pypi-` 开头
- [ ] 令牌长度约200-250字符
- [ ] 没有空格或换行符
- [ ] 没有遗漏开头或结尾的字符
- [ ] 令牌在PyPI账号中显示为活跃状态
- [ ] 令牌的范围包含 docx-mcp 项目或整个账号

## 🧪 验证令牌格式

令牌示例格式（不是真实令牌）：
```
pypi-AgEIcHlwaS5vcmcCJDU0ZDVmNzViLWQyNmMtNGRjYS05ZjAxLTU1N2JlMjJmNzgzZgACEFsxL...很长的字符串...zAa_N-Gdw
```

正确的令牌应该：
- 开头: `pypi-`
- 中间: 大量随机字符（大小写字母、数字、下划线、连字符）
- 结尾: 不固定，但不应该被截断

## ⚠️ 安全提示

1. **不要分享令牌**
   - 令牌=完全访问权限
   - 如果不慎泄露，立即撤销

2. **不要提交到Git**
   - 将 `.pypirc` 加入 `.gitignore`
   - 永远不要提交包含令牌的文件

3. **定期更新令牌**
   - 建议每3-6个月更新一次
   - 长期不使用的令牌应该删除

## 🔄 替代上传方法

如果令牌问题持续存在，可以尝试：

### 方法1：使用GitHub Actions

在GitHub仓库中配置自动发布：
```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  release:
    types: [created]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
    - run: |
        pip install build twine
        python -m build
        twine upload dist/*
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### 方法2：使用PyPI的Web界面

某些情况下可以通过Web界面上传（不常用）。

## 📞 需要帮助？

如果问题仍然存在：

1. **检查PyPI状态**
   - 访问：https://status.python.org/
   - 确认PyPI服务正常

2. **查看PyPI帮助**
   - 访问：https://pypi.org/help/

3. **检查包格式**
   - 运行：`python -m twine check dist/*`
   - 确保没有格式错误

4. **查看详细日志**
   - 运行：`python -m twine upload dist/* --verbose`
   - 检查详细的错误信息

## ✅ 成功标志

上传成功时会看到：

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading docx_mcp-0.1.5-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uploading docx_mcp-0.1.5.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View at:
https://pypi.org/project/docx-mcp/0.1.5/
```

然后可以验证：
```bash
pip install docx-mcp==0.1.5
python -c "from final_complete_server import mcp; print(len(mcp._tools))"
# 应该输出: 42
```

---

**下一步**: 重新生成完整的API令牌，然后重试上传。

