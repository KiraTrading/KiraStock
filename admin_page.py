import streamlit as st
import google.generativeai as genai
import os
import requests
import base64
import pandas as pd
import io
from datetime import datetime


# ==========================================
# 1. GitHub Helper Functions (讀寫分離)
# ==========================================
def get_github_file(repo, path, token, branch="main"):
    """從 GitHub 讀取原始文件"""
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        sha = response.json()['sha']
        return content, sha
    return None, None


def push_to_github(repo, path, token, content, sha, message, branch="main"):
    """推送到 GitHub"""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    message_bytes = content.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_content = base64_bytes.decode('ascii')

    data = {
        "message": message,
        "content": base64_content,
        "branch": branch
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, json=data, headers=headers)
    return response


# ==========================================
# 2. Main Render Function
# ==========================================
def render_admin_console():
    # --- 安全驗證 ---
    password = st.text_input("🔒 Enter Admin Password", type="password")

    if "ADMIN_PASSWORD" in st.secrets:
        correct_password = st.secrets["ADMIN_PASSWORD"]
    else:
        st.error("❌ ADMIN_PASSWORD not found in secrets.toml")
        st.stop()

    if password != correct_password:
        st.warning("⛔ Access Denied")
        st.stop()

    # --- CONFIGURATION ---
    REPO_OWNER = "ParisTrader"  # 你的 GitHub 用戶名
    PUBLIC_REPO = "paristrader-terminal"  # 你的 Repo 名稱
    PRIVATE_REPO = "paristrader-private"
    BRANCH = "main"

    # CSV Path inside the repo
    TRADE_CSV_PATH = "Trade/swing_trades.csv"

    try:
        GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except FileNotFoundError:
        st.error("❌ secrets.toml file not found!")
        st.stop()

    genai.configure(api_key=GEMINI_API_KEY)

    st.title("🕵️‍♂️ Paris Admin Console")

    # 使用 Tabs 分隔功能
    tab_writer, tab_trader = st.tabs(["✍️ AI Content Generator", "📊 Trade Manager"])

    # =========================================================
    # TAB 1: AI Content Generator (你原本的代碼)
    # =========================================================
    # =========================================================
    # TAB 1: AI Content Generator (已升級 IG Able 版)
    # =========================================================
    with tab_writer:
        st.subheader("Daily Insight Generator")
        col_input, col_preview = st.columns([1, 1])

        with col_input:
            raw_text = st.text_area("Paste News/Article Here:", height=300)
            user_instruction = st.text_input("Extra Instructions:", "")
            generate_btn = st.button("🚀 Generate Draft", type="primary")

        # Session State for Draft
        if "draft_content" not in st.session_state: st.session_state.draft_content = ""
        if "draft_title" not in st.session_state: st.session_state.draft_title = ""

        PARIS_PERSONA = """
            You are Paris Trader. You are a financial blogger. Based on the material I provided. Rewrite blog.The content need to be in paragraphs and summarize 2 sentences as article title
            ROLE & TONE:
            - **Identity:** Cynical, sharp, "Smart Money" veteran.
            - **Tone:** Direct, condensed, include details.
            - **Language:** Traditional Chinese (Hong Kong Finance Style), polite tone. written chinese, not cantonese.
            """

        if generate_btn and raw_text:
            with st.spinner("Gemini is working..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"{PARIS_PERSONA}\n\nINPUT TEXT:\n{raw_text}\n\nINSTRUCTIONS: {user_instruction}"
                    response = model.generate_content(prompt)
                    content = response.text
                    lines = content.split('\n')
                    # 簡單清理 Title，避免 Markdown 符號
                    title = lines[0].replace('#', '').replace('*', '').strip()
                    body = "\n".join(lines[1:])
                    st.session_state.draft_title = title
                    st.session_state.draft_content = body
                except Exception as e:
                    st.error(f"API Error: {e}")

        with col_preview:
            st.markdown("### 🛠️ Final Polish (IG Metadata)")
            final_title = st.text_input("Title (Headline)", value=st.session_state.draft_title)

            # --- 新增：IG 元素選擇器 ---
            c1, c2 = st.columns(2)
            with c1:
                # 標籤：顯示在卡片右上角
                tag_option = st.selectbox("📌 Category",
                                          ["Macro Outlook", "Stock Hunter", "Option Flow", "Crypto", "Market Recap"])
            with c2:
                # 情緒：顯示顏色或 Emoji
                sentiment_option = st.selectbox("🐂🐻 Sentiment", ["Bullish (看好)", "Bearish (看淡)", "Neutral (觀望)",
                                                                 "Warning (預警)"])

            final_content = st.text_area("Markdown Content", value=st.session_state.draft_content, height=400)

            if st.button("✅ Upload Insight to GitHub", type="primary"):
                if final_title and final_content:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    safe_title = "".join([c if c.isalnum() else "_" for c in final_title])[:50]
                    filename = f"{date_str}_{safe_title}.md"

                    # --- 構建包含 Metadata 的 Markdown ---
                    # 這些 **Key:** 讓 app.py 可以讀取並顯示在漂亮的 UI 上
                    full_content = (
                        f"# {final_title}\n"
                        f"**Date:** {date_str}\n"
                        f"**Tag:** {tag_option}\n"
                        f"**Sentiment:** {sentiment_option}\n\n"
                        f"{final_content}"
                    )

                    try:
                        # Upload Logic
                        git_path = f"DailyInsights/{filename}"
                        _, sha = get_github_file(f"{REPO_OWNER}/{PUBLIC_REPO}", git_path, GITHUB_TOKEN)

                        resp = push_to_github(
                            f"{REPO_OWNER}/{PUBLIC_REPO}",
                            git_path,
                            GITHUB_TOKEN,
                            full_content,
                            sha,
                            f"Add insight: {safe_title}",
                            BRANCH
                        )

                        if resp.status_code in [200, 201]:
                            st.success("🎉 Published successfully!")
                            st.balloons()
                        else:
                            st.error(f"Upload failed: {resp.status_code}")
                    except Exception as e:
                        st.error(f"Error: {e}")


    # =========================================================
    # TAB 2: Trade Manager (新功能)
    # =========================================================
        # =========================================================
        # TAB 2: Trade Manager (修復版)
        # =========================================================
        with tab_trader:
            st.subheader("📊 Manage Swing Trades")
            st.info("Directly edit the CSV below. Click 'Save Changes' to push to GitHub.")

            # 1. Load Data Button
            if "trade_df" not in st.session_state:
                st.session_state.trade_df = None

            # 這裡不需要 session_state.trade_sha，因為我們在存檔時會重新抓取最新的 SHA，這樣更安全

            # 自動加載或手動刷新
            if st.button("🔄 Refresh Data from GitHub") or st.session_state.trade_df is None:
                with st.spinner("Fetching latest CSV..."):
                    content, sha = get_github_file(f"{REPO_OWNER}/{PUBLIC_REPO}", TRADE_CSV_PATH, GITHUB_TOKEN, BRANCH)
                    if content:
                        # Read into Pandas
                        df = pd.read_csv(io.StringIO(content))

                        # 強制轉換日期格式，避免編輯器報錯
                        if 'EntryDate' in df.columns:
                            df['EntryDate'] = pd.to_datetime(df['EntryDate'], errors='coerce')
                        if 'ExitDate' in df.columns:
                            df['ExitDate'] = pd.to_datetime(df['ExitDate'], errors='coerce')

                        st.session_state.trade_df = df
                    else:
                        st.error("Failed to fetch CSV. Check path and token.")

            # 2. Data Editor
            if st.session_state.trade_df is not None:
                df = st.session_state.trade_df

                # 配置編輯器
                # 🔥 [修正 1] 加入 key="trade_editor"，這能幫助 Streamlit 在 Rerun 時保持狀態穩定
                edited_df = st.data_editor(
                    df,
                    key="trade_editor",
                    num_rows="dynamic",
                    use_container_width=True,
                    column_config={
                        "Ticker": st.column_config.TextColumn("Ticker", required=True),
                        "EntryDate": st.column_config.DateColumn("Entry Date", format="YYYY-MM-DD"),
                        "ExitDate": st.column_config.DateColumn("Exit Date", format="YYYY-MM-DD"),
                        "EntryPrice": st.column_config.NumberColumn("Entry Price", format="%.2f"),
                        "ExitPrice": st.column_config.NumberColumn("Exit Price", format="%.2f"),
                        "Type": st.column_config.SelectboxColumn("Type", options=["Long", "Short"], required=True),
                        "Status": st.column_config.SelectboxColumn("Status", options=["Open", "Closed", "Pending"],
                                                                   required=True),
                        "Notes": st.column_config.TextColumn("Notes", width="large"),
                        "PnL": st.column_config.TextColumn("PnL %")
                    },
                    hide_index=True
                )

                # 3. Save Button
                if st.button("💾 Save Changes to BOTH Repos", type="primary"):
                    try:
                        # 🔥 [修正 2] 數據清洗：移除 Ticker 為空的「幽靈行」
                        # 當你按 + 新增行但沒打字時，Ticker 會是 None/NaN，這會導致 CSV 出錯或存入空行
                        clean_df = edited_df.dropna(subset=["Ticker"])

                        # 二次過濾：移除 Ticker 為空字串的情況
                        clean_df = clean_df[clean_df["Ticker"].astype(str).str.strip() != ""]

                        if clean_df.empty:
                            st.warning("⚠️ Dataframe is empty or Ticker is missing. Nothing to save.")
                            st.stop()

                        # Debug 預覽：讓你知道你到底存了什麼
                        with st.expander("🕵️‍♂️ Debug: Preview data being saved", expanded=False):
                            st.dataframe(clean_df)

                        # A. Convert DF back to CSV string
                        csv_buffer = io.StringIO()
                        clean_df.to_csv(csv_buffer, index=False)
                        new_csv_content = csv_buffer.getvalue()

                        # B. Define targets
                        targets = [
                            {"name": "Public", "repo": f"{REPO_OWNER}/{PUBLIC_REPO}"},
                            {"name": "Private", "repo": f"{REPO_OWNER}/{PRIVATE_REPO}"}
                        ]

                        success_count = 0
                        status_msg = st.empty()

                        # C. Loop through targets and push
                        for target in targets:
                            repo_full_name = target['repo']
                            status_msg.info(f"⏳ Updating {target['name']} ({repo_full_name})...")

                            # STEP 1: 獲取最新的 SHA (Concurrency Control)
                            _, current_sha = get_github_file(repo_full_name, TRADE_CSV_PATH, GITHUB_TOKEN, BRANCH)

                            # STEP 2: 推送更新
                            resp = push_to_github(
                                repo_full_name,
                                TRADE_CSV_PATH,
                                GITHUB_TOKEN,
                                new_csv_content,
                                current_sha,
                                f"Sync trades {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                                BRANCH
                            )

                            if resp.status_code in [200, 201]:
                                st.toast(f"✅ {target['name']} Repo Updated!", icon="🎉")
                                success_count += 1
                            else:
                                st.error(f"❌ Failed to update {target['name']}: {resp.status_code} - {resp.text}")

                        # D. Final Result
                        if success_count == len(targets):
                            st.success(f"🏆 All Repos Synced Successfully! ({success_count}/{len(targets)})")

                            # 🔥 [修正 3] 只有成功存檔後，才更新 session_state
                            # 這樣下次 Rerun 時，編輯器會顯示剛存好的、乾淨的數據
                            st.session_state.trade_df = clean_df
                            st.balloons()

                    except Exception as e:
                        st.error(f"System Error: {e}")
