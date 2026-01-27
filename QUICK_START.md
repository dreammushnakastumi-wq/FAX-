# クイックスタートガイド

FAX注文処理アプリを最短で起動する方法を説明します。

## 方法1: Streamlit Cloud（推奨・最も簡単）

### 前提条件
- GitHubアカウント
- Streamlit Cloudアカウント（無料、GitHubアカウントでサインアップ可能）

### 手順

1. **GitHubリポジトリを作成**
   - GitHubで新しいリポジトリを作成
   - このフォルダの内容をプッシュ

2. **Streamlit Cloudに接続**
   - https://streamlit.io/cloud にアクセス
   - GitHubアカウントでログイン
   - 「New app」をクリック
   - リポジトリとブランチを選択
   - Main file path: `fax_order_app.py` を指定
   - 「Deploy!」をクリック

3. **Secretsを設定**
   - デプロイ後、Settings > Secrets を開く
   - `.streamlit/secrets.toml.example` の内容を参考に設定
   - 実際の値を入力して保存

4. **完了**
   - 数秒でアプリが起動します
   - URLが発行されるので、ブラウザでアクセス

**メリット**: ブラウザからどこでもアクセス可能、サーバー管理不要、修正も自動反映

---

## 方法2: ローカル実行（Windows）

### 前提条件
- Python 3.8以上がインストールされていること

### 手順

1. **セットアップを実行**
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

4. **ブラウザでアクセス**
   - http://localhost:8501 が自動的に開きます

---

## 方法3: ローカル実行（Mac/Linux）

### 前提条件
- Python 3.8以上がインストールされていること

### 手順

1. **セットアップを実行**
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

4. **ブラウザでアクセス**
   - http://localhost:8501 が自動的に開きます

---

## 必要な設定値の取得方法

### Google Sheets ID
1. Googleスプレッドシートを開く
2. URLから取得: `https://docs.google.com/spreadsheets/d/【ここがID】/edit`

### Google Document AI設定
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを作成（または既存のプロジェクトを選択）
3. Document AI APIを有効化
4. Document AI > プロセッサー > プロセッサーを作成
5. プロジェクトIDとプロセッサーIDをコピー

### サービスアカウントキー
1. Google Cloud Console > IAMと管理 > サービスアカウント
2. サービスアカウントを作成
3. キー > キーを追加 > JSONを作成
4. ダウンロードしたJSONファイルの内容を `SERVICE_ACCOUNT_KEY` に設定

### Claude APIキー
1. [Anthropic Console](https://console.anthropic.com/)にアクセス
2. API Keys > Create Key
3. 生成されたキーをコピー

---

## よくある質問

### Q: ポート8501が使用中と表示される
A: 既存のStreamlitプロセスを停止してください：
```powershell
# Windows
Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

### Q: プロキシエラーが発生する
A: 環境変数のプロキシ設定を確認してください。コード内で自動的に無効化されますが、問題が続く場合は環境変数を確認してください。

### Q: 初期化エラーが発生する
A: `.streamlit/secrets.toml` の設定値を確認してください。すべての必須項目が正しく設定されている必要があります。

### Q: 修正を反映したい
A: 
- **Streamlit Cloud**: GitHubにプッシュすると自動的に反映されます
- **ローカル実行**: ファイルを編集して、アプリを再起動してください

---

## トラブルシューティング

詳細なトラブルシューティングは `SETUP_GUIDE.md` を参照してください。
