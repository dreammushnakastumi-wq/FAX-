#!/bin/bash
# FAX注文処理アプリ - 起動スクリプト（Mac/Linux用）

echo "========================================"
echo "FAX注文処理アプリを起動します..."
echo "========================================"
echo ""

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "エラー: 仮想環境が見つかりません。"
    echo "まず ./setup.sh を実行してください。"
    exit 1
fi

# 仮想環境を有効化してアプリを起動
source venv/bin/activate
echo "アプリを起動中..."
echo "ブラウザで http://localhost:8501 が自動的に開きます。"
echo "終了する場合は Ctrl+C を押してください。"
echo ""
streamlit run fax_order_app.py
