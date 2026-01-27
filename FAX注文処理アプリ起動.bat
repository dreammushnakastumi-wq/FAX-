@echo off
chcp 65001 >nul 2>&1
title FAX注文処理アプリ

echo ============================================================
echo   FAX注文処理アプリを起動します
echo ============================================================
echo.
echo ブラウザが自動的に開きます
echo 終了する場合は Ctrl+C を押してください
echo ============================================================
echo.

REM バッチファイルのディレクトリに移動
set "BATCH_DIR=%~dp0"
cd /d "%BATCH_DIR%"

REM 必要なファイルの確認
if not exist "fax_order_app.py" (
    echo [エラー] fax_order_app.py が見つかりません。
    echo このバッチファイルを正しいフォルダで実行してください。
    echo.
    pause
    exit /b 1
)

echo 必要なファイルを確認しました。
echo.

REM Pythonの確認
echo Pythonのインストールを確認中...
python --version >nul 2>&1
if errorlevel 1 (
    echo [エラー] Pythonが見つかりません。
    echo Python 3.8以上をインストールしてください: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
) else (
    echo Pythonが見つかりました。
    python --version
)
echo.

REM 仮想環境の確認
if exist venv (
    echo 仮想環境を有効化中...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [警告] 仮想環境の有効化に失敗しました。
        echo グローバル環境で起動を試みます...
        echo.
    ) else (
        echo 仮想環境を有効化しました。
        echo.
    )
) else (
    echo [警告] 仮想環境が見つかりません。
    echo グローバル環境で起動を試みます...
    echo 初回起動の場合は setup.bat を実行してください。
    echo.
)

REM Streamlitの確認
echo Streamlitのインストールを確認中...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [エラー] Streamlitがインストールされていません。
    echo setup.bat を実行してセットアップしてください。
    echo.
    pause
    exit /b 1
) else (
    echo Streamlitがインストールされています。
)
echo.

REM アプリの起動
echo ============================================================
echo アプリを起動中...
echo ============================================================
echo.
echo ブラウザで http://localhost:8501 が開きます
echo 終了する場合は Ctrl+C を押してください
echo.

REM Streamlitを起動（ブラウザを自動で開く）
python -m streamlit run fax_order_app.py

REM エラーハンドリング
if errorlevel 1 (
    echo.
    echo [エラー] アプリの起動に失敗しました。
    echo 上記のエラーメッセージを確認してください。
    echo.
    echo よくある問題:
    echo - setup.bat を実行してセットアップを完了してください
    echo - .streamlit\secrets.toml の設定を確認してください
    echo - ポート8501が既に使用されている場合は、他のアプリを終了してください
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo アプリが終了しました。
    echo.
    pause
)
