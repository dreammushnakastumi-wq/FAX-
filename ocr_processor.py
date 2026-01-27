"""
OCR処理モジュール
Google Document AIを使用したPDFファイルのOCR処理
"""
import os
import logging
from typing import Optional, List
from google.cloud import documentai
from google.api_core import exceptions as api_exceptions

# プロキシ設定を無効化（プロキシエラーを回避）
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRProcessor:
    """Google Document AIを使用したOCR処理クラス"""
    
    def __init__(self, project_id: str, processor_id: str, location: str = 'asia-northeast1'):
        """
        Args:
            project_id: Google Cloud プロジェクトID
            processor_id: Document AIプロセッサーID
            location: プロセッサーのロケーション
        """
        self.project_id = project_id
        self.processor_id = processor_id
        self.location = location
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Document AIクライアントを初期化"""
        try:
            self.client = documentai.DocumentProcessorServiceClient()
            logger.info("Document AIクライアント初期化完了")
        except Exception as e:
            logger.error(f"Document AIクライアント初期化エラー: {e}")
            raise
    
    def extract_text(self, file_path: str) -> str:
        """ファイルからテキストを抽出
        
        Args:
            file_path: 処理するファイルのパス（PDF）
            
        Returns:
            抽出されたテキスト
        """
        try:
            # ファイルを読み込み
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            logger.info(f"Document AIで処理開始: {file_path}")
            
            # プロセッサー名を構築
            processor_name = self.client.processor_path(
                self.project_id, self.location, self.processor_id
            )
            
            # リクエストを作成
            raw_document = documentai.RawDocument(
                content=file_content,
                mime_type='application/pdf'
            )
            
            request = documentai.ProcessRequest(
                name=processor_name,
                raw_document=raw_document
            )
            
            # 処理実行
            result = self.client.process_document(request=request)
            document = result.document
            
            # テキストを抽出
            text = document.text
            
            logger.info(f"Document AI処理完了: {file_path} ({len(text)}文字抽出)")
            return text
            
        except api_exceptions.GoogleAPIError as e:
            logger.error(f"Document AI APIエラー {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Document AI処理エラー {file_path}: {e}")
            raise
    
    def extract_text_by_pages(self, file_path: str) -> List[str]:
        """ファイルからページごとにテキストを抽出
        
        Args:
            file_path: 処理するファイルのパス（PDF）
            
        Returns:
            ページごとのテキストのリスト（[page1_text, page2_text, ...]）
        """
        try:
            # ファイルを読み込み
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            logger.info(f"Document AIで処理開始（ページ分割）: {file_path}")
            
            # プロセッサー名を構築
            processor_name = self.client.processor_path(
                self.project_id, self.location, self.processor_id
            )
            
            # リクエストを作成
            raw_document = documentai.RawDocument(
                content=file_content,
                mime_type='application/pdf'
            )
            
            request = documentai.ProcessRequest(
                name=processor_name,
                raw_document=raw_document
            )
            
            # 処理実行
            result = self.client.process_document(request=request)
            document = result.document
            
            # ページごとのテキストを抽出
            page_texts = []
            full_text = document.text
            
            if not document.pages:
                # ページ情報が取得できない場合は、全体を1ページとして扱う
                logger.warning("ページ情報が取得できませんでした。全体を1ページとして処理します。")
                page_texts = [full_text]
            else:
                total_pages = len(document.pages)
                logger.info(f"PDFファイルは {total_pages} ページです")
                
                # 各ページのテキスト範囲を取得
                for page_num, page in enumerate(document.pages, 1):
                    page_text = ""
                    
                    # ページのlayoutからtext_anchorを取得
                    if hasattr(page, 'layout') and page.layout:
                        if hasattr(page.layout, 'text_anchor') and page.layout.text_anchor:
                            text_anchor = page.layout.text_anchor
                            if text_anchor.text_segments:
                                # text_segmentsの最初と最後を使用してテキスト範囲を取得
                                start_index = text_anchor.text_segments[0].start_index
                                end_index = text_anchor.text_segments[-1].end_index
                                page_text = full_text[start_index:end_index]
                            else:
                                # text_segmentsが空の場合はフォールバック
                                page_text = self._estimate_page_text(full_text, page_num, total_pages)
                        else:
                            # text_anchorがない場合はフォールバック
                            page_text = self._estimate_page_text(full_text, page_num, total_pages)
                    else:
                        # layout情報がない場合はフォールバック
                        page_text = self._estimate_page_text(full_text, page_num, total_pages)
                    
                    page_texts.append(page_text)
                    logger.info(f"ページ {page_num}/{total_pages} のテキスト抽出完了 ({len(page_text)}文字)")
            
            logger.info(f"Document AI処理完了（ページ分割）: {file_path} ({len(page_texts)}ページ, 合計{len(full_text)}文字)")
            return page_texts
            
        except api_exceptions.GoogleAPIError as e:
            logger.error(f"Document AI APIエラー {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Document AI処理エラー（ページ分割） {file_path}: {e}")
            # エラーが発生した場合は、既存のextract_text()を使用してフォールバック
            logger.warning("ページ分割に失敗しました。全体テキストとして処理します。")
            try:
                full_text = self.extract_text(file_path)
                return [full_text]
            except:
                raise
    
    def _estimate_page_text(self, full_text: str, page_num: int, total_pages: int) -> str:
        """ページ番号に基づいてテキストを推定（フォールバック用）
        
        Args:
            full_text: 全体のテキスト
            page_num: ページ番号（1から始まる）
            total_pages: 総ページ数
            
        Returns:
            推定されたページのテキスト
        """
        if total_pages == 1:
            return full_text
        
        # ページごとに均等に分割（簡易的な方法）
        chars_per_page = len(full_text) // total_pages
        start_index = (page_num - 1) * chars_per_page
        end_index = page_num * chars_per_page if page_num < total_pages else len(full_text)
        return full_text[start_index:end_index]
