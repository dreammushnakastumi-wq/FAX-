# GitHubリポジトリ作成手順

## ステップ1: GitHubでリポジトリを作成

1. **GitHubにアクセス**
   - https://github.com/ にアクセス
   - アカウントでログイン（アカウントがない場合は作成）

2. **新しいリポジトリを作成**
   - 右上の「+」アイコンをクリック
   - 「New repository」を選択

3. **リポジトリ情報を入力**
   - **Repository name**: `fax-order-processor`（任意の名前）
   - **Description**: 「FAX注文書自動処理システム」（オプション）
   - **Visibility**: 
     - **Public**: 誰でもコードを見られる（無料）
     - **Private**: 自分だけが見られる（有料プランが必要な場合あり）
   - **Initialize this repository with**: すべて**チェックしない**
     - README、.gitignore、licenseは既に存在するため

4. **「Create repository」をクリック**

5. **リポジトリURLをコピー**
   - 作成されたリポジトリのページで、HTTPSのURLをコピー
   - 例: `https://github.com/あなたのユーザー名/fax-order-processor.git`

## ステップ2: リポジトリURLを設定

リポジトリを作成したら、以下のコマンドを実行して接続します：

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"

# リモートリポジトリを追加（URLは実際のリポジトリURLに置き換え）
git remote add origin https://github.com/あなたのユーザー名/fax-order-processor.git

# ブランチ名をmainに変更
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

## 認証について

初回プッシュ時、認証が求められる場合があります：

**Personal Access Tokenを使用（推奨）**
1. GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. 「Generate new token (classic)」をクリック
3. Note: 「FAX Order Processor」など任意の名前
4. Expiration: 有効期限を設定（または「No expiration」）
5. Select scopes: `repo` にチェック
6. 「Generate token」をクリック
7. 表示されたトークンをコピー（一度しか表示されません）
8. パスワードの代わりにこのトークンを入力

## 次のステップ

リポジトリにプッシュできたら、`DEPLOYMENT.md` を参照してStreamlit Cloudにデプロイしてください。
