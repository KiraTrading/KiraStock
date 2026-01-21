import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import sys
import glob
import time

# Add Trade folder path
sys.path.append('Trade')
try:
    from Trade import trade_app
except ImportError:
    pass


# ==========================================
# 🔐 Security Login System
# ==========================================


def check_access_or_show_teaser(page_name, teaser_image_url=None, description=None):
    """
    如果已登入 -> 返回 True
    如果未登入 -> 顯示該功能的銷售文案 (Teaser) + 登入/購買按鈕 -> 返回 False
    """
    if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
        return True

    # --- 未登入狀態下的 Teaser 介面 ---
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px; background: rgba(17, 24, 39, 0.6); border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3);">
        <h2 style="color: #60a5fa;">🔒 Locked Feature: {page_name}</h2>
        <p style="font-size: 1.2em; color: #e2e8f0; max-width: 600px; margin: 0 auto;">
            {description if description else "This institutional-grade tool is reserved for VIP members."}
        </p>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 30px 0;">
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔑 Member Login")
        with st.form(f"login_form_{page_name}"):
            email_input = st.text_input("Email", key=f"email_{page_name}")
            password_input = st.text_input("Password", type="password", key=f"pw_{page_name}")
            submit = st.form_submit_button("Login to Access", type="secondary", use_container_width=True)

            if submit:
                # 這裡填入你的驗證邏輯
                try:
                    valid_emails = st.secrets["allowed_users"]["emails"]
                    correct_password = st.secrets["access_password"]
                    if email_input in valid_emails and password_input == correct_password:
                        st.session_state["authentication_status"] = True
                        st.session_state["user_email"] = email_input
                        st.success("Access Granted.")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid Credentials")
                except:
                    st.error("System Config Error")

    with c2:
        st.markdown("#### 🚀 Not a Member?")
        st.markdown("""
        <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #2563EB;">
            <p style="font-size: 0.9em; margin-bottom: 15px;">
                Unlock this tool and get full access to Stock DNA, Option Flows, and my personal trade portfolio.
            </p>
            <a href="https://parisprogram.uk/zh/member-dash/plans/" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: #fbbf24; color: black; border: none; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                    Get VIP Access Now
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 如果有預覽圖，可以放在下面 (Optional)
    if teaser_image_url:
        st.image(teaser_image_url, caption="Preview of Tool (Blur)", use_column_width=True)

    return False


# --- Main Program Logic ---
# Uncomment to enable login
# if not login_system():
#    st.stop()

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ParisTrader - Quant Trading & Market Analysis | 2026香港投資銀行學習",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. Custom CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;700&display=swap');

    .stApp {
        background: transparent !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', 'Microsoft JhengHei', sans-serif;
        color: #e2e8f0;
    }

    @media (min-width: 768.1px) {
        header { visibility: hidden !important; }
        [data-testid="stSidebarCollapseButton"] { display: none !important; }
        section[data-testid="stSidebar"] button { display: none !important; }
        [data-testid="stToolbar"], [data-testid="stHeaderActionElements"] { visibility: hidden !important; display: none !important; }
        #MainMenu { visibility: hidden !important; display: none !important; }
    }

    @media (max-width: 768px) {
        header { visibility: visible !important; background: transparent !important; }
        header button[kind="header"] {
            background-color: rgba(17, 24, 39, 0.6) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
        }
        .block-container {
            padding-top: 3rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.2rem !important; }
    }

    footer { visibility: hidden !important; display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }

    .fixed-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
        z-index: -1; 
        background-color: #020617;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
        -webkit-mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
    }

    .fixed-blobs {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
        z-index: -1;
        background: 
            radial-gradient(circle at 10% 10%, rgba(79, 70, 229, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 20%, rgba(14, 165, 233, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 30% 90%, rgba(16, 185, 129, 0.1) 0%, transparent 40%);
        filter: blur(60px); pointer-events: none;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827; 
        border-right: 1px solid #374151;
        z-index: 999999 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #F3F4F6 !important;
    }

    .metric-card {
        background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;
        padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .metric-card h4 { color: #94a3b8; font-size: 0.9em; text-transform: uppercase; margin: 0; }
    .metric-card h2 { color: #f8fafc; margin: 5px 0; font-size: 1.8em; }

    .profile-card {
        background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;
        padding: 25px; text-align: center;
    }

    .custom-footer {
        margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; color: #94a3b8; font-size: 0.8rem;
    }
    .custom-footer a { color: #60a5fa; text-decoration: none; margin: 0 10px; }
    .custom-footer a:hover { text-decoration: underline; }

    .legal-text {
        font-size: 0.95rem; line-height: 1.7; color: #e2e8f0; text-align: justify;
        background: rgba(255, 255, 255, 0.03); padding: 30px;
        border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .legal-text h3 { color: #f8fafc !important; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px; }
    .legal-text h4 { color: #e2e8f0 !important; margin-top: 20px; font-weight: bold; }
    .legal-text strong { color: #f8fafc !important; }
</style>

<div class="fixed-bg"></div>
<div class="fixed-blobs"></div>
""", unsafe_allow_html=True)


# ==========================================
# 3. Helper Functions
# ==========================================
import base64
import re

def load_markdown_with_images(file_path):
    """
    讀取 Markdown 檔案，並自動將本地圖片路徑轉換為 Base64 編碼。
    修復了 PC 版圖片過大導致版面跑位的問題。
    """
    if not os.path.exists(file_path):
        return f"<div style='color:red'>⚠️ File not found: {file_path}</div>"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正則表達式：尋找 ![alt](path) 格式的圖片語法
    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    def replace_image_link(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # 檢查是否為本地路徑 (不包含 http 開頭)
        if not image_path.startswith('http') and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode()
                    ext = image_path.split('.')[-1].lower()
                    mime_type = f"image/{ext}"
                    if ext == 'svg': mime_type = "image/svg+xml"

                    # [關鍵修改]
                    # 1. 外層 div 加入 text-align: center 讓圖片在 PC 上置中
                    # 2. img 標籤改用 max-width: 100% (不強制拉伸，只限制最大寬度)
                    # 3. 加入 max-height: 600px 限制 PC 上圖片不要高過 600px，避免佔滿畫面
                    # 4. width: auto; height: auto 保持圖片原始比例
                    return (
                        f'<div style="width:100%; text-align: center; margin: 20px 0;">'
                        f'<img src="data:{mime_type};base64,{b64_string}" alt="{alt_text}" '
                        f'style="max-width: 100%; max-height: 800px; width: auto; height: auto; '
                        f'border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">'
                        f'</div>'
                    )
            except Exception as e:
                return f"⚠️ Image Load Error: {str(e)}"

        return match.group(0)

    # 執行替換
    enhanced_content = image_pattern.sub(replace_image_link, content)
    return enhanced_content
def load_weekly_analysis():
    file_path = os.path.join("WeeklyContent", "latest_analysis.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "⚠️ Weekly analysis not uploaded yet (File not found: WeeklyContent/latest_analysis.md)"


def load_html_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return f"<div style='padding:20px; color:red;'>⚠️ File not found: {file_path}</div>"


import os
import streamlit.components.v1 as components


def load_stock_dna_with_injection():
    # 1. Get absolute paths to ensure it works from any directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "FamaFrench", "index.html")
    csv_factor_path = os.path.join(current_dir, "FamaFrench", "stock_factor_data.csv")
    csv_returns_path = os.path.join(current_dir, "FamaFrench", "stock_returns_data.csv")

    if not os.path.exists(html_path):
        return f"<div style='color:red'>HTML not found: {html_path}</div>"

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # ---------------------------------------------------------
    # 1. Inject Factor Data (Your original logic)
    # ---------------------------------------------------------
    if os.path.exists(csv_factor_path):
        with open(csv_factor_path, 'r', encoding='utf-8') as f:
            csv_data = f.read()
            # Clean up backticks just in case
            csv_data = csv_data.replace('`', '')

        # JS to inject: Create variable -> Parse variable -> Disable download
        injection_js = f"""
        var csvData = `{csv_data}`;
        Papa.parse(csvData, {{
            download: false, 
        """

        target_str = 'Papa.parse("stock_factor_data.csv", {'
        if target_str in html_content:
            html_content = html_content.replace(target_str, injection_js)

    # ---------------------------------------------------------
    # 2. Inject Returns Data (The NEW addition)
    # ---------------------------------------------------------
    if os.path.exists(csv_returns_path):
        with open(csv_returns_path, 'r', encoding='utf-8') as f:
            returns_data = f.read()
            returns_data = returns_data.replace('`', '')

        # JS to inject: Use a DIFFERENT variable name (returnsCSVData)
        injection_js_ret = f"""
        var returnsCSVData = `{returns_data}`;
        Papa.parse(returnsCSVData, {{
            download: false, 
        """

        target_str_ret = 'Papa.parse("stock_returns_data.csv", {'
        if target_str_ret in html_content:
            html_content = html_content.replace(target_str_ret, injection_js_ret)

    # ---------------------------------------------------------
    # 3. Global Cleanup
    # ---------------------------------------------------------
    # Since we injected 'download: false', we remove the original 'download: true'
    # to avoid syntax errors or conflicting keys in the JS object.
    html_content = html_content.replace('download: true,', '')

    return html_content


def get_latest_file_content(folder_path, pattern="*.html"):
    if not os.path.exists(folder_path):
        return None, f"Directory not found: {folder_path}"

    search_pattern = os.path.join(folder_path, pattern)
    list_of_files = glob.glob(search_pattern)

    if not list_of_files:
        return None, f"No files found matching {pattern}."

    latest_file = max(list_of_files, key=os.path.getctime)

    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return f.read(), os.path.basename(latest_file)
    except Exception as e:
        return None, str(e)


# ==========================================
# 4. Main App Interface (Mixed Navigation)
# ==========================================

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #374151; margin-bottom: 20px;'>
        <h2 style='color: #F3F4F6; margin:0; letter-spacing: 1px; font-weight: 700;'>ParisTrader</h2>
        <p style='color: #9CA3AF; font-size: 0.85em; margin-top:5px;'>Quant Research</p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # IMPROVED NAVIGATION LOGIC WITH DEEP LINKING
    # -------------------------------------------------------------------------

    # 1. Capture the URL params
    query_params = st.query_params
    url_main_page = query_params.get("page", "Home")  # Default to Home
    url_sub_page = query_params.get("sub", None)  # Capture sub-page

    # Define Main Menu Options
    main_options = [
        "Home", "Market Intelligence", "Stock", "Option",
        "Future", "My Portfolio", "MT5 EA", "Education", "Community", "Resources", "Membership"
    ]

    # Determine default index for Main Menu based on URL
    try:
        main_default_index = main_options.index(url_main_page)
    except ValueError:
        main_default_index = 0

    # 2. Render the Main Sidebar Menu
    selected_nav = option_menu(
        menu_title="Navigation",
        options=main_options,
        icons=[
            "house", "globe", "search", "layers",
            "graph-up-arrow", "briefcase", "robot", "mortarboard", "people-fill", "collection", "gem"
        ],
        menu_icon="compass",
        default_index=main_default_index,  # Sync with URL
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#9CA3AF", "font-size": "15px"},
            "nav-link": {
                "font-size": "15px", "text-align": "left", "margin": "5px",
                "color": "#D1D5DB", "--hover-color": "#1F2937",
            },
            "nav-link-selected": {"background-color": "#2563EB", "color": "#FFFFFF", "font-weight": "600"},
        }
    )

    # 3. Handle Sub-Menus and Update URL for Sub-Pages
    target_page = selected_nav  # Default target is the main selection


    # --- Helper to handle sub-menu logic ---
    def handle_submenu(key_name, options, icons):
        # Calculate default index for sub-menu based on URL 'sub' param
        # Only if the main page matches the current selection
        default_sub_index = 0
        if url_main_page == selected_nav and url_sub_page in options:
            default_sub_index = options.index(url_sub_page)

        selection = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            default_index=default_sub_index,
            styles={
                "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.03)",
                              "border-radius": "10px"},
                "nav-link": {"font-size": "14px", "margin": "3px", "--hover-color": "#374151"},
                "nav-link-selected": {"background-color": "#4B5563"},
            },
            key=key_name  # Unique key is important
        )
        return selection


    # --- Sub-menu Logic ---
    if selected_nav == "Market Intelligence":
        st.caption("MARKET MODULES")
        target_page = handle_submenu(
            "sub_market",
            ["Market Risk", "Market Breadth"],
            ["activity", "bar-chart-line"]
        )

    elif selected_nav == "Stock":
        st.caption("STOCK RESEARCH")
        target_page = handle_submenu(
            "sub_stock",
            ["Earnings", "Stock DNA", "Thematic Basket", "ETF Smart Money", "Insider Trading",
             "Short Squeeze", "Volatility Target", "Industry Sector Heatmap", "S&P 500 Heatmap"],
            ["cash-coin", "radar", "basket", "graph-up-arrow", "people", "lightning-charge", "bullseye",
             "grid-3x3", "fire"]
        )

    elif selected_nav == "Future":
        st.caption("FUTURES & TRENDS")
        target_page = handle_submenu(
            "sub_future",
            ["Volume Profile", "Intraday Volatility", "HSI CBBC Ladder"],
            ["bar-chart-steps", "lightning-charge", "distribute-vertical"]
        )

    elif selected_nav == "Option":
        st.caption("DERIVATIVES ANALYTICS")
        target_page = handle_submenu(
            "sub_option",
            ["US Option", "HK Option"],
            ["currency-dollar", "globe-asia-australia"]
        )

    elif selected_nav == "MT5 EA":
        st.caption("AUTOMATED TRADING")
        target_page = handle_submenu(
            "sub_ea",
            ["EA Introduction"],
            ["robot"]
        )

    # --- 4. Deep Linking: Update URL based on final selection ---
    # Case A: Sidebar item matches target (Home, Education, etc. - No sub-menu)
    if selected_nav == target_page:
        # Check if we need to update URL (avoid infinite rerun loops)
        if url_main_page != selected_nav or url_sub_page is not None:
            st.query_params["page"] = selected_nav
            # Remove 'sub' param if it exists, as this page has no sub-menu
            if "sub" in st.query_params:
                del st.query_params["sub"]
            # time.sleep(0.1) # Optional: sometimes helps with race conditions

    # Case B: Target is a sub-menu item
    else:
        # Check if URL needs update
        if url_main_page != selected_nav or url_sub_page != target_page:
            st.query_params["page"] = selected_nav
            st.query_params["sub"] = target_page

    st.markdown("---")
    # ... (Keep your existing Promo Button code here) ...
    st.markdown("""
            <div style="background: linear-gradient(45deg, #1e3a8a, #3b82f6); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px;">
                <h4 style="color: white; margin:0; font-size: 16px;">🚀 Unlock Pro Data</h4>
                <p style="color: #dbeafe; font-size: 12px; margin: 5px 0;">Access Insider & Option Flows</p>
                <a href="https://parisprogram.uk/" target="_blank" style="text-decoration: none;">
                    <button style="width: 100%; background: #ffffff; color: #2563EB; border: none; padding: 8px; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 5px;">
                        Join VIP Now
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

# Handle Legal from Footer (Special Case)
if url_main_page == "Legal" and selected_nav == "Home":
    target_page = "Legal"

# ==========================================
# 🔒 權限控制與銷售轉化中心
# ==========================================

locked_pages = [
    "My Portfolio",
    "Stock DNA",
    "ETF Smart Money",
    "Insider Trading",
    "Short Squeeze",
    "Volatility Target",
    "US Option",
    "HK Option",
    "Volume Profile",
    "Intraday Volatility",
    "HSI CBBC Ladder"
]

teaser_content = {
    "Stock DNA": "Discover the hidden factors driving stock prices using Fama-French models. Identify high-quality alpha before the market moves.",
    "ETF Smart Money": "Track leveraged ETF flows to spot market reversals instantly. Don't fight the trend, ride the institutional wave.",
    "Insider Trading": "See what CEOs and CFOs are doing with their own money. Real-time cluster buying alerts.",
    "Short Squeeze": "Identify the next GME/AMC before it explodes. High short interest + High borrow cost scanner.",
    "US Option": "Follow the Smart Money. Real-time unusual options activity and gamma exposure levels.",
    "HK Option": "Advanced market scanner for HK derivatives. Visualise the heavy zones and institutional positioning.",
    "My Portfolio": "Access my personal trade journal. See exactly when I enter and exit positions in Stocks and Options.",
    "Volume Profile": "Professional grade Volume Profile analysis to identify key support and resistance levels.",
    "Intraday Volatility": "Monitor real-time volatility spikes to capture intraday momentum.",
    "HSI CBBC Ladder": "Visualise the Bear/Bull contract heavy zones to predict market dealer hedging moves."
}

if target_page in locked_pages:
    desc = teaser_content.get(target_page, "Access professional-grade tools designed for serious traders.")
    if not check_access_or_show_teaser(target_page, description=desc):
        st.stop()

# --- Content Routing (Based on target_page) ---
# [PAGE] HOME
if target_page == "Home":
    col_main, col_profile = st.columns([0.7, 0.3], gap="large")

    with col_main:
        st.markdown("""
        <h1 style='color:white;'>前Ibanker開發-香港首個機構級數據</h1>
        <h3 style='color:#94a3b8;'>美股分析|期權策略|期貨自動交易EA Algo</h3>
        <p style='font-size: 1.1em; color: #64748b;'>
        2026散戶黑科技,你不是只看圖表交易吧?!
        </p>
                <p style='font-size: 1.1em; color: #64748b;'>
        有志加入投行工作,或成為持續盈利交易員必備學習資源平台!
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")

        components.html("""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
          {
          "symbols": [
            {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
            {"proName": "FOREXCOM:NSXUSD", "title": "US 100"},
            {"description": "Gold", "proName": "OANDA:XAUUSD"}
          ],
          "showSymbolLogo": true,
          "colorTheme": "dark",
          "isTransparent": true,
          "displayMode": "adaptive",
          "locale": "en"
          }
          </script>
        </div>
        """, height=100)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📺 網站使用教學")
        st.video("https://www.youtube.com/watch?v=qb3XtEPj8cA")

        st.markdown("<br>", unsafe_allow_html=True)

        st.link_button(
            label="📊 點擊閱讀：下周大市分析 (Weekly Market Analysis)",
            url="https://parisprogram.uk/zh/member/post/RPT-20260117202415071?hash=c2894152df242ddf36604b022a1fbf98fe6b210be085496dba758628c35ebbc4",
            type="primary",
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("🧠 Week Ahead")

        with st.container():
            analysis_content = load_weekly_analysis()
            with st.expander("📖 Click to expand/collapse full analysis", expanded=True):
                st.markdown(analysis_content)

    with col_profile:
        img_path = "static/profile.jpg"
        if not os.path.exists(img_path):
            img_src = "https://ui-avatars.com/api/?name=Paris+Trader&background=0D8ABC&color=fff&size=150"
        else:
            img_src = img_path

        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        if os.path.exists(img_path):
            st.image(img_path, width=120)
        else:
            st.image(img_src, width=120)

        st.markdown("""
            <h3 style="margin-top:10px; color:#F3F4F6;">Paris Trader</h3>
            <p style="color: #9CA3AF; font-size: 0.9em;">Quantitative Analyst | Trader</p>
            <hr style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="text-align: left; font-size: 0.9em; line-height: 1.6; color: #e2e8f0;">
                Focusing on quantitative factor mining and algorithmic trading. Specialized in transforming complex financial models into executable trading strategies. Providing TradingView indicators and backtesting.
                <br><br>
                <b>Main Strategies:</b><br>
                • Multi-Factor Long/Short<br>
                • Future Scapling on HSI/NQ/GC <br>
                • Unusual Options Activity Trading Strategies on U.S. market<br>
            </p>
            <a href="https://t.me/ParisTrader" target="_blank" style="text-decoration: none;">
                <button style="background-color:#2563EB; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; width:100%; margin-top:10px; font-weight:bold;">
                    Contact Me
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

# [PAGE] Market Dashboard
elif target_page == "Market Dashboard":
    st.title("Market Dashboard")
    path = os.path.join("MarketDashboard", "main_auto", "output")
    html_content, filename = get_latest_file_content(path)

    if html_content:
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning("⚠️ No dashboard files found.")
        st.error(f"Error: {filename}")

# [PAGE] Market Risk
elif target_page == "Market Risk":
    st.title("⚠️ Market Implied Risk")
    path = "ImpliedParameters"

    html_content, filename = get_latest_file_content(path)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        fix_style = """
        <style>
            body {
                display: block !important;
                height: auto !important;
                min-height: 100vh;
                padding-top: 50px;
                background-color: #020617 !important;
            }
            .card { margin: 0 auto !important; }
        </style>
        """
        html_content = html_content.replace("<head>", "<head>" + fix_style)
        components.html(html_content, height=2200, scrolling=True)
    else:
        st.warning("⚠️ No risk reports found.")
        st.info("Please ensure `ImpliedParameters/implied_params_*.html` exists.")

# [PAGE] Market Breadth
elif target_page == "Market Breadth":
    st.title("🌊 Market Breadth")
    path = os.path.join("MarketDashboard", "MarketBreadth")
    html_content, filename = get_latest_file_content(path, "market_breadth_*.html")

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=2200, scrolling=True)
    else:
        st.warning("⚠️ Market Breadth report not found.")
        st.info(f"Please ensure `{path}` contains `market_breadth_*.html` files.")

# [PAGE] Industry Sector Heatmap
elif target_page == "Industry Sector Heatmap":
    st.title("🔥 Industry Sector Heatmap")
    st.caption("Daily Return Heatmap (Last 20 Days)")
    path = "MarketDashboard"
    pattern = "sector_etf_heatmap_*.html"
    html_content, filename = get_latest_file_content(path, pattern)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("⚠️ Sector Heatmap not found.")
        st.info(f"Please ensure `{path}/{pattern}` exists.")

# [PAGE] Earnings
elif target_page == "Earnings":
    st.title("📅 Earnings Calendar Analysis")
    path = "Earnings"
    html_content, filename = get_latest_file_content(path)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning("⚠️ No earnings reports found.")
        st.info("Please ensure there is an `Earnings` folder in the root directory containing .html files.")

# [PAGE] Stock DNA
elif target_page == "Stock DNA":
    st.title("🧬 Stock Factor DNA")
    html_content = load_stock_dna_with_injection()
    if html_content and "HTML not found" not in html_content:
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.error("FamaFrench/index.html not found")

# [PAGE] S&P 500 Heatmap
elif target_page == "S&P 500 Heatmap":
    st.title("🔥 S&P 500 Performance Heatmap (YTD)")
    st.caption("Top 50 Best Performers - Daily Returns Tracking")

    # Assumes the script saves the file into the 'Stock' folder.
    # If the script runs in the root, change this to path = "."
    path = "Stock"

    # Look for files matching the new timestamped pattern
    html_content, filename = get_latest_file_content(path, "sp500_clean_heatmap_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        # Height is adjustable depending on how many rows (50 rows needs ~1500px)
        components.html(html_content, height=1600, scrolling=True)
    else:
        st.warning("⚠️ No S&P 500 Heatmap found.")
        st.info(f"Please run `sp500_ytd_ranking.py` and ensure the output is saved in `{path}` folder.")

# [PAGE] Thematic Basket
elif target_page == "Thematic Basket":
    st.title("🧺 Thematic Basket Analysis")
    path = "ThematicBasket"
    html_content, filename = get_latest_file_content(path, "elite_signal_dashboard_*.html")

    if html_content:
        st.caption(f"📅 Strategy Report: {filename}")
        components.html(html_content, height=6000, scrolling=True)
    else:
        st.warning("⚠️ No basket reports found.")
        st.info(f"Checking path: {os.path.abspath(path)}")

# [PAGE] ETF Smart Money
elif target_page == "ETF Smart Money":
    st.title("🚀 ETF Smart Money Tracker")
    st.caption("Tracking Leveraged ETF Relative Volume Spikes")
    path = "xETF"
    html_content, filename = get_latest_file_content(path, "ETF_Smart_Money_Report_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No ETF Smart Money reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `ETF_Smart_Money_Report_*.html` files.")

# [PAGE] Insider Trading
elif target_page == "Insider Trading":
    st.title("🕴️ Insider Trading Activity")
    st.caption("Daily Cluster Buys & Significant Insider Transactions")
    path = "Insider"
    html_content, filename = get_latest_file_content(path, "Insider_Trading_Report_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Insider Trading reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `Insider_Trading_Report_*.html` files.")

# [PAGE] Short Squeeze
elif target_page == "Short Squeeze":
    st.title("⚡ Short Squeeze Scanner")
    st.caption("Retail Hype & High Short Interest Candidates")
    path = "Short_squeeze"
    html_content, filename = get_latest_file_content(path, "Short_squeeze_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Short Squeeze reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `Short_squeeze_*.html` files.")

# [PAGE] Reddit Sentiment
elif target_page == "Reddit Sentiment":
    path = "Rddt"
    html_content, filename = get_latest_file_content(path, "reddit_scanner_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Reddit reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `reddit_scanner_*.html` files.")

# [PAGE] Volatility Target
elif target_page == "Volatility Target":
    st.title("📉 Volatility Target Strategy")
    path = "VolTarget"
    html_content, filename = get_latest_file_content(path, "vol_tool_*.html")

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=1500, scrolling=True)
    else:
        st.warning("⚠️ Volatility Tool not found.")
        st.info("Please ensure `vol_tool_*.html` exists in the `VolTarget` folder.")

# [PAGE] US Option
elif target_page == "US Option":
    st.title("🇺🇸 US Option Strike Analysis")
    st.caption("Tracking Unusual Options Activity & Gamma Levels")
    path = "Option"
    search_pattern = "option_strike_analysis_*.html"
    html_content, filename = get_latest_file_content(path, search_pattern)

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No US Option reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `{search_pattern}` files.")

# [PAGE] HK Option
elif target_page == "HK Option":
    st.title("🇭🇰 HK Option Market Analysis")
    st.caption("Market Scanner, Stock Ranking & Heatmaps")
    path = "Option"
    search_pattern = "HK_Option_Market_Analysis_v6_*.html"
    html_content, filename = get_latest_file_content(path, search_pattern)

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No HK Option reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `{search_pattern}` files.")

# [PAGE] Volume Profile
elif target_page == "Volume Profile":
    st.title("📊 Volume Profile Analysis")
    path = "VP"
    html_content, filename = get_latest_file_content(path)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.warning("⚠️ 尚未部署 Volume Profile 模組 (VP 資料夾為空)")

# [PAGE] Future -> Intraday Volatility
elif target_page == "Intraday Volatility":
    st.title("⚡ Intraday Volatility Analysis")
    html_path = os.path.join("MarketDashboard", "Intraday_Volatility.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("⚠️ 找不到 Intraday Volatility 報告")
        st.info(f"請確認檔案 `{html_path}` 是否存在。")

# [PAGE] Future -> HSI CBBC Ladder
elif target_page == "HSI CBBC Ladder":
    st.title("🐻 HSI CBBC Heavy Zone (牛熊重貨區)")
    html_path = os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("⚠️ 尚未生成牛熊證分佈報告")
        st.info(f"請確認檔案 `{html_path}` 是否存在。")

# [PAGE] My Portfolio
elif target_page == "My Portfolio":
    st.title("💼 Paris Picks")
    path = "Trade"

    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])

    with tab1:
        html_content, filename = get_latest_file_content(path, "trade_record_*.html")
        if html_content:
            st.caption(f"📅 Stock Report: {filename}")
            components.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Trade Record HTML not found.")
            st.info("Please verify that the GitHub Action has run successfully.")

    with tab2:
        html_content_opt, filename_opt = get_latest_file_content(path, "option_record_*.html")
        if html_content_opt:
            st.caption(f"📅 Option Report: {filename_opt}")
            components.html(html_content_opt, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Option Record HTML not found.")
            st.info("Please verify `option_record_*.html` exists in `Trade` folder.")

# [PAGE] MT5 EA - Introduction
elif target_page == "EA Introduction":
    st.title("🤖 MT5 Expert Advisor")
    html_path = os.path.join("MT5EA", "ea_marketing.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=3000, scrolling=True)
    else:
        st.warning("⚠️ No marketing content found.")
        st.info("Please ensure `MT5EA/ea_marketing.html` exists.")


# [PAGE] LEGAL
elif target_page == "Legal":
    st.title("📜 Legal & Compliance")
    tab1, tab2, tab3 = st.tabs(["Disclaimer", "Privacy Policy", "Terms of Use"])
    with tab1:
        html = load_html_file(os.path.join("Legal", "disclaimer.html"))
        st.html(html)
    with tab2:
        html = load_html_file(os.path.join("Legal", "privacy.html"))
        st.html(html)
    with tab3:
        html = load_html_file(os.path.join("Legal", "terms.html"))
        st.html(html)

# [PAGE] Resources
elif target_page == "Resources":
    st.title("🔗 Trading Resources")
    html_path = os.path.join("Resources", "external_links.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.warning("⚠️ Resources file not found.")
        st.info(f"Please ensure `{html_path}` exists.")

elif target_page == "Community":
    # 不顯示 Streamlit 預設標題，因為 HTML 裡已經有了

    html_file_path = os.path.join("Community", "community_promo.html")

    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # 使用 components.html 渲染，height 設定高一點以容納整個頁面
            # scrolling=True 讓用戶可以捲動
            components.html(html_content, height=1200, scrolling=True)
    else:
        st.error(f"⚠️ Community page file not found at: {html_file_path}")


# [PAGE] Education Hub
elif target_page == "Education":
    st.title("🎓 Quant Academy")
    st.caption("Institutional Trading Knowledge & Strategies")

    # 1. 定義文章清單
    # 【重要修正】Keys (例如 "stock_dna", "bull_call") 必須唯一，不能重複！
    articles = {
        "stock_dna": {
            "title": "獨家工具：Stock DNA 因子分析儀說明書",
            "file": "1_stock_dna_guide.md",
            "icon": "🧬",
            "desc": "如何使用機構級工具拆解持倉風險與屬性。"
        },
        # --- 期權系列 (Options Play) ---
        "bull_call": {
            "title": "期權教學：Bull Call Spread 實戰詳解",
            "file": "2_bull_call_spread.md",
            "icon": "🐂",  # 使用牛圖標代表 Bull
            "desc": "看對市卻輸錢？學會這個對沖策略，降低成本抗 Theta"
        },
        "naked_long": {
            "title": "期權教學：Naked Long 的時間博弈",
            "file": "3_naked_long_strategy.md",
            "icon": "⏳",  # 使用沙漏代表時間 Theta
            "desc": "為什麼橫盤不要買 Weekly？Python 數據回測告訴你真相。"
        },
        "ea_manual": {
            "title": "MT5 神器：Paris摩打手Assistant",
            "file": "4_mt5_ea_manual.md",
            "icon": "🤖",
            "desc": "告別手動算點數，隱形止損與一鍵反手神器。"
        },
        "gold_excalibur": {
            "title": "MT5 神器：黃金自動現金流馬丁策略",
            "file": "5_paris_gold_excalibur.md",
            "icon": "⚔️",
            "desc": "結合 Fate 趨勢引擎與 ATR 動態網格的機構級黃金策略。"
        },
        "fate_indicator": {
            "title": "MT5 指標：Fate 趨勢判定反轉系統",
            "file": "6_paris_fate_indicator_guide.md",
            "icon": "🧭",
            "desc": "整合波動率與動能的機構級圖表系統，自動繪製 TP/SL。"
        },
        "tv_heatmap": {
            "title": "TradingView 神器：期貨動能熱力圖",
            "file": "7_tv_volume_heatmap.md",
            "icon": "📊",
            "desc": "一眼看穿大戶資金流向，監控全球 18 大資產 Z-Score。"
        },
        "risk_sizing": {
            "title": "交易操作教室：何為波動性<均注>",
            "file": "8_volatility_sizing.md",
            "icon": "⚖️",
            "desc": "贏單常有卻輸在資金管理？學會 ATR 動態注碼，像機構一樣控盤。"
        },
        "risk_monitor_guide": {
            "title": "大市雷達：如何識別見頂/見底信號？",
            "file": "9_risk_dashboard_guide.md",
            "icon": "📟",
            "desc": "學會解讀 VIX, Skew 與 Z-Score，像機構一樣捕捉轉折點。"
        },
    }

    # 準備選單需要的標題列表和圖標列表
    # 我們將使用 "Title" 作為選單顯示的文字，而不是 Key
    options_titles = [data["title"] for data in articles.values()]
    options_icons = [data["icon"] for data in articles.values()]

    # 2. 建立兩欄佈局：左邊是文章列表，右邊是內容閱讀區
    col_list, col_content = st.columns([1, 2.5], gap="large")

    with col_list:
        st.markdown("### 📚 Article List")

        # 【修正邏輯】移除 st.radio，直接使用 option_menu 的回傳值
        selected_title = option_menu(
            menu_title=None,
            options=options_titles,  # 顯示中文標題
            icons=options_icons,  # 顯示對應圖標
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"background-color": "rgba(255,255,255,0.05)", "padding": "10px"},
                "nav-link": {"font-size": "14px", "margin": "5px", "text-align": "left"},
                "nav-link-selected": {"background-color": "#2563EB"},
                "icon": {"font-size": "18px"}
            }
        )

    with col_content:
        # 【反向查找】根據選中的 Title 找回對應的 Article 資料
        # 這是最簡單的寫法，確保選單選什麼，內容就出什麼
        current_article = next((item for item in articles.values() if item["title"] == selected_title), None)

        if current_article:
            file_path = os.path.join("Education", current_article["file"])

            # 顯示漂亮的標題頭
            st.markdown(f"""
            <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #2563EB; margin-bottom: 20px;">
                <h2 style="margin:0; color: white;">{current_article['icon']} {current_article['title']}</h2>
                <p style="margin-top:5px; color: #94a3b8;">{current_article['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

            # 使用 Base64 Loader 讀取內容
            content = load_markdown_with_images(file_path)
            st.markdown(content, unsafe_allow_html=True)

            # CTA
            st.divider()
            st.success("💡 喜歡這篇深度分析？ 加入 VIP 會員解鎖實戰交易數據與工具。")
        else:
            st.error("Error loading article.")

# [PAGE] Membership (Sales Page)
elif target_page == "Membership":
    st.title("💎 Upgrade to Institutional Level")
    st.caption("Stop guessing. Start trading with data used by professionals.")

    st.markdown("""
    <style>
        .plan-card {
            background: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            height: 100%;
            transition: transform 0.3s;
        }
        .plan-card:hover { transform: translateY(-5px); border-color: #3b82f6; }
        .plan-title { font-size: 1.5rem; font-weight: bold; color: #fff; }
        .plan-price { font-size: 2.5rem; font-weight: 700; color: #3b82f6; margin: 20px 0; }
        .plan-price span { font-size: 1rem; color: #9ca3af; font-weight: 400; }
        .feature-list { list-style: none; padding: 0; text-align: left; margin: 20px 0; color: #e2e8f0; }
        .feature-list li { margin-bottom: 12px; display: flex; align-items: center; }
        .feature-list li::before { content: "✓"; color: #10b981; margin-right: 10px; font-weight: bold; }
        .locked-feature { color: #6b7280; text-decoration: line-through; }
        .locked-feature::before { content: "✕"; color: #ef4444; }
        .cta-button {
            background: linear-gradient(90deg, #2563EB, #1d4ed8);
            color: white; padding: 12px 25px; border-radius: 8px;
            text-decoration: none; display: inline-block; width: 100%;
            font-weight: bold; margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="plan-card">
            <div class="plan-title">Basic Visitor</div>
            <div class="plan-price">$0 <span>/ month</span></div>
            <ul class="feature-list">
                <li>Daily Market Risk Dashboard</li>
                <li>Basic Stock Function</li>
                <li>Weekly Market Analysis Blog</li>
                <li class="locked-feature">Investing community access</li>
                <li class="locked-feature">Institutional Factor Model on Stock DNA</li>
                <li class="locked-feature">Smart Money Flow (Options&ETF)</li>
                <li class="locked-feature">Insider Trading Alerts</li>
                <li class="locked-feature">Volume Profile & Directional Tradingview indicators(with tp/sl)</li>
                <li class="locked-feature">Paris Top Picks (My Portfolio on stock & options)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="position: relative;">
            <div style="position: absolute; top: -15px; right: 0; left: 0; margin: auto; width: 120px; background: #fbbf24; color: black; font-weight: bold; text-align: center; padding: 5px; border-radius: 20px; z-index: 10;">MOST POPULAR</div>
            <div class="plan-card" style="border: 2px solid #3b82f6; background: rgba(30, 58, 138, 0.2);">
                <div class="plan-title">VIP Access</div>
                <div class="plan-price">HK$1200 <span>/ month</span></div>
                <p style="color:#94a3b8; font-size:0.9em;">For serious traders aiming for consistent profitability.</p>
                <ul class="feature-list">
                    <li><b>Everything in Basic</b></li>
                    <li>🧬 <b>Stock DNA:</b> Factor-based stock scoring</li>
                    <li>⚡ <b>Option Flow:</b> Track unusual institutional activity</li>
                    <li>🕴️ <b>Insider Trading:</b> Real-time CEO/CFO buys</li>
                    <li>🎯 <b>TradingView Indicators:</b> provide direction(key support/resistant level)</li>
                    <li>📊 <b>Futures Algo:</b> Volume Profile & Heavy Zone</li>
                    <li>💼 <b>My Portfolio:</b> Follow my profitable trade selection</li>
                </ul>
                <a href="https://parisprogram.uk/zh/member-dash/plans/" target="_blank" class="cta-button">UNLOCK NOW 🔓</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💡 Why Upgrade?")
    st.info(
        "The data provided in the VIP section is the same data I used during my time as an Investment Banker. Retail tools show you 'what' happened. Our tools show you 'where' the money is going before the move happens.")


# ==========================================
# 5. Global Footer
# ==========================================
# [UPDATED] Added Legal link in footer
st.markdown("""
<div class="custom-footer">
    <p>
        © 2026 Paris Trader. All rights reserved.<br>
        <span style="font-size: 0.75rem; color: #6B7280;">
        Not financial advice · For informational and educational purposes only · I am not a licensed financial advisor in Hong Kong or any jurisdiction · Investments carry risk of total loss · Paris Trader accepts no liability.
        </span>
    </p>
    <p>
        <a href="https://t.me/algoparistrader" target="_blank">@ParisTrader on TG</a> | 
        <a href="?page=Legal" target="_self" style="color: #6B7280; text-decoration: none;">Legal & Compliance</a>
    </p>
</div>
""", unsafe_allow_html=True)