@echo off
REM FAX注文処理アプリ - セットアップスクリプト（Windows用）
echo ========================================
echo FAX注文処理アプリ - セットアップ
echo ========================================
echo.

REM Pythonの確認
echo [1/4] Pythonのバージョンを確認中...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo エラー: Pythonがインストールされていません。
    echo Python 3.8以上をインストールしてください: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo Pythonが見つかりました。
echo.

REM 仮想環境の作成
echo [2/4] 仮想環境を作成中...
if exist venv (
    echo 仮想環境は既に存在します。
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo エラー: 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
    echo 仮想環境を作成しました。
)
echo.

REM 依存関係のインストール
echo [3/4] 依存関係をインストール中...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo エラー: 依存関係のインストールに失敗しました。
    pause
    exit /b 1
)
echo 依存関係のインストールが完了しました。
echo.

REM 設定ファイルの確認
echo [4/4] 設定ファイルを確認中...
if exist .streamlit\secrets.toml (
    echo 設定ファイル（.streamlit\secrets.toml）が存在します。
) else (
    echo 警告: 設定ファイル（.streamlit\secrets.toml）が見つかりません。
    echo .streamlit\secrets.toml.exampleをコピーして設定してください。
    copy .streamlit\secrets.toml.example .streamlit\secrets.toml >nul 2>&1
    if %errorlevel% equ 0 (
        echo .streamlit\secrets.toml.exampleからテンプレートをコピーしました。
        echo 実際の値を設定してください。
    )
)
echo.

echo ========================================
echo セットアップが完了しました！
echo ========================================
echo.
echo 次のステップ:
echo 1. .streamlit\secrets.tomlに実際の設定値を入力してください
echo 2. run.batを実行してアプリを起動してください
echo.
pause
