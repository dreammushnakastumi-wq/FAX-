"""
FAX注文書自動処理システム Streamlit WEBアプリ
Streamlit Community Cloud対応版
"""
import os
import tempfile
import json
from pathlib import Path
from dotenv import load_dotenv
import logging
import streamlit as st
import pandas as pd

# プロキシ設定を無効化（プロキシエラーを回避）
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

from ocr_processor import OCRProcessor
from ai_extractor import AIExtractor
from google_sheets import GoogleSheetsClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境変数を読み込み（ローカル環境用）
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="FAX注文書自動処理システム",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSSでフォントサイズを大きくする
st.markdown("""
<style>
    .main .block-container {
        font-size: 28px;
    }
    h1 {
        font-size: 3.5rem !important;
    }
    h2 {
        font-size: 3rem !important;
    }
    h3 {
        font-size: 2.5rem !important;
    }
    .stMarkdown {
        font-size: 28px !important;
    }
    .stDataFrame {
        font-size: 26px !important;
    }
    /* データエディタ（表）のフォントサイズを大きく */
    .stDataEditor {
        font-size: 36px !important;
    }
    .stDataEditor table {
        font-size: 36px !important;
    }
    .stDataEditor th {
        font-size: 36px !important;
        padding: 24px !important;
        font-weight: bold !important;
    }
    .stDataEditor td {
        font-size: 36px !important;
        padding: 24px !important;
    }
    .stDataEditor input {
        font-size: 36px !important;
        padding: 20px !important;
        min-height: 60px !important;
    }
    .stDataEditor textarea {
        font-size: 36px !important;
        padding: 20px !important;
    }
    /* テキスト入力フィールドのフォントサイズ */
    .stTextInput input {
        font-size: 28px !important;
        padding: 16px !important;
        min-height: 50px !important;
    }
    /* ボタンのフォントサイズ */
    .stButton > button {
        font-size: 26px !important;
        padding: 16px 32px !important;
    }
    /* セレクトボックスのフォントサイズ */
    .stSelectbox label {
        font-size: 28px !important;
    }
    .stSelectbox select {
        font-size: 28px !important;
        padding: 16px !important;
    }
    .editable-field {
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    .editable-field:hover {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.error = None
    st.session_state.ocr_processor = None
    st.session_state.ai_extractor = None
    st.session_state.sheets_client = None
    st.session_state.processed_data = []
    st.session_state.combined_data = []


def get_secrets():
    """Streamlit Secretsまたは環境変数から設定を取得"""
    secrets = {}
    
    # Streamlit Secretsから読み込み（優先）
    try:
        if hasattr(st, 'secrets') and st.secrets:
            secrets['spreadsheet_id'] = st.secrets.get('GOOGLE_SHEETS_ID', os.getenv('GOOGLE_SHEETS_ID'))
            secrets['project_id'] = st.secrets.get('DOCUMENT_AI_PROJECT_ID', os.getenv('DOCUMENT_AI_PROJECT_ID'))
            secrets['processor_id'] = st.secrets.get('DOCUMENT_AI_PROCESSOR_ID', os.getenv('DOCUMENT_AI_PROCESSOR_ID'))
            secrets['location'] = st.secrets.get('DOCUMENT_AI_LOCATION', os.getenv('DOCUMENT_AI_LOCATION', 'asia-northeast1'))
            # SERVICE_ACCOUNT_KEYは文字列として取得（プレースホルダーの場合はNone）
            service_account_key = st.secrets.get('SERVICE_ACCOUNT_KEY', '')
            if service_account_key and service_account_key.strip() and 'your-project-id' not in service_account_key:
                secrets['service_account_key'] = service_account_key
            else:
                secrets['service_account_key'] = None
            secrets['anthropic_api_key'] = st.secrets.get('ANTHROPIC_API_KEY', os.getenv('ANTHROPIC_API_KEY'))
            secrets['openai_api_key'] = st.secrets.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
            secrets['api_type'] = st.secrets.get('AI_API_TYPE', os.getenv('AI_API_TYPE', 'claude'))
        else:
            # 環境変数から読み込み（ローカル環境用）
            secrets['spreadsheet_id'] = os.getenv('GOOGLE_SHEETS_ID')
            secrets['project_id'] = os.getenv('DOCUMENT_AI_PROJECT_ID')
            secrets['processor_id'] = os.getenv('DOCUMENT_AI_PROCESSOR_ID')
            secrets['location'] = os.getenv('DOCUMENT_AI_LOCATION', 'asia-northeast1')
            secrets['service_account_key'] = None  # ローカル環境ではファイルから読み込む
            secrets['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
            secrets['openai_api_key'] = os.getenv('OPENAI_API_KEY')
            secrets['api_type'] = os.getenv('AI_API_TYPE', 'claude')
    except Exception as e:
        logger.warning(f"Secrets読み込みエラー: {e}")
        # 環境変数から読み込み
        secrets['spreadsheet_id'] = os.getenv('GOOGLE_SHEETS_ID')
        secrets['project_id'] = os.getenv('DOCUMENT_AI_PROJECT_ID')
        secrets['processor_id'] = os.getenv('DOCUMENT_AI_PROCESSOR_ID')
        secrets['location'] = os.getenv('DOCUMENT_AI_LOCATION', 'asia-northeast1')
        secrets['service_account_key'] = None
        secrets['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
        secrets['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        secrets['api_type'] = os.getenv('AI_API_TYPE', 'claude')
    
    return secrets


def initialize_components(api_type: str = 'claude'):
    """コンポーネントを初期化"""
    try:
        secrets = get_secrets()
        
        # 必須設定のチェック
        if not secrets['spreadsheet_id']:
            raise ValueError("GOOGLE_SHEETS_IDが設定されていません。")
        
        if not secrets['project_id'] or not secrets['processor_id']:
            raise ValueError("DOCUMENT_AI_PROJECT_IDまたはDOCUMENT_AI_PROCESSOR_IDが設定されていません。")
        
        # AI APIキーのチェック
        if api_type == 'claude' and not secrets['anthropic_api_key']:
            raise ValueError("ANTHROPIC_API_KEYが設定されていません。")
        elif api_type == 'openai' and not secrets['openai_api_key']:
            raise ValueError("OPENAI_API_KEYが設定されていません。")
        
        # Document AI認証の設定（環境変数またはサービスアカウントキー）
        if secrets['service_account_key']:
            # Streamlit Secretsからサービスアカウントキーを設定
            service_account_info = json.loads(secrets['service_account_key'])
            # 一時ファイルを作成して環境変数に設定
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
                json.dump(service_account_info, tmp_file)
                tmp_path = tmp_file.name
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = tmp_path
        
        # インスタンスの作成
        ocr_processor = OCRProcessor(
            secrets['project_id'], 
            secrets['processor_id'], 
            secrets['location']
        )
        
        ai_extractor = AIExtractor(api_type=api_type)
        
        # Google Sheetsクライアントの作成
        credentials_path = 'config/service-account-key.json' if not secrets['service_account_key'] else None
        sheets_client = GoogleSheetsClient(
            secrets['spreadsheet_id'],
            service_account_key=secrets['service_account_key'],
            credentials_path=credentials_path
        )
        
        # ヘッダー行の確認・作成
        sheets_client.create_header_if_needed()
        
        st.session_state.ocr_processor = ocr_processor
        st.session_state.ai_extractor = ai_extractor
        st.session_state.sheets_client = sheets_client
        st.session_state.initialized = True
        st.session_state.error = None
        
        return True
        
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)
        logger.error(f"初期化エラー: {e}", exc_info=True)
        return False


def process_file_for_web(file_path: str, filename: str) -> dict:
    """ファイルを処理して結果を返す（WEBアプリ用）"""
    ocr_processor = st.session_state.ocr_processor
    ai_extractor = st.session_state.ai_extractor
    
    result = {
        'filename': filename,
        'success': False,
        'pages': [],
        'error': None,
        'total_pages': 0
    }
    
    try:
        logger.info(f"処理開始: {filename}")
        
        # OCR処理
        try:
            logger.info(f"OCR処理開始: {filename}")
            logger.info(f"OCRプロセッサー: {type(ocr_processor).__name__}")
            logger.info(f"ファイルパス: {file_path}")
            logger.info(f"ファイル存在確認: {os.path.exists(file_path)}")
            
            page_texts = ocr_processor.extract_text_by_pages(file_path)
            logger.info(f"OCR処理完了: {filename} ({len(page_texts)}ページ)")
        except Exception as e:
            logger.warning(f"ページ分割に失敗しました。全体テキストとして処理します: {e}")
            logger.warning(f"エラー詳細: {str(e)}")
            try:
                logger.info(f"全体テキスト抽出を試行: {filename}")
                text = ocr_processor.extract_text(file_path)
                if not text.strip():
                    raise ValueError("テキストが抽出できませんでした")
                page_texts = [text]
                logger.info(f"OCR処理完了（全体テキスト）: {filename} ({len(text)}文字)")
            except Exception as ocr_error:
                error_msg = f"OCR処理エラー: {str(ocr_error)}"
                result['error'] = error_msg
                logger.error(f"OCR処理エラー {file_path}: {ocr_error}", exc_info=True)
                import traceback
                logger.error(f"OCRエラートレースバック: {traceback.format_exc()}")
                return result
        
        total_pages = len(page_texts)
        result['total_pages'] = total_pages
        
        if total_pages == 0:
            raise ValueError("ページが抽出できませんでした")
        
        # 各ページを処理
        for page_num, page_text in enumerate(page_texts, 1):
            if not page_text.strip():
                logger.warning(f"ページ {page_num} のテキストが空です。スキップします。")
                continue
            
            page_filename = f"{filename} (ページ{page_num})"
            logger.info(f"AI抽出開始: {page_filename}")
            
            try:
                # AIでデータ抽出
                logger.info(f"AI抽出開始: {page_filename} (テキスト長: {len(page_text)}文字)")
                logger.info(f"AI抽出器: {type(ai_extractor).__name__}, APIタイプ: {ai_extractor.api_type}")
                order_data = ai_extractor.extract(page_text, page_filename)
                logger.info(f"AI抽出完了: {page_filename}")
                
                result['pages'].append({
                    'page_num': page_num,
                    'data': order_data,
                    'success': True
                })
            except Exception as ai_error:
                error_msg = f"AI抽出エラー（ページ{page_num}）: {str(ai_error)}"
                logger.error(f"AI抽出エラー {page_filename}: {ai_error}", exc_info=True)
                result['pages'].append({
                    'page_num': page_num,
                    'data': {},
                    'success': False,
                    'error': error_msg
                })
        
        result['success'] = len(result['pages']) > 0
        
        if not result['success']:
            result['error'] = "すべてのページで処理に失敗しました"
        
        logger.info(f"処理完了: {filename} (成功: {result['success']}, ページ数: {len(result['pages'])})")
        
    except Exception as e:
        error_msg = f"処理エラー: {str(e)}"
        result['error'] = error_msg
        logger.error(f"処理エラー {file_path}: {e}", exc_info=True)
        import traceback
        logger.error(f"トレースバック: {traceback.format_exc()}")
    
    return result


def main():
    """メイン処理"""
    st.title("📄 FAX注文書自動処理システム")
    st.markdown("---")
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # AI APIタイプの選択
        api_type = st.selectbox(
            "使用するAI API",
            ["claude", "openai"],
            index=0
        )
        
        # 初期化ボタン
        if st.button("🔄 システム初期化", use_container_width=True):
            with st.spinner("初期化中..."):
                if initialize_components(api_type):
                    st.success("✓ 初期化完了")
                    st.rerun()
                else:
                    st.error(f"✗ 初期化エラー: {st.session_state.error}")
        
        st.markdown("---")
        
        # ステータス表示
        if st.session_state.initialized:
            st.success("✓ システム準備完了")
        else:
            st.error("✗ システム未初期化")
            if st.session_state.error:
                st.caption(f"エラー: {st.session_state.error}")
    
    # メイン画面
    if not st.session_state.initialized:
        st.warning("⚠️ サイドバーから「システム初期化」を実行してください。")
        st.info("""
        **初期化に必要な設定:**
        
        **Streamlit Cloudの場合:**
        - Streamlit Secretsに以下を設定してください:
          - `GOOGLE_SHEETS_ID`
          - `DOCUMENT_AI_PROJECT_ID`
          - `DOCUMENT_AI_PROCESSOR_ID`
          - `DOCUMENT_AI_LOCATION` (オプション、デフォルト: asia-northeast1)
          - `SERVICE_ACCOUNT_KEY` (サービスアカウントキーのJSON文字列)
          - `ANTHROPIC_API_KEY` または `OPENAI_API_KEY`
          - `AI_API_TYPE` (オプション、デフォルト: claude)
        
        **ローカル環境の場合:**
        - `.env`ファイルに上記の設定を追加
        - `config/service-account-key.json`にサービスアカウントキーを配置
        """)
        return
    
    # ファイルアップロード
    st.subheader("📎 ファイルアップロード")
    uploaded_files = st.file_uploader(
        "PDFファイルをアップロードしてください（複数選択可能、最大10ファイル）",
        type=['pdf'],
        accept_multiple_files=True,
        help="FAX注文書のPDFファイルを選択してください。複数のファイルを同時にアップロードできます（最大10ファイル）。"
    )
    
    # アップロードされたファイルのリストを表示（最大10ファイル）
    if uploaded_files is not None and len(uploaded_files) > 0:
        st.info(f"📄 アップロードされたファイル: {len(uploaded_files)}個")
        # 最大10ファイルまで表示
        display_files = uploaded_files[:10]
        for idx, file in enumerate(display_files, 1):
            st.text(f"{idx}. {file.name}")
        if len(uploaded_files) > 10:
            st.warning(f"⚠️ {len(uploaded_files)}個のファイルがアップロードされましたが、最初の10ファイルのみ処理されます。")
            uploaded_files = uploaded_files[:10]
    
    # 既存の統合データがある場合は表示
    if 'combined_data' in st.session_state and st.session_state.combined_data:
        st.subheader("📊 抽出結果（編集可能）")
        st.markdown("💡 **ヒント:** 表を直接編集できます。編集内容は自動的に保存されます。")
        
        # DataFrameに変換
        df = pd.DataFrame(st.session_state.combined_data)
        
        # データが30行未満の場合は空行を追加して30行にする
        min_rows = 30
        if len(df) < min_rows:
            # 空の行を追加
            empty_rows = []
            for i in range(min_rows - len(df)):
                empty_row = {col: '' for col in df.columns}
                empty_rows.append(empty_row)
            if empty_rows:
                empty_df = pd.DataFrame(empty_rows)
                df = pd.concat([df, empty_df], ignore_index=True)
        
        # 編集可能なテーブルとして表示
        edited_df = st.data_editor(
            df,
            width='stretch',
            num_rows="fixed",
            key="combined_data_editor_existing",
            column_config={
                'ファイル名': st.column_config.TextColumn('ファイル名', disabled=True),
                'ページ': st.column_config.NumberColumn('ページ', disabled=True, format="%d"),
                '日付': st.column_config.TextColumn('日付'),
                '発注番号': st.column_config.TextColumn('発注番号'),
                '得意先名': st.column_config.TextColumn('得意先名'),
                '納品先名': st.column_config.TextColumn('納品先名'),
                '品名': st.column_config.TextColumn('品名'),
                '数量': st.column_config.TextColumn('数量'),
                '単位': st.column_config.TextColumn('単位'),
                '単価': st.column_config.TextColumn('単価'),
                '金額': st.column_config.TextColumn('金額'),
                '納品日': st.column_config.TextColumn('納品日'),
                '備考': st.column_config.TextColumn('備考'),
                '処理日時': st.column_config.TextColumn('処理日時', disabled=True),
                '元ファイル名': st.column_config.TextColumn('元ファイル名', disabled=True)
            }
        )
        
        # スプレッドシートに保存（1回押すだけで確認メッセージを表示）
        confirm_save_key = "confirm_save_all_combined_existing"
        if confirm_save_key not in st.session_state:
            st.session_state[confirm_save_key] = False
        
        if st.button("💾 スプレッドシートに保存", key="save_to_sheets_existing", type="primary", use_container_width=True):
            st.session_state[confirm_save_key] = True
        
        if st.session_state[confirm_save_key]:
            st.warning("⚠️ 本当にスプレッドシートに保存しますか？")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✓ はい、保存します", key="confirm_save_yes_existing", type="primary", use_container_width=True):
                    try:
                        # 編集されたデータを取得
                        edited_data_list = edited_df.to_dict('records')
                        
                        # スプレッドシート形式に変換
                        rows_to_save = []
                        for row in edited_data_list:
                            rows_to_save.append([
                                row.get('日付', ''),
                                row.get('発注番号', ''),
                                row.get('得意先名', ''),
                                row.get('納品先名', ''),
                                row.get('品名', ''),
                                row.get('数量', ''),
                                row.get('単位', ''),
                                row.get('単価', ''),
                                row.get('金額', ''),
                                row.get('納品日', ''),
                                row.get('備考', ''),
                                row.get('処理日時', ''),
                                row.get('元ファイル名', '')
                            ])
                        
                        # スプレッドシートに保存
                        st.session_state.sheets_client.append_rows(None, rows_to_save)
                        st.success(f"✓ {len(rows_to_save)}行をスプレッドシートに保存しました")
                        st.session_state[confirm_save_key] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"保存エラー: {e}")
                        logger.error(f"保存エラー: {e}", exc_info=True)
                        st.session_state[confirm_save_key] = False
            with col_no:
                if st.button("✗ キャンセル", key="confirm_save_no_existing", use_container_width=True):
                    st.session_state[confirm_save_key] = False
                    st.rerun()
        
        st.markdown("---")
    
    if uploaded_files is not None and len(uploaded_files) > 0:
        # 初期化チェック（ボタンの外で確認）
        if not st.session_state.initialized:
            st.warning("⚠️ システムが初期化されていません。サイドバーから「システム初期化」を実行してください。")
        
        if st.session_state.ocr_processor is None or st.session_state.ai_extractor is None:
            st.warning("⚠️ システムコンポーネントが初期化されていません。サイドバーから「システム初期化」を再実行してください。")
        
        # 処理実行ボタン
        button_pressed = st.button("🚀 処理開始", type="primary", use_container_width=True)
        
        # ボタンが押されたことを即座にログに記録（printも使用して確実に出力）
        if button_pressed:
            print("=" * 50)
            print("処理開始ボタンが押されました")
            print(f"初期化状態: {st.session_state.initialized}")
            print(f"OCRプロセッサー: {st.session_state.ocr_processor is not None}")
            print(f"AI抽出器: {st.session_state.ai_extractor is not None}")
            print(f"アップロードファイル数: {len(uploaded_files)}")
            print("=" * 50)
            
            logger.info("=" * 50)
            logger.info("処理開始ボタンが押されました")
            logger.info(f"初期化状態: {st.session_state.initialized}")
            logger.info(f"OCRプロセッサー: {st.session_state.ocr_processor is not None}")
            logger.info(f"AI抽出器: {st.session_state.ai_extractor is not None}")
            logger.info(f"アップロードファイル数: {len(uploaded_files)}")
            logger.info("=" * 50)
            
            # 初期化チェック
            if not st.session_state.initialized:
                error_msg = "⚠️ システムが初期化されていません。サイドバーから「システム初期化」を実行してください。"
                print(f"エラー: {error_msg}")
                logger.error(error_msg)
                st.error(error_msg)
                st.stop()
            
            if st.session_state.ocr_processor is None or st.session_state.ai_extractor is None:
                error_msg = "⚠️ システムコンポーネントが初期化されていません。サイドバーから「システム初期化」を再実行してください。"
                print(f"エラー: {error_msg}")
                logger.error(error_msg)
                st.error(error_msg)
                st.stop()
            
            # 処理実行
            print("処理実行を開始します...")
            logger.info("処理実行を開始します...")
            
            # UI要素を作成
            progress_bar = st.progress(0)
            status_text = st.empty()
            error_container = st.empty()
            
            # すぐにメッセージを表示（処理が開始されたことを明確にする）
            status_text.info("🔄 処理を開始します...")
            progress_bar.progress(0.01)
            
            all_results = []
            tmp_paths = []
            
            try:
                logger.info(f"アップロードされたファイル数: {len(uploaded_files)}")
                total_files = len(uploaded_files)
                status_text.info(f"📋 {total_files}個のファイルを処理します...")
                progress_bar.progress(0.05)
                # 各ファイルを順次処理
                for file_idx, uploaded_file in enumerate(uploaded_files):
                    filename = uploaded_file.name
                    logger.info(f"ファイル処理開始: {filename} ({file_idx + 1}/{total_files})")
                    status_text.info(f"📷 処理中: {filename} ({file_idx + 1}/{total_files})")
                    progress_bar.progress((file_idx / total_files) * 0.7)
                    
                    try:
                        # 一時ファイルとして保存
                        logger.info(f"ファイル読み込み開始: {filename}")
                        status_text.info(f"📄 ファイルを読み込み中: {filename}")
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            file_content = uploaded_file.read()
                            tmp_file.write(file_content)
                            tmp_path = tmp_file.name
                            tmp_paths.append(tmp_path)
                        logger.info(f"ファイル読み込み完了: {filename} ({len(file_content)} bytes)")
                        
                        # OCR処理
                        logger.info(f"OCR処理開始: {filename}")
                        status_text.info(f"🔍 OCR処理中: {filename}... (これには数秒〜数十秒かかる場合があります)")
                        progress_bar.progress((file_idx / total_files) * 0.7 + 0.05)
                        
                        # ファイル処理（OCR + AI抽出）
                        logger.info(f"process_file_for_web呼び出し: {filename}")
                        try:
                            result = process_file_for_web(tmp_path, filename)
                            logger.info(f"process_file_for_web完了: {filename}, success={result.get('success')}")
                        except Exception as process_error:
                            import traceback
                            error_detail = traceback.format_exc()
                            logger.error(f"process_file_for_webエラー {filename}: {process_error}", exc_info=True)
                            logger.error(f"トレースバック: {error_detail}")
                            result = {
                                'filename': filename,
                                'success': False,
                                'pages': [],
                                'error': f"処理エラー: {str(process_error)}",
                                'total_pages': 0
                            }
                        all_results.append(result)
                        
                        progress_bar.progress((file_idx + 1) / total_files * 0.8)
                        
                        if result['success']:
                            status_text.success(f"✅ 処理完了: {filename} ({result.get('total_pages', 0)}ページ)")
                            logger.info(f"処理完了: {filename} ({result.get('total_pages', 0)}ページ)")
                        else:
                            error_msg = result.get('error', '不明なエラー')
                            status_text.warning(f"⚠️ 処理失敗: {filename} - {error_msg}")
                            error_container.error(f"エラー詳細: {error_msg}")
                            logger.error(f"処理失敗: {filename} - {error_msg}")
                            
                    except Exception as e:
                        import traceback
                        error_detail = traceback.format_exc()
                        error_msg = f"ファイル処理エラー ({filename}): {str(e)}"
                        status_text.error(f"❌ {error_msg}")
                        error_container.error(f"{error_msg}\n\n詳細:\n{error_detail}")
                        logger.error(f"ファイル処理エラー {filename}: {e}", exc_info=True)
                        logger.error(f"トレースバック: {error_detail}")
                        all_results.append({
                            'filename': filename,
                            'success': False,
                            'pages': [],
                            'error': error_msg,
                            'total_pages': 0
                        })
                
                # データ統合処理（すべてのファイル処理完了後）
                status_text.info("📊 データを統合中...")
                progress_bar.progress(0.85)
                
                # 処理履歴に追加
                if 'processed_data' not in st.session_state:
                    st.session_state.processed_data = []
                st.session_state.processed_data.extend(all_results)
                
                # 統合データの準備
                if 'combined_data' not in st.session_state:
                    st.session_state.combined_data = []
                
                # 全ページのデータを統合
                combined_rows = []
                for result in all_results:
                    if result['success']:
                        for page_info in result['pages']:
                            page_num = page_info['page_num']
                            order_data = page_info['data']
                            
                            # 編集されたデータのキー
                            edit_key = f"edited_data_{result['filename']}_{page_num}"
                            
                            # 編集されたデータがない場合は元のデータを使用
                            if edit_key in st.session_state:
                                order_data = st.session_state[edit_key]
                            
                            # 商品情報がある場合は各商品ごとに1行
                            if order_data.get('items'):
                                for item in order_data.get('items', []):
                                    combined_rows.append({
                                        'ファイル名': result['filename'],
                                        'ページ': page_num,
                                        '日付': order_data.get('date', ''),
                                        '発注番号': order_data.get('order_number', ''),
                                        '得意先名': order_data.get('customer_name', ''),
                                        '納品先名': order_data.get('delivery_name', ''),
                                        '品名': item.get('product_name', ''),
                                        '数量': item.get('quantity', ''),
                                        '単位': item.get('unit', ''),
                                        '単価': item.get('unit_price', ''),
                                        '金額': item.get('amount', ''),
                                        '納品日': order_data.get('delivery_date', ''),
                                        '備考': order_data.get('remarks', ''),
                                        '処理日時': order_data.get('processed_at', ''),
                                        '元ファイル名': order_data.get('filename', '')
                                    })
                            else:
                                # 商品情報がない場合は1行だけ
                                combined_rows.append({
                                    'ファイル名': result['filename'],
                                    'ページ': page_num,
                                    '日付': order_data.get('date', ''),
                                    '発注番号': order_data.get('order_number', ''),
                                    '得意先名': order_data.get('customer_name', ''),
                                    '納品先名': order_data.get('delivery_name', ''),
                                    '品名': '',
                                    '数量': '',
                                    '単位': '',
                                    '単価': '',
                                    '金額': '',
                                    '納品日': order_data.get('delivery_date', ''),
                                    '備考': order_data.get('remarks', ''),
                                    '処理日時': order_data.get('processed_at', ''),
                                    '元ファイル名': order_data.get('filename', '')
                                })
                
                # 統合データをセッション状態に保存
                st.session_state.combined_data = combined_rows
                
                progress_bar.progress(0.95)
                
                # 結果表示
                total_pages = sum(r.get('total_pages', 0) for r in all_results if r['success'])
                success_count = sum(1 for r in all_results if r['success'])
                
                progress_bar.progress(1.0)
                status_text.success(f"✅ 全処理完了: {success_count}/{total_files}ファイル成功 ({total_pages}ページ)")
                
                if success_count < total_files:
                    error_container.warning(f"⚠️ {total_files - success_count}個のファイルでエラーが発生しました。")
                
                st.success(f"処理完了: {success_count}/{total_files}ファイル成功 ({total_pages}ページ)")
                
                # 統合データの表示と編集
                if combined_rows:
                    st.subheader("📊 抽出結果（編集可能）")
                    st.markdown("💡 **ヒント:** 表を直接編集できます。編集内容は自動的に保存されます。")
                    
                    # DataFrameに変換
                    df = pd.DataFrame(combined_rows)
                    
                    # データが30行未満の場合は空行を追加して30行にする
                    min_rows = 30
                    if len(df) < min_rows:
                        # 空の行を追加
                        empty_rows = []
                        for i in range(min_rows - len(df)):
                            empty_row = {col: '' for col in df.columns}
                            empty_rows.append(empty_row)
                        if empty_rows:
                            empty_df = pd.DataFrame(empty_rows)
                            df = pd.concat([df, empty_df], ignore_index=True)
                    
                    # 編集可能なテーブルとして表示
                    edited_df = st.data_editor(
                        df,
                        width='stretch',
                        num_rows="fixed",
                        key="combined_data_editor_new",
                        column_config={
                            'ファイル名': st.column_config.TextColumn('ファイル名', disabled=True),
                            'ページ': st.column_config.NumberColumn('ページ', disabled=True, format="%d"),
                            '日付': st.column_config.TextColumn('日付'),
                            '発注番号': st.column_config.TextColumn('発注番号'),
                            '得意先名': st.column_config.TextColumn('得意先名'),
                            '納品先名': st.column_config.TextColumn('納品先名'),
                            '品名': st.column_config.TextColumn('品名'),
                            '数量': st.column_config.TextColumn('数量'),
                            '単位': st.column_config.TextColumn('単位'),
                            '単価': st.column_config.TextColumn('単価'),
                            '金額': st.column_config.TextColumn('金額'),
                            '納品日': st.column_config.TextColumn('納品日'),
                            '備考': st.column_config.TextColumn('備考'),
                            '処理日時': st.column_config.TextColumn('処理日時', disabled=True),
                            '元ファイル名': st.column_config.TextColumn('元ファイル名', disabled=True)
                        }
                    )
                    
                    # スプレッドシートに保存（1回押すだけで確認メッセージを表示）
                    confirm_save_key = "confirm_save_all_combined_new"
                    if confirm_save_key not in st.session_state:
                        st.session_state[confirm_save_key] = False
                    
                    if st.button("💾 スプレッドシートに保存", key="save_to_sheets_new", type="primary", use_container_width=True):
                        st.session_state[confirm_save_key] = True
                    
                    if st.session_state[confirm_save_key]:
                        st.warning("⚠️ 本当にスプレッドシートに保存しますか？")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("✓ はい、保存します", key="confirm_save_yes_new", type="primary", use_container_width=True):
                                try:
                                    # 編集されたデータを取得
                                    edited_data_list = edited_df.to_dict('records')
                                    
                                    # スプレッドシート形式に変換
                                    rows_to_save = []
                                    for row in edited_data_list:
                                        rows_to_save.append([
                                            row.get('日付', ''),
                                            row.get('発注番号', ''),
                                            row.get('得意先名', ''),
                                            row.get('納品先名', ''),
                                            row.get('品名', ''),
                                            row.get('数量', ''),
                                            row.get('単位', ''),
                                            row.get('単価', ''),
                                            row.get('金額', ''),
                                            row.get('納品日', ''),
                                            row.get('備考', ''),
                                            row.get('処理日時', ''),
                                            row.get('元ファイル名', '')
                                        ])
                                    
                                    # スプレッドシートに保存
                                    st.session_state.sheets_client.append_rows(None, rows_to_save)
                                    st.success(f"✓ {len(rows_to_save)}行をスプレッドシートに保存しました")
                                    st.session_state[confirm_save_key] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"保存エラー: {e}")
                                    logger.error(f"保存エラー: {e}", exc_info=True)
                                    st.session_state[confirm_save_key] = False
                        with col_no:
                            if st.button("✗ キャンセル", key="confirm_save_no_new", use_container_width=True):
                                st.session_state[confirm_save_key] = False
                                st.rerun()
                
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                logger.error(f"メイン処理エラー: {e}", exc_info=True)
                logger.error(f"トレースバック: {error_detail}")
                status_text.error("❌ 処理失敗")
                progress_bar.progress(1.0)
                error_container.error(f"処理エラー: {str(e)}\n\n詳細:\n{error_detail}")
                st.error(f"処理エラー: {str(e)}")
                st.exception(e)
            
            finally:
                # 一時ファイルを削除
                for tmp_path in tmp_paths:
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
        
        st.markdown("---")
    
    # 処理履歴
    if st.session_state.processed_data:
        st.subheader("📋 処理履歴")
        for i, result in enumerate(st.session_state.processed_data):
            with st.expander(f"📄 {result['filename']} ({result.get('total_pages', 0)}ページ)", expanded=False):
                st.write(f"ステータス: {'✅ 成功' if result['success'] else '❌ 失敗'}")
                if result.get('error'):
                    st.error(f"エラー: {result['error']}")


if __name__ == "__main__":
    main()
