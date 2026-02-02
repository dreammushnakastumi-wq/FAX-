@echo off
chcp 65001 >nul 2>&1
title FAX Order Processing App

echo ============================================================
echo   Starting FAX Order Processing App
echo ============================================================
echo.
echo Browser will open automatically
echo Press Ctrl+C to exit
echo ============================================================
echo.

REM バッチファイルのディレクトリに移動
set "BATCH_DIR=%~dp0"
cd /d "%BATCH_DIR%"

REM Check required files
if not exist "fax_order_app.py" (
    echo [ERROR] fax_order_app.py not found.
    echo Please run this batch file in the correct folder.
    echo.
    pause
    exit /b 1
)

echo Required files confirmed.
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Please install Python 3.8 or higher: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
) else (
    echo Python found.
    python --version
)
echo.

REM Check virtual environment
if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [WARNING] Failed to activate virtual environment.
        echo Attempting to start with global environment...
        echo.
    ) else (
        echo Virtual environment activated.
        echo.
    )
) else (
    echo [WARNING] Virtual environment not found.
    echo Attempting to start with global environment...
    echo Please run setup.bat for first-time setup.
    echo.
)

REM Check Streamlit installation
echo Checking Streamlit installation...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [ERROR] Streamlit is not installed.
    echo Please run setup.bat to complete setup.
    echo.
    pause
    exit /b 1
) else (
    echo Streamlit is installed.
)
echo.

REM Start application
echo ============================================================
echo Starting application...
echo ============================================================
echo.
echo Browser will open at http://localhost:8501
echo Press Ctrl+C to exit
echo.

REM Streamlitを起動（ブラウザを自動で開く）
python -m streamlit run fax_order_app.py

REM Error handling
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start application.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo - Run setup.bat to complete setup
    echo - Check .streamlit\secrets.toml configuration
    echo - If port 8501 is already in use, close other applications
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo Application closed.
    echo.
    pause
)
