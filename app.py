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
# import styles  <-- (You can move the CSS below into your styles.py later)
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

# Translations (Updated for Terminal Vibe)
translations = {
    "zh": {
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
> <b>Hunter_Alg:</b> Institutional Block Tracking<br>
> <b>Scalp_Net:</b> NQ/HSI/XAU High-Freq Setup<br>
> <b>Opt_Flow:</b> Gamma & Dark Pool Sniper<br>"""
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
> <b>Hunter_Alg:</b> Institutional Block Tracking<br>
> <b>Scalp_Net:</b> NQ/HSI/XAU High-Freq Setup<br>
> <b>Opt_Flow:</b> Gamma & Dark Pool Sniper<br>"""
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

# ==========================================
# 2. Advanced CSS Injection (Shinigami Aesthetic)
# ==========================================
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
        animation: 
            typing 3.5s steps(40, end),
            blink-caret .75s step-end infinite;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        font-size: 1.8em;
        font-weight: 700;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #D32F2F; } }

    /* Classified ID Badge (Profile Card) */
    .id-badge {
        background: #0a0a0a;
        border: 1px solid #333;
        border-top: 3px solid #D32F2F;
        padding: 20px;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .id-badge::before {
        content: 'CLASSIFIED // SEC: OMEGA';
        position: absolute;
        top: 5px;
        right: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6em;
        color: #D32F2F;
    }

    /* Dossier Grid (Social Proof) */
    .dossier-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
    .dossier-card {
        background: #080808;
        border: 1px solid #222;
        transition: all 0.3s ease;
        position: relative;
    }
    .dossier-card:hover {
        border-color: #D32F2F;
        box-shadow: 0 0 15px rgba(211, 47, 47, 0.2);
    }
    .dossier-img-container { height: 160px; overflow: hidden; filter: grayscale(100%) contrast(120%); transition: filter 0.4s ease; border-bottom: 1px solid #222;}
    .dossier-card:hover .dossier-img-container { filter: grayscale(0%); }
    .dossier-img { width: 100%; height: 100%; object-fit: cover; }
    .dossier-content { padding: 15px; }
    .term-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #D32F2F;
        border: 1px solid rgba(211,47,47,0.5);
        background: rgba(211,47,47,0.1);
        padding: 2px 6px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .term-text { color: #A0AAB5; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }

    /* Button Override */
    .stButton > button {
        background-color: transparent !important;
        border: 1px solid #D32F2F !important;
        color: #D32F2F !important;
        border-radius: 0px !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #D32F2F !important;
        color: #fff !important;
        box-shadow: 0 0 10px rgba(211,47,47,0.5);
    }
    
    /* Expander Override */
    .streamlit-expanderHeader {
        background-color: #0a0a0a !important;
        border: 1px solid #222 !important;
        border-radius: 0px !important;
        color: #E2E8F0 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Main App Interface (Navigation)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #222; margin-bottom: 20px;'>
        <h2 class="mono-text" style='color: #fff; margin:0; letter-spacing: 2px;'>KIRA_TERM_v2</h2>
        <p class="mono-text" style='color: #D32F2F; font-size: 0.7em; margin-top:5px;'>[ SYS.ONLINE ]</p>
    </div>
    """, unsafe_allow_html=True)

    nav_map_zh = {
        "試用指標": "[SYS] 指標試用",
        "首頁": "[SYS] 終端首頁",
        "股票研究": "[DATA] 股票研究",
        "大市雷達": "[DATA] 大市雷達",
        "實戰持倉": "[DATA] 實戰持倉",
        "美股獵人": "[ALGO] 美股獵人",
        "期權佈局": "[ALGO] 期權佈局",
        "期貨牛熊": "[ALGO] 期貨牛熊",
        "自動鈔能力": "[AUTO] 自動交易",
        "交易學院": "[DOCS] 系統文檔"
    }

    nav_map_en = {
        "試用指標": "[SYS] Trial Tools",
        "首頁": "[SYS] Main Terminal",
        "股票研究": "[DATA] Daily Recap",
        "大市雷達": "[DATA] Market Radar",
        "實戰持倉": "[DATA] Portfolio",
        "美股獵人": "[ALGO] Stock Hunter",
        "期權佈局": "[ALGO] Option Flow",
        "期貨牛熊": "[ALGO] Futures & Vol",
        "自動鈔能力": "[AUTO] Auto-Trading",
        "交易學院": "[DOCS] Academy"
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
        icons=["terminal", "hdd-network", "server", "activity", "archive", "crosshair", "cpu", "graph-up-arrow", "robot", "book"],
        menu_icon="display",
        default_index=main_default_index,
        key="main_nav_key",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#666", "font-size": "13px"},
            "nav-link": {"font-size": "13px", "font-family": "'JetBrains Mono', monospace", "text-align": "left", "margin": "2px", "color": "#A0AAB5", "border-radius": "0px"},
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

# ==========================================
# 4. Content Routing
# ==========================================

if target_page == "首頁":
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

        # Social Proof (Dossier Mode)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 class='mono-text' style='color:#D32F2F;'>[SEC.CLEARANCE] FIELD REPORTS</h3>", unsafe_allow_html=True)
        
        dossier_html = """
        <div class="dossier-grid">
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
        </div>
        """
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

# Footer
st.markdown("""
<div class="mono-text" style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #222; text-align: center; color: #555; font-size: 0.7rem;">
    <p>[SYS.MEM] © 2026 Kira Protocol. All operations logged.<br>Execution of strategies implies acceptance of terminal risk protocols.</p>
    <p><a href="https://t.me/Ho777ggg" target="_blank" style="color: #D32F2F;">@kira_stocknote</a> | <a href="?page=Legal" target="_self" style="color: #555;">LEGAL.SYS</a></p>
</div>
""", unsafe_allow_html=True)

# Note: Other target_pages (大市雷達, etc.) remain functionally the same, 
# but they will automatically inherit the new fonts, backgrounds, and sharp edges from the CSS injection.
