# streamlit_app.py 使用ガイド

## 概要

`streamlit_app.py`は、出荷管理自動化システムのStreamlit版Webアプリケーションです。
既存のモジュール（`ocr_processor.py`、`ai_extractor.py`、`google_sheets.py`）を活用して、
FAX注文書のPDFファイルを処理し、Googleスプレッドシートに自動保存します。

## ファイル構成

```
fax_order/
├── streamlit_app.py      # 新規作成：Streamlit版Webアプリ
├── ocr_processor.py      # 既存：OCR処理モジュール（変更なし）
├── ai_extractor.py       # 既存：AI抽出モジュール（変更なし）
├── google_sheets.py      # 既存：Googleスプレッドシート連携（変更なし）
└── requirements.txt      # 既存：依存関係（streamlit含む）
```

## 機能

### 必須機能

1. ✅ **PDFファイルのアップロード機能**（複数ファイル対応）
2. ✅ **アップロードされたPDFのOCR処理**
3. ✅ **抽出データのプレビュー表示**
4. ✅ **Googleスプレッドシートへのデータ書き込み**
5. ✅ **処理状況のリアルタイム表示**（プログレスバー）
6. ✅ **成功/エラーメッセージの表示**

### UI構成

- **サイドバー**：
  - 設定表示（スプレッドシートID、OCR言語、AI APIタイプ）
  - システム初期化ボタン
  - ファイルアップローダー
  - ステータス表示

- **メインエリア**：
  - アップロードされたファイル一覧
  - 処理結果の表示
  - 抽出データのプレビュー
  - スプレッドシートへの保存ボタン
  - 処理履歴

## セットアップ

### 必要な環境変数

#### Streamlit Cloudの場合

Streamlit Secretsに以下を設定：

```toml
GOOGLE_SHEETS_ID = "your-spreadsheet-id"
DOCUMENT_AI_PROJECT_ID = "your-project-id"
DOCUMENT_AI_PROCESSOR_ID = "your-processor-id"
DOCUMENT_AI_LOCATION = "asia-northeast1"
SERVICE_ACCOUNT_KEY = '{"type": "service_account", ...}'
ANTHROPIC_API_KEY = "your-anthropic-api-key"
# または
OPENAI_API_KEY = "your-openai-api-key"
AI_API_TYPE = "claude"  # または "openai"
```

#### ローカル環境の場合

`.env`ファイルに以下を設定：

```env
GOOGLE_SHEETS_ID=your-spreadsheet-id
DOCUMENT_AI_PROJECT_ID=your-project-id
DOCUMENT_AI_PROCESSOR_ID=your-processor-id
DOCUMENT_AI_LOCATION=asia-northeast1
ANTHROPIC_API_KEY=your-anthropic-api-key
OPENAI_API_KEY=your-openai-api-key
AI_API_TYPE=claude
```

また、`config/service-account-key.json`にサービスアカウントキーを配置してください。

## 使い方

### 1. アプリの起動

#### ローカル実行

```bash
streamlit run streamlit_app.py
```

#### Streamlit Cloud

1. GitHubリポジトリにプッシュ
2. Streamlit Cloudでデプロイ
3. `streamlit_app.py`をメインファイルとして指定

### 2. システム初期化

1. サイドバーから「🔄 システム初期化」をクリック
2. 必要な設定が完了していることを確認
3. 「✓ システム準備完了」と表示されればOK

### 3. ファイルアップロード

1. サイドバーの「📎 ファイルアップロード」からPDFファイルを選択
2. 複数のファイルを同時にアップロード可能
3. アップロードされたファイル一覧が表示されます

### 4. 処理開始

1. メインエリアの「🚀 処理開始」ボタンをクリック
2. プログレスバーで処理状況を確認
3. 各ファイルの処理状況がリアルタイムで表示されます

### 5. 結果の確認

1. 処理完了後、「📊 抽出データのプレビュー」に結果が表示されます
2. 表形式で抽出データを確認できます
3. 必要に応じてデータを確認・修正

### 6. スプレッドシートに保存

1. 「💾 スプレッドシートに保存」ボタンをクリック
2. データがGoogleスプレッドシートに保存されます
3. 保存成功メッセージが表示されます

## 処理フロー

1. **ファイルアップロード**
   - PDFファイルをアップロード

2. **OCRでテキスト抽出**（`ocr_processor`使用）
   - Google Document AIを使用
   - ページごとにテキストを抽出

3. **データ抽出**（`ai_extractor`使用）
   - Claude/GPT-4 APIを使用
   - OCRテキストから構造化データを抽出

4. **スプレッドシートにフォーマット**
   - 抽出データをスプレッドシート形式に変換

5. **Google Sheetsに書き込み**（`google_sheets`使用）
   - Google Sheets APIを使用
   - データをスプレッドシートに追加

6. **結果表示**
   - 処理結果を表示
   - エラーがあればエラーメッセージを表示

## 既存モジュールとの連携

### ocr_processor.py

```python
from ocr_processor import OCRProcessor

ocr_processor = OCRProcessor(project_id, processor_id, location)
text = ocr_processor.extract_text(file_path)  # 全体テキスト
page_texts = ocr_processor.extract_text_by_pages(file_path)  # ページごと
```

### ai_extractor.py

```python
from ai_extractor import AIExtractor

ai_extractor = AIExtractor(api_type='claude')
order_data = ai_extractor.extract(text, filename)
```

### google_sheets.py

```python
from google_sheets import GoogleSheetsClient

sheets_client = GoogleSheetsClient(spreadsheet_id, service_account_key)
sheets_client.create_header_if_needed()
sheets_client.append_rows(None, rows_to_save)
```

## エラーハンドリング

- **初期化エラー**: 設定が不足している場合にエラーメッセージを表示
- **OCR処理エラー**: ページ分割に失敗した場合は全体テキストとして処理
- **AI抽出エラー**: 各ページでエラーが発生した場合、そのページをスキップ
- **保存エラー**: スプレッドシートへの保存に失敗した場合、エラーメッセージを表示

## トラブルシューティング

### システムが初期化できない

- Streamlit Secretsまたは`.env`ファイルの設定を確認
- サービスアカウントキーが正しく設定されているか確認
- APIキーが正しく設定されているか確認

### OCR処理が失敗する

- Google Document AIの設定を確認
- プロジェクトID、プロセッサーIDが正しいか確認
- サービスアカウントにDocument AI APIの権限があるか確認

### AI抽出が失敗する

- APIキーが正しく設定されているか確認
- APIの使用制限に達していないか確認
- ネットワーク接続を確認

### スプレッドシートに保存できない

- スプレッドシートIDが正しいか確認
- サービスアカウントにスプレッドシートへの書き込み権限があるか確認
- スプレッドシートが存在するか確認

## 既存のfax_order_app.pyとの違い

### streamlit_app.pyの特徴

- **シンプルなUI**: 必要最小限の機能に絞った構成
- **明確な処理フロー**: アップロード→処理→プレビュー→保存の流れが明確
- **エラーハンドリング**: 各段階でのエラーを適切に処理
- **既存モジュールの活用**: 既存のモジュールをそのまま使用

### fax_order_app.pyとの違い

- **編集機能**: `fax_order_app.py`には編集機能があるが、`streamlit_app.py`にはない
- **複雑なUI**: `fax_order_app.py`はより複雑なUIを持っている
- **データ統合**: `fax_order_app.py`は複数ファイルのデータを統合して編集可能にする

## デプロイ

### Streamlit Cloudへのデプロイ

1. GitHubリポジトリにプッシュ
2. Streamlit Cloudで新しいアプリを作成
3. リポジトリとブランチを選択
4. メインファイルに`streamlit_app.py`を指定
5. Streamlit Secretsに必要な設定を追加
6. デプロイ

### ローカル実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# アプリの起動
streamlit run streamlit_app.py
```

## 今後の拡張予定

- [ ] 抽出データの編集機能
- [ ] バッチ処理機能
- [ ] 処理履歴の詳細表示
- [ ] エクスポート機能（CSV、Excel）
- [ ] 設定の保存・読み込み機能

## サポート

問題が発生した場合は、以下のドキュメントを参照してください：

- `SETUP_GUIDE.md` - 包括的なセットアップガイド
- `DEPLOYMENT.md` - デプロイに関する詳細
- `QUICK_START.md` - クイックスタートとFAQ
