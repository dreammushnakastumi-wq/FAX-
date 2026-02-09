"""
OCR処理モジュール
Google Document AIを使用したPDFファイルのOCR処理
"""
import os
import logging
import tempfile
from typing import Optional, List
from google.cloud import documentai
from google.api_core import exceptions as api_exceptions
from pypdf import PdfReader, PdfWriter

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
        # PDFのページ数を確認
        try:
            page_count = self._get_pdf_page_count(file_path)
            logger.info(f"PDFページ数: {page_count}ページ")
        except Exception as e:
            logger.warning(f"ページ数取得に失敗しました。通常処理を続行します: {e}")
            page_count = None
        
        # 15ページ以上の場合は分割して処理
        split_files = []
        temp_files_to_cleanup = []
        
        try:
            if page_count and page_count > 15:
                logger.info(f"PDFが{page_count}ページのため、15ページごとに分割して処理します")
                split_files = self._split_pdf(file_path, max_pages=15)
                # 元のファイル以外の一時ファイルを記録（クリーンアップ用）
                temp_files_to_cleanup = [f for f in split_files if f != file_path]
            else:
                split_files = [file_path]
            
            # すべての分割ファイル（または元のファイル）を処理
            all_page_texts = []
            
            for split_file in split_files:
                try:
                    # ファイルを読み込み
                    with open(split_file, 'rb') as f:
                        file_content = f.read()
                    
                    logger.info(f"Document AIで処理開始（ページ分割）: {split_file}")
                    
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
                    full_text = document.text
                    
                    if not document.pages:
                        # ページ情報が取得できない場合は、全体を1ページとして扱う
                        logger.warning("ページ情報が取得できませんでした。全体を1ページとして処理します。")
                        all_page_texts.append(full_text)
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
                            
                            all_page_texts.append(page_text)
                            logger.info(f"ページ {page_num}/{total_pages} のテキスト抽出完了 ({len(page_text)}文字)")
                    
                    logger.info(f"Document AI処理完了（ページ分割）: {split_file} ({len(document.pages) if document.pages else 1}ページ)")
                    
                except api_exceptions.GoogleAPIError as e:
                    error_msg = str(e)
                    # ページ数制限エラーの場合
                    if "PAGE_LIMIT_EXCEEDED" in error_msg or "page limit" in error_msg.lower():
                        logger.error(f"Document AI APIエラー（ページ数制限） {split_file}: {e}")
                        raise Exception(f"PDF分割処理後もページ数制限エラーが発生しました: {e}")
                    else:
                        logger.error(f"Document AI APIエラー {split_file}: {e}")
                        raise
                except Exception as e:
                    logger.error(f"Document AI処理エラー（ページ分割） {split_file}: {e}")
                    raise
            
            logger.info(f"Document AI処理完了（全分割ファイル）: {file_path} (合計{len(all_page_texts)}ページ)")
            return all_page_texts
            
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
        finally:
            # 一時ファイルをクリーンアップ
            for temp_file in temp_files_to_cleanup:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                        logger.info(f"一時ファイルを削除: {temp_file}")
                except Exception as e:
                    logger.warning(f"一時ファイル削除エラー {temp_file}: {e}")
    
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
    
    def _get_pdf_page_count(self, file_path: str) -> int:
        """PDFファイルのページ数を取得
        
        Args:
            file_path: PDFファイルのパス
            
        Returns:
            ページ数
        """
        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except Exception as e:
            logger.error(f"PDFページ数取得エラー {file_path}: {e}")
            raise
    
    def _split_pdf(self, file_path: str, max_pages: int = 15) -> List[str]:
        """PDFを指定ページ数ごとに分割
        
        Args:
            file_path: 元のPDFファイルパス
            max_pages: 1つのPDFの最大ページ数（デフォルト: 15）
        
        Returns:
            分割されたPDFファイルパスのリスト（分割不要の場合は元のファイルパスのみ）
        """
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            
            if total_pages <= max_pages:
                logger.info(f"PDF分割不要: {total_pages}ページ（上限: {max_pages}ページ）")
                return [file_path]  # 分割不要
            
            logger.info(f"PDF分割開始: {total_pages}ページを{max_pages}ページごとに分割")
            split_files = []
            
            for start_page in range(0, total_pages, max_pages):
                end_page = min(start_page + max_pages, total_pages)
                writer = PdfWriter()
                
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # 一時ファイルとして保存
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                writer.write(temp_file)
                temp_file.close()
                split_files.append(temp_file.name)
                logger.info(f"PDF分割完了: ページ {start_page + 1}-{end_page} -> {temp_file.name}")
            
            logger.info(f"PDF分割完了: {len(split_files)}個のファイルに分割")
            return split_files
            
        except Exception as e:
            logger.error(f"PDF分割エラー {file_path}: {e}")
            raise