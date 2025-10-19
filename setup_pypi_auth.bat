@echo off
REM 帮助配置PyPI认证的脚本

echo.
echo ================================================
echo   PyPI 认证配置助手
echo ================================================
echo.
echo 此脚本将帮助你配置PyPI认证
echo.

REM 检查.pypirc是否存在
set PYPIRC=%USERPROFILE%\.pypirc

if exist "%PYPIRC%" (
    echo [信息] 找到现有的 .pypirc 文件
    echo 位置: %PYPIRC%
    echo.
    set /p overwrite="是否要覆盖现有配置? (yes/no): "
    if not "%overwrite%"=="yes" (
        echo [取消] 保持现有配置不变
        pause
        exit /b 0
    )
)

echo.
echo ================================================
echo   获取PyPI API令牌
echo ================================================
echo.
echo 请按照以下步骤操作:
echo.
echo 1. 访问 PyPI 网站:
echo    https://pypi.org/account/login/
echo.
echo 2. 登录你的PyPI账号
echo    (如果没有账号，请先注册)
echo.
echo 3. 创建API令牌:
echo    https://pypi.org/manage/account/token/
echo.
echo 4. 点击 "Add API token" 按钮
echo.
echo 5. 填写令牌信息:
echo    - Token name: docx-mcp-upload
echo    - Scope: Entire account (首次上传)
echo.
echo 6. 点击 "Add token" 并复制生成的令牌
echo    格式: pypi-AgEIcHlwaS5vcmcC...
echo.
echo ================================================
echo.

set /p token="请粘贴你的PyPI API令牌: "

if "%token%"=="" (
    echo.
    echo [错误] 令牌不能为空
    pause
    exit /b 1
)

REM 检查令牌格式
echo %token% | findstr /C:"pypi-" >nul
if errorlevel 1 (
    echo.
    echo [警告] 令牌格式可能不正确
    echo 正确格式应该以 "pypi-" 开头
    echo.
    set /p continue="是否继续? (yes/no): "
    if not "%continue%"=="yes" (
        echo [取消] 配置已取消
        pause
        exit /b 0
    )
)

REM 创建.pypirc文件
echo.
echo [创建] 正在创建 .pypirc 配置文件...
echo.

(
echo [distutils]
echo index-servers =
echo     pypi
echo.
echo [pypi]
echo username = __token__
echo password = %token%
) > "%PYPIRC%"

if errorlevel 1 (
    echo.
    echo [错误] 创建配置文件失败
    pause
    exit /b 1
)

echo [成功] 配置文件已创建！
echo 位置: %PYPIRC%
echo.

REM 验证配置
echo ================================================
echo   验证配置
echo ================================================
echo.
echo 配置文件内容:
echo ------------------------------------------------
type "%PYPIRC%"
echo ------------------------------------------------
echo.

echo ✅ 认证配置完成！
echo.
echo ================================================
echo   下一步操作
echo ================================================
echo.
echo 现在你可以上传包到PyPI了:
echo.
echo   python -m twine upload dist/*
echo.
echo 或使用上传脚本:
echo.
echo   upload_to_pypi.bat
echo.
echo ================================================
echo.

set /p upload_now="是否现在就上传? (yes/no): "

if "%upload_now%"=="yes" (
    echo.
    echo [上传] 开始上传到PyPI...
    echo ================================================
    python -m twine upload dist/*
    
    if errorlevel 0 (
        echo.
        echo ✅ 上传成功！
        echo.
        echo 查看你的包:
        echo https://pypi.org/project/docx-mcp/
        echo.
        echo 测试安装:
        echo pip install docx-mcp==0.1.5
    ) else (
        echo.
        echo ❌ 上传失败，请检查错误信息
    )
) else (
    echo.
    echo [提示] 稍后你可以手动上传:
    echo   python -m twine upload dist/*
)

echo.
pause

