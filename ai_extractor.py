"""
AI構造化抽出モジュール
Claude/GPT-4 APIを使用してOCRテキストから構造化データを抽出
"""
import json
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time

# プロキシ設定を無効化（プロキシエラーを回避）
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Claude API
try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    logger.warning("anthropicパッケージがインストールされていません。Claude APIは使用できません。")

# OpenAI API（オプション）
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("openaiパッケージがインストールされていません。GPT-4 APIは使用できません。")


class AIExtractor:
    """AIを使用した構造化データ抽出クラス"""
    
    def __init__(self, api_type: str = 'claude', api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Args:
            api_type: 使用するAPIタイプ（'claude' または 'openai'）
            api_key: APIキー（Noneの場合は環境変数から取得）
            model: 使用するモデル名（Noneの場合はデフォルト）
        """
        self.api_type = api_type.lower()
        self.api_key = api_key or self._get_api_key()
        self.model = model or self._get_default_model()
        self.client = None
        self._initialize_client()
    
    def _get_api_key(self) -> Optional[str]:
        """環境変数からAPIキーを取得"""
        if self.api_type == 'claude':
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                # APIキーから余分な空白や改行を削除し、文字列として返す
                return str(api_key).strip()
            return None
        elif self.api_type == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                return str(api_key).strip()
            return None
        return None
    
    def _get_default_model(self) -> str:
        """デフォルトモデル名を取得"""
        if self.api_type == 'claude':
            return os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
        elif self.api_type == 'openai':
            return os.getenv('OPENAI_MODEL', 'gpt-4o')
        return 'claude-sonnet-4-5-20250929'
    
    def _initialize_client(self):
        """APIクライアントを初期化"""
        if not self.api_key:
            raise ValueError(f"{self.api_type.upper()} APIキーが設定されていません。環境変数を確認してください。")
        
        if self.api_type == 'claude':
            if not CLAUDE_AVAILABLE:
                raise ImportError("anthropicパッケージがインストールされていません。pip install anthropic を実行してください。")
            # APIキーから余分な空白や改行を削除
            api_key_clean = self.api_key.strip()
            self.client = Anthropic(api_key=api_key_clean)
            logger.info(f"Claude APIクライアント初期化完了（モデル: {self.model}）")
        
        elif self.api_type == 'openai':
            if not OPENAI_AVAILABLE:
                raise ImportError("openaiパッケージがインストールされていません。pip install openai を実行してください。")
            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"OpenAI APIクライアント初期化完了（モデル: {self.model}）")
        
        else:
            raise ValueError(f"サポートされていないAPIタイプ: {self.api_type}")
    
    def _create_extraction_prompt(self, text: str) -> str:
        """構造化抽出用のプロンプトを作成
        
        Args:
            text: OCRで抽出されたテキスト
            
        Returns:
            プロンプト文字列
        """
        prompt = f"""以下のFAX注文書のテキストから、注文情報を構造化して抽出してください。

【抽出する項目】
- 日付（YYYY-MM-DD形式）
- 発注番号（発注№、注文番号など）
- 得意先名（発注者名）
  ※重要：得意先名は、右上の発注№や発注日に近い部分にある会社名を抽出してください。
  例：株式会社 新栄物産など、発注番号の近くに記載されている会社名が正しい得意先名です。
- 納品先名
- 商品情報（複数商品がある場合は全て抽出）
  - 品名
  - 数量（正確に抽出してください。抜けや間違いがないよう注意）
  - 単位（kg、CS、個、箱など。見つからない場合は空文字列）
  - 単価
  - 金額
- 納品日（YYYY-MM-DD形式、あれば）
- 備考（特記事項、メモなど）

【テキスト】
{text}

【出力形式】
JSON形式で出力してください。以下の形式に従ってください：

{{
  "date": "2024-01-15",
  "order_number": "PO-2024-001",
  "customer_name": "株式会社サンプル",
  "delivery_name": "株式会社納品先",
  "items": [
    {{
      "product_name": "商品名1",
      "quantity": "10",
      "unit": "kg",
      "unit_price": "1000",
      "amount": "10000"
    }},
    {{
      "product_name": "商品名2",
      "quantity": "5",
      "unit": "CS",
      "unit_price": "2000",
      "amount": "10000"
    }}
  ],
  "delivery_date": "2024-01-20",
  "remarks": "特記事項があれば記載"
}}

見つからない項目は空文字列（""）または空配列（[]）で返してください。
日付は必ずYYYY-MM-DD形式で返してください。
"""
        return prompt
    
    def _extract_with_claude(self, text: str, max_retries: int = 3) -> Dict:
        """Claude APIを使用してデータを抽出
        
        Args:
            text: OCRで抽出されたテキスト
            max_retries: 最大リトライ回数
            
        Returns:
            抽出されたデータの辞書
        """
        prompt = self._create_extraction_prompt(text)
        
        for attempt in range(max_retries):
            try:
                # プロンプトが文字列であることを確認
                if not isinstance(prompt, str):
                    prompt = str(prompt)
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                # レスポンスからテキストを取得
                content = response.content[0].text
                
                # JSONを抽出（コードブロックがある場合は除去）
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                # JSONをパース
                data = json.loads(content)
                
                logger.info("Claude APIでデータ抽出成功")
                return data
                
            except json.JSONDecodeError as e:
                logger.warning(f"JSON解析エラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数バックオフ
                    continue
                raise
            except Exception as e:
                logger.error(f"Claude API呼び出しエラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
    
    def _extract_with_openai(self, text: str, max_retries: int = 3) -> Dict:
        """OpenAI APIを使用してデータを抽出
        
        Args:
            text: OCRで抽出されたテキスト
            max_retries: 最大リトライ回数
            
        Returns:
            抽出されたデータの辞書
        """
        prompt = self._create_extraction_prompt(text)
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたはFAX注文書から構造化データを抽出する専門家です。JSON形式で正確にデータを返してください。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type": "json_object"}
                )
                
                # レスポンスからテキストを取得
                content = response.choices[0].message.content
                
                # JSONをパース
                data = json.loads(content)
                
                logger.info("OpenAI APIでデータ抽出成功")
                return data
                
            except json.JSONDecodeError as e:
                logger.warning(f"JSON解析エラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
            except Exception as e:
                logger.error(f"OpenAI API呼び出しエラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
    
    def extract(self, text: str, filename: str = '') -> Dict:
        """OCRテキストから構造化データを抽出
        
        Args:
            text: OCRで抽出されたテキスト
            filename: 元ファイル名
            
        Returns:
            抽出された注文データの辞書
        """
        logger.info(f"AI抽出開始: {filename}")
        
        try:
            if self.api_type == 'claude':
                data = self._extract_with_claude(text)
            elif self.api_type == 'openai':
                data = self._extract_with_openai(text)
            else:
                raise ValueError(f"サポートされていないAPIタイプ: {self.api_type}")
            
            # データがリストの場合は最初の要素を取得
            if isinstance(data, list):
                if len(data) > 0:
                    data = data[0]
                else:
                    logger.warning("AIからのレスポンスが空のリストです。デフォルト値を設定します。")
                    data = {}
            
            # データが辞書でない場合はエラー
            if not isinstance(data, dict):
                logger.error(f"予期しないデータ型: {type(data)}。データ: {data}")
                raise ValueError(f"AIからのレスポンスが辞書形式ではありません: {type(data)}")
            
            # データを標準形式に変換
            result = {
                'date': data.get('date', ''),
                'order_number': data.get('order_number', ''),
                'customer_name': data.get('customer_name', ''),
                'delivery_name': data.get('delivery_name', ''),
                'delivery_date': data.get('delivery_date', ''),
                'items': data.get('items', []),
                'remarks': data.get('remarks', ''),
                'filename': filename,
                'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'raw_text': text[:500]  # デバッグ用
            }
            
            logger.info(f"AI抽出完了: 日付={result['date']}, 発注番号={result['order_number']}, 得意先={result['customer_name']}, 商品数={len(result['items'])}")
            
            return result
            
        except Exception as e:
            logger.error(f"AI抽出エラー: {e}", exc_info=True)
            raise
    
    def format_for_sheets(self, order_data: Dict) -> List[List[str]]:
        """スプレッドシート用にフォーマット
        
        Args:
            order_data: 抽出された注文データ
            
        Returns:
            スプレッドシートの行データのリスト
        """
        rows = []
        
        if not order_data.get('items'):
            # 商品情報がない場合は1行だけ
            rows.append([
                order_data.get('date', ''),
                order_data.get('order_number', ''),
                order_data.get('customer_name', ''),
                order_data.get('delivery_name', ''),
                '',  # 品名
                '',  # 数量
                '',  # 単位
                '',  # 単価
                '',  # 金額
                order_data.get('delivery_date', ''),
                order_data.get('remarks', ''),
                order_data.get('processed_at', ''),
                order_data.get('filename', ''),
            ])
        else:
            # 各商品ごとに1行
            for item in order_data['items']:
                rows.append([
                    order_data.get('date', ''),
                    order_data.get('order_number', ''),
                    order_data.get('customer_name', ''),
                    order_data.get('delivery_name', ''),
                    item.get('product_name', ''),
                    item.get('quantity', ''),
                    item.get('unit', ''),
                    item.get('unit_price', ''),
                    item.get('amount', ''),
                    order_data.get('delivery_date', ''),
                    order_data.get('remarks', ''),
                    order_data.get('processed_at', ''),
                    order_data.get('filename', ''),
                ])
        
        return rows
