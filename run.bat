@echo off
REM FAX注文処理アプリ - 起動スクリプト（Windows用）
echo ========================================
echo FAX注文処理アプリを起動します...
echo ========================================
echo.

REM 仮想環境の確認
if not exist venv (
    echo エラー: 仮想環境が見つかりません。
    echo まず setup.bat を実行してください。
    pause
    exit /b 1
)

REM 仮想環境を有効化してアプリを起動
call venv\Scripts\activate.bat
echo アプリを起動中...
echo ブラウザで http://localhost:8501 が自動的に開きます。
echo 終了する場合は Ctrl+C を押してください。
echo.
streamlit run fax_order_app.py
