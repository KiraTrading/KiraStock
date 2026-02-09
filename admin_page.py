import streamlit as st
import google.generativeai as genai
import os
import requests
import base64
from datetime import datetime


# 把原本的邏輯包裝成一個函數
def render_admin_console():
    # --- 0. 安全驗證 (簡單密碼鎖) ---
    # 請在 .streamlit/secrets.toml 加入: ADMIN_PASSWORD = "你的密碼"
    password = st.text_input("🔒 Enter Admin Password", type="password")

    if "ADMIN_PASSWORD" in st.secrets:
        correct_password = st.secrets["ADMIN_PASSWORD"]
    else:
        st.error("❌ ADMIN_PASSWORD not found in secrets.toml")
        st.stop()

    if password != correct_password:
        st.warning("⛔ Access Denied")
        st.stop()

    # --- 驗證通過後才顯示內容 ---

    # CONFIGURATION
    LOCAL_SAVE_FOLDER = r"E:\ALGO_Snake\Website\DailyInsights"  # 如果是部署到雲端，這個路徑可能無效，建議只用 GitHub Upload
    REPO_OWNER = "ParisTrader"
    REPO_NAME = "paristrader-terminal"
    BRANCH = "main"

    try:
        GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except FileNotFoundError:
        st.error("❌ secrets.toml file not found!")
        st.stop()

    genai.configure(api_key=GEMINI_API_KEY)

    st.title("🕵️‍♂️ Paris Content Generator (Admin Only)")
    st.markdown("---")

    # Input Area
    col_input, col_preview = st.columns([1, 1])

    with col_input:
        st.header("1. Source Material")
        raw_text = st.text_area("Paste News/Article Here:", height=300)
        user_instruction = st.text_input("Extra Instructions:", "")
        generate_btn = st.button("🚀 Generate Draft", type="primary")

    # Session State Initialization
    if "draft_content" not in st.session_state: st.session_state.draft_content = ""
    if "draft_title" not in st.session_state: st.session_state.draft_title = ""

    # PARIS PERSONA (保持你修改後的版本)
    PARIS_PERSONA = """
    You are Paris Trader. You are a Senior Portfolio Manager and Ex-Prop Trader. You write concise, high-impact market memos for institutional desks.

    ROLE & TONE:
    - **Identity:** Cynical, sharp, "Smart Money" veteran.
    - **Tone:** Direct, condensed, judgmental. No fluff.
    - **Language:** Traditional Chinese (Hong Kong Finance Style) mixed with English financial terminology (e.g., "Yield Curve", "Supply Indigestion", "Risk Premium").
    - **Style:** Write like a Bloomberg Terminal chat or an internal Hedge Fund memo. Short sentences. High information density.

    CRITICAL FORMATTING RULES (DO NOT IGNORE):
    1. **NO HEADERS:** Do NOT output text like "Key Bullet Points:", "The Paris Take:", or "Introduction".
    2. **NO FILLER WORDS:** Do NOT use "Firstly", "Secondly", "In conclusion", "It is worth noting".
    3. **STRUCTURE:**
       - Line 1: A punchy, HK-style Title.
       - Line 2: A clear Directional Tag (e.g., 【看淡 - Bearish】).
       - Body: A seamless blend of facts and analysis. Use bullet points *only* if listing specific data, otherwise use short paragraphs.

    CORE OBJECTIVE:
    **Don't summarize the news. Interpret the PnL impact.**
    - If supply is up, don't just say "supply is increasing." Say "Supply indigestion is crushing the long end."
    - Focus on: Liquidity, structure, flows, and positioning.
    """
    # Generation Logic
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

    # Review & Publish Section
    with col_preview:
        st.header("2. Review & Publish")
        final_title = st.text_input("Title", value=st.session_state.draft_title)
        final_content = st.text_area("Markdown Content", value=st.session_state.draft_content, height=500)

        st.markdown("### Preview")
        if final_title: st.markdown(f"## {final_title}")
        if final_content: st.markdown(final_content)

        st.divider()
        upload_btn = st.button("✅ Upload to GitHub", type="primary", use_container_width=True)

        if upload_btn and final_title and final_content:
            date_str = datetime.now().strftime("%Y-%m-%d")
            safe_title = "".join([c if c.isalnum() else "_" for c in final_title])[:50]
            filename = f"{date_str}_{safe_title}.md"
            full_file_content = f"# {final_title}\n**Date:** {date_str}\n\n{final_content}"

            # GitHub Upload Logic
            try:
                with st.status("☁️ Uploading to GitHub...", expanded=True) as status:
                    git_path = f"DailyInsights/{filename}"
                    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{git_path}"

                    message_bytes = full_file_content.encode('utf-8')
                    base64_bytes = base64.b64encode(message_bytes)
                    base64_content = base64_bytes.decode('ascii')

                    data = {
                        "message": f"Add insight: {safe_title}",
                        "content": base64_content,
                        "branch": BRANCH
                    }

                    headers = {
                        "Authorization": f"token {GITHUB_TOKEN}",
                        "Accept": "application/vnd.github.v3+json"
                    }

                    # Check if file exists to update or create
                    get_resp = requests.get(url, headers=headers)
                    if get_resp.status_code == 200:
                        data["sha"] = get_resp.json()["sha"]

                    response = requests.put(url, json=data, headers=headers)

                    if response.status_code in [200, 201]:
                        status.update(label="🎉 Upload Complete!", state="complete", expanded=False)
                        st.balloons()
                    else:
                        st.error(f"❌ Upload Failed: {response.status_code}")
                        st.json(response.json())

            except Exception as e:
                st.error(f"❌ API Connection Error: {str(e)}")