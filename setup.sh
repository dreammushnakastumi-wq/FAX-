#!/bin/bash
# FAX注文処理アプリ - セットアップスクリプト（Mac/Linux用）

echo "========================================"
echo "FAX注文処理アプリ - セットアップ"
echo "========================================"
echo ""

# Pythonの確認
echo "[1/4] Pythonのバージョンを確認中..."
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python3がインストールされていません。"
    echo "Python 3.8以上をインストールしてください。"
    exit 1
fi
python3 --version
echo "Pythonが見つかりました。"
echo ""

# 仮想環境の作成
echo "[2/4] 仮想環境を作成中..."
if [ -d "venv" ]; then
    echo "仮想環境は既に存在します。"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "エラー: 仮想環境の作成に失敗しました。"
        exit 1
    fi
    echo "仮想環境を作成しました。"
fi
echo ""

# 依存関係のインストール
echo "[3/4] 依存関係をインストール中..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "エラー: 依存関係のインストールに失敗しました。"
    exit 1
fi
echo "依存関係のインストールが完了しました。"
echo ""

# 設定ファイルの確認
echo "[4/4] 設定ファイルを確認中..."
if [ -f ".streamlit/secrets.toml" ]; then
    echo "設定ファイル（.streamlit/secrets.toml）が存在します。"
else
    echo "警告: 設定ファイル（.streamlit/secrets.toml）が見つかりません。"
    echo ".streamlit/secrets.toml.exampleをコピーして設定してください。"
    if [ -f ".streamlit/secrets.toml.example" ]; then
        cp .streamlit/secrets.toml.example .streamlit/secrets.toml
        echo ".streamlit/secrets.toml.exampleからテンプレートをコピーしました。"
        echo "実際の値を設定してください。"
    fi
fi
echo ""

echo "========================================"
echo "セットアップが完了しました！"
echo "========================================"
echo ""
echo "次のステップ:"
echo "1. .streamlit/secrets.tomlに実際の設定値を入力してください"
echo "2. ./run.sh を実行してアプリを起動してください"
echo ""
