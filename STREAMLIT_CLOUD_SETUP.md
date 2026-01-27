# Streamlit Cloudデプロイ手順

## 前提条件

- GitHubリポジトリにコードがプッシュされていること
- Streamlit Cloudアカウント（GitHubアカウントでサインアップ可能）

## ステップ1: Streamlit Cloudにアクセス

1. **Streamlit Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - 「Sign in」をクリック

2. **GitHubアカウントでログイン**
   - 「Continue with GitHub」をクリック
   - GitHubアカウントで認証
   - 必要に応じて権限を付与

## ステップ2: アプリを作成

1. **「New app」をクリック**

2. **アプリ情報を入力**
   - **Repository**: ドロップダウンからGitHubリポジトリを選択
     - リポジトリが表示されない場合は、「Authorize」をクリックして権限を付与
   - **Branch**: `main` を選択
   - **Main file path**: `fax_order_app.py` を入力

3. **「Deploy!」をクリック**
   - デプロイが開始されます（通常1-2分）
   - ログが表示され、エラーがないか確認できます

## ステップ3: Secretsの設定

1. **Settingsを開く**
   - デプロイ後、アプリの「Settings」タブをクリック

2. **Secretsタブを選択**

3. **設定値を入力**
   - `.streamlit/secrets.toml.example` の内容を参考に、以下の値を設定：

```toml
GOOGLE_SHEETS_ID = "実際のスプレッドシートID"
DOCUMENT_AI_PROJECT_ID = "実際のプロジェクトID"
DOCUMENT_AI_PROCESSOR_ID = "実際のプロセッサーID"
DOCUMENT_AI_LOCATION = "asia-northeast1"
SERVICE_ACCOUNT_KEY = """{
  "type": "service_account",
  "project_id": "実際のプロジェクトID",
  ...
}"""
AI_API_TYPE = "claude"
ANTHROPIC_API_KEY = "実際のClaude APIキー"
```

**重要**: `SERVICE_ACCOUNT_KEY` はJSON全体を文字列として設定します。三重引用符（`"""`）を使用してください。

4. **「Save」をクリック**
   - アプリが自動的に再デプロイされます

## ステップ4: アクセス

1. **URLを確認**
   - デプロイが完了すると、URLが発行されます
   - 例: `https://your-app-name.streamlit.app`

2. **動作確認**
   - ブラウザでURLにアクセス
   - アプリが正常に表示されるか確認
   - サイドバーから「システム初期化」を実行してエラーがないか確認

## ステップ5: 他のPCからアクセス

- 発行されたURLを他のPCのブラウザで開くだけで使用できます
- どのPCからでも、ブラウザがあればアクセス可能です

## 今後の更新方法

コードを修正した場合：

1. **ローカルで修正**
   ```powershell
   cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
   # ファイルを編集
   ```

2. **GitHubにプッシュ**
   ```powershell
   git add .
   git commit -m "修正内容の説明"
   git push origin main
   ```

3. **自動デプロイ**
   - Streamlit Cloudが自動的に変更を検知
   - 数秒で新しいバージョンがデプロイされる
   - ブラウザをリロードすると新しいバージョンが表示される

## トラブルシューティング

### デプロイが失敗する

1. **ログを確認**
   - Streamlit Cloudダッシュボード > アプリ > Logs
   - エラーメッセージを確認

2. **よくある原因**
   - `requirements.txt` に依存関係が不足している
   - 構文エラーがある
   - Secretsが正しく設定されていない

3. **対処法**
   - エラーメッセージに従って修正
   - ローカルで動作確認してからプッシュ

### Secretsが反映されない

1. Secretsの保存を確認
2. アプリを再デプロイ（Settings > Reboot app）
3. Secretsの形式が正しいか確認（TOML形式）

### デプロイが遅い

- 通常、デプロイは1-2分で完了します
- 初回デプロイは少し時間がかかる場合があります
- 5分以上かかる場合は、ログを確認してください

## 参考

詳細は `DEPLOYMENT.md` を参照してください。
