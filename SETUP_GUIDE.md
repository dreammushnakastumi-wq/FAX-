# FAX注文処理アプリ - セットアップガイド

このガイドでは、FAX注文処理アプリを他のPCでも使えるようにする方法を説明します。

## 目次

1. [Streamlit Cloudでのデプロイ（推奨）](#streamlit-cloudでのデプロイ)
2. [GitHub経由での修正反映](#github経由での修正反映)
3. [ローカル実行方法](#ローカル実行方法)
4. [トラブルシューティング](#トラブルシューティング)

---

## Streamlit Cloudでのデプロイ

### メリット
- ブラウザからどこでもアクセス可能
- サーバー管理不要
- 修正をGitHubにプッシュするだけで自動反映
- 無料で利用可能

### 前提条件
- GitHubアカウント
- Streamlit Cloudアカウント（無料）

### 手順

#### ステップ1: GitHubリポジトリの作成

1. GitHubにログイン
2. 右上の「+」> 「New repository」をクリック
3. リポジトリ名を入力（例: `fax-order-processor`）
4. 「Public」または「Private」を選択
5. 「Create repository」をクリック

#### ステップ2: ローカルリポジトリをGitHubにプッシュ

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"

# 既存のGitリポジトリを確認
git status

# GitHubリポジトリをリモートとして追加（URLは実際のリポジトリURLに置き換え）
git remote add origin https://github.com/あなたのユーザー名/fax-order-processor.git

# ブランチ名をmainに変更（必要に応じて）
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

#### ステップ3: Streamlit Cloudに接続

1. https://streamlit.io/cloud にアクセス
2. 「Sign in」をクリックしてGitHubアカウントでログイン
3. 「New app」をクリック
4. 以下の情報を入力：
   - **Repository**: 作成したGitHubリポジトリを選択
   - **Branch**: `main` を選択
   - **Main file path**: `fax_order_app.py` を入力
5. 「Deploy!」をクリック

#### ステップ4: Secretsの設定

1. デプロイ後、アプリの「Settings」を開く
2. 「Secrets」タブを選択
3. `.streamlit/secrets.toml.example` の内容を参考に、以下の値を設定：

```toml
GOOGLE_SHEETS_ID = "実際のスプレッドシートID"
DOCUMENT_AI_PROJECT_ID = "実際のプロジェクトID"
DOCUMENT_AI_PROCESSOR_ID = "実際のプロセッサーID"
DOCUMENT_AI_LOCATION = "asia-northeast1"
SERVICE_ACCOUNT_KEY = """実際のサービスアカウントキー（JSON文字列）"""
AI_API_TYPE = "claude"
ANTHROPIC_API_KEY = "実際のClaude APIキー"
```

4. 「Save」をクリック
5. アプリが自動的に再デプロイされます

#### ステップ5: アクセス

- デプロイが完了すると、URLが発行されます（例: `https://your-app.streamlit.app`）
- このURLを他のPCからもアクセスできます

---

## GitHub経由での修正反映

### 修正を反映する手順

1. **ローカルで修正**
   ```powershell
   cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
   # ファイルを編集
   ```

2. **変更をコミット**
   ```powershell
   git add .
   git commit -m "修正内容の説明"
   ```

3. **GitHubにプッシュ**
   ```powershell
   git push origin main
   ```

4. **自動反映**
   - Streamlit Cloudが自動的に変更を検知
   - 数秒で新しいバージョンがデプロイされる
   - ブラウザをリロードすると新しいバージョンが表示される

### 他のPCで最新版を取得

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git pull origin main
```

---

## ローカル実行方法

### Windows

1. **セットアップ**
   ```powershell
   cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
   .\setup.bat
   ```

2. **設定ファイルを編集**
   - `.streamlit\secrets.toml` を開く
   - 実際の値を設定

3. **アプリを起動**
   ```powershell
   .\run.bat
   ```

### Mac/Linux

1. **セットアップ**
   ```bash
   cd /path/to/fax_order
   chmod +x setup.sh run.sh
   ./setup.sh
   ```

2. **設定ファイルを編集**
   - `.streamlit/secrets.toml` を開く
   - 実際の値を設定

3. **アプリを起動**
   ```bash
   ./run.sh
   ```

### 手動セットアップ（スクリプトを使用しない場合）

```powershell
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# 仮想環境の有効化（Mac/Linux）
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# アプリの起動
streamlit run fax_order_app.py
```

---

## トラブルシューティング

### ポート8501が使用中

**Windows:**
```powershell
# ポート8501を使用しているプロセスを確認
netstat -ano | findstr :8501

# プロセスを停止（PIDを確認してから）
Stop-Process -Id [PID] -Force
```

**Mac/Linux:**
```bash
# ポート8501を使用しているプロセスを確認
lsof -i :8501

# プロセスを停止（PIDを確認してから）
kill -9 [PID]
```

### プロキシエラー

コード内で自動的にプロキシ設定を無効化していますが、問題が続く場合は環境変数を確認してください：

```powershell
# 環境変数を確認
echo $env:HTTP_PROXY
echo $env:HTTPS_PROXY

# 環境変数を削除（必要に応じて）
Remove-Item Env:\HTTP_PROXY
Remove-Item Env:\HTTPS_PROXY
```

### 初期化エラー

1. `.streamlit/secrets.toml` の設定値を確認
2. すべての必須項目が設定されているか確認
3. APIキーが正しいか確認
4. Google Cloudのサービスアカウントに適切な権限が付与されているか確認

### 依存関係のインストールエラー

```powershell
# pipをアップグレード
pip install --upgrade pip

# 仮想環境を再作成
Remove-Item -Recurse -Force venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Streamlit Cloudでのデプロイエラー

1. `requirements.txt` にすべての依存関係が記載されているか確認
2. `.streamlit/config.toml` が存在するか確認
3. Secretsが正しく設定されているか確認
4. Streamlit Cloudのログを確認（Settings > Logs）

---

## 設定値の取得方法

詳細は `QUICK_START.md` の「必要な設定値の取得方法」セクションを参照してください。

---

## 次のステップ

- `DEPLOYMENT.md` - より詳細なデプロイ手順
- `RESTORE_GUIDE.md` - 以前の状態に戻す方法
