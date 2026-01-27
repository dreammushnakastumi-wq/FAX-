"""
Googleスプレッドシート連携モジュール
データをGoogleスプレッドシートに自動投入する
"""
import os
import json
from typing import List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

try:
    import httplib2
    HTTPLIB2_AVAILABLE = True
except ImportError:
    HTTPLIB2_AVAILABLE = False

# プロキシ設定を無効化（プロキシエラーを回避）
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Sheets API スコープ
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsClient:
    """Googleスプレッドシート連携クラス"""
    
    def __init__(self, spreadsheet_id: str, service_account_key: Optional[str] = None, 
                 credentials_path: Optional[str] = None):
        """
        Args:
            spreadsheet_id: GoogleスプレッドシートのID
            service_account_key: サービスアカウントキーのJSON文字列（Streamlit Secrets用）
            credentials_path: 認証情報JSONファイルのパス（ローカル環境用、後方互換性）
        """
        self.spreadsheet_id = spreadsheet_id
        self.service_account_key = service_account_key
        self.credentials_path = credentials_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Google API認証（サービスアカウントを使用）"""
        creds = None
        
        # Streamlit Secretsからサービスアカウントキーを読み込む（優先）
        if self.service_account_key:
            try:
                service_account_info = json.loads(self.service_account_key)
                creds = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=SCOPES
                )
                logger.info("サービスアカウント認証完了（Streamlit Secrets）")
            except Exception as e:
                logger.error(f"サービスアカウントキーの読み込みエラー: {e}")
                raise
        
        # ファイルからサービスアカウントキーを読み込む（後方互換性）
        elif self.credentials_path and os.path.exists(self.credentials_path):
            try:
                creds = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=SCOPES
                )
                logger.info("サービスアカウント認証完了（ファイル）")
            except Exception as e:
                logger.error(f"サービスアカウントファイルの読み込みエラー: {e}")
                raise
        
        # 環境変数からサービスアカウントキーを読み込む（後方互換性）
        elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                creds = service_account.Credentials.from_service_account_file(
                    os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
                    scopes=SCOPES
                )
                logger.info("サービスアカウント認証完了（環境変数）")
            except Exception as e:
                logger.error(f"環境変数からのサービスアカウント読み込みエラー: {e}")
                raise
        
        else:
            raise ValueError(
                "認証情報が見つかりません。以下のいずれかを設定してください:\n"
                "1. Streamlit SecretsのSERVICE_ACCOUNT_KEY\n"
                "2. credentials_pathパラメータ\n"
                "3. GOOGLE_APPLICATION_CREDENTIALS環境変数"
            )
        
        # プロキシなしでHTTPクライアントを作成（可能な場合）
        if HTTPLIB2_AVAILABLE:
            try:
                http = httplib2.Http(proxy_info=None)
                self.service = build('sheets', 'v4', credentials=creds, http=http)
            except Exception as e:
                logger.warning(f"プロキシなしHTTPクライアントの作成に失敗: {e}。デフォルト設定を使用します。")
                self.service = build('sheets', 'v4', credentials=creds)
        else:
            self.service = build('sheets', 'v4', credentials=creds)
        logger.info("Google Sheets API認証完了")
    
    def append_rows(self, sheet_name: str = None, values: List[List[str]] = None):
        """スプレッドシートに行を追加
        
        Args:
            sheet_name: シート名（Noneの場合は最初のシートを使用）
            values: 追加する行データのリスト
        """
        if sheet_name is None:
            sheet_name = self.get_first_sheet_name()
        
        try:
            body = {
                'values': values
            }
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{sheet_name}'!A:Z",
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"{len(values)}行を追加しました: {sheet_name}")
            return result
        except HttpError as error:
            logger.error(f"スプレッドシート更新エラー: {error}")
            raise
    
    def get_first_sheet_name(self) -> str:
        """最初のシート名を取得
        
        Returns:
            最初のシート名
        """
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            sheets = spreadsheet.get('sheets', [])
            if sheets:
                return sheets[0]['properties']['title']
            return 'Sheet1'
        except HttpError as error:
            logger.error(f"シート名取得エラー: {error}")
            return 'Sheet1'
    
    def get_header_row(self, sheet_name: str = None) -> List[str]:
        """ヘッダー行を取得
        
        Args:
            sheet_name: シート名（Noneの場合は最初のシートを使用）
            
        Returns:
            ヘッダー行のリスト
        """
        if sheet_name is None:
            sheet_name = self.get_first_sheet_name()
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{sheet_name}'!A1:M1"
            ).execute()
            
            values = result.get('values', [])
            if values:
                return values[0]
            return []
        except HttpError as error:
            logger.error(f"ヘッダー取得エラー: {error}")
            return []
    
    def create_header_if_needed(self, sheet_name: str = None):
        """ヘッダー行が存在しない場合に作成
        
        Args:
            sheet_name: シート名（Noneの場合は最初のシートを使用）
        """
        if sheet_name is None:
            sheet_name = self.get_first_sheet_name()
        
        headers = self.get_header_row(sheet_name)
        expected_headers = [
            '日付', '発注番号', '得意先名', '納品先名', '品名', '数量', 
            '単位', '単価', '金額', '納品日', '備考', '処理日時', '元ファイル名'
        ]
        
        if not headers or headers != expected_headers:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{sheet_name}'!A1:M1",
                valueInputOption='USER_ENTERED',
                body={'values': [expected_headers]}
            ).execute()
            logger.info(f"ヘッダー行を作成しました: {sheet_name}")
