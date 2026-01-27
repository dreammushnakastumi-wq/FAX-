@echo off
chcp 65001 >nul 2>&1
title GitHubにプッシュ

echo ============================================================
echo   GitHubにプッシュ
echo ============================================================
echo.

REM 現在のディレクトリに移動
cd /d "%~dp0"

REM リモートが設定されているか確認
git remote -v >nul 2>&1
if errorlevel 1 (
    echo [エラー] リモートリポジトリが設定されていません。
    echo まず connect_to_github.bat を実行してください。
    echo.
    pause
    exit /b 1
)

echo リモートリポジトリを確認中...
git remote -v
echo.

REM ブランチ名を確認
git branch --show-current | findstr main >nul 2>&1
if errorlevel 1 (
    echo ブランチ名をmainに変更中...
    git branch -M main
)

echo.
echo GitHubにプッシュ中...
echo 初回プッシュ時、認証が求められる場合があります。
echo Personal Access Tokenを使用してください。
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo [エラー] プッシュに失敗しました。
    echo.
    echo 認証エラーの場合:
    echo 1. GitHub > Settings > Developer settings > Personal access tokens
    echo 2. 「Generate new token (classic)」でトークンを作成
    echo 3. スコープで「repo」にチェック
    echo 4. パスワードの代わりにトークンを入力
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo プッシュが完了しました！
echo ============================================================
echo.
echo 次のステップ:
echo 1. GitHubのリポジトリページでファイルが表示されているか確認
echo 2. Streamlit Cloudにデプロイ（DEPLOYMENT.mdを参照）
echo.
pause
