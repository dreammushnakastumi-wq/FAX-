# Streamlit Cloudで「Manage app」を見つける方法

## 📋 問題

https://share.streamlit.io/ を開いたが、「Manage app」が見つからない

## 🔍 原因

「Manage app」ボタンは、**アプリのページ**にあります。
トップページ（ダッシュボード）には表示されません。

## ✅ 解決方法

### Step 1: Streamlit Cloudにログイン

1. **https://share.streamlit.io/ にアクセス**
2. **右上の「Sign in」をクリック**
   - GitHubアカウントでログイン

### Step 2: ダッシュボードからアプリを選択

1. **ログイン後、ダッシュボードが表示されます**
   - デプロイ済みのアプリの一覧が表示されます

2. **アプリを探す**
   - アプリ名を確認（例: `fax-order-app`、`fax`など）
   - または、最近デプロイしたアプリを探す

3. **アプリをクリック**
   - アプリ名をクリック
   - または、「Open app」ボタンをクリック

### Step 3: アプリのページを開く

1. **アプリが新しいタブで開きます**
   - アプリのURLが表示されます
   - 例: `https://share.streamlit.io/your-username/your-app-name/main`

2. **アプリのページで「Manage app」を探す**
   - 画面の**右下**を確認
   - 「**Manage app**」という小さなボタンがあります
   - または、画面の右上に「⚙️」アイコンがある場合もあります

### Step 4: 「Manage app」をクリック

1. **「Manage app」ボタンをクリック**
   - ドロップダウンメニューが開きます

2. **「Settings」を選択**
   - メニューから「Settings」をクリック

3. **「Repository」を確認**
   - 設定画面で「Repository」セクションを探す
   - GitHubリポジトリのURLが表示されます

---

## 🎯 別の方法：直接アプリのURLにアクセス

アプリのURLが分かっている場合：

1. **アプリのURLに直接アクセス**
   - 例: `https://share.streamlit.io/your-username/your-app-name/main`
   - ブラウザの履歴から探すこともできます

2. **「Manage app」を探す**
   - 画面の右下を確認

---

## 🔍 「Manage app」ボタンの見つけ方

### 場所1: 画面右下

- 画面の**右下**に小さなボタンがあります
- 「**Manage app**」というテキストが表示されています

### 場所2: 画面右上

- 画面の**右上**に「⚙️」アイコンがある場合があります
- このアイコンをクリックすると、設定メニューが開きます

### 場所3: ハンバーガーメニュー

- 画面の左上に「☰」アイコンがある場合があります
- このアイコンをクリックすると、メニューが開きます

---

## 📸 画面の確認ポイント

### ダッシュボード（トップページ）

- ✅ アプリの一覧が表示される
- ✅ 各アプリに「Open app」ボタンがある
- ❌ 「Manage app」ボタンは**ない**

### アプリのページ

- ✅ アプリが実行されている
- ✅ 画面右下に「**Manage app**」ボタンがある
- ✅ または、画面右上に「⚙️」アイコンがある

---

## 🆘 まだ見つからない場合

### 方法1: ブラウザの検索機能を使用

1. **`Ctrl + F`を押す**
2. **「Manage」と入力**
3. **検索結果を確認**

### 方法2: アプリのURLを確認

1. **ブラウザのアドレスバーを確認**
   - アプリのURLが表示されています
   - 例: `https://share.streamlit.io/your-username/your-app-name/main`

2. **このURLから直接アクセス**
   - ブラウザの履歴から探すこともできます

### 方法3: GitHubで直接確認

「Manage app」が見つからない場合は、GitHubで直接リポジトリを確認する方が簡単です：

1. **GitHubにアクセス**
   - https://github.com にアクセス
   - ログイン

2. **リポジトリ一覧を確認**
   - 右上のプロフィールアイコン → 「Your repositories」
   - `fax-order`、`fax`などの名前のリポジトリを探す

3. **リポジトリを開く**
   - リポジトリをクリック
   - ブラウザのアドレスバーにURLが表示されます

---

## ✅ 確認チェックリスト

- [ ] Streamlit Cloudにログインできた
- [ ] ダッシュボードが表示された
- [ ] アプリの一覧が表示された
- [ ] アプリをクリックして開いた
- [ ] アプリのページが表示された
- [ ] 画面右下に「Manage app」ボタンがある
- [ ] 「Manage app」をクリックできた
- [ ] 「Settings」を選択できた
- [ ] 「Repository」セクションを見つけた

---

## 📞 次のステップ

「Manage app」を見つけて「Repository」のURLを確認したら：

1. **URLをコピー**
2. **PowerShellで以下を実行**（`YOUR_REPO_URL`を実際のURLに置き換え）：
   ```powershell
   git commit -m "Fix: Remove pytesseract import and add streamlit_app.py"
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

または、GitHubで直接リポジトリを見つけた場合は、そのURLを使用してください。
