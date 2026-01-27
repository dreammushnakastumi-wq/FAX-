@echo off
chcp 65001 >nul 2>&1
title GitHubリポジトリ接続

echo ============================================================
echo   GitHubリポジトリへの接続
echo ============================================================
echo.

REM 現在のディレクトリに移動
cd /d "%~dp0"

REM 既存のリモートを確認
echo 現在のリモート設定を確認中...
git remote -v
echo.

REM 既存のリモートがある場合は削除
if exist .git\config (
    findstr /C:"[remote" .git\config >nul 2>&1
    if %errorlevel% equ 0 (
        echo 既存のリモートが見つかりました。
        echo 削除してから新しいリモートを追加します。
        git remote remove origin 2>nul
    )
)

echo GitHubリポジトリのURLを入力してください。
echo 例: https://github.com/あなたのユーザー名/fax-order-processor.git
echo.
set /p REPO_URL="リポジトリURL: "

if "%REPO_URL%"=="" (
    echo [エラー] URLが入力されていません。
    pause
    exit /b 1
)

echo.
echo リモートリポジトリを追加中...
git remote add origin "%REPO_URL%"

if errorlevel 1 (
    echo [エラー] リモートの追加に失敗しました。
    pause
    exit /b 1
)

echo リモートが正常に追加されました。
echo.

REM リモート設定を確認
echo リモート設定を確認:
git remote -v
echo.

echo ============================================================
echo 次のステップ
echo ============================================================
echo.
echo GitHubにプッシュするには、以下のコマンドを実行してください:
echo   git push -u origin main
echo.
echo または、push_to_github.bat を実行してください。
echo.
pause
