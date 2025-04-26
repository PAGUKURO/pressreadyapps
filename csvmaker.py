import streamlit as st
import os
import pandas as pd
import shutil
from datetime import datetime

st.set_page_config(page_title="ファイルコピー＆CSV出力ツール", layout="wide")

# 固定の保存先ディレクトリ
SAVE_DIR = "C:/Users/kurop/Documents/0424"
# CSV出力先
CSV_OUTPUT_DIR = "C:/Users/fujifilm/Desktop/MURE"

st.title("ファイルコピー＆CSV出力ツール")
st.write("ファイルをアップロードすると、指定フォルダにコピーして一覧をCSVに出力します。")

# サイドバー設定
st.sidebar.header("設定")
csv_output_dir = st.sidebar.text_input(
    "CSV出力先（絶対パス）", 
    value=CSV_OUTPUT_DIR
)

# 保存先フォルダの確認と作成
if not os.path.exists(SAVE_DIR):
    try:
        os.makedirs(SAVE_DIR)
        st.sidebar.success(f"保存先フォルダを作成しました: {SAVE_DIR}")
    except Exception as e:
        st.sidebar.error(f"保存先フォルダの作成に失敗しました: {e}")

# ファイルアップローダー
uploaded_files = st.file_uploader("ファイルをアップロード（複数選択可）", 
                                 type=None, accept_multiple_files=True)

if uploaded_files:
    st.write(f"{len(uploaded_files)}個のファイルがアップロードされました")
    
    # 処理ボタン
    if st.button("ファイルをコピーしてCSV出力", type="primary"):
        with st.spinner("処理中..."):
            file_list = []
            
            # 各ファイルを指定フォルダにコピー
            for uploaded_file in uploaded_files:
                # 保存先のファイルパス
                save_path = os.path.join(SAVE_DIR, uploaded_file.name)
                
                # ファイルをコピー
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # ファイル名と絶対パスを記録
                file_name = os.path.splitext(uploaded_file.name)[0]
                file_list.append({"JobName": file_name, "Pass": save_path})
            
            # DataFrameに変換
            df = pd.DataFrame(file_list)
            
            # CSVに出力
            if not os.path.exists(csv_output_dir):
                os.makedirs(csv_output_dir)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"filelist_{timestamp}.csv"
            output_path = os.path.join(csv_output_dir, output_filename)
            
            # BOM付きUTF-8でCSV出力
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            st.success(f"処理が完了しました！\n- {len(file_list)}個のファイルを '{SAVE_DIR}' にコピーしました\n- CSVファイルを '{output_path}' に出力しました")
            
            # プレビュー表示
            st.subheader("ファイル一覧プレビュー")
            st.dataframe(df)
            
            # ダウンロードボタン
            with open(output_path, "rb") as f:
                st.download_button(
                    label="CSVファイルをダウンロード",
                    data=f,
                    file_name=output_filename,
                    mime="text/csv"
                )
else:
    st.info("ファイルをアップロードしてください")

# 使い方ガイド
with st.expander("使い方"):
    st.markdown(f"""
    ### 使い方ガイド
    1. 「ファイルをアップロード」エリアに処理したいファイルをドラッグ＆ドロップするか、「Browse files」ボタンでファイルを選択します
    2. 複数のファイルを一度に選択することができます
    3. ファイルのアップロードが完了したら「ファイルをコピーしてCSV出力」ボタンをクリックします
    4. アップロードされたファイルは自動的に以下のフォルダにコピーされます：
       - 保存先: `{SAVE_DIR}`
    5. ファイル一覧のCSVファイルは以下のフォルダに出力されます：
       - CSV出力先: `{csv_output_dir}`
    
    ### 出力されるCSVファイル形式
    - **JobName**: ファイル名（拡張子なし）
    - **Pass**: ファイルの絶対パス（`{SAVE_DIR}`内のパス）
    """)

# フッター
st.markdown("---")
st.caption("ファイルコピー＆CSV出力ツール v1.0")