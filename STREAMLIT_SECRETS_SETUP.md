# Streamlit Cloud Secrets設定ガイド

## 📋 問題

```
✗ 初期化エラー: GOOGLE_SHEETS_IDが設定されていません。
```

## ✅ 解決方法

Streamlit CloudのSecretsに必要な設定を追加する必要があります。

---

## 📝 Step 1: Streamlit Cloudでアプリを開く

1. **Streamlit Cloudにアクセス**
   - https://share.streamlit.io にアクセス
   - ログイン（GitHubアカウント）

2. **アプリのページを開く**
   - デプロイ済みのアプリをクリック

3. **「Manage app」をクリック**
   - 画面右下の「Manage app」ボタンをクリック

---

## 📝 Step 2: Secretsを開く

1. **「Settings」タブをクリック**
   - 「Manage app」メニューから「Settings」を選択

2. **「Secrets」セクションを探す**
   - 設定画面の中に「**Secrets**」というセクションがあります
   - 「Secrets」の下にテキストエリアがあります

3. **「Edit secrets」をクリック**
   - 「Secrets」セクションの「Edit secrets」ボタンをクリック

---

## 📝 Step 3: Secretsを設定

### 必要な設定項目

以下の設定を追加してください：

```toml
GOOGLE_SHEETS_ID = "your-spreadsheet-id-here"
DOCUMENT_AI_PROJECT_ID = "your-project-id-here"
DOCUMENT_AI_PROCESSOR_ID = "your-processor-id-here"
DOCUMENT_AI_LOCATION = "asia-northeast1"
SERVICE_ACCOUNT_KEY = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
'''
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
AI_API_TYPE = "claude"
```

### 各設定項目の説明

#### 1. GOOGLE_SHEETS_ID

GoogleスプレッドシートのIDを設定します。

**取得方法**:
1. Googleスプレッドシートを開く
2. ブラウザのアドレスバーを確認
3. URLからIDをコピー
   - 例: `https://docs.google.com/spreadsheets/d/1tQmBGOeOX--VyZ2Zx.../edit`
   - ID部分: `1tQmBGOeOX--VyZ2Zx...`

**設定例**:
```toml
GOOGLE_SHEETS_ID = "1tQmBGOeOX--VyZ2Zx..."
```

#### 2. DOCUMENT_AI_PROJECT_ID

Google CloudプロジェクトIDを設定します。

**取得方法**:
1. Google Cloud Consoleにアクセス
2. プロジェクトを選択
3. プロジェクトIDをコピー

**設定例**:
```toml
DOCUMENT_AI_PROJECT_ID = "your-project-id"
```

#### 3. DOCUMENT_AI_PROCESSOR_ID

Document AIプロセッサーIDを設定します。

**取得方法**:
1. Google Cloud Console → Document AI
2. プロセッサーを選択
3. プロセッサーIDをコピー

**設定例**:
```toml
DOCUMENT_AI_PROCESSOR_ID = "your-processor-id"
```

#### 4. DOCUMENT_AI_LOCATION

Document AIプロセッサーのロケーションを設定します。

**設定例**:
```toml
DOCUMENT_AI_LOCATION = "asia-northeast1"
```

#### 5. SERVICE_ACCOUNT_KEY

サービスアカウントキーのJSONを設定します。

**取得方法**:
1. Google Cloud Console → IAM & Admin → Service Accounts
2. サービスアカウントを選択
3. 「Keys」タブ → 「Add Key」→ 「Create new key」
4. JSON形式を選択してダウンロード
5. JSONファイルの内容をすべてコピー

**設定例**:
```toml
SERVICE_ACCOUNT_KEY = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  ...
}
'''
```

**重要**: 
- 3つのシングルクォート（`'''`）で囲む
- JSONの内容をそのまま貼り付ける

#### 6. ANTHROPIC_API_KEY

Claude APIキーを設定します。

**取得方法**:
1. Anthropic Consoleにアクセス
2. API Keysセクションでキーを取得
3. キーをコピー

**設定例**:
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

#### 7. AI_API_TYPE

使用するAI APIタイプを設定します。

**設定例**:
```toml
AI_API_TYPE = "claude"
```

または、OpenAIを使用する場合：
```toml
AI_API_TYPE = "openai"
OPENAI_API_KEY = "sk-..."
```

---

## 📝 Step 4: Secretsを保存

1. **設定を入力**
   - 上記の設定をテキストエリアに入力

2. **「Save」をクリック**
   - 画面下部の「Save」ボタンをクリック

3. **確認メッセージ**
   - 「Secrets saved successfully」と表示されればOK

---

## 📝 Step 5: アプリを再起動

1. **「Reboot app」をクリック**
   - 「Settings」タブの「Reboot app」ボタンをクリック

2. **アプリをリロード**
   - ブラウザで`F5`キーを押す
   - または、アプリのURLに再度アクセス

3. **初期化を確認**
   - サイドバーから「🔄 システム初期化」をクリック
   - 「✓ 初期化完了」と表示されればOK

---

## 🔍 設定の確認方法

### ローカル環境で確認

`.streamlit/secrets.toml`ファイルを作成して、ローカルでテストできます：

```toml
GOOGLE_SHEETS_ID = "your-spreadsheet-id"
DOCUMENT_AI_PROJECT_ID = "your-project-id"
DOCUMENT_AI_PROCESSOR_ID = "your-processor-id"
DOCUMENT_AI_LOCATION = "asia-northeast1"
SERVICE_ACCOUNT_KEY = '''
{
  "type": "service_account",
  ...
}
'''
ANTHROPIC_API_KEY = "your-api-key"
AI_API_TYPE = "claude"
```

---

## 🆘 トラブルシューティング

### 問題1: Secretsが保存されない

**解決方法**:
- シンタックスエラーがないか確認
- `SERVICE_ACCOUNT_KEY`は3つのシングルクォート（`'''`）で囲む
- JSONの形式が正しいか確認

### 問題2: まだエラーが表示される

**解決方法**:
1. 「Reboot app」をクリック
2. アプリをリロード（`F5`キー）
3. サイドバーから「🔄 システム初期化」を再実行

### 問題3: SERVICE_ACCOUNT_KEYの形式エラー

**解決方法**:
- JSONを3つのシングルクォート（`'''`）で囲む
- JSONの内容に改行が含まれていてもOK
- 例：
  ```toml
  SERVICE_ACCOUNT_KEY = '''
  {
    "type": "service_account",
    "project_id": "...",
    ...
  }
  '''
  ```

---

## ✅ 確認チェックリスト

- [ ] Streamlit Cloudにアクセスできた
- [ ] 「Manage app」→「Settings」を開けた
- [ ] 「Secrets」セクションを見つけた
- [ ] 「Edit secrets」をクリックできた
- [ ] 必要な設定をすべて入力した
- [ ] 「Save」をクリックした
- [ ] 「Reboot app」をクリックした
- [ ] アプリをリロードした
- [ ] 「🔄 システム初期化」を実行した
- [ ] 「✓ 初期化完了」と表示された

---

## 📞 次のステップ

Secretsを設定してアプリを再起動したら：

1. **サイドバーから「🔄 システム初期化」をクリック**
2. **「✓ 初期化完了」と表示されることを確認**
3. **PDFファイルをアップロードしてテスト**

問題が解決しない場合は、Streamlit Cloudのログを確認してください：
- 「Manage app」→「Logs」でエラーの詳細を確認
