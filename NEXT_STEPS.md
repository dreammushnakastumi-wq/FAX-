# 次のステップ - GitHubリポジトリ作成とStreamlit Cloudデプロイ

## ✅ 完了した作業

1. ✅ 未コミットの変更をコミット
2. ✅ ブランチ名を`main`に変更

## 📋 これから行う作業

### ステップ1: GitHubリポジトリを作成

1. **GitHubにアクセス**
   - https://github.com/ にアクセスしてログイン

2. **新しいリポジトリを作成**
   - 右上の「+」> 「New repository」
   - Repository name: `fax-order-processor`（任意の名前）
   - Visibility: Public または Private を選択
   - **重要**: 「Initialize this repository with README」は**チェックしない**
   - 「Create repository」をクリック

3. **リポジトリURLをコピー**
   - 作成されたページで、HTTPSのURLをコピー
   - 例: `https://github.com/あなたのユーザー名/fax-order-processor.git`

### ステップ2: ローカルリポジトリをGitHubに接続

リポジトリを作成したら、以下のコマンドを実行してください：

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"

# リモートリポジトリを追加（URLは実際のリポジトリURLに置き換え）
git remote add origin https://github.com/あなたのユーザー名/fax-order-processor.git

# GitHubにプッシュ
git push -u origin main
```

**認証について**: 初回プッシュ時、Personal Access Tokenの入力が求められる場合があります。
- GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
- 「Generate new token (classic)」でトークンを作成（`repo`スコープが必要）
- パスワードの代わりにトークンを入力

### ステップ3: Streamlit Cloudにデプロイ

1. **Streamlit Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - GitHubアカウントでサインアップ/ログイン

2. **アプリを作成**
   - 「New app」をクリック
   - Repository: 作成したGitHubリポジトリを選択
   - Branch: `main` を選択
   - Main file path: `fax_order_app.py` を入力
   - 「Deploy!」をクリック

3. **Secretsを設定**
   - デプロイ後、Settings > Secrets を開く
   - `.streamlit/secrets.toml.example` の内容を参考に、実際の値を設定：
     - `GOOGLE_SHEETS_ID`
     - `DOCUMENT_AI_PROJECT_ID`
     - `DOCUMENT_AI_PROCESSOR_ID`
     - `DOCUMENT_AI_LOCATION`
     - `SERVICE_ACCOUNT_KEY`（JSON文字列）
     - `AI_API_TYPE`
     - `ANTHROPIC_API_KEY`

4. **アクセス**
   - デプロイが完了すると、URLが発行されます（例: `https://your-app.streamlit.app`）
   - このURLを他のPCからもアクセスできます

## 📚 詳細な手順

詳細は以下のドキュメントを参照してください：
- `GITHUB_SETUP.md` - GitHub設定の詳細手順
- `DEPLOYMENT.md` - Streamlit Cloudデプロイの詳細手順
- `SETUP_GUIDE.md` - セットアップガイド
