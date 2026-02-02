@echo off
chcp 65001 >nul
echo ========================================
echo pytesseractエラー修正スクリプト
echo ========================================
echo.

cd /d "%~dp0"

echo [Step 1] 現在のディレクトリを確認...
cd
echo 現在のディレクトリ: %CD%
echo.

echo [Step 2] Gitの状態を確認...
git status
echo.

echo [Step 3] 変更されたファイルを確認...
git status --short
echo.

echo [Step 4] ocr_processor.pyの6行目を確認...
findstr /n "^import" ocr_processor.py | findstr /n "6"
echo.

echo [Step 5] ファイルをステージング...
git add ocr_processor.py
if exist streamlit_app.py (
    git add streamlit_app.py
    echo streamlit_app.pyも追加しました
)
echo.

echo [Step 6] コミット...
git commit -m "Fix: Remove pytesseract import and add streamlit_app.py"
echo.

echo [Step 7] GitHubにプッシュ...
echo 注意: 認証が求められる場合があります
git push origin main
echo.

echo ========================================
echo 完了しました！
echo ========================================
echo.
echo 次のステップ:
echo 1. Streamlit Cloudにアクセス
echo 2. 「Manage app」をクリック
echo 3. 「Reboot app」をクリック
echo 4. アプリをリロードしてエラーが解消されたか確認
echo.
pause
