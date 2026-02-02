# pytesseractエラー修正 ステップバイステップガイド

## 📋 全体の流れ

1. 現在のファイルを確認
2. GitHubリポジトリに接続
3. 変更をコミット
4. GitHubにプッシュ
5. Streamlit Cloudで再デプロイ

---

## 📝 Step 1: 現在のファイルを確認

### Step 1-1: ファイルの場所を確認

1. **エクスプローラーを開く**
   - `Windowsキー + E`を押す

2. **フォルダに移動**
   - アドレスバーに以下を入力：
   ```
   C:\Users\ML-Y\Desktop\カーソル\fax_order
   ```
   - `Enter`キーを押す

### Step 1-2: ocr_processor.pyを確認

1. **ocr_processor.pyファイルを開く**
   - `ocr_processor.py`を右クリック
   - 「プログラムから開く」→「メモ帳」または「VS Code」を選択

2. **6行目を確認**
   - 6行目が以下のようになっているか確認：
   ```python
   import logging
   ```
   - ✅ 正しい: `import logging`
   - ❌ 間違い: `import pytesseract`

3. **ファイルを閉じる**
   - 変更がない場合はそのまま閉じる

---

## 📝 Step 2: PowerShellを開く

### Step 2-1: PowerShellを起動

1. **Windowsキーを押す**
2. **「powershell」と入力**
3. **「Windows PowerShell」をクリック**
4. PowerShellウィンドウが開きます

### Step 2-2: 作業ディレクトリに移動

1. **以下のコマンドをコピー**
   ```powershell
   cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
   ```

2. **PowerShellに貼り付け**
   - `Ctrl + V`で貼り付け
   - `Enter`キーを押す

3. **現在のディレクトリを確認**
   - 以下のコマンドを実行：
   ```powershell
   pwd
   ```
   - `C:\Users\ML-Y\Desktop\カーソル\fax_order`と表示されればOK

---

## 📝 Step 3: Gitの状態を確認

### Step 3-1: Gitリポジトリか確認

1. **以下のコマンドを実行**
   ```powershell
   git status
   ```

2. **結果を確認**
   - ✅ 「On branch main」と表示されれば、Gitリポジトリです
   - ❌ 「fatal: not a git repository」と表示された場合は、Step 4に進んでください

### Step 3-2: 変更されたファイルを確認

1. **以下のコマンドを実行**
   ```powershell
   git status
   ```

2. **表示されるファイルを確認**
   - `ocr_processor.py`が表示されていればOK
   - `streamlit_app.py`も表示されていればOK

---

## 📝 Step 4: GitHubリポジトリに接続（初回のみ）

### Step 4-1: GitHubリポジトリが既に存在する場合

1. **リモートリポジトリを確認**
   ```powershell
   git remote -v
   ```
   - URLが表示されれば、既に接続されています
   - Step 5に進んでください

### Step 4-2: GitHubリポジトリが存在しない場合

1. **GitHubでリポジトリを作成**
   - ブラウザで https://github.com にアクセス
   - 「New repository」をクリック
   - リポジトリ名を入力（例: `fax-order-app`）
   - 「Create repository」をクリック

2. **リモートリポジトリを追加**
   - GitHubで作成したリポジトリのURLをコピー
   - 以下のコマンドを実行（`YOUR_REPO_URL`を実際のURLに置き換え）：
   ```powershell
   git remote add origin YOUR_REPO_URL
   ```
   例：
   ```powershell
   git remote add origin https://github.com/your-username/fax-order-app.git
   ```

---

## 📝 Step 5: 変更をステージング

### Step 5-1: ファイルを追加

1. **以下のコマンドを実行**
   ```powershell
   git add ocr_processor.py
   ```

2. **streamlit_app.pyも追加（存在する場合）**
   ```powershell
   git add streamlit_app.py
   ```

3. **すべての変更を追加する場合**
   ```powershell
   git add .
   ```

### Step 5-2: 追加されたファイルを確認

1. **以下のコマンドを実行**
   ```powershell
   git status
   ```

2. **確認**
   - `ocr_processor.py`が緑色で表示されればOK
   - 「Changes to be committed」と表示されればOK

---

## 📝 Step 6: 変更をコミット

### Step 6-1: コミットメッセージを入力

1. **以下のコマンドを実行**
   ```powershell
   git commit -m "Fix: Remove pytesseract import and add streamlit_app.py"
   ```

2. **結果を確認**
   - 「1 file changed」または「2 files changed」と表示されればOK

### Step 6-2: コミットが成功したか確認

1. **以下のコマンドを実行**
   ```powershell
   git log --oneline -1
   ```

2. **確認**
   - 最新のコミットが表示されればOK

---

## 📝 Step 7: GitHubにプッシュ

### Step 7-1: ブランチを確認

1. **以下のコマンドを実行**
   ```powershell
   git branch
   ```
   - `* main`と表示されればOK
   - 別のブランチの場合は、`git checkout main`で切り替え

### Step 7-2: GitHubにプッシュ

1. **以下のコマンドを実行**
   ```powershell
   git push origin main
   ```

2. **認証が求められた場合**
   - GitHubのユーザー名とパスワード（またはPersonal Access Token）を入力
   - Personal Access Tokenの作成方法：
     - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
     - 「Generate new token」をクリック
     - 必要な権限を選択（`repo`など）
     - トークンをコピーして使用

3. **プッシュが成功したか確認**
   - 「Writing objects: 100%」と表示されればOK
   - エラーが表示された場合は、エラーメッセージを確認

---

## 📝 Step 8: Streamlit Cloudで再デプロイ

### Step 8-1: Streamlit Cloudにアクセス

1. **ブラウザで開く**
   - https://share.streamlit.io にアクセス
   - または、既存のStreamlit CloudアプリのURLにアクセス

2. **ログイン**
   - GitHubアカウントでログイン

### Step 8-2: アプリを管理

1. **アプリのページを開く**
   - デプロイ済みのアプリをクリック

2. **「Manage app」をクリック**
   - 画面右下の「Manage app」ボタンをクリック

### Step 8-3: アプリを再起動

1. **「Reboot app」をクリック**
   - 「Settings」タブを開く
   - 「Reboot app」ボタンをクリック

2. **または、自動再デプロイを待つ**
   - Streamlit Cloudは自動的に変更を検知して再デプロイします
   - 数分待ってからアプリをリロード

### Step 8-4: エラーが解消されたか確認

1. **アプリをリロード**
   - ブラウザで`F5`キーを押す
   - または、ブラウザの更新ボタンをクリック

2. **エラーが表示されないか確認**
   - ✅ エラーが表示されなければ成功
   - ❌ まだエラーが表示される場合は、Step 9を参照

---

## 📝 Step 9: トラブルシューティング

### 問題1: Gitリポジトリではない

**エラー**: `fatal: not a git repository`

**解決方法**:
1. 以下のコマンドを実行：
   ```powershell
   git init
   ```
2. Step 4に戻ってGitHubリポジトリに接続

### 問題2: プッシュが拒否される

**エラー**: `error: failed to push some refs`

**解決方法**:
1. 最新の変更を取得：
   ```powershell
   git pull origin main --rebase
   ```
2. 再度プッシュ：
   ```powershell
   git push origin main
   ```

### 問題3: 認証エラー

**エラー**: `Authentication failed`

**解決方法**:
1. Personal Access Tokenを使用：
   - GitHub → Settings → Developer settings → Personal access tokens
   - 新しいトークンを作成
   - パスワードの代わりにトークンを使用

### 問題4: Streamlit Cloudでまだエラーが表示される

**解決方法**:
1. **ログを確認**
   - 「Manage app」→「Logs」をクリック
   - エラーの詳細を確認

2. **キャッシュをクリア**
   - 「Manage app」→「Settings」→「Clear cache」をクリック

3. **アプリを再起動**
   - 「Manage app」→「Reboot app」をクリック

4. **GitHubリポジトリを確認**
   - GitHubで`ocr_processor.py`を開く
   - 6行目が`import logging`になっているか確認

---

## ✅ 完了確認チェックリスト

- [ ] `ocr_processor.py`の6行目が`import logging`になっている
- [ ] PowerShellで作業ディレクトリに移動できた
- [ ] `git status`でファイルの状態を確認できた
- [ ] `git add`でファイルを追加できた
- [ ] `git commit`でコミットできた
- [ ] `git push`でGitHubにプッシュできた
- [ ] Streamlit Cloudでアプリを再起動した
- [ ] エラーが表示されなくなった

---

## 📞 サポート

問題が解決しない場合は、以下を確認してください：

1. **GitHubリポジトリの内容**
   - `ocr_processor.py`の6行目を確認
   - `import pytesseract`があれば、ローカルのファイルをプッシュ

2. **Streamlit Cloudのログ**
   - 「Manage app」→「Logs」でエラーの詳細を確認

3. **ローカルファイルの確認**
   - `ocr_processor.py`の内容を確認
   - `pytesseract`のインポートがないことを確認
