# デプロイ手順詳細ガイド

FAX注文処理アプリをStreamlit Cloudにデプロイする詳細な手順を説明します。

## 目次

1. [事前準備](#事前準備)
2. [GitHubリポジトリの準備](#githubリポジトリの準備)
3. [Streamlit Cloudへのデプロイ](#streamlit-cloudへのデプロイ)
4. [設定の確認とテスト](#設定の確認とテスト)
5. [修正の反映方法](#修正の反映方法)

---

## 事前準備

### 必要なアカウント

1. **GitHubアカウント**
   - https://github.com/ でアカウント作成
   - 無料プランで問題ありません

2. **Streamlit Cloudアカウント**
   - https://streamlit.io/cloud でGitHubアカウントを使ってサインアップ
   - 無料で利用可能

3. **Google Cloud Platformアカウント**
   - Document AIとGoogle Sheets APIを使用するため
   - 無料トライアルで開始可能

4. **Anthropicアカウント（Claude API使用時）**
   - https://console.anthropic.com/ でアカウント作成
   - APIキーを取得

### 必要な情報

- GoogleスプレッドシートID
- Google Cloud プロジェクトID
- Document AIプロセッサーID
- サービスアカウントキー（JSON）
- Claude APIキーまたはOpenAI APIキー

---

## GitHubリポジトリの準備

### ステップ1: ローカルリポジトリの確認

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"

# Gitリポジトリの状態を確認
git status

# コミット履歴を確認
git log --oneline
```

### ステップ2: GitHubでリポジトリを作成

1. GitHubにログイン
2. 右上の「+」> 「New repository」
3. リポジトリ名を入力（例: `fax-order-processor`）
4. 説明を追加（オプション）
5. 「Public」または「Private」を選択
   - **Public**: 誰でもコードを見られる（無料）
   - **Private**: 自分だけが見られる（有料プランが必要な場合あり）
6. 「Initialize this repository with a README」は**チェックしない**
7. 「Create repository」をクリック

### ステップ3: リモートリポジトリの追加

GitHubで作成したリポジトリのURLをコピー（例: `https://github.com/username/fax-order-processor.git`）

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"

# リモートリポジトリを追加
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git

# リモートが正しく設定されたか確認
git remote -v
```

### ステップ4: GitHubにプッシュ

```powershell
# ブランチ名をmainに変更（必要に応じて）
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

初回プッシュ時、GitHubの認証が求められる場合があります。Personal Access Tokenを使用してください。

---

## Streamlit Cloudへのデプロイ

### ステップ1: Streamlit Cloudにログイン

1. https://streamlit.io/cloud にアクセス
2. 「Sign in」をクリック
3. GitHubアカウントで認証

### ステップ2: 新しいアプリを作成

1. 「New app」をクリック
2. 以下の情報を入力：

   **Repository**
   - ドロップダウンからGitHubリポジトリを選択
   - リポジトリが表示されない場合は、「Authorize」をクリックして権限を付与

   **Branch**
   - `main` を選択（または使用しているブランチ名）

   **Main file path**
   - `fax_order_app.py` を入力

3. 「Deploy!」をクリック

### ステップ3: デプロイの確認

- デプロイが開始されます（通常1-2分）
- ログが表示され、エラーがないか確認できます
- デプロイが完了すると、URLが発行されます

---

## 設定の確認とテスト

### Secretsの設定

1. アプリの「Settings」を開く
2. 「Secrets」タブを選択
3. 以下の形式でSecretsを設定：

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

4. 「Save」をクリック
5. アプリが自動的に再デプロイされます

### アプリのテスト

1. 発行されたURLにアクセス
2. サイドバーから「システム初期化」を実行
3. エラーが表示されないか確認
4. テスト用のPDFファイルをアップロードして処理を実行

---

## 修正の反映方法

### 基本的なワークフロー

```mermaid
graph LR
    A[ローカルで修正] --> B[Gitにコミット]
    B --> C[GitHubにプッシュ]
    C --> D[Streamlit Cloudが自動検知]
    D --> E[自動デプロイ]
    E --> F[ブラウザで確認]
```

### 詳細な手順

1. **ローカルでファイルを編集**
   ```powershell
   cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
   # ファイルを編集（エディタで）
   ```

2. **変更をステージング**
   ```powershell
   git add .
   # または特定のファイルのみ
   git add fax_order_app.py
   ```

3. **コミット**
   ```powershell
   git commit -m "修正内容の説明"
   ```

4. **GitHubにプッシュ**
   ```powershell
   git push origin main
   ```

5. **自動デプロイの確認**
   - Streamlit Cloudのダッシュボードでデプロイ状況を確認
   - 通常、数秒でデプロイが完了します
   - ブラウザをリロードして変更を確認

### デプロイの確認方法

1. Streamlit Cloudダッシュボードでアプリを開く
2. 「Activity」タブでデプロイ履歴を確認
3. 最新のデプロイが成功しているか確認
4. エラーがある場合は「Logs」タブで確認

---

## 複数PCでの使用

### PC1（開発用PC）での作業

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
# ファイルを編集
git add .
git commit -m "修正内容"
git push origin main
```

### PC2（他のPC）での使用

**方法1: Streamlit Cloud経由（推奨）**
- ブラウザでStreamlit CloudのURLにアクセス
- 修正は自動的に反映されます

**方法2: ローカル実行**
```powershell
# GitHubからクローン
git clone https://github.com/あなたのユーザー名/リポジトリ名.git
cd リポジトリ名

# セットアップ
.\setup.bat  # Windows
# または
./setup.sh   # Mac/Linux

# 設定ファイルを編集
# .streamlit/secrets.toml に実際の値を設定

# アプリを起動
.\run.bat    # Windows
# または
./run.sh     # Mac/Linux

# 最新版を取得（修正が反映された場合）
git pull origin main
```

---

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

---

## セキュリティのベストプラクティス

1. **Secretsの管理**
   - `.streamlit/secrets.toml` をGitにコミットしない（.gitignoreで除外済み）
   - Streamlit CloudのSecrets機能を使用

2. **リポジトリの公開設定**
   - 機密情報を含む場合はPrivateリポジトリを使用
   - Publicリポジトリの場合は、Secretsに機密情報を設定

3. **APIキーの管理**
   - APIキーをコードに直接書かない
   - Secretsまたは環境変数を使用

---

## 次のステップ

- `SETUP_GUIDE.md` - 包括的なセットアップガイド
- `QUICK_START.md` - クイックスタートガイド
- `RESTORE_GUIDE.md` - 以前の状態に戻す方法
