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
        You are Paris Trader. You are a Senior Portfolio Manager and Ex-Prop Trader. You write concise, high-impact market memos for institutional desks.

        ROLE & TONE:
        - **Identity:** Cynical, sharp, "Smart Money" veteran.
        - **Tone:** Direct, condensed, judgmental. No fluff.
        - **Language:** Traditional Chinese (Hong Kong Finance Style) mixed with English financial terminology.
        - **Style:** Bloomberg Terminal chat style. Short sentences. High information density.

        CRITICAL FORMATTING RULES:
        1. **NO HEADERS:** No "Key Bullet Points" or "Introduction".
        2. **STRUCTURE:**
           - Line 1: Punchy Title.
           - Line 2: Directional Tag (e.g., 【看淡 - Bearish】).
           - Body: Seamless blend of facts and analysis.

        CORE OBJECTIVE:
        **Interpret PnL impact.** Focus on Liquidity, structure, flows, and positioning.
        """

        if generate_btn and raw_text:
            with st.spinner("Gemini is working..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"{PARIS_PERSONA}\n\nINPUT TEXT:\n{raw_text}\n\nINSTRUCTIONS: {user_instruction}"
                    response = model.generate_content(prompt)
                    content = response.text
                    lines = content.split('\n')
                    title = lines[0].replace('#', '').replace('*', '').strip()
                    body = "\n".join(lines[1:])
                    st.session_state.draft_title = title
                    st.session_state.draft_content = body
                except Exception as e:
                    st.error(f"API Error: {e}")

        with col_preview:
            final_title = st.text_input("Title", value=st.session_state.draft_title)
            final_content = st.text_area("Markdown Content", value=st.session_state.draft_content, height=500)

            if st.button("✅ Upload Insight to GitHub", type="primary"):
                if final_title and final_content:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    safe_title = "".join([c if c.isalnum() else "_" for c in final_title])[:50]
                    filename = f"{date_str}_{safe_title}.md"
                    full_content = f"# {final_title}\n**Date:** {date_str}\n\n{final_content}"

                    try:
                        # Upload Logic
                        git_path = f"DailyInsights/{filename}"
                        # Check existing
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
                        else:
                            st.error(f"Upload failed: {resp.status_code}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # =========================================================
    # TAB 2: Trade Manager (新功能)
    # =========================================================
    with tab_trader:
        st.subheader("📊 Manage Swing Trades")
        st.info("Directly edit the CSV below. Click 'Save Changes' to push to GitHub.")

        # 1. Load Data Button
        if "trade_df" not in st.session_state:
            st.session_state.trade_df = None
        if "trade_sha" not in st.session_state:
            st.session_state.trade_sha = None

        # 自動加載或手動刷新
            # 自動加載或手動刷新
        if st.button("🔄 Refresh Data from GitHub") or st.session_state.trade_df is None:
            with st.spinner("Fetching latest CSV..."):
                content, sha = get_github_file(f"{REPO_OWNER}/{PUBLIC_REPO}", TRADE_CSV_PATH, GITHUB_TOKEN, BRANCH)
                if content:
                    st.session_state.trade_sha = sha
                    # Read into Pandas
                    df = pd.read_csv(io.StringIO(content))

                    # 🔥 [關鍵修正] 強制將日期欄位轉為 datetime 格式，否則編輯器會報錯
                    # errors='coerce' 會把空的日期變成 NaT (Not a Time)，Streamlit 能正確處理
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

            # 配置編輯器 (讓輸入更方便)
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",  # 允許新增行
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
            # 3. Save Button (Dual Push Logic)
            if st.button("💾 Save Changes to BOTH Repos", type="primary"):
                try:
                    # A. Convert DF back to CSV string
                    csv_buffer = io.StringIO()
                    edited_df.to_csv(csv_buffer, index=False)
                    new_csv_content = csv_buffer.getvalue()

                    # B. Define targets (Public & Private)
                    targets = [
                        {"name": "Public", "repo": f"{REPO_OWNER}/{PUBLIC_REPO}"},
                        {"name": "Private", "repo": f"{REPO_OWNER}/{PRIVATE_REPO}"}
                    ]

                    success_count = 0
                    status_msg = st.empty()  # 用來顯示進度

                    # C. Loop through targets and push
                    for target in targets:
                        repo_full_name = target['repo']
                        status_msg.info(f"⏳ Updating {target['name']} ({repo_full_name})...")

                        # STEP 1: 必須先獲取該 Repo 該檔案當下的 SHA
                        # (不能用 session_state.trade_sha，因為那是讀取時那個 Repo 的 SHA)
                        _, current_sha = get_github_file(repo_full_name, TRADE_CSV_PATH, GITHUB_TOKEN, BRANCH)

                        # STEP 2: 推送更新
                        resp = push_to_github(
                            repo_full_name,
                            TRADE_CSV_PATH,
                            GITHUB_TOKEN,
                            new_csv_content,
                            current_sha,  # 使用剛抓到的 SHA
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
                        st.balloons()

                        # 更新 Session State (通常我們只要更新顯示用的那個)
                        st.session_state.trade_df = edited_df
                        # 這裡不需要更新 trade_sha，因為下次存檔會重新抓新的 SHA

                except Exception as e:
                    st.error(f"System Error: {e}")
