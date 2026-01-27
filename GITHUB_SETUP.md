# GitHubリポジトリ作成とプッシュの手順書

このガイドでは、FAX注文処理アプリをGitHubリポジトリにプッシュする手順を説明します。

## 前提条件

- GitHubアカウントを持っていること
- Gitがインストールされていること
- ローカルにGitリポジトリが初期化されていること

---

## 手順1: GitHubでリポジトリを作成

### 1-1. GitHubにログイン

1. https://github.com/ にアクセス
2. アカウントでログイン

### 1-2. 新しいリポジトリを作成

1. 右上の「+」アイコンをクリック
2. 「New repository」を選択

3. リポジトリ情報を入力：
   - **Repository name**: `fax-order-processor`（任意の名前）
   - **Description**: 「FAX注文書自動処理システム」（オプション）
   - **Visibility**: 
     - **Public**: 誰でもコードを見られる（無料）
     - **Private**: 自分だけが見られる（有料プランが必要な場合あり）
   - **Initialize this repository with**: すべて**チェックしない**
     - README、.gitignore、licenseは既に存在するため

4. 「Create repository」をクリック

### 1-3. リポジトリURLをコピー

作成されたリポジトリのページで、HTTPSのURLをコピーします。
例: `https://github.com/あなたのユーザー名/fax-order-processor.git`

---

## 手順2: ローカルリポジトリをGitHubに接続

### 2-1. 現在のディレクトリに移動

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
```

### 2-2. Gitの状態を確認

```powershell
# リポジトリの状態を確認
git status

# リモートリポジトリの確認
git remote -v
```

既にリモートが設定されている場合は、以下のコマンドで削除してから再追加：

```powershell
git remote remove origin
```

### 2-3. リモートリポジトリを追加

```powershell
# リモートリポジトリを追加（URLは実際のリポジトリURLに置き換え）
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git

# 正しく設定されたか確認
git remote -v
```

出力例：
```
origin  https://github.com/あなたのユーザー名/fax-order-processor.git (fetch)
origin  https://github.com/あなたのユーザー名/fax-order-processor.git (push)
```

---

## 手順3: GitHubにプッシュ

### 3-1. ブランチ名を確認・変更

```powershell
# 現在のブランチ名を確認
git branch

# ブランチ名がmainでない場合、mainに変更
git branch -M main
```

### 3-2. 変更をコミット（未コミットの変更がある場合）

```powershell
# 変更を確認
git status

# すべての変更をステージング
git add .

# コミット
git commit -m "GitHubリポジトリに初回プッシュ"
```

### 3-3. GitHubにプッシュ

```powershell
# 初回プッシュ
git push -u origin main
```

### 3-4. 認証

初回プッシュ時、認証が求められる場合があります：

**方法1: Personal Access Token（推奨）**
1. GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. 「Generate new token」をクリック
3. スコープで `repo` にチェック
4. トークンを生成してコピー
5. パスワードの代わりにトークンを入力

**方法2: GitHub CLI**
```powershell
# GitHub CLIをインストール（未インストールの場合）
# https://cli.github.com/

# 認証
gh auth login
```

---

## 手順4: プッシュの確認

1. GitHubのリポジトリページをリロード
2. ファイルが表示されているか確認
3. 以下のファイルが含まれていることを確認：
   - `fax_order_app.py`
   - `ocr_processor.py`
   - `ai_extractor.py`
   - `google_sheets.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `.streamlit/secrets.toml.example`
   - `.gitignore`

**重要**: `.streamlit/secrets.toml` は表示されないはずです（.gitignoreで除外されているため）

---

## 今後の作業フロー

### 修正を反映する場合

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"

# 変更を確認
git status

# 変更をステージング
git add .

# コミット
git commit -m "修正内容の説明"

# GitHubにプッシュ
git push origin main
```

### 他のPCで最新版を取得

```powershell
# 既存のリポジトリをクローン
git clone https://github.com/あなたのユーザー名/リポジトリ名.git

# または、既存のリポジトリを更新
cd リポジトリ名
git pull origin main
```

---

## トラブルシューティング

### エラー: "remote origin already exists"

既にリモートが設定されている場合：

```powershell
# 既存のリモートを削除
git remote remove origin

# 新しいリモートを追加
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
```

### エラー: "failed to push some refs"

リモートリポジトリに既にファイルがある場合：

```powershell
# リモートの変更を取得
git pull origin main --allow-unrelated-histories

# 競合を解決してから再度プッシュ
git push origin main
```

### エラー: 認証に失敗する

Personal Access Tokenを使用してください：

1. GitHub > Settings > Developer settings > Personal access tokens
2. 新しいトークンを生成
3. パスワードの代わりにトークンを入力

---

## 次のステップ

GitHubリポジトリにプッシュしたら、`DEPLOYMENT.md` を参照してStreamlit Cloudにデプロイしてください。
