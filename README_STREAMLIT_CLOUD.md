# Streamlit Community Cloud デプロイガイド

このガイドでは、FAX注文書自動処理システムをStreamlit Community Cloudにデプロイする手順を説明します。

## 前提条件

- GitHubアカウント
- Streamlit Community Cloudアカウント（無料）
- Google Cloud Platformアカウント
- Claude APIキーまたはOpenAI APIキー

## ステップ1: GitHubリポジトリの準備

1. このプロジェクトをGitHubリポジトリにプッシュします
2. 以下のファイルがリポジトリに含まれていることを確認：
   - `fax_order_app.py`
   - `ocr_processor.py`
   - `ai_extractor.py`
   - `google_sheets.py`
   - `requirements.txt`
   - `.streamlit/config.toml`

## ステップ2: Google Cloud設定

### 2-1. サービスアカウントの作成

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを選択（または新規作成）
3. 「APIとサービス」→「認証情報」を開く
4. 「認証情報を作成」→「サービスアカウント」を選択
5. サービスアカウント名を入力（例: "fax-processor"）
6. 「作成して続行」をクリック
7. ロールを割り当て：
   - **Document AI API User**
   - **Google Sheets API User**
8. 「完了」をクリック

### 2-2. サービスアカウントキーの取得

1. 作成したサービスアカウントをクリック
2. 「キー」タブ→「キーを追加」→「JSONを作成」
3. **JSONファイルをダウンロード**（後で使用します）

### 2-3. Document AIプロセッサーの作成

1. 「Document AI」→「プロセッサー」を開く
2. 「プロセッサーを作成」をクリック
3. プロセッサータイプ: **「Form Parser」**を選択
4. プロセッサー名を入力
5. リージョン: `asia-northeast1`を選択
6. 「作成」をクリック
7. **プロセッサーIDをコピー**（後で使用します）

### 2-4. Googleスプレッドシートの準備

1. [Googleスプレッドシート](https://docs.google.com/spreadsheets)で新しいスプレッドシートを作成
2. スプレッドシートのURLから**スプレッドシートIDをコピー**
   - URL例: `https://docs.google.com/spreadsheets/d/1tQmBGOeOX--VyZ2Zx/edit`
   - スプレッドシートID: `1tQmBGOeOX--VyZ2Zx`
3. サービスアカウントのメールアドレスにスプレッドシートの編集権限を付与
   - スプレッドシートの「共有」ボタンをクリック
   - サービスアカウントのメールアドレス（例: `fax-processor@your-project.iam.gserviceaccount.com`）を追加
   - 権限: **編集者**を選択

## ステップ3: Streamlit Cloudへのデプロイ

### 3-1. Streamlit Cloudにログイン

1. [Streamlit Community Cloud](https://share.streamlit.io/)にアクセス
2. 「Sign in」をクリックしてGitHubアカウントでログイン

### 3-2. アプリの作成

1. 「New app」をクリック
2. 以下の情報を入力：
   - **Repository**: あなたのGitHubリポジトリを選択
   - **Branch**: `main`（または使用しているブランチ）
   - **Main file path**: `fax_order_app.py`
3. 「Deploy!」をクリック

### 3-3. Secretsの設定

デプロイが開始されたら、Secretsを設定します：

1. アプリの設定画面で「Secrets」タブを開く
2. 以下のSecretsを追加：

```toml
GOOGLE_SHEETS_ID = "あなたのスプレッドシートID"
DOCUMENT_AI_PROJECT_ID = "あなたのプロジェクトID"
DOCUMENT_AI_PROCESSOR_ID = "あなたのプロセッサーID"
DOCUMENT_AI_LOCATION = "asia-northeast1"
SERVICE_ACCOUNT_KEY = """
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
"""
AI_API_TYPE = "claude"
ANTHROPIC_API_KEY = "あなたのClaude APIキー"
```

**重要**: `SERVICE_ACCOUNT_KEY`には、ステップ2-2でダウンロードしたJSONファイルの内容をそのまま貼り付けます。改行は`\\n`として記述してください。

### 3-4. デプロイの確認

1. Secretsを保存すると、自動的に再デプロイが開始されます
2. デプロイが完了したら、アプリのURLにアクセス
3. サイドバーから「システム初期化」をクリックして動作確認

## トラブルシューティング

### エラー: "認証情報が見つかりません"

- Streamlit Secretsに`SERVICE_ACCOUNT_KEY`が正しく設定されているか確認
- JSONの形式が正しいか確認（改行は`\\n`として記述）

### エラー: "GOOGLE_SHEETS_IDが設定されていません"

- Streamlit Secretsに`GOOGLE_SHEETS_ID`が設定されているか確認

### エラー: "スプレッドシート更新エラー"

- サービスアカウントにスプレッドシートの編集権限が付与されているか確認
- スプレッドシートIDが正しいか確認

### OCR処理が失敗する

- Document AI APIが有効になっているか確認
- プロセッサーIDが正しいか確認
- サービスアカウントに「Document AI API User」ロールが付与されているか確認

## ローカル環境での動作確認

Streamlit Cloudにデプロイする前に、ローカル環境で動作確認することをお勧めします：

1. 依存関係をインストール：
   ```bash
   pip install -r requirements.txt
   ```

2. `.streamlit/secrets.toml`を作成（`.streamlit/secrets.toml.example`をコピー）

3. 実際の値を設定

4. アプリを起動：
   ```bash
   streamlit run fax_order_app.py
   ```

## セキュリティに関する注意事項

- **SecretsファイルはGitにコミットしないでください**
- `.gitignore`に`.streamlit/secrets.toml`が含まれていることを確認
- サービスアカウントキーは機密情報です。適切に管理してください

## サポート

問題が発生した場合は、以下を確認してください：

1. Streamlit Cloudのログ（アプリの設定画面から確認可能）
2. Google Cloud ConsoleのAPI使用状況
3. エラーメッセージの内容
