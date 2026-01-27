@echo off
chcp 65001 >nul 2>&1
title デスクトップショートカット作成

echo ============================================================
echo   FAX注文処理アプリ - デスクトップショートカット作成
echo ============================================================
echo.

REM PowerShellスクリプトを使用してショートカットを作成
set "BATCH_DIR=%~dp0"
set "SHORTCUT_NAME=FAX注文処理アプリ起動"
set "TARGET_PATH=%BATCH_DIR%FAX注文処理アプリ起動.bat"
set "DESKTOP=%USERPROFILE%\Desktop"

echo ショートカットを作成中...
echo 対象: %TARGET_PATH%
echo 保存先: %DESKTOP%\%SHORTCUT_NAME%.lnk
echo.

REM バッチファイルをデスクトップにコピー
echo デスクトップにバッチファイルをコピー中...
robocopy "%~dp0" "%USERPROFILE%\Desktop" "FAX注文処理アプリ起動.bat" /NP /NFL /NDL >nul 2>&1
if exist "%USERPROFILE%\Desktop\FAX注文処理アプリ起動.bat" (
    echo デスクトップに起動用バッチファイルをコピーしました。
    set "RESULT=OK"
) else (
    echo [警告] 自動コピーに失敗しました。
    echo.
    echo 手動で以下のファイルをデスクトップにコピーしてください:
    echo %TARGET_PATH%
    echo.
    echo または、このフォルダから「FAX注文処理アプリ起動.bat」を
    echo 右クリックして「送る」→「デスクトップ（ショートカットを作成）」を選択してください。
    set "RESULT=MANUAL"
)

echo.
echo ============================================================
if "%RESULT%"=="OK" (
    echo 完了！
    echo ============================================================
    echo.
    echo デスクトップに「FAX注文処理アプリ起動.bat」をコピーしました。
    echo このファイルをダブルクリックすると、アプリが起動します。
) else (
    echo 手動でのコピーが必要です
    echo ============================================================
    echo.
    echo 上記の手順に従って、バッチファイルをデスクトップに配置してください。
)
echo.
pause
