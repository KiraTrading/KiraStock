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
    page_title="ParisTrader - Smart Money Tracker | 量化終端",
    page_icon="🦅",
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


# 翻譯字典 (已更新為合規的中性、客觀字眼)
translations = {
    "zh": {
        "slogan_title": "量化期權與市場數據終端",
        "slogan_sub": "客觀追蹤期權異動與宏觀資金流向",
        "intro_text": "利用數據模型與 API 整合公開資訊，提供即時的市場深度與期權數據視覺化分析。<br>A quantitative approach to market data.",
        "tutorial": "📺 系統操作說明",
        "weekly_btn": "📊 本週宏觀數據整理 (Weekly Data)",
        "week_ahead": "🧠 Week Ahead Data",
        "expander_title": "📖 點擊展開：宏觀經濟日曆",
        "contact_btn": "聯絡系統管理員",
        "vip_promo_title": "👑 解鎖大戶底牌",
        "vip_promo_desc": "偷看機構持倉 (Insider)<br>& 聰明錢流向 (Flow)",
        "vip_join": "🚀 立即加入 (Join Now)",
        "nav_title": "導航選單",
        "settings": "語言設定 / Settings",
        "profile_text": """我們致力於將機構級市場數據視覺化，提供客觀的量化分析工具。
<br><br>
<b>系統核心模組:</b><br>
• 🐳 <b>Stock Hunter:</b> 機構建倉數據追蹤<br>
• ⚡ <b>Futures Dashboard:</b> 宏觀期貨數據整合<br>
• 🎯 <b>Option Flow:</b> 異動期權掃描與統計<br>"""
    },
    "en": {
        "slogan_title": "Quantitative Options & Market Data Terminal",
        "slogan_sub": "Objective tracking of option anomalies and macro flow",
        "intro_text": "Integrating public information via data models and APIs to provide real-time market depth and options data visualization.<br>A quantitative approach to market data.",
        "tutorial": "📺 System Documentation",
        "weekly_btn": "📊 Weekly Macro Data Summary",
        "week_ahead": "🧠 Week Ahead Data",
        "expander_title": "📖 Click to Expand: Macro Calendar",
        "contact_btn": "Contact Administrator",
        "vip_promo_title": "👑 Unlock Institutional Data",
        "vip_promo_desc": "Insider Holdings<br>& Smart Money Flow",
        "vip_join": "🚀 Join Now",
        "nav_title": "Navigation",
        "settings": "Settings",
        "profile_text": """Dedicated to visualizing institutional market data and providing objective quantitative tools.
<br><br>
<b>Core Modules:</b><br>
• 🐳 <b>Stock Hunter:</b> Institutional Build Tracking<br>
• ⚡ <b>Futures Dashboard:</b> Macro Futures Integration<br>
• 🎯 <b>Option Flow:</b> Unusual Options Scanning<br>"""
    }
}

# 確保 t(key) 函數定義在呼叫它之前，避免 NameError
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
        styles={"container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.03)",
                              "border-radius": "10px"},
                "nav-link": {"font-size": "14px", "margin": "3px", "--hover-color": "#374151"},
                "nav-link-selected": {"background-color": "#4B5563"}},
        key=key_name
    )


# Apply CSS
styles.apply_custom_css()
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 20px !important; font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2563EB !important; border-bottom-color: #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Main App Interface (Navigation)
# ==========================================

# --- Sidebar ---
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

    # 在選單頂部當眼處加入營運公司資訊 (稅局要求)
    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #374151; margin-bottom: 20px;'>
        <h2 style='color: #F3F4F6; margin:0; letter-spacing: 1px; font-weight: 700;'>ParisTrader</h2>
        <p style='color: #9CA3AF; font-size: 0.85em; margin-top:5px;'>Quantitative Data Terminal</p>
        <p style='color: #6B7280; font-size: 0.7em; margin-top:5px; font-weight: 600;'></p>
    </div>
    """, unsafe_allow_html=True)

    # 合規處理：隱藏升級、持倉、以及 CFD 開戶優惠，加入法律條款
    nav_map_zh = {
        # "升級會員": "💎 升級會員 (VIP)",
        # "CFD開戶優惠": "🎁 開戶專屬優惠",
        "試用指標": "🔥 試用指標教學",
        "首頁": "首頁",
        "大市雷達": "大市雷達",
        # "個人持倉": "個人持倉",
        "美股獵人": "美股獵人",
        "期權佈局": "期權佈局",
        "期貨牛熊": "期貨牛熊",
        "EA程式回測": "EA程式回測",
        "交易學院": "交易學院",
        "Legal": "📜 條款及細則"
    }

    nav_map_en = {
        # "升級會員": "💎 Go VIP",
        # "CFD開戶優惠": "🎁 Broker Offer",
        "試用指標": "🔥 Trial Indicator",
        "首頁": "Home",
        "大市雷達": "Market Radar",
        # "個人持倉": "Portfolio",
        "美股獵人": "Stock Hunter",
        "期權佈局": "Option Flow",
        "期貨牛熊": "Futures & Vol",
        "EA程式回測": "EA Backtesting",
        "交易學院": "Academy",
        "Legal": "📜 Legal & Terms"
    }

    current_nav_map = nav_map_zh if st.session_state['language'] == 'zh' else nav_map_en
    display_options = list(current_nav_map.values())
    
    # --- Navigation Logic Fix ---
    query_params = st.query_params
    # 獲取 URL 參數，默認為 "首頁"
    url_main_page = query_params.get("page", "首頁")

    # 處理 Sub Page 參數
    url_sub_page = query_params.get("sub", None)

    # 1. 計算 Menu 的 Default Index
    try:
        main_default_index = list(nav_map_zh.keys()).index(url_main_page)
    except ValueError:
        main_default_index = 0

    # 2. 渲染 Option Menu
    # 加入了 "shield-check" 圖標用於法律條款
    selected_display = option_menu(
        menu_title=t("nav_title"),
        options=display_options,
        icons=["lightning-charge", "house", "activity", "crosshair", "layers", "graph-up-arrow", "robot", "mortarboard", "shield-check"],
        menu_icon="compass",
        default_index=main_default_index,
        key="main_nav_key",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#9CA3AF", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "5px", "color": "#D1D5DB",
                         "--hover-color": "#1F2937"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "#FFFFFF", "font-weight": "600"},
        }
    )

    # 3. 反向查找：將 Menu 顯示的文字轉回系統內部的 Key
    selected_nav = [k for k, v in current_nav_map.items() if v == selected_display][0]

    # 4. 關鍵修復：處理隱藏頁面邏輯 & URL 同步
    if url_main_page == "SecretAdmin" and selected_nav == "首頁":
        target_page = "SecretAdmin"
    elif url_main_page == "Legal" and selected_nav == "首頁":
        target_page = "Legal"
    else:
        target_page = selected_nav
        if target_page != url_main_page:
            st.query_params["page"] = target_page

    # 處理 EA 子菜單邏輯
    if selected_nav == "EA程式回測":
        st.caption("AUTOMATED TRADING")
        ea_options_display = ["EA 介紹"] if st.session_state['language'] == 'zh' else ["EA Intro"]
        target_sub = handle_submenu("sub_ea", ea_options_display, ["robot"], url_sub_page)

        if target_sub == "EA Intro":
            target_page = "EA 介紹"
        elif target_sub == "EA 介紹":
            target_page = "EA 介紹"

    st.markdown("---")

if url_main_page == "Legal" and selected_nav == "首頁":
    target_page = "Legal"

# ==========================================
# 3. Security Check
# ==========================================
# 確保美股獵人在進入時就嚴格阻擋
locked_pages = ["美股獵人"] 
if target_page in locked_pages:
    if not utils.check_access_or_show_teaser(target_page):
        st.stop()

# ==========================================
# 4. Content Routing
# ==========================================

if target_page == "SecretAdmin":
    admin_page.render_admin_console()

elif target_page == "首頁":
    # 合規設定：加入非常清晰的停止收生公告
    st.info("📌 **本系統僅提供客觀市場數據作學術與教育用途。")
    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_profile = st.columns([0.7, 0.3], gap="large")
    with col_main:
        st.markdown(f"""
            <h1 style='color:white; font-weight:800; font-size: 2.5em;'>{t('slogan_title')}</h1>
            <h3 style='color:#94a3b8; font-size: 1.3em;'>{t('slogan_sub')}</h3>
            <p style='font-size: 1.1em; color: #64748b; line-height: 1.6; margin-top: 15px;'>
            {t('intro_text')}
            </p>
            """, unsafe_allow_html=True)

        st.markdown("---")

        components.html("""
        <div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        {"symbols": [{"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"}, {"proName": "FOREXCOM:NSXUSD", "title": "US 100"}, {"description": "Gold", "proName": "OANDA:XAUUSD"}],
        "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "en"}</script></div>""",
                        height=100)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(t('tutorial'))
        st.video("https://www.youtube.com/watch?v=qb3XtEPj8cA")
        st.markdown("<br>", unsafe_allow_html=True)

        st.link_button(
            label=t('weekly_btn'),
            url="https://parisprogram.uk/zh/member/post/RPT-20260131182122129?hash=e71209296eb426dd311b01d899a5615e5c858f30f34d39be3e589d137227761f",
            type="primary",
            use_container_width=True
        )

    with col_profile:
        img_path = "static/profile.jpg"

        def get_image_base64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
            return "https://ui-avatars.com/api/?name=Paris+Trader&background=0D8ABC&color=fff&size=150"

        img_src = get_image_base64(img_path)

        st.markdown(f"""
<div class="profile-card">
<img src="{img_src}" width="120" style="border-radius:50%; border: 3px solid #2563EB;">
<h3 style="margin-top:10px; color:#F3F4F6;">Paris Trader</h3>
<p style="color: #60A5FA; font-weight: bold; font-size: 0.9em;">Data & Analytics</p>
<hr style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);">
<div style="text-align: left; font-size: 0.9em; line-height: 1.6; color: #cbd5e1;">
{t('profile_text')}
</div>
<a href="https://t.me/ParisTrader" target="_blank">
<button style="background-color:#2563EB; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; width:100%; margin-top:10px; font-weight:bold; box-shadow: 0 4px 6px rgba(37,99,235,0.3);">
{t('contact_btn')}
</button>
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

elif target_page == "試用指標":
    st.title("🔥 獨家指標試用與教學")
    st.caption("透過量化指標，客觀評估市場結構")
    html_content = utils.load_html_file(os.path.join("Community", "indicator.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.error("⚠️ 找不到 indicator.html，請檢查檔案是否已上傳或路徑是否正確。")

elif target_page == "大市雷達":
    st.title("📡 Market Radar (大市雷達)")
    st.caption("識別市場轉勢訊號 | Detect Market Reversals")
    tab_risk, tab_breadth, tab_cftc = st.tabs(["⚠️ 恐慌指數 Risk Meter", "🌊 市場寬度 Breadth", "🐋 莊家持倉 COT"])

    is_vip = st.session_state.get("authentication_status", False)

    with tab_risk:
        st.subheader("Market Implied Risk")
        html_content, _ = utils.get_latest_file_content("ImpliedParameters")
        if html_content:
            fix_style = "<style>body {display: block !important; height: auto !important; min-height: 100vh; padding-top: 50px; background-color: #020617 !important;} .card { margin: 0 auto !important; }</style>"
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
            if html:
                components.html(html, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No US reports found.")
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
        if html_str:
            components.html(html_str, height=2000, scrolling=True)
        else:
            st.warning("⚠️ No HK reports found.")

elif target_page == "期貨牛熊":
    st.title("🎢 Futures & Trends")
    st.caption("短線波幅與牛熊重貨區 | Volatility & Heavy Zones")
    tab_vol, tab_vp, tab_cbbc = st.tabs(
        ["⚡ 日內波幅 (Volatility)", "📊 成交分佈 (Volume Profile)", "🐻 牛熊重貨區 (CBBC)"])

    is_vip = st.session_state.get("authentication_status", False)

    with tab_vol:
        st.subheader("Intraday Volatility Analysis")
        html_content = utils.load_html_file(os.path.join("MarketDashboard", "Intraday_Volatility.html"))

        if "File not found" not in html_content:
            if is_vip:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Recent Volatility Only)")
                components.html(html_content, height=600, scrolling=False)
                utils.check_access_or_show_teaser("Volatility Full Access", description="Unlock real-time volatility levels.")
        else:
            st.warning("⚠️ Report not found")

    with tab_vp:
        st.subheader("Volume Profile Analysis")
        if utils.check_access_or_show_teaser("成交分佈 Volume Profile"):
            html_content, filename = utils.get_latest_file_content("VP", "volume_profile_dashboard_*.html")
            if html_content:
                components.html(html_content, height=1000, scrolling=True)
            else:
                st.warning("⚠️ No VP reports found")

    with tab_cbbc:
        st.subheader("HSI CBBC Heavy Zone")
        if utils.check_access_or_show_teaser("牛熊重貨區 CBBC Ladder", description="客觀呈現市場重貨區分佈"):
            html_content = utils.load_html_file(os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html"))
            if "File not found" not in html_content:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Report not found")

elif target_page == "個人持倉":
    st.title("💼 Paris Picks (內部量化倉位紀錄)")
    path = "Trade"
    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])
    is_vip = st.session_state.get("authentication_status", False)

    with tab1:
        html_content, filename = utils.get_latest_file_content(path, "trade_record_*.html")
        if html_content:
            st.caption(f"📅 Report: {filename}")
            if is_vip:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Showing Top Holdings Only)")
                utils.check_access_or_show_teaser("Stock Journal Full Access", description="Unlock full trade journal.")
                components.html(html_content, height=800, scrolling=False)
        else:
            st.warning("⚠️ Report not found.")
    with tab2:
        if utils.check_access_or_show_teaser("Option Desk"):
            html_content, filename = utils.get_latest_file_content(path, "option_record_*.html")
            if html_content:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Report not found.")

elif target_page == "EA 介紹":
    st.title("🤖 MT5 Expert Advisor (EA)")
    html_content = utils.load_html_file(os.path.join("MT5EA", "ea_marketing.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.warning("⚠️ Content not found.")

# 交易學院：嚴格鎖定內容，未解鎖前只會顯示標題與大鎖頭提示
elif target_page == "交易學院":
    st.title("🎓 交易學院 (Academy)")
    if utils.check_access_or_show_teaser("交易學院", description="此為會員專屬內容，解鎖進階量化策略文獻。"):
        education_page.render_education_page(utils.check_access_or_show_teaser, utils.load_markdown_with_images)

elif target_page == "Legal":
    st.title("📜 法律條款及細則 (Legal & Terms)")
    file_path = os.path.join("Legal", "paris_terms.html")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_string = f.read()
        # 加入 components.html 渲染，高度設為 1200 讓內容能充分顯示，支援滾動
        components.html(html_string, height=1200, scrolling=True)
    except FileNotFoundError:
        st.error(f"⚠️ 找不到檔案 {file_path}。請確認檔案已放置於 Legal 資料夾內。")
    except Exception as e:
        st.error(f"⚠️ 讀取條款檔案時發生錯誤: {e}")

elif target_page == "CFD開戶優惠":
    st.title("🔗 Trading Resources")
    html_content = utils.load_html_file(os.path.join("Resources", "external_links.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.warning("⚠️ Content not found.")

elif target_page == "升級會員":
    st.title("💎 升級機構級數據")
    html_content = utils.load_html_file(os.path.join("Community", "community_promo.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.error("⚠️ Content not found")

# Footer 
st.markdown("""
<div class="custom-footer" style="border-top: 1px solid #374151; padding-top: 20px; margin-top: 40px; text-align: center;">
    <p style="color: #D1D5DB; font-weight: 600; margin-bottom: 5px;">O</p>
    <p style="color: #9CA3AF; font-size: 0.8em; margin-bottom: 5px;">All data and tools provided are for educational and quantitative research purposes only and do not constitute financial or investment advice.</p>
    <p>© 2026 Paris Trader. All rights reserved.<br><span style="font-size: 0.75rem; color: #6B7280;">Strictly no investment advisory services provided.</span></p>
    <p><a href="https://t.me/Ho777ggg" target="_blank" style="color: #60A5FA;">@ParisTrader Admin</a> | <a href="?page=Legal" target="_self" style="color: #6B7280; text-decoration: none;">Legal</a></p>
</div>
""", unsafe_allow_html=True)
