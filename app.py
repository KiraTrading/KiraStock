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
    page_title="Kira Trader - Smart Money Tracker | 散戶救星",
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


# 翻譯字典
translations = {
    "zh": {
        "slogan_title": "不再做韭菜 | 直接跟蹤大戶聰明錢",
        "slogan_sub": "揭秘華爾街底牌：期權異動 | 莊家成本 | 趨勢預判",
        "intro_text": "傳統圖表只告訴你「過去」發生什麼，我們的數據告訴你<b>「未來」大戶想去哪裡</b>。<br>Stop guessing. See the cards the dealer is holding.",
        "tutorial": "📺 網站使用教學",
        "weekly_btn": "📊 偷看本週大戶部署 (Weekly Analysis)",
        "week_ahead": "🧠 Week Ahead Strategy",
        "expander_title": "📖 點擊展開：大市前瞻與劇本",
        "contact_btn": "聯絡我 Contact Me",
        "vip_promo_title": "👑 解鎖大戶底牌",
        "vip_promo_desc": "偷看機構持倉 (Insider)<br>& 聰明錢流向 (Flow)",
        "vip_join": "🚀 立即加入 (Join Now)",
        "nav_title": "導航選單",
        "settings": "語言設定 / Settings",
        "profile_text": """我將投資銀行的機構級數據平民化，幫你避開散戶陷阱。
<br><br>
<b>核心武器 (My Edge):</b><br>
• 🐳 <b>Stock Hunter:</b> 捕捉機構建倉股<br>
• ⚡ <b>Futures Scalping:</b> NQ/HSI/黃金短線<br>
• 🎯 <b>Option Flow:</b> 異動期權狙擊<br>"""
    },
    "en": {
        "slogan_title": "Stop Retail Trading | Follow Smart Money",
        "slogan_sub": "Reveal Wall St Cards: Option Flow | Dealer Cost | Trend Prediction",
        "intro_text": "Traditional charts only show you the 'Past'. Our data tells you <b>where Smart Money is going in the 'Future'</b>.<br>Stop guessing. See the cards the dealer is holding.",
        "tutorial": "📺 Platform Tutorial",
        "weekly_btn": "📊 Weekly Institutional Analysis",
        "week_ahead": "🧠 Week Ahead Strategy",
        "expander_title": "📖 Click to Expand: Market Outlook",
        "contact_btn": "Contact Me",
        "vip_promo_title": "👑 Unlock Institutional Data",
        "vip_promo_desc": "Insider Holdings<br>& Smart Money Flow",
        "vip_join": "🚀 Join Now",
        "nav_title": "Navigation",
        "settings": "Settings",
        "profile_text": """Democratizing institutional data to help you avoid retail traps.
<br><br>
<b>My Edge:</b><br>
• 🐳 <b>Stock Hunter:</b> Track Institutional Builds<br>
• ⚡ <b>Futures Scalping:</b> NQ/HSI/Gold Scalping<br>
• 🎯 <b>Option Flow:</b> Sniper Unusual Activity<br>"""
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

    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #374151; margin-bottom: 20px;'>
        <h2 style='color: #F3F4F6; margin:0; letter-spacing: 1px; font-weight: 700;'>KiraTrader</h2>
        <p style='color: #9CA3AF; font-size: 0.85em; margin-top:5px;'>Follow The Smart Money</p>
    </div>
    """, unsafe_allow_html=True)

    nav_map_zh = {
        # "升級會員": "💎 升級會員 (VIP)",
        # "CFD開戶優惠": "🎁 開戶專屬優惠",
        "試用指標": "🔥 試用指標教學",
        "首頁": "首頁",
        "股票研究": "股票研究",
        # "宏觀專欄": "宏觀專欄",
        "大市雷達": "大市雷達",
        "實戰持倉": "實戰持倉",
        "美股獵人": "美股獵人",
        "期權佈局": "期權佈局",
        "期貨牛熊": "期貨牛熊",
        "自動鈔能力": "自動鈔能力",
        "交易學院": "交易學院"
    }

    nav_map_en = {
        # "升級會員": "💎 Go VIP",
        # "CFD開戶優惠": "🎁 Broker Offer",
        "試用指標": "🔥 Trial Indicator",
        "首頁": "Home",
        "股票研究": "Daily Recap",
        # "宏觀專欄": "Research",
        "大市雷達": "Market Radar",
        "實戰持倉": "Portfolio",
        "美股獵人": "Stock Hunter",
        "期權佈局": "Option Flow",
        "期貨牛熊": "Futures & Vol",
        "自動鈔能力": "Auto-Trading (EA)",
        "交易學院": "Academy"
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

    # 2. 渲染 Option Menu (已移除 gem, gift, globe 圖標以符合選單數量)
    selected_display = option_menu(
        menu_title=t("nav_title"),
        options=display_options,
        icons=["lightning-charge", "house", "journal-bookmark", "activity", "briefcase",
               "crosshair", "layers", "graph-up-arrow", "robot", "mortarboard"],
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

    # 3. 反向查找：將 Menu 顯示的文字 (中/英) 轉回系統內部的 Key (中文)
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
    if selected_nav == "自動鈔能力":
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
locked_pages = []
if target_page in locked_pages:
    if not utils.check_access_or_show_teaser(target_page):
        st.stop()

# ==========================================
# 4. Content Routing
# ==========================================

if target_page == "SecretAdmin":
    admin_page.render_admin_console()

elif target_page == "首頁":
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

        # =========== 實戰成績與會員反饋 (Social Proof) 區塊 開始 ===========
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔥 實戰成績與會員反饋")
        st.caption("真實數據說話，見證機構級數據與資金流的威力")

        # 【防呆機制】：這裡面的 HTML 程式碼完全沒有任何縮排，確保不會觸發 Streamlit Markdown Code Block 解析錯誤
        social_proof_html = """
<style>
.social-proof-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 15px; margin-bottom: 20px; }
.sp-card { background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; overflow: hidden; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); position: relative; }
.sp-card:hover { transform: translateY(-8px); border-color: #F59E0B; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5), 0 0 15px rgba(245, 158, 11, 0.15); }
.sp-img-container { width: 100%; height: 180px; background-color: #0f172a; overflow: hidden; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.sp-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.sp-card:hover .sp-img { transform: scale(1.08); }
.sp-content { padding: 16px; }
.sp-tag { font-size: 0.75rem; background: rgba(37, 99, 235, 0.2); color: #60A5FA; padding: 4px 8px; border-radius: 4px; font-weight: 700; display: inline-block; margin-bottom: 10px; letter-spacing: 0.5px; }
.sp-tag.gold { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }
.sp-text { color: #cbd5e1; font-size: 0.95rem; font-weight: 500; line-height: 1.5; margin: 0; min-height: 42px; }
.sp-author { margin-top: 15px; font-size: 0.8rem; color: #64748b; display: flex; align-items: center; gap: 5px; }
.sp-disclaimer { font-size: 0.75rem; color: #475569; text-align: right; margin-top: 10px; font-style: italic; }
</style>
<div class="social-proof-grid">
<div class="sp-card">
<div class="sp-img-container">
<img src="https://raw.githubusercontent.com/ParisTrader/paristrader-terminal/main/Community/comm_pnl1.jpg" class="sp-img" alt="Member PnL 1" onerror="this.src='https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=500&auto=format&fit=crop';">
</div>
<div class="sp-content">
<div class="sp-tag">📊 波段捕捉</div>
<p class="sp-text">「執行力與紀律的展現 - 運用大市雷達成功捕捉波段起漲點。」</p>
<div class="sp-author">👤 VIP 群組實戰回單</div>
</div>
</div>
<div class="sp-card">
<div class="sp-img-container" style="background: #0f172a; padding: 20px; display:flex; flex-direction: column; justify-content:center;">
<div style="background: rgba(255,255,255,0.05); padding: 12px 15px; border-radius: 12px; border-left: 3px solid #F59E0B; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
<div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 5px; font-weight:bold;">Member-老登</div>
<div style="font-size: 0.9rem; color: #f8fafc; line-height: 1.4;">這速度太誇張了... 剛才那波油價拉升直接抓到。🚀</div>
<div style="font-size: 0.7rem; color: #64748b; text-align: right; margin-top: 5px;">10:45 AM</div>
</div>
</div>
<div class="sp-content">
<div class="sp-tag gold">⚡ 情報領先</div>
<p class="sp-text">「比散戶新聞快最少 5 分鐘！即時捕捉機構 Block Trade 佈局和突發新聞。」</p>
<div class="sp-author">💬 內部交易員交流群</div>
</div>
</div>
<div class="sp-card">
<div class="sp-img-container">
<img src="https://raw.githubusercontent.com/ParisTrader/paristrader-terminal/main/Community/comm_pnl2.jpg" class="sp-img" alt="Member PnL 2" onerror="this.src='https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=500&auto=format&fit=crop';">
</div>
<div class="sp-content">
<div class="sp-tag">🎯 數據反轉</div>
<p class="sp-text">「群組即時提示驗證 - 把握非農數據後的反轉，避開假突破。」</p>
<div class="sp-author">👤 VIP 群組實戰回單</div>
</div>
</div>
</div>
<div class="sp-disclaimer">* 過去績效不代表未來收益，交易皆具風險，請自行評估。</div>
"""
        st.markdown(social_proof_html, unsafe_allow_html=True)
        st.markdown("---")

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
<h3 style="margin-top:10px; color:#F3F4F6;">Kira Trader</h3>
<p style="color: #60A5FA; font-weight: bold; font-size: 0.9em;">Ex-Ibank Derivative Trader</p>
<hr style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);">
<div style="text-align: left; font-size: 0.9em; line-height: 1.6; color: #cbd5e1;">
{t('profile_text')}
</div>
<a href="https://t.me/kira_stocknote" target="_blank">
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

elif target_page == "股票研究":
    st.title("📈 股票研究 (Daily Recap)")
    if utils.check_access_or_show_teaser("股票研究", description="此為會員專屬內容，解鎖深度每日覆盤與個股解析。"):
        recap_page.render_recap_page(utils.load_markdown_with_images)

elif target_page == "宏觀專欄":
    # --- Custom CSS: Mobile Optimized & Clean Archive ---
    st.markdown("""
    <style>
        /* 1. Global Card Style - 縮小 Padding */
        .ig-card-container {
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px; /* 稍微減小圓角 */
            padding: 15px; /* 從 20px 減小到 15px */
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        /* 2. Featured Card (Top) */
        .featured-header {
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px; /* 減小底部間距 */
            margin-bottom: 10px;
        }
        .featured-tag {
            background-color: #2563EB;
            color: white;
            padding: 3px 10px; /* 縮小 Tag */
            border-radius: 15px;
            font-size: 0.75rem; /* 縮小字體 */
            font-weight: 600;
            text-transform: uppercase;
        }
        .featured-title {
            color: #F8FAFC; 
            font-size: 1.25rem; /* 從 1.8rem 改為 1.25rem (適合手機) */
            font-weight: 700; 
            margin-top: 8px;
            line-height: 1.4;
        }

        /* 手機版特別優化 (螢幕寬度小於 600px) */
        @media (max-width: 600px) {
            .featured-title { font-size: 1.1rem; } /* 手機上標題更小 */
            .ig-card-container { padding: 12px; }  /* 手機上內距更緊湊 */
        }

        /* 3. Archive Expander Styling */
        .streamlit-expanderHeader {
            background-color: #1e293b !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: #E2E8F0 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important; /* 列表標題字體縮小 */
            transition: all 0.2s;
            padding: 10px !important; /* 縮小列表高度 */
        }
        .streamlit-expanderHeader:hover {
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
        }
        .streamlit-expanderContent {
            background-color: #0f172a !important;
            border-radius: 0 0 8px 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-top: none;
            padding: 15px !important;
        }
        .streamlit-expanderHeader p {
            font-size: 0.95rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🦅 知世界事，賺世界錢")
    st.caption("洞察先機 (Kira Trader Prediction)")

    files = sorted(glob.glob(os.path.join("DailyInsights", "*.md")), reverse=True)

    if not files:
        st.info("No insights published yet.")
    else:
        # --- Parser Function ---
        def parse_insight(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                raw = f.read()
            lines = raw.split('\n')

            meta = {
                "title": lines[0].replace('#', '').replace('*', '').strip(),
                "date": "Recent",
                "tag": "MEMO",
                "sentiment": "",
            }

            body_start = 1
            for idx, line in enumerate(lines):
                line = line.strip()
                if "**Date:**" in line: meta["date"] = line.replace("**Date:**", "").strip()
                if "**Tag:**" in line:
                    meta["tag"] = line.replace("**Tag:**", "").strip()
                elif line.startswith("Tag:"):
                    meta["tag"] = line.replace("Tag:", "").strip()
                if "**Sentiment:**" in line: meta["sentiment"] = line.replace("**Sentiment:**", "").strip()
                if idx > 0 and idx < 8 and line == "":
                    body_start = idx + 1

            full_body = "\n".join(lines[body_start:]).strip()
            return meta, full_body


        # ==========================================
        # 1. FEATURED POST (置頂)
        # ==========================================
        latest_file = files[0]
        meta, full_body = parse_insight(latest_file)

        with st.container():
            icon = "🦅"
            if "Bullish" in meta['sentiment']:
                icon = "🐂"
            elif "Bearish" in meta['sentiment']:
                icon = "🐻"
            elif "Warning" in meta['sentiment']:
                icon = "⚠️"

            # 🔥🔥🔥 MODIFIED HEADER: 小字體 & 緊湊排版 🔥🔥🔥
            header_html = f"""
            <div class="ig-card-container">
                <div class="featured-header">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="featured-tag">{meta['tag']}</span>
                        <span style="
                            color: #94a3b8; /* 顏色改淡一點，不搶眼 */
                            font-size: 0.85rem; /* 從 1.3rem 改為 0.85rem */
                            font-weight: 600; 
                        ">
                            🗓️ {meta['date']}
                        </span>
                    </div>
                    <div class="featured-title">{icon} {meta['title']}</div>
                    <div style="color:#60A5FA; font-weight:bold; margin-top:5px; font-size: 0.85rem;">{meta['sentiment']}</div>
                </div>
            """
            st.markdown(header_html, unsafe_allow_html=True)
            st.markdown(full_body)

            footer_html = """
                <div style="margin-top:15px; padding-top:10px; border-top:1px dashed #334155; text-align:right; font-size:0.75rem; color:#64748b;">
                    @KiraTrader | Institutional Data
                </div>
            </div>
            """
            st.markdown(footer_html, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📚 過往分析")

        # ==========================================
        # 2. ARCHIVE GRID (歸檔)
        # ==========================================
        if len(files) > 1:
            cols = st.columns(2)
            for i, file_path in enumerate(files[1:]):
                meta, full_body = parse_insight(file_path)
                col = cols[i % 2]
                with col:
                    emoji_map = {"Bullish": "🟢", "Bearish": "🔴", "Neutral": "⚪", "Warning": "⚠️"}
                    sent_key = meta['sentiment'].split('(')[0].strip()
                    status_icon = emoji_map.get(sent_key, "📄")

                    # 列表標題也縮小日期顯示
                    card_title = f"{status_icon} {meta['title']} <span style='font-size:0.8em; color:#9ca3af'>({meta['date']})</span>"

                    expander_label = f"{status_icon} {meta['title']} | {meta['date']}"

                    with st.expander(expander_label, expanded=False):
                        st.caption(f"📌 {meta['tag']} | {meta['sentiment']}")
                        st.markdown(full_body)


elif target_page == "試用指標":
    st.title("🔥 獨家指標試用與教學")
    st.caption("透過量化指標，捕捉最佳進出場時機")

    # 讀取 HTML 檔案
    html_content = utils.load_html_file(os.path.join("Community", "indicator.html"))

    if "File not found" not in html_content:
        # 👇 就是改這一行！把 st.markdown 換成 st.html
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
                utils.check_access_or_show_teaser("Risk Meter Full Access",
                                                  description="Unlock full implied volatility data.")
        else:
            st.warning("⚠️ No risk reports found.")

    with tab_breadth:
        st.subheader("Market Breadth")
        html_content, _ = utils.get_latest_file_content(os.path.join("MarketDashboard", "MarketBreadth"),
                                                        "market_breadth_*.html")

        if html_content:
            if is_vip:
                components.html(html_content, height=2200, scrolling=True)
            else:
                st.info("👀 Preview Mode (Showing Partial Data)")
                components.html(html_content, height=800, scrolling=False)
                utils.check_access_or_show_teaser("Market Breadth Full Access",
                                                  description="Unlock full breadth indicators.")
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
                utils.check_access_or_show_teaser("CFTC Report Full Access",
                                                  description="See all institutional positioning.")
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
                utils.check_access_or_show_teaser("Volatility Full Access",
                                                  description="Unlock real-time volatility levels.")
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
        if utils.check_access_or_show_teaser("牛熊重貨區 CBBC Ladder", description="看穿大戶屠牛/殺熊目標價"):
            html_content = utils.load_html_file(os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html"))
            if "File not found" not in html_content:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Report not found")

elif target_page == "實戰持倉":
    st.title("💼 Kira Picks (百萬美金實戰倉位)")
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
                components.html(html_content, height=800, scrolling=False)
                utils.check_access_or_show_teaser("Stock Journal Full Access", description="Unlock full trade journal.")
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
        st.html(html_content) # ✅ 讓系統自動適應高度
    else:
        st.warning("⚠️ Content not found.")

elif target_page == "交易學院":
    st.title("🎓 交易學院 (Academy)")
    if utils.check_access_or_show_teaser("交易學院", description="此為會員專屬內容，解鎖進階量化策略與教學。"):
        education_page.render_education_page(utils.check_access_or_show_teaser, utils.load_markdown_with_images)

elif target_page == "Legal":
    st.title("📜 Legal & Compliance")
    t1, t2, t3 = st.tabs(["Disclaimer", "Privacy", "Terms"])
    with t1:
        st.html(utils.load_html_file(os.path.join("Legal", "disclaimer.html")))
    with t2:
        st.html(utils.load_html_file(os.path.join("Legal", "privacy.html")))
    with t3:
        st.html(utils.load_html_file(os.path.join("Legal", "terms.html")))

elif target_page == "CFD開戶優惠":
    st.title("🔗 Trading Resources")
    html_content = utils.load_html_file(os.path.join("Resources", "external_links.html"))
    if "File not found" not in html_content:
        st.html(html_content) # ✅ 讓系統自動適應高度
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
<div class="custom-footer">
    <p>© 2026 Kira Trader. All rights reserved.<br><span style="font-size: 0.75rem; color: #6B7280;">Not financial advice.</span></p>
    <p><a href="https://t.me/kira_stocknote" target="_blank">@kira_stocknote on TG</a> | <a href="?page=Legal" target="_self" style="color: #6B7280; text-decoration: none;">Legal</a></p>
</div>
""", unsafe_allow_html=True)