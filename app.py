import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import sys
import glob
import pandas as pd
import json
import base64
import html

# --- Custom Modules ---
import styles
import utils
import education_page
import stock_page
import strategy_logic
import recap_page
import admin_page

maxMessageSize = 600

# Add Trade folder path
sys.path.append('Trade')
try:
    from Trade import trade_app
except ImportError:
    pass

# ==========================================
# 1. Page Configuration & CSS
# ==========================================
st.set_page_config(
    page_title="Kira Terminal | Quantitative Intel",
    page_icon="☠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Language Setup ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'zh'

def toggle_language():
    if st.session_state['language'] == 'zh':
        st.session_state['language'] = 'en'
    else:
        st.session_state['language'] = 'zh'

# Translations (Terminal Vibe with Kira identity)
translations = {
    "zh": {
        "slogan_title": "> 我是投資美股的夜神月...",
        "slogan_sub": "夜晚我翻開這本筆記本，看透市場結構的底層邏輯。",
        "intro_text": "傳統圖表只告訴你「過去」發生什麼，我的死神之眼看到<b>「未來」大戶想去哪裡</b>。<br>停止散戶式盲猜。用機構級數據執行判決。",
        "tutorial": "[SYS.TUTORIAL] Initialize Override",
        "weekly_btn": "[SYS.DECRYPT] 偷看本週大戶部署",
        "week_ahead": "SYSTEM DIRECTIVE: Week Ahead",
        "expander_title": ">_ Access Market Intel",
        "contact_btn": "INITIATE COMMS (聯絡我)",
        "nav_title": "TERMINAL OVERRIDE",
        "profile_text": """SYSTEM AUTHORIZATION GRANTED.<br>我將投資銀行的數據平民化，幫你避開散戶陷阱。
<br><br>
<b>[CORE.PROTOCOLS]:</b><br>
> 🐳 <b>Stock Hunter:</b> 捕捉機構建倉股<br>
> ⚡ <b>Futures Scalping:</b> NQ/HSI/黃金短線<br>
> 🎯 <b>Option Flow:</b> 異動期權狙擊<br>"""
    },
    "en": {
        "slogan_title": "> INITIALIZING KIRA PROTOCOL...",
        "slogan_sub": "[SYS] Decrypting institutional order flow & market structure.",
        "intro_text": "Retail charts display history. The Kira Terminal visualizes <b>Future Institutional Intent</b>.<br>Cease retail speculation. Execute with Shinigami precision.",
        "tutorial": "[SYS.TUTORIAL] Initialize Override",
        "weekly_btn": "[SYS.DECRYPT] Institutional Weekly Deployment",
        "week_ahead": "SYSTEM DIRECTIVE: Week Ahead",
        "expander_title": ">_ Access Market Intel",
        "contact_btn": "INITIATE COMMS",
        "nav_title": "TERMINAL OVERRIDE",
        "profile_text": """SYSTEM AUTHORIZATION GRANTED.<br>Democratizing dark pool mechanics.
<br><br>
<b>[CORE.PROTOCOLS]:</b><br>
> 🐳 <b>Hunter_Alg:</b> Institutional Block Tracking<br>
> ⚡ <b>Scalp_Net:</b> NQ/HSI/XAU High-Freq Setup<br>
> 🎯 <b>Opt_Flow:</b> Gamma & Dark Pool Sniper<br>"""
    }
}

def t(key):
    return translations[st.session_state['language']].get(key, key)

# Helper Function: Handle Submenu
def handle_submenu(key_name, options, icons, default_url_sub=None):
    default_sub_index = 0
    if default_url_sub and (default_url_sub in options):
        default_sub_index = options.index(default_url_sub)
    elif default_url_sub:
        matches = [i for i, opt in enumerate(options) if default_url_sub in opt]
        if matches: default_sub_index = matches[0]

    return option_menu(
        menu_title=None, options=options, icons=icons, default_index=default_sub_index,
        styles={"container": {"padding": "0!important", "background-color": "#0a0a0a", "border": "1px solid #222", "border-radius": "0px"},
                "nav-link": {"font-size": "13px", "font-family": "monospace", "margin": "0px", "--hover-color": "#1a1a1a", "border-radius": "0px"},
                "nav-link-selected": {"background-color": "#1a1a1a", "color": "#D32F2F", "border-left": "3px solid #D32F2F"}},
        key=key_name
    )

# Apply CSS
styles.apply_custom_css()
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global App Background */
    .stApp {
        background-color: #050505 !important;
        background-image: 
            linear-gradient(rgba(211, 47, 47, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(211, 47, 47, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #E2E8F0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Override Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #222 !important;
    }

    /* Monospace Headers & Text */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    p, span, div {
        font-family: 'Space Grotesk', sans-serif;
    }
    .mono-text {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Typewriter Effect for Hero Slogan */
    .typewriter {
        overflow: hidden;
        border-right: .15em solid #D32F2F;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        font-size: 1.8em;
        font-weight: 700;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #D32F2F; } }

    /* Classified ID Badge (Profile Card) */
    .id-badge {
        background: #0a0a0a; border: 1px solid #333; border-top: 3px solid #D32F2F; padding: 20px;
        position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .id-badge::before {
        content: 'CLASSIFIED // SEC: OMEGA'; position: absolute; top: 5px; right: 10px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.6em; color: #D32F2F;
    }

    /* Dossier Grid (Social Proof) */
    .dossier-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
    .dossier-card { background: #080808; border: 1px solid #222; transition: all 0.3s ease; position: relative; }
    .dossier-card:hover { border-color: #D32F2F; box-shadow: 0 0 15px rgba(211, 47, 47, 0.2); }
    .dossier-img-container { height: 160px; overflow: hidden; filter: grayscale(100%) contrast(120%); transition: filter 0.4s ease; border-bottom: 1px solid #222;}
    .dossier-card:hover .dossier-img-container { filter: grayscale(0%); }
    .dossier-img { width: 100%; height: 100%; object-fit: cover; }
    .dossier-content { padding: 15px; }
    .term-tag {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D32F2F;
        border: 1px solid rgba(211,47,47,0.5); background: rgba(211,47,47,0.1); padding: 2px 6px; display: inline-block; margin-bottom: 10px;
    }
    .term-text { color: #A0AAB5; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }

    /* Button Override */
    .stButton > button {
        background-color: transparent !important; border: 1px solid #D32F2F !important;
        color: #D32F2F !important; border-radius: 0px !important; font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase; transition: all 0.2s;
    }
    .stButton > button:hover { background-color: #D32F2F !important; color: #fff !important; box-shadow: 0 0 10px rgba(211,47,47,0.5); }
    
    /* Expander Override */
    .streamlit-expanderHeader {
        background-color: #0a0a0a !important; border: 1px solid #222 !important; border-radius: 0px !important;
        color: #E2E8F0 !important; font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { color: #D32F2F !important; border-bottom-color: #D32F2F !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Main App Interface (Navigation)
# ==========================================
with st.sidebar:
    col_lang1, col_lang2 = st.columns([1, 3])
    with col_lang1:
        st.write("🌐")
    with col_lang2:
        lang_choice = st.radio("Language", ["中文", "English"],
                               index=0 if st.session_state['language'] == 'zh' else 1,
                               horizontal=True, label_visibility="collapsed")
        new_lang = 'zh' if lang_choice == "中文" else 'en'
        if new_lang != st.session_state['language']:
            st.session_state['language'] = new_lang
            st.rerun()

    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #222; margin-bottom: 20px;'>
        <h2 class="mono-text" style='color: #fff; margin:0; letter-spacing: 2px;'>Stock Note</h2>
        <p class="mono-text" style='color: #D32F2F; font-size: 0.7em; margin-top:5px;'>[股票筆記本]</p>
    </div>
    """, unsafe_allow_html=True)

    nav_map_zh = {
        "試用指標": "🔥 指標試用",
        "首頁": "🏠 終端首頁",
        "股票研究": "📈 股票研究",
        "大市雷達": "📡 大市雷達",
        "實戰持倉": "💼 實戰持倉",
        "美股獵人": "🐳 美股獵人",
        "期權佈局": "🎯 期權佈局",
        "期貨牛熊": "🎢 期貨牛熊",
        "自動鈔能力": "🤖 自動交易",
        "交易學院": "🎓 系統文檔"
    }

    nav_map_en = {
        "試用指標": "🔥 Trial Tools",
        "首頁": "🏠 Main Terminal",
        "股票研究": "📈 Daily Recap",
        "大市雷達": "📡 Market Radar",
        "實戰持倉": "💼 Portfolio",
        "美股獵人": "🐳 Stock Hunter",
        "期權佈局": "🎯 Option Flow",
        "期貨牛熊": "🎢 Futures & Vol",
        "自動鈔能力": "🤖 Auto-Trading",
        "交易學院": "🎓 Academy"
    }

    current_nav_map = nav_map_zh if st.session_state['language'] == 'zh' else nav_map_en
    display_options = list(current_nav_map.values())
    
    query_params = st.query_params
    url_main_page = query_params.get("page", "首頁")
    url_sub_page = query_params.get("sub", None)

    try:
        main_default_index = list(nav_map_zh.keys()).index(url_main_page)
    except ValueError:
        main_default_index = 0

    selected_display = option_menu(
        menu_title=t("nav_title"),
        options=display_options,
        icons=["", "", "", "", "", "", "", "", "", ""], # 移除預設 icon，使用文字內建 Emoji
        menu_icon="display",
        default_index=main_default_index,
        key="main_nav_key",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {"font-size": "14px", "font-family": "'JetBrains Mono', monospace", "text-align": "left", "margin": "2px", "color": "#A0AAB5", "border-radius": "0px"},
            "nav-link-selected": {"background-color": "#111", "color": "#D32F2F", "border-left": "3px solid #D32F2F"},
        }
    )

    selected_nav = [k for k, v in current_nav_map.items() if v == selected_display][0]

    if url_main_page == "SecretAdmin" and selected_nav == "首頁":
        target_page = "SecretAdmin"
    elif url_main_page == "Legal" and selected_nav == "首頁":
        target_page = "Legal"
    else:
        target_page = selected_nav
        if target_page != url_main_page:
            st.query_params["page"] = target_page

    if selected_nav == "自動鈔能力":
        st.caption("AUTOMATED TRADING")
        ea_options_display = ["EA 介紹"] if st.session_state['language'] == 'zh' else ["EA Intro"]
        target_sub = handle_submenu("sub_ea", ea_options_display, ["robot"], url_sub_page)
        target_page = "EA 介紹"

    st.markdown("---")

if url_main_page == "Legal" and selected_nav == "首頁":
    target_page = "Legal"

# ==========================================
# 3. Security Check
# ==========================================
locked_pages = []
if target_page in locked_pages:
    if not utils.check_access_or_show_teaser(target_page):
        st.stop()

# ==========================================
# 4. Content Routing (Complete Integrations)
# ==========================================

if target_page == "SecretAdmin":
    admin_page.render_admin_console()

elif target_page == "首頁":
    col_main, col_profile = st.columns([0.7, 0.3], gap="large")
    with col_main:
        st.markdown(f"""
            <div class="typewriter">{t('slogan_title')}</div>
            <h3 class="mono-text" style='color:#666; font-size: 1.1em; margin-top:10px;'>{t('slogan_sub')}</h3>
            <p style='font-size: 1em; color: #888; line-height: 1.6; margin-top: 15px; border-left: 2px solid #333; padding-left: 10px;'>
            {t('intro_text')}
            </p>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Market Tape (Dark Mode)
        components.html("""
        <div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        {"symbols": [{"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"}, {"proName": "FOREXCOM:NSXUSD", "title": "US 100"}, {"description": "Gold", "proName": "OANDA:XAUUSD"}],
        "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "en"}</script></div>""",
                        height=100)

        # Social Proof (Dossier Mode) - FIX: Removed indentation to prevent Markdown code block rendering
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 class='mono-text' style='color:#D32F2F;'>[SEC.CLEARANCE] FIELD REPORTS</h3>", unsafe_allow_html=True)
        
        dossier_html = """<div class="dossier-grid">
<div class="dossier-card">
<div class="dossier-img-container">
<img src="https://raw.githubusercontent.com/ParisTrader/paristrader-terminal/main/Community/comm_pnl1.jpg" class="dossier-img" onerror="this.src='https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=500&auto=format&fit=crop';">
</div>
<div class="dossier-content">
<div class="term-tag">OP: TREND_CATCH</div>
<p class="term-text">> "Execution confirmed. Radar intercepted vector breakout at origin."</p>
</div>
</div>
<div class="dossier-card">
<div class="dossier-img-container" style="display:flex; flex-direction:column; justify-content:center; padding: 20px; background: #050505;">
<div style="border-left: 2px solid #D32F2F; padding-left: 10px;">
<span style="color:#666; font-family:monospace; font-size:0.7em;">LOG: 10:45 AM [MEMBER ID: 884]</span>
<p style="color:#ddd; font-family:monospace; font-size:0.85em; margin-top:5px;">> Velocity off the charts. Oil surge detected pre-retail news. 🩸</p>
</div>
</div>
<div class="dossier-content">
<div class="term-tag">OP: ALPHA_LEAK</div>
<p class="term-text">> "Data propagation 5 mins ahead of retail terminals. Block trade captured."</p>
</div>
</div>
<div class="dossier-card">
<div class="dossier-img-container">
<img src="https://raw.githubusercontent.com/ParisTrader/paristrader-terminal/main/Community/comm_pnl2.jpg" class="dossier-img" onerror="this.src='https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=500&auto=format&fit=crop';">
</div>
<div class="dossier-content">
<div class="term-tag">OP: DATA_PIVOT</div>
<p class="term-text">> "NFP reversal predicted via options flow matrix. Fakeout avoided."</p>
</div>
</div>
</div>"""
        st.markdown(dossier_html, unsafe_allow_html=True)
        st.markdown("---")

    with col_profile:
        img_path = "static/profile.jpg"

        def get_image_base64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
            return "https://ui-avatars.com/api/?name=Kira&background=0a0a0a&color=D32F2F&size=150"

        img_src = get_image_base64(img_path)

        # ID BADGE UI
        st.markdown(f"""
        <div class="id-badge">
            <img src="{img_src}" width="100" style="filter: grayscale(100%) contrast(150%); border: 2px solid #222; float: right; margin-left: 15px;">
            <h3 class="mono-text" style="margin-top:0px; color:#fff; font-size:1.2em;">KIRA</h3>
            <p class="mono-text" style="color: #D32F2F; font-weight: bold; font-size: 0.7em; margin-top:-10px;">ID: EX-IBANK // RANK: QUANT</p>
            <div style="clear: both;"></div>
            <hr style="margin: 15px 0; border-top: 1px dashed #333;">
            <div class="mono-text" style="font-size: 0.8em; line-height: 1.6; color: #888;">
                {t('profile_text')}
            </div>
            <a href="https://t.me/kira_stocknote" target="_blank" style="text-decoration: none;">
                <div style="background-color:#111; color:#D32F2F; border:1px solid #D32F2F; text-align:center; padding:10px; margin-top:15px; font-family:'JetBrains Mono', monospace; font-size: 0.8em; text-transform: uppercase; transition: 0.3s;">
                    {t('contact_btn')}
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

elif target_page == "Market Dashboard":
    st.title("Market Dashboard")
    path = os.path.join("MarketDashboard", "main_auto", "output")
    html_content, filename = utils.get_latest_file_content(path)
    if html_content:
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning(f"⚠️ No dashboard files found. Error: {filename}")

elif target_page == "股票研究":
    st.title("📈 股票研究 (Daily Recap)")
    if utils.check_access_or_show_teaser("股票研究", description="此為會員專屬內容，解鎖深度每日覆盤與個股解析。"):
        recap_page.render_recap_page(utils.load_markdown_with_images)

elif target_page == "宏觀專欄":
    st.markdown("""
    <style>
        .ig-card-container {
            background: #0a0a0a; border: 1px solid #222; border-radius: 0px; padding: 15px; margin-bottom: 15px;
        }
        .featured-header { border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 10px; }
        .featured-tag { background-color: rgba(211,47,47,0.1); color: #D32F2F; border: 1px solid #D32F2F; padding: 2px 8px; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; }
        .featured-title { color: #fff; font-size: 1.25rem; font-weight: 700; margin-top: 8px; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🦅 知世界事，賺世界錢")
    st.caption("洞察先機 (Kira Trader Prediction)")
    files = sorted(glob.glob(os.path.join("DailyInsights", "*.md")), reverse=True)

    if not files:
        st.info("No insights published yet.")
    else:
        def parse_insight(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                raw = f.read()
            lines = raw.split('\n')
            meta = {"title": lines[0].replace('#', '').replace('*', '').strip(), "date": "Recent", "tag": "MEMO", "sentiment": ""}
            body_start = 1
            for idx, line in enumerate(lines):
                line = line.strip()
                if "**Date:**" in line: meta["date"] = line.replace("**Date:**", "").strip()
                if "**Tag:**" in line: meta["tag"] = line.replace("**Tag:**", "").strip()
                elif line.startswith("Tag:"): meta["tag"] = line.replace("Tag:", "").strip()
                if "**Sentiment:**" in line: meta["sentiment"] = line.replace("**Sentiment:**", "").strip()
                if idx > 0 and idx < 8 and line == "": body_start = idx + 1
            full_body = "\n".join(lines[body_start:]).strip()
            return meta, full_body

        latest_file = files[0]
        meta, full_body = parse_insight(latest_file)

        with st.container():
            icon = "🦅"
            if "Bullish" in meta['sentiment']: icon = "🐂"
            elif "Bearish" in meta['sentiment']: icon = "🐻"
            elif "Warning" in meta['sentiment']: icon = "⚠️"

            header_html = f"""
            <div class="ig-card-container">
                <div class="featured-header">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="featured-tag">{meta['tag']}</span>
                        <span class="mono-text" style="color: #666; font-size: 0.85rem;">🗓️ {meta['date']}</span>
                    </div>
                    <div class="featured-title">{icon} {meta['title']}</div>
                    <div style="color:#D32F2F; font-weight:bold; margin-top:5px; font-size: 0.85rem; font-family:'JetBrains Mono', monospace;">{meta['sentiment']}</div>
                </div>
            """
            st.markdown(header_html, unsafe_allow_html=True)
            st.markdown(full_body)
            st.markdown('<div style="margin-top:15px; padding-top:10px; border-top:1px dashed #222; text-align:right; font-size:0.7rem; color:#666; font-family:\'JetBrains Mono\', monospace;">@KiraTrader | Institutional Data</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📚 歷史數據 (Archive)")

        if len(files) > 1:
            cols = st.columns(2)
            for i, file_path in enumerate(files[1:]):
                meta, full_body = parse_insight(file_path)
                col = cols[i % 2]
                with col:
                    emoji_map = {"Bullish": "🟢", "Bearish": "🔴", "Neutral": "⚪", "Warning": "⚠️"}
                    sent_key = meta['sentiment'].split('(')[0].strip()
                    status_icon = emoji_map.get(sent_key, "📄")
                    expander_label = f"{status_icon} {meta['title']} | {meta['date']}"
                    with st.expander(expander_label, expanded=False):
                        st.caption(f"📌 {meta['tag']} | {meta['sentiment']}")
                        st.markdown(full_body)

elif target_page == "試用指標":
    st.title("🔥 獨家指標試用與教學")
    st.caption("透過量化指標，捕捉最佳進出場時機")
    html_content = utils.load_html_file(os.path.join("Community", "indicator.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.error("⚠️ 找不到 indicator.html，請檢查檔案是否已上傳或路徑是否正確。")

elif target_page == "大市雷達":
    st.title("📡 Market Radar")
    st.caption("識別市場轉勢訊號 | Detect Market Reversals")
    tab_risk, tab_breadth, tab_cftc = st.tabs(["⚠️ 恐慌指數 Risk Meter", "🌊 市場寬度 Breadth", "🐋 莊家持倉 COT"])
    is_vip = st.session_state.get("authentication_status", False)

    with tab_risk:
        st.subheader("Market Implied Risk")
        html_content, _ = utils.get_latest_file_content("ImpliedParameters")
        if html_content:
            fix_style = "<style>body {display: block !important; height: auto !important; min-height: 100vh; padding-top: 50px; background-color: #050505 !important;} .card { margin: 0 auto !important; border-radius: 0px !important; border: 1px solid #222 !important; }</style>"
            final_html = html_content.replace("<head>", "<head>" + fix_style)
            if is_vip:
                components.html(final_html, height=2200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Showing Partial Data)")
                components.html(final_html, height=800, scrolling=False)
                utils.check_access_or_show_teaser("Risk Meter Full Access", description="Unlock full implied volatility data.")
        else:
            st.warning("⚠️ No risk reports found.")

    with tab_breadth:
        st.subheader("Market Breadth")
        html_content, _ = utils.get_latest_file_content(os.path.join("MarketDashboard", "MarketBreadth"), "market_breadth_*.html")
        if html_content:
            if is_vip:
                components.html(html_content, height=2200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Showing Partial Data)")
                components.html(html_content, height=800, scrolling=False)
                utils.check_access_or_show_teaser("Market Breadth Full Access", description="Unlock full breadth indicators.")
        else:
            st.warning("⚠️ Market Breadth report not found.")

    with tab_cftc:
        st.subheader("CFTC Institutional Positioning")
        html_content, _ = utils.get_latest_file_content("MarketDashboard", "cftc_pro_report*.html")
        if html_content:
            if is_vip:
                components.html(html_content, height=2200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Showing Top Positions)")
                components.html(html_content, height=800, scrolling=False)
                utils.check_access_or_show_teaser("CFTC Report Full Access", description="See all institutional positioning.")
        else:
            st.warning("⚠️ CFTC Report not found.")

elif target_page == "美股獵人":
    stock_page.render_stock_page()

elif target_page == "期權佈局":
    st.title("🎯 Options Flow Analytics")
    st.caption("跟蹤聰明錢異動 | Track Smart Money Flow")
    tab_us, tab_strat, tab_hk = st.tabs(["🇺🇸 美股期權異動", "🛠️ 策略模擬器 Strategy", "🇭🇰 港股期權佈局"])

    with tab_us:
        st.subheader("US Option Strike Analysis")
        if utils.check_access_or_show_teaser("美股期權 US Option", description="Follow the Smart Money."):
            html, _ = utils.get_latest_file_content("Option", "option_strike_*.html")
            if html: components.html(html, height=2000, scrolling=True)
            else: st.warning("⚠️ No US reports found.")
    with tab_strat:
        st.subheader("Interactive Option Strategy Builder")
        if utils.check_access_or_show_teaser("期權策略 Strategy", description="Quantitative Analysis."):
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                ticker = c1.text_input("Ticker", "NVDA", key="strat_ticker").upper()
                width = c2.number_input("Width ($)", 5, key="strat_width")
                call_otm = c3.number_input("Call OTM %", 1.03, step=0.01, key="strat_call")
                put_itm = c4.number_input("Put ITM %", 0.97, step=0.01, key="strat_put")
                if st.button("🚀 Generate", type="primary", use_container_width=True, key="strat_btn"):
                    with st.status(f"Processing {ticker}...", expanded=True) as status:
                        try:
                            _, _, date = strategy_logic.get_local_data(ticker)
                            status.write(f"✅ Loaded data: {date}")
                            html_str, msg = strategy_logic.generate_strategy_html(ticker, width, call_otm, put_itm)
                            if html_str:
                                status.update(label="Done!", state="complete")
                                components.html(html_str, height=1400, scrolling=True)
                            else:
                                status.update(label="Failed", state="error")
                                st.error(msg)
                        except Exception as e:
                            st.error(f"Error: {e}")
    with tab_hk:
        st.subheader("HK Option Market Analysis")
        html_str, _ = utils.get_latest_file_content("Option", "HK_Option_Market_*.html")
        if html_str: components.html(html_str, height=2000, scrolling=True)
        else: st.warning("⚠️ No HK reports found.")

elif target_page == "期貨牛熊":
    st.title("🎢 Futures & Trends")
    st.caption("短線波幅與牛熊重貨區 | Volatility & Heavy Zones")
    tab_vol, tab_vp, tab_cbbc = st.tabs(["⚡ 日內波幅 (Volatility)", "📊 成交分佈 (Volume Profile)", "🐻 牛熊重貨區 (CBBC)"])
    is_vip = st.session_state.get("authentication_status", False)

    with tab_vol:
        st.subheader("Intraday Volatility Analysis")
        html_content = utils.load_html_file(os.path.join("MarketDashboard", "Intraday_Volatility.html"))
        if "File not found" not in html_content:
            if is_vip: components.html(html_content, height=1200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Recent Volatility Only)")
                components.html(html_content, height=600, scrolling=False)
                utils.check_access_or_show_teaser("Volatility Full Access", description="Unlock real-time volatility levels.")
        else: st.warning("⚠️ Report not found")

    with tab_vp:
        st.subheader("Volume Profile Analysis")
        if utils.check_access_or_show_teaser("成交分佈 Volume Profile"):
            html_content, filename = utils.get_latest_file_content("VP", "volume_profile_dashboard_*.html")
            if html_content: components.html(html_content, height=1000, scrolling=True)
            else: st.warning("⚠️ No VP reports found")

    with tab_cbbc:
        st.subheader("HSI CBBC Heavy Zone")
        if utils.check_access_or_show_teaser("牛熊重貨區 CBBC Ladder", description="看穿大戶屠牛/殺熊目標價"):
            html_content = utils.load_html_file(os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html"))
            if "File not found" not in html_content: components.html(html_content, height=1200, scrolling=True)
            else: st.warning("⚠️ Report not found")

elif target_page == "實戰持倉":
    st.title("💼 Kira Picks (百萬美金實戰倉位)")
    path = "Trade"
    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])
    is_vip = st.session_state.get("authentication_status", False)

    with tab1:
        html_content, filename = utils.get_latest_file_content(path, "trade_record_*.html")
        if html_content:
            st.caption(f"📅 Report: {filename}")
            if is_vip: components.html(html_content, height=1200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Showing Top Holdings Only)")
                components.html(html_content, height=800, scrolling=False)
                utils.check_access_or_show_teaser("Stock Journal Full Access", description="Unlock full trade journal.")
        else: st.warning("⚠️ Report not found.")
    with tab2:
        if utils.check_access_or_show_teaser("Option Desk"):
            html_content, filename = utils.get_latest_file_content(path, "option_record_*.html")
            if html_content: components.html(html_content, height=1200, scrolling=True)
            else: st.warning("⚠️ Report not found.")

elif target_page == "EA 介紹":
    st.title("🤖 MT5 Expert Advisor (EA)")
    html_content = utils.load_html_file(os.path.join("MT5EA", "ea_marketing.html"))
    if "File not found" not in html_content: st.html(html_content) 
    else: st.warning("⚠️ Content not found.")

elif target_page == "交易學院":
    st.title("🎓 交易學院 (Academy)")
    if utils.check_access_or_show_teaser("交易學院", description="此為會員專屬內容，解鎖進階量化策略與教學。"):
        education_page.render_education_page(utils.check_access_or_show_teaser, utils.load_markdown_with_images)

elif target_page == "CFD開戶優惠":
    st.title("🔗 Trading Resources")
    html_content = utils.load_html_file(os.path.join("Resources", "external_links.html"))
    if "File not found" not in html_content: st.html(html_content) 
    else: st.warning("⚠️ Content not found.")

elif target_page == "升級會員":
    st.title("💎 升級機構級數據")
    html_content = utils.load_html_file(os.path.join("Community", "community_promo.html"))
    if "File not found" not in html_content: st.html(html_content)
    else: st.error("⚠️ Content not found")

# Footer
st.markdown("""
<div class="mono-text" style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #222; text-align: center; color: #555; font-size: 0.7rem;">
    <p>[SYS.MEM] © 2026 Kira Protocol. All operations logged.<br>Execution of strategies implies acceptance of terminal risk protocols.</p>
    <p><a href="https://t.me/kira_stocknote" target="_blank" style="color: #D32F2F;">@kira_stocknote</a> | <a href="?page=Legal" target="_self" style="color: #555;">LEGAL.SYS</a></p>
</div>
""", unsafe_allow_html=True)
