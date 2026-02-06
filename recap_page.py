import streamlit as st
import os
import glob


def render_recap_page(load_markdown_func):
    st.title("♟️ 每日操盤日記 (Trade Recap)")
    st.caption("回顧市場邏輯 | 驗證交易系統 | 僅供教學參考")

    # --- ⚠️ 合規免責聲明 (Compliance Shield) ---
    st.warning("""
    **⚠️ 免責聲明 (Disclaimer):**

    本頁面內容僅為個人交易紀錄與學術研究分享，**並非投資建議 (Not Financial Advice)**。
    所有圖表、點位與分析僅用於驗證量化策略的有效性。過往績效不代表未來表現。請勿盲目跟單，投資涉及風險，請自行評估。
    """)

    st.markdown("---")

    # --- 讀取 Markdown 檔案 ---
    # 假設檔案格式為: YYYY-MM-DD_Title.md
    folder_path = "TradeRecaps"

    # 確保資料夾存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        st.info(f"請在 `{folder_path}` 資料夾中放入 .md 檔案")
        return

    files = sorted(glob.glob(os.path.join(folder_path, "*.md")), reverse=True)

    if not files:
        st.info("📭 暫無復盤日記，請稍後再來。")
    else:
        # Timeline 樣式顯示
        for file_path in files:
            try:
                filename = os.path.basename(file_path)
                # 簡單解析日期 (假設檔名頭10個字是日期)
                date_str = filename[:10]
                display_title = filename[11:].replace(".md", "").replace("_", " ")

                with st.expander(f"📅 {date_str} | {display_title}", expanded=True):
                    # 使用傳入的 markdown loader (包含圖片處理功能)
                    content = load_markdown_func(file_path)
                    st.markdown(content, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading {filename}: {e}")