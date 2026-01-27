# FAX注文書自動処理システム

FAX注文書をPDFとして受け取り、OCRとAIを使用して自動的に構造化データを抽出し、Googleスプレッドシートに保存するWebアプリケーションです。

## 特徴

- **OCR処理**: Google Document AIを使用した高精度なテキスト抽出
- **AI抽出**: Claude/GPT-4を使用した構造化データ抽出
- **自動保存**: Googleスプレッドシートへの自動保存
- **編集機能**: 抽出結果を編集してから保存可能
- **複数ファイル対応**: 最大10ファイルまで同時処理
- **ページ分割対応**: 複数ページのPDFを自動的に分割処理

## クイックスタート

### 最短で起動する方法

1. **Streamlit Cloud（推奨）**
   - `QUICK_START.md` を参照
   - ブラウザからどこでもアクセス可能

2. **ローカル実行**
   ```powershell
   # Windows
   .\setup.bat
   .\run.bat
   
   # Mac/Linux
   ./setup.sh
   ./run.sh
   ```

詳細は `QUICK_START.md` を参照してください。

## セットアップ方法

### 必要なもの

- Python 3.8以上
- Google Cloud Platformアカウント（Document AI API使用）
- Claude APIキーまたはOpenAI APIキー
- Googleスプレッドシート

### 詳細なセットアップ手順

- `SETUP_GUIDE.md` - 包括的なセットアップガイド
- `DEPLOYMENT.md` - Streamlit Cloudへのデプロイ手順
- `GITHUB_SETUP.md` - GitHubリポジトリの作成とプッシュ手順

## ファイル構成

```
fax_order/
├── fax_order_app.py          # メインアプリケーション
├── ocr_processor.py          # OCR処理モジュール
├── ai_extractor.py           # AI抽出モジュール
├── google_sheets.py          # Googleスプレッドシート連携モジュール
├── requirements.txt          # 依存関係
├── setup.bat                 # Windows用セットアップスクリプト
├── run.bat                   # Windows用起動スクリプト
├── setup.sh                  # Mac/Linux用セットアップスクリプト
├── run.sh                    # Mac/Linux用起動スクリプト
├── .streamlit/
│   ├── config.toml           # Streamlit設定
│   └── secrets.toml.example  # 設定テンプレート
├── README.md                 # このファイル
├── QUICK_START.md            # クイックスタートガイド
├── SETUP_GUIDE.md            # セットアップガイド
├── DEPLOYMENT.md             # デプロイ手順
├── GITHUB_SETUP.md           # GitHub設定手順
└── RESTORE_GUIDE.md          # 状態を戻す手順
```

## 使い方

1. **システム初期化**
   - サイドバーから「システム初期化」をクリック
   - 必要な設定が完了していることを確認

2. **ファイルアップロード**
   - PDFファイルをアップロード（最大10ファイル）

3. **処理開始**
   - 「処理開始」ボタンをクリック
   - OCR処理とAI抽出が自動実行されます

4. **結果の確認と編集**
   - 抽出結果が表形式で表示されます
   - 必要に応じて編集できます

5. **スプレッドシートに保存**
   - 「スプレッドシートに保存」ボタンをクリック
   - 確認メッセージが表示されたら「はい、保存します」をクリック

## 他のPCで使用する方法

### Streamlit Cloudを使用（推奨）

1. GitHubリポジトリにプッシュ（`GITHUB_SETUP.md`を参照）
2. Streamlit Cloudにデプロイ（`DEPLOYMENT.md`を参照）
3. 発行されたURLを他のPCからアクセス

**メリット**: 
- ブラウザからどこでもアクセス可能
- 修正をGitHubにプッシュするだけで自動反映
- サーバー管理不要

### ローカル実行

1. GitHubからリポジトリをクローン
2. `setup.bat`（Windows）または `setup.sh`（Mac/Linux）を実行
3. `.streamlit/secrets.toml` に設定を入力
4. `run.bat`（Windows）または `run.sh`（Mac/Linux）で起動

## 修正の反映方法

### Streamlit Cloudの場合

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git add .
git commit -m "修正内容の説明"
git push origin main
```

GitHubにプッシュすると、Streamlit Cloudが自動的に変更を検知してデプロイします。

### ローカル実行の場合

ファイルを編集して、アプリを再起動してください。

## トラブルシューティング

- `QUICK_START.md` - よくある質問
- `SETUP_GUIDE.md` - トラブルシューティングセクション

## 状態を戻す方法

以前の状態に戻したい場合は、`RESTORE_GUIDE.md` を参照してください。

## ライセンス

このプロジェクトは個人利用を目的としています。

## サポート

問題が発生した場合は、以下のドキュメントを参照してください：

- `SETUP_GUIDE.md` - 包括的なセットアップガイド
- `DEPLOYMENT.md` - デプロイに関する詳細
- `QUICK_START.md` - クイックスタートとFAQ
