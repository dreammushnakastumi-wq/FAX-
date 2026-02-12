"""
出荷管理自動化システム - Streamlit版Webアプリ
FAX注文書処理システムのWebアプリケーション版
"""
import os
import tempfile
import logging
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

# プロキシ設定を無効化（プロキシエラーを回避）
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

# 既存モジュールをインポート
from ocr_processor import OCRProcessor
from ai_extractor import AIExtractor
from google_sheets import GoogleSheetsClient

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境変数を読み込み（ローカル環境用）
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="注文書データ化アプリ",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# セッション状態の初期化
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.error = None
    st.session_state.ocr_processor = None
    st.session_state.ai_extractor = None
    st.session_state.sheets_client = None
    st.session_state.processed_files = []
    st.session_state.extracted_data = []
    st.session_state.pdf_files = {}  # PDFファイルのバイトデータを保存（filename: bytes）
    st.session_state.edited_data = None  # 編集されたデータ（DataFrame形式）


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
            # SERVICE_ACCOUNT_KEYは文字列として取得
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
        
        # Document AI認証の設定
        if secrets['service_account_key']:
            # Streamlit Secretsからサービスアカウントキーを設定
            import json
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


def process_file(file_path: str, filename: str) -> dict:
    """ファイルを処理して結果を返す
    
    Args:
        file_path: ファイルのパス
        filename: ファイル名
        
    Returns:
        処理結果の辞書
    """
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
            page_texts = ocr_processor.extract_text_by_pages(file_path)
            logger.info(f"OCR処理完了: {filename} ({len(page_texts)}ページ)")
        except Exception as e:
            logger.warning(f"ページ分割に失敗しました。全体テキストとして処理します: {e}")
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
                order_data = ai_extractor.extract(page_text, page_filename)
                logger.info(f"AI抽出完了: {page_filename}")
                
                # デバッグ: order_dataの内容を確認
                st.write(f"DEBUG process_file: AI抽出成功 - {page_filename}")
                st.write(f"DEBUG process_file: order_data type = {type(order_data)}")
                st.write(f"DEBUG process_file: order_data is None? {order_data is None}")
                if order_data:
                    st.write(f"DEBUG process_file: order_data keys = {list(order_data.keys()) if isinstance(order_data, dict) else 'Not a dict'}")
                
                # order_dataが有効な場合のみsuccess: Trueを設定
                if order_data is not None:
                    page_info = {
                        'page_num': page_num,
                        'data': order_data,
                        'success': True  # 明示的にTrueを設定
                    }
                    st.write(f"DEBUG process_file: page_info['success'] = {page_info['success']}")
                    result['pages'].append(page_info)
                    logger.info(f"ページ {page_num} の処理成功: {page_filename}")
                else:
                    # order_dataがNoneの場合はエラーとして扱う
                    error_msg = f"AI抽出結果がNoneです（ページ{page_num}）"
                    logger.warning(f"AI抽出結果がNone: {page_filename}")
                    st.write(f"DEBUG process_file: order_data is None, setting success=False")
                    result['pages'].append({
                        'page_num': page_num,
                        'data': {},
                        'success': False,
                        'error': error_msg
                    })
            except Exception as ai_error:
                error_msg = f"AI抽出エラー（ページ{page_num}）: {str(ai_error)}"
                logger.error(f"AI抽出エラー {page_filename}: {ai_error}", exc_info=True)
                st.write(f"DEBUG process_file: AI抽出エラー - {error_msg}")
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
    
    return result


def format_data_for_display(results: list) -> pd.DataFrame:
    """処理結果をDataFrameに変換
    
    Args:
        results: 処理結果のリスト
        
    Returns:
        DataFrame
    """
    rows = []
    
    # デバッグ
    st.write(f"DEBUG format_data_for_display: results count = {len(results)}")
    
    for result in results:
        st.write(f"DEBUG: Processing result: {result.get('filename', 'unknown')}")
        st.write(f"DEBUG: success = {result.get('success', False)}")
        st.write(f"DEBUG: pages count = {len(result.get('pages', []))}")
        
        if result['success']:
            for page_info in result['pages']:
                st.write(f"DEBUG: page_info.success = {page_info.get('success', False)}")
                if page_info['success']:
                    order_data = page_info['data']
                    st.write(f"DEBUG: order_data keys = {list(order_data.keys())}")
                    st.write(f"DEBUG: order_data.get('items') = {order_data.get('items')}")
                    
                    # 商品情報がある場合は各商品ごとに1行
                    if order_data.get('items'):
                        st.write(f"DEBUG: items count = {len(order_data.get('items', []))}")
                        for item in order_data.get('items', []):
                            rows.append({
                                'ファイル名': result['filename'],
                                'ページ': page_info['page_num'],
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
                        st.write(f"DEBUG: No items, adding single row")
                        rows.append({
                            'ファイル名': result['filename'],
                            'ページ': page_info['page_num'],
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
                else:
                    st.write(f"DEBUG: page_info.success is False, skipping")
        else:
            st.write(f"DEBUG: result.success is False, skipping")
    
    st.write(f"DEBUG: Total rows created = {len(rows)}")
    return pd.DataFrame(rows)


def main():
    """メイン処理"""
    st.title("📝 注文書データ化アプリ")
    st.markdown("---")
    
    # 設定・ファイルアップロードをexpanderに移動
    uploaded_files = None
    with st.expander("⚙️ 設定・ファイルアップロード", expanded=False):
        col_setting1, col_setting2 = st.columns(2)
        
        with col_setting1:
            st.subheader("⚙️ 設定")
            
            # 設定表示
            secrets = get_secrets()
            st.text(f"スプレッドシートID: {secrets['spreadsheet_id'][:20] + '...' if secrets['spreadsheet_id'] else '未設定'}")
            st.text(f"OCR言語: jpn+eng")
            st.text(f"AI APIタイプ: {secrets['api_type']}")
            
            st.markdown("---")
            
            # AI APIタイプの選択
            api_type = st.selectbox(
                "使用するAI API",
                ["claude", "openai"],
                index=0 if secrets['api_type'] == 'claude' else 1
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
        
        with col_setting2:
            st.subheader("📎 ファイルアップロード")
            uploaded_files = st.file_uploader(
                "PDFファイルをアップロード",
                type=['pdf'],
                accept_multiple_files=True,
                help="FAX注文書のPDFファイルを選択してください。複数のファイルを同時にアップロードできます。"
            )
            
            if uploaded_files:
                st.info(f"📄 {len(uploaded_files)}個のファイルがアップロードされました")
                for idx, file in enumerate(uploaded_files, 1):
                    st.text(f"{idx}. {file.name}")
    
    # メイン画面
    if not st.session_state.initialized:
        st.warning("⚠️ 上記の「設定・ファイルアップロード」から「システム初期化」を実行してください。")
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
    
    # ファイルアップロード済みの場合
    if uploaded_files:
        # 処理実行ボタン
        if st.button("🚀 処理開始", type="primary", use_container_width=True):
            # 初期化チェック
            if not st.session_state.initialized:
                st.error("⚠️ システムが初期化されていません。サイドバーから「システム初期化」を実行してください。")
                st.stop()
            
            if st.session_state.ocr_processor is None or st.session_state.ai_extractor is None:
                st.error("⚠️ システムコンポーネントが初期化されていません。サイドバーから「システム初期化」を再実行してください。")
                st.stop()
            
            # 処理実行
            progress_bar = st.progress(0)
            status_text = st.empty()
            error_container = st.empty()
            
            status_text.info("🔄 処理を開始します...")
            progress_bar.progress(0.01)
            
            all_results = []
            tmp_paths = []
            
            try:
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
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            file_content = uploaded_file.read()
                            tmp_file.write(file_content)
                            tmp_path = tmp_file.name
                            tmp_paths.append(tmp_path)
                        
                        # PDFのバイトデータをセッションステートに保存（後で表示用に使用）
                        st.session_state.pdf_files[filename] = file_content
                        
                        # OCR処理
                        status_text.info(f"🔍 OCR処理中: {filename}...")
                        progress_bar.progress((file_idx / total_files) * 0.7 + 0.05)
                        
                        # ファイル処理（OCR + AI抽出）
                        result = process_file(tmp_path, filename)
                        all_results.append(result)
                        
                        progress_bar.progress((file_idx + 1) / total_files * 0.8)
                        
                        if result['success']:
                            status_text.success(f"✅ 処理完了: {filename} ({result.get('total_pages', 0)}ページ)")
                        else:
                            error_msg = result.get('error', '不明なエラー')
                            status_text.warning(f"⚠️ 処理失敗: {filename} - {error_msg}")
                            error_container.error(f"エラー詳細: {error_msg}")
                            
                    except Exception as e:
                        import traceback
                        error_detail = traceback.format_exc()
                        error_msg = f"ファイル処理エラー ({filename}): {str(e)}"
                        status_text.error(f"❌ {error_msg}")
                        error_container.error(f"{error_msg}\n\n詳細:\n{error_detail}")
                        logger.error(f"ファイル処理エラー {filename}: {e}", exc_info=True)
                        all_results.append({
                            'filename': filename,
                            'success': False,
                            'pages': [],
                            'error': error_msg,
                            'total_pages': 0
                        })
                
                # データ統合処理
                status_text.info("📊 データを統合中...")
                progress_bar.progress(0.85)
                
                # 処理履歴に追加
                st.session_state.processed_files = all_results
                
                # デバッグ: all_resultsの内容を確認
                st.write("DEBUG: all_results count:", len(all_results))
                st.write("DEBUG: all_results success count:", sum(1 for r in all_results if r.get('success', False)))
                if all_results:
                    st.write("DEBUG: First result keys:", list(all_results[0].keys()) if all_results[0] else [])
                    if all_results[0].get('success') and all_results[0].get('pages'):
                        st.write("DEBUG: First result pages count:", len(all_results[0]['pages']))
                
                # データをDataFrameに変換
                df = format_data_for_display(all_results)
                st.write("DEBUG: df rows:", len(df))
                st.write("DEBUG: df columns:", list(df.columns) if len(df) > 0 else [])
                st.write("DEBUG: df.to_dict('records'):", df.to_dict('records')[:1] if len(df) > 0 else [])
                
                st.session_state.extracted_data = df.to_dict('records')
                
                progress_bar.progress(0.95)
                
                # 結果表示
                total_pages = sum(r.get('total_pages', 0) for r in all_results if r['success'])
                success_count = sum(1 for r in all_results if r['success'])
                
                progress_bar.progress(1.0)
                
                # デバッグ用: extracted_dataの内容を確認
                st.write("DEBUG: extracted_data exists?", bool(st.session_state.extracted_data))
                st.write("DEBUG: extracted_data length:", len(st.session_state.extracted_data) if st.session_state.extracted_data else 0)
                if st.session_state.extracted_data:
                    st.write("DEBUG: First row:", st.session_state.extracted_data[0])
                
                status_text.success(f"✅ 全処理完了: {success_count}/{total_files}ファイル成功 ({total_pages}ページ)")
                
                if success_count < total_files:
                    error_container.warning(f"⚠️ {total_files - success_count}個のファイルでエラーが発生しました。")
                
                st.success(f"処理完了: {success_count}/{total_files}ファイル成功 ({total_pages}ページ)")
                
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                logger.error(f"メイン処理エラー: {e}", exc_info=True)
                status_text.error("❌ 処理失敗")
                progress_bar.progress(1.0)
                error_container.error(f"処理エラー: {str(e)}\n\n詳細:\n{error_detail}")
                st.error(f"処理エラー: {str(e)}")
            
            finally:
                # 一時ファイルを削除
                for tmp_path in tmp_paths:
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
    
    # 読み取りデータの表示と編集
    if st.session_state.extracted_data:
        st.markdown("---")
        st.subheader("📊 読み取りデータ")
        
        # データをDataFrameに変換（編集済みデータがあればそれを使用）
        if st.session_state.edited_data is not None:
            df = st.session_state.edited_data.copy()
        else:
            df = pd.DataFrame(st.session_state.extracted_data)
        
        # データエディタで編集
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="data_editor_main"
        )
        
        # 編集されたデータを反映
        st.session_state.edited_data = edited_df
        st.session_state.extracted_data = edited_df.to_dict('records')
        
        # スプレッドシートに保存
        st.markdown("---")
        st.subheader("💾 スプレッドシートに保存")
        
        if st.button("💾 スプレッドシートに保存", type="primary", use_container_width=True):
            try:
                # スプレッドシート形式に変換
                rows_to_save = []
                for row in st.session_state.extracted_data:
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
                
            except Exception as e:
                st.error(f"保存エラー: {e}")
                logger.error(f"保存エラー: {e}", exc_info=True)
    
    # 処理履歴
    if st.session_state.processed_files:
        st.markdown("---")
        st.subheader("📋 処理履歴")
        for i, result in enumerate(st.session_state.processed_files):
            with st.expander(f"📄 {result['filename']} ({result.get('total_pages', 0)}ページ)", expanded=False):
                st.write(f"ステータス: {'✅ 成功' if result['success'] else '❌ 失敗'}")
                if result.get('error'):
                    st.error(f"エラー: {result['error']}")


if __name__ == "__main__":
    main()
