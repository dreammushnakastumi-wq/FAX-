# Streamlit CloudでリポジトリURLを確認する方法

## 📋 手順

### Step 1: Streamlit Cloudにアクセス

1. **ブラウザで開く**
   - https://share.streamlit.io にアクセス
   - または、既存のStreamlitアプリのURLにアクセス

2. **ログイン**
   - GitHubアカウントでログイン（まだログインしていない場合）

### Step 2: アプリのページを開く

1. **アプリ一覧から選択**
   - Streamlit Cloudのダッシュボードで、デプロイ済みのアプリをクリック
   - または、アプリのURLに直接アクセス

2. **アプリが開く**
   - アプリのページが表示されます

### Step 3: 「Manage app」をクリック

1. **画面右下を確認**
   - 画面の右下に「**Manage app**」というボタンがあります
   - このボタンをクリック

2. **メニューが表示される**
   - ドロップダウンメニューが開きます

### Step 4: 「Settings」タブを開く

1. **「Settings」をクリック**
   - メニューから「**Settings**」を選択

2. **設定画面が表示される**
   - アプリの設定が表示されます

### Step 5: 「Repository」を確認

1. **「Repository」セクションを探す**
   - 設定画面の中に「**Repository**」というセクションがあります

2. **リポジトリURLを確認**
   - 「Repository」の下に、GitHubリポジトリのURLが表示されます
   - 例: `https://github.com/your-username/fax-order-app`
   - または: `your-username/fax-order-app`

3. **URLをコピー**
   - URLをクリックして選択
   - `Ctrl + C`でコピー

---

## 📸 画面の見つけ方（詳細）

### 方法1: アプリページから

1. **アプリのページを開く**
   ```
   https://share.streamlit.io/your-username/your-app-name/main
   ```

2. **右下の「Manage app」をクリック**
   - 画面の右下に小さなボタンがあります

3. **「Settings」を選択**

### 方法2: Streamlit Cloudダッシュボードから

1. **ダッシュボードにアクセス**
   - https://share.streamlit.io にアクセス
   - ログインしている場合は、アプリ一覧が表示されます

2. **アプリをクリック**
   - デプロイ済みのアプリをクリック

3. **「Manage app」→「Settings」を選択**

---

## 🔍 リポジトリURLの見つけ方（別の方法）

### 方法1: GitHubで直接確認

1. **GitHubにアクセス**
   - https://github.com にアクセス
   - ログイン

2. **リポジトリ一覧を確認**
   - 右上のプロフィールアイコンをクリック
   - 「Your repositories」をクリック
   - `fax-order`や`fax`などの名前のリポジトリを探す

3. **リポジトリを開く**
   - リポジトリをクリック
   - ブラウザのアドレスバーにURLが表示されます
   - 例: `https://github.com/your-username/fax-order-app`

### 方法2: Streamlit Cloudのデプロイ履歴から確認

1. **「Manage app」→「Activity」を開く**
   - デプロイ履歴が表示されます

2. **最新のデプロイを確認**
   - 最新のデプロイの詳細を開く
   - リポジトリ情報が表示される場合があります

---

## 📝 リポジトリURLの形式

リポジトリURLは以下のいずれかの形式です：

1. **HTTPS形式**:
   ```
   https://github.com/your-username/repo-name.git
   ```
   または
   ```
   https://github.com/your-username/repo-name
   ```

2. **SSH形式**:
   ```
   git@github.com:your-username/repo-name.git
   ```

3. **短縮形式**:
   ```
   your-username/repo-name
   ```

**PowerShellで使用する場合は、HTTPS形式を使用してください。**

---

## ✅ 確認チェックリスト

- [ ] Streamlit Cloudにアクセスできた
- [ ] アプリのページを開けた
- [ ] 「Manage app」ボタンを見つけた
- [ ] 「Settings」タブを開けた
- [ ] 「Repository」セクションを見つけた
- [ ] リポジトリURLをコピーした

---

## 🆘 見つからない場合

### リポジトリURLが見つからない場合

1. **GitHubで直接確認**
   - GitHubにアクセス
   - リポジトリ一覧から該当するリポジトリを探す

2. **Streamlit Cloudの設定を確認**
   - 「Manage app」→「Settings」→「Repository」を再度確認
   - ブラウザの検索機能（`Ctrl + F`）で「Repository」を検索

3. **新しいリポジトリを作成**
   - GitHubで新しいリポジトリを作成
   - Streamlit Cloudでそのリポジトリを使用するように設定

---

## 📞 次のステップ

リポジトリURLが見つかったら：

1. **URLをコピー**
2. **PowerShellで以下を実行**（`YOUR_REPO_URL`を実際のURLに置き換え）：
   ```powershell
   git commit -m "Fix: Remove pytesseract import and add streamlit_app.py"
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

例：
```powershell
git commit -m "Fix: Remove pytesseract import and add streamlit_app.py"
git remote add origin https://github.com/your-username/fax-order-app.git
git push -u origin main
```
