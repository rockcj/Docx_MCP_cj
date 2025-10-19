@echo off
REM 上传到PyPI的Windows批处理脚本

echo.
echo ================================================
echo   DOCX MCP - 上传到PyPI
echo ================================================
echo.

REM 检查dist目录是否存在
if not exist "dist" (
    echo [错误] dist目录不存在，请先运行构建命令
    echo   python -m build
    pause
    exit /b 1
)

REM 检查是否有构建文件
if not exist "dist\docx_mcp-0.1.5-py3-none-any.whl" (
    echo [错误] 找不到wheel文件，请先运行构建命令
    echo   python -m build
    pause
    exit /b 1
)

echo [成功] 找到构建文件:
dir dist\*.whl
dir dist\*.tar.gz
echo.

echo ================================================
echo   上传选项:
echo ================================================
echo   1. 上传到 TestPyPI (测试环境，推荐)
echo   2. 上传到 PyPI (正式环境)
echo   3. 退出
echo ================================================
echo.

set /p choice="请选择 (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo [测试] 上传到 TestPyPI...
    echo ================================================
    python -m twine upload --repository testpypi dist/*
    echo.
    echo [完成] 上传完成！
    echo.
    echo 测试安装命令:
    echo pip install --index-url https://test.pypi.org/simple/ docx-mcp==0.1.5
    echo.
    pause
    exit /b 0
)

if "%choice%"=="2" (
    echo.
    echo [警告] 即将上传到正式PyPI环境
    set /p confirm="确认上传? (yes/no): "
    
    if "%confirm%"=="yes" (
        echo.
        echo [上传] 上传到 PyPI...
        echo ================================================
        python -m twine upload dist/*
        echo.
        echo [完成] 上传完成！
        echo.
        echo 安装命令:
        echo pip install docx-mcp==0.1.5
        echo.
        pause
        exit /b 0
    ) else (
        echo [取消] 取消上传
        pause
        exit /b 0
    )
)

if "%choice%"=="3" (
    echo.
    echo [退出] 再见！
    exit /b 0
)

echo.
echo [错误] 无效选择
pause
exit /b 1

