# pytesseractエラーの修正方法

## 問題

Streamlit Cloudで以下のエラーが発生：
```
ModuleNotFoundError: This app has encountered an error.
File "/mount/src/fax-/ocr_processor.py", line 6, in <module>
    import pytesseract
```

## 原因

Streamlit Cloudにデプロイされている`ocr_processor.py`が古いバージョンで、`pytesseract`をインポートしようとしています。
現在のローカルファイルには`pytesseract`のインポートはありません（Google Document AIを使用）。

## 解決方法

### 方法1: 最新のファイルをGitHubにプッシュ（推奨）

1. **現在のファイルを確認**
   ```bash
   cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
   type ocr_processor.py | findstr /n "pytesseract"
   ```
   何も表示されなければ、ファイルは正しいです。

2. **GitHubにプッシュ**
   ```bash
   git add ocr_processor.py
   git commit -m "Fix: Remove pytesseract import (use Google Document AI)"
   git push origin main
   ```

3. **Streamlit Cloudで再デプロイ**
   - Streamlit Cloudが自動的に変更を検知して再デプロイします
   - または、Streamlit Cloudの「Manage app」→「Reboot app」をクリック

### 方法2: Streamlit Cloudで直接確認

1. **Streamlit Cloudのログを確認**
   - 「Manage app」→「Logs」をクリック
   - エラーの詳細を確認

2. **GitHubリポジトリを確認**
   - GitHubで`ocr_processor.py`を開く
   - 6行目に`import pytesseract`があるか確認
   - あれば、ローカルのファイルをプッシュ

## 確認事項

### 現在のocr_processor.pyの状態

現在のファイルは以下のインポートのみ：
```python
import os
import logging
from typing import Optional, List
from google.cloud import documentai
from google.api_core import exceptions as api_exceptions
```

`pytesseract`のインポートは**ありません**。

### requirements.txtの確認

`requirements.txt`にも`pytesseract`は含まれていません（正しい）。

## トラブルシューティング

### エラーが続く場合

1. **GitHubリポジトリを確認**
   - `ocr_processor.py`の内容を確認
   - 6行目に`import pytesseract`があるか確認

2. **ローカルファイルとGitHubの差分を確認**
   ```bash
   git diff HEAD ocr_processor.py
   ```

3. **強制的にプッシュ（注意：他の変更を上書きする可能性があります）**
   ```bash
   git add ocr_processor.py
   git commit -m "Fix: Remove pytesseract import"
   git push origin main --force
   ```

### まだエラーが発生する場合

1. **Streamlit Cloudのキャッシュをクリア**
   - 「Manage app」→「Settings」→「Clear cache」をクリック

2. **アプリを再起動**
   - 「Manage app」→「Reboot app」をクリック

## 確認コマンド

### ローカルで確認

```bash
# ファイルの内容を確認
type ocr_processor.py | findstr /n "pytesseract"

# 何も表示されなければ、ファイルは正しいです
```

### GitHubで確認

1. GitHubリポジトリを開く
2. `ocr_processor.py`を開く
3. 6行目を確認
4. `import pytesseract`があれば、ローカルのファイルをプッシュ

## まとめ

- **現在のローカルファイルは正しい**（`pytesseract`のインポートなし）
- **Streamlit Cloudにデプロイされているファイルが古い**
- **最新のファイルをGitHubにプッシュして再デプロイ**
