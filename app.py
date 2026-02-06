import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import sys
import glob
import time
import base64
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from io import BytesIO
from datetime import datetime
import education_page
import strategy_logic

maxMessageSize = 600

# Add Trade folder path
sys.path.append('Trade')
try:
    from Trade import trade_app
except ImportError:
    pass

# ==========================================
# 0. Strategy Helper Functions (Adapted for Offline)
# ==========================================
# Set Matplotlib style for consistency
plt.style.use('dark_background')
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
                login_success = False
                # 這裡填入你的驗證邏輯
                try:
                    valid_emails = st.secrets["allowed_users"]["emails"]
                    correct_password = st.secrets["access_password"]
                    if email_input in valid_emails and password_input == correct_password:
                        st.session_state["authentication_status"] = True
                        st.session_state["user_email"] = email_input
                        st.success("Access Granted.")
                        login_success = True  # 標記為成功
                    else:
                        st.error("Invalid Credentials")
                except Exception as e:  # ⚠️ 修改這裡：只捕捉一般錯誤，不捕捉系統訊號
                    st.error(f"System Config Error: {e}")
                # ⚠️ 將 rerun 移到 try/except 外面執行
                if login_success:
                    time.sleep(0.5)
                    st.rerun()
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

    /* Navigation Font Optimization for Bilingual Headers */
    [data-testid="stSidebarNav"] span {
        font-size: 14px !important;
        white-space: nowrap;
    }
    .nav-link {
        font-size: 14px !important;
        padding: 8px 10px !important;
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


def load_options_strategy_dashboard():
    """
    Reads the options dashboard HTML and injects the JSON data
    directly into the script to avoid local file loading issues.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "Option", "options_dashboard.html")
    json_path = os.path.join(current_dir, "Option", "all_strategies_data.json")

    if not os.path.exists(html_path):
        return f"<div style='padding:20px; color:red;'>⚠️ HTML File not found: {html_path}</div>"

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()

        # We inject the JSON data as a global JS variable.
        # You may need to ensure your HTML script uses 'window.allStrategiesData'
        # instead of fetch('all_strategies_data.json').
        injection_js = f"<script>window.allStrategiesData = {json_data};</script>"

        if "<head>" in html_content:
            html_content = html_content.replace("<head>", f"<head>{injection_js}")
        else:
            html_content = injection_js + html_content

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
    # IMPROVED NAVIGATION LOGIC (Fixing the Double-Click Bug)
    # -------------------------------------------------------------------------

    # 1. 定義 Callback 函數：當選單改變時，立即更新 URL
    def on_nav_change(key):
        # 獲取選單現在的選擇 (透過 key)
        if "main_nav_key" in st.session_state:
            new_selection = st.session_state["main_nav_key"]
            # 立即更新 URL，這樣下一次 Rerun 時讀取到的就是正確的 Page
            st.query_params["page"] = new_selection
            # 切換主頁面時，清除子頁面參數，避免邏輯衝突
            if "sub" in st.query_params:
                del st.query_params["sub"]


    # 2. Capture the URL params
    query_params = st.query_params
    url_main_page = query_params.get("page", "首頁 Home")  # Default to Home
    url_sub_page = query_params.get("sub", None)  # Capture sub-page

    # Define Main Menu Options (HK Style)
    main_options = [
        "首頁 Home",
        "研究專欄 Research",
        "大市情報 Intelligence",
        "實戰持倉 Portfolio",
        "美股數據 Stock",
        "期權分析 Option",
        "期貨/牛熊 Future",
        "自動交易 MT5 EA",
        "交易學院 Education",
        "交易社群 Community",
        "工具資源 Resources",
        "升級會員 VIP"
    ]

    # Determine default index for Main Menu based on URL
    # Support for legacy URLs (e.g., "Home" maps to "首頁 Home")
    try:
        # Try exact match first
        main_default_index = main_options.index(url_main_page)
    except ValueError:
        # Fallback: fuzzy match (e.g. url "Home" finds "首頁 Home")
        matches = [i for i, opt in enumerate(main_options) if url_main_page in opt]
        main_default_index = matches[0] if matches else 0

    # 3. Render the Main Sidebar Menu
    selected_nav = option_menu(
        menu_title="Navigation",
        options=main_options,
        icons=[
            "house", "globe", "search", "briefcase", "list-task", "layers",
            "graph-up-arrow", "robot", "mortarboard", "people-fill", "collection", "gem"
        ],
        menu_icon="compass",
        default_index=main_default_index,  # Sync with URL
        key="main_nav_key",  # 設定一個唯一的 key
        on_change=on_nav_change,  # 綁定回調函數
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
        if (url_main_page in selected_nav) and (url_sub_page in options):
            default_sub_index = options.index(url_sub_page)
        # Robust check for partial matches in URL sub params
        elif (url_main_page in selected_nav) and url_sub_page:
            matches = [i for i, opt in enumerate(options) if url_sub_page in opt]
            if matches:
                default_sub_index = matches[0]

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


    # --- Sub-menu Logic (HK Style) ---
    if selected_nav == "大市情報 Intelligence":
        # logic: No sidebar submenu. We will handle tabs in the main view.
        target_page = "大市情報 Intelligence"

    elif selected_nav == "美股數據 Stock":
        # logic: No sidebar submenu. We will handle tabs in the main view.
        target_page = "美股數據 Stock"

    elif selected_nav == "期貨/牛熊 Future":
        # logic: No sidebar submenu. We will handle tabs in the main view.
        target_page = "期貨/牛熊 Future"


    elif selected_nav == "期權分析 Option":
        # logic: No sidebar submenu. We will handle tabs in the main view.
        target_page = "期權分析 Option"

    elif selected_nav == "自動交易 MT5 EA":
        st.caption("AUTOMATED TRADING")
        target_page = handle_submenu(
            "sub_ea",
            ["EA 介紹 Introduction"],
            ["robot"]
        )

    # --- 4. Deep Linking: Update URL based on final selection ---

    # Case A: Sidebar item matches target (Home, Education, etc. - No sub-menu)
    # COMMENTED OUT TO FIX DOUBLE CLICK BUG (Handled by on_nav_change)
    # if selected_nav == target_page:
    #     if url_main_page != selected_nav or url_sub_page is not None:
    #         st.query_params["page"] = selected_nav
    #         # Remove 'sub' param if it exists, as this page has no sub-menu
    #         if "sub" in st.query_params:
    #             del st.query_params["sub"]
    #         # time.sleep(0.1) # Optional: sometimes helps with race conditions

    # Case B: Target is a sub-menu item
    if selected_nav != target_page:
        # Check if URL needs update
        if url_main_page != selected_nav or url_sub_page != target_page:
            st.query_params["page"] = selected_nav
            st.query_params["sub"] = target_page

    st.markdown("---")

    # ---------------------------------------------------------
    # ✨ 改良後的 VIP 升級按鈕 (Gold/Pulse Effect) - [已修復連結]
    # ---------------------------------------------------------
    st.markdown("""
        <style>
            /* 定義呼吸燈動畫 */
            @keyframes pulse-gold {
                0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
                100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
            }

            .vip-promo-card {
                background: linear-gradient(135deg, #B45309 0%, #F59E0B 50%, #D97706 100%);
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                margin-bottom: 20px;
                margin-top: 10px;
                border: 1px solid #FCD34D;
                animation: pulse-gold 2s infinite;
            }

            /* 修改重點：直接將 link 變成按鈕樣式，移除 button 標籤以修復點擊問題 */
            a.vip-button-link {
                display: block;
                width: 100%;
                background: #FFFFFF;
                color: #B45309 !important; /* 強制深金色文字 */
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: 800;
                cursor: pointer;
                margin-top: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                transition: transform 0.1s;
                text-decoration: none !important; /* 移除底線 */
                text-align: center;
                box-sizing: border-box; /* 確保 padding 不會撐破寬度 */
            }

            a.vip-button-link:hover {
                transform: scale(1.02);
                background: #FEF3C7;
                color: #92400E !important;
            }

            a.vip-button-link:visited, a.vip-button-link:active {
                color: #B45309 !important;
            }
        </style>

        <div class="vip-promo-card">
            <h3 style="color: #FFFFFF; margin:0; font-size: 18px; font-weight: 800; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
                👑 升級 VIP 會員
            </h3>
            <p style="color: #FEF3C7; font-size: 12px; margin: 8px 0; line-height: 1.4;">
                解鎖機構級數據 (Stock DNA)<br>
                & 實戰倉位 (Portfolio)
            </p>
            <a href="?page=升級會員 VIP" target="_self" class="vip-button-link">
                🚀 立即加入 (Join Now)
            </a>
        </div>
    """, unsafe_allow_html=True)

# Handle Legal from Footer (Special Case)
if url_main_page == "Legal" and selected_nav == "首頁 Home":
    target_page = "Legal"

# ==========================================
# 🔒 權限控制與銷售轉化中心
# ==========================================

# NOTE: Locked page logic is now handled inside the Tabs of each section.
# The global check here is kept only for standalone pages if any.
locked_pages = []

# Updated keys for teaser content (used inside Tabs)
teaser_content = {
    "因子模型 Stock DNA": "Discover the hidden factors driving stock prices using Fama-French models. Identify high-quality alpha before the market moves.",
    "ETF資金流 Smart Money": "Track leveraged ETF flows to spot market reversals instantly. Don't fight the trend, ride the institutional wave.",
    "內部交易 Insider": "See what CEOs and CFOs are doing with their own money. Real-time cluster buying alerts.",
    "挾淡倉 Short Squeeze": "Identify the next GME/AMC before it explodes. High short interest + High borrow cost scanner.",
    "美股期權 US Option": "Follow the Smart Money. Real-time unusual options activity and gamma exposure levels.",
    "港股期權 HK Option": "Advanced market scanner for HK derivatives. Visualise the heavy zones and institutional positioning.",
    "實戰持倉 Portfolio": "Access my personal trade journal. See exactly when I enter and exit positions in Stocks and Options.",
    "成交分佈 Volume Profile": "Professional grade Volume Profile analysis to identify key support and resistance levels.",
    "日內波幅 Volatility": "Monitor real-time volatility spikes to capture intraday momentum.",
    "牛熊重貨區 CBBC Ladder": "Visualise the Bear/Bull contract heavy zones to predict market dealer hedging moves.",
    "期權策略 Strategy": "Quantitative Analysis & Strategy Performance."
}

if target_page in locked_pages:
    desc = teaser_content.get(target_page, "Access professional-grade tools designed for serious traders.")
    if not check_access_or_show_teaser(target_page, description=desc):
        st.stop()

# --- Content Routing (Based on target_page) ---
# [PAGE] HOME
if target_page == "首頁 Home":
    col_main, col_profile = st.columns([0.7, 0.3], gap="large")

    with col_main:
        st.markdown("""
        <h1 style='color:white;'>Ex-Ibanker開發-首個機構級黑科技</h1>
        <h3 style='color:#94a3b8;'>美股期權策略|NQ HSI 金期貨自動交易EA </h3>
        <p style='font-size: 1.1em; color: #64748b;'>
        贏錢不可能只看圖表交易 ,持續盈利交易員必備學習資源平台!
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
            url="https://parisprogram.uk/zh/member/post/RPT-20260131182122129?hash=e71209296eb426dd311b01d899a5615e5c858f30f34d39be3e589d137227761f",
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
            <p style="color: #9CA3AF; font-size: 0.9em;">Ex-Ibank Quantitative Trader</p>
            <hr style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="text-align: left; font-size: 0.9em; line-height: 1.6; color: #e2e8f0;">
                專注於量化因子挖掘與程式化交易。擅長將複雜的金融模型轉化為可執行的實戰策略，並提供獨家 TradingView 指標與回測數據。
                <br><br>
                <b>擅長策略 Core Strategies:</b><br>
                • 美股多因子長短倉 (Multi-Factor L/S)<br>
                • 期貨NQ黃金HSI Scalping (Future Scalping)<br>
                • 美股期權異動簍略 (Unusual Options)<br>
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

# [PAGE] Research
elif target_page == "研究專欄 Research":
    st.title("🦅 Research Paper from Paris")
    st.caption("Institutional Perspectives on Daily Flows")

    # 1. 讀取所有 MD 檔
    files = sorted(glob.glob(os.path.join("DailyInsights", "*.md")), reverse=True)

    if not files:
        st.info("No insights published yet. Stay tuned.")
    else:
        # 2. 顯示邏輯 (Timeline 樣式)
        # 【修改點】：加入 enumerate 以獲取 index (i)
        for i, file_path in enumerate(files):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split('\n')
            title = lines[0].replace('# ', '')

            date_display = "Recent"
            body_start_index = 1
            for idx, line in enumerate(lines):
                if "**Date:**" in line:
                    date_display = line.replace("**Date:**", "").strip()
                    body_start_index = idx + 1
                    break

            body = "\n".join(lines[body_start_index:])

            with st.container():
                col_date, col_text = st.columns([1, 5])

                with col_date:
                    st.markdown(f"""
                    <div style="background: rgba(37, 99, 235, 0.2); padding: 5px; border-radius: 5px; text-align: center; border: 1px solid #3b82f6;">
                        <span style="font-size: 0.8em; color: #93c5fd; font-weight: bold;">{date_display}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with col_text:
                    # 【修改點】：只展開第一個 (i == 0)
                    is_expanded = (i == 0)
                    with st.expander(f"📄 {title}", expanded=is_expanded):
                        st.markdown(body)
                        st.markdown("---")

# [PAGE] Intelligence (Consolidated Tabs)
elif target_page == "大市情報 Intelligence":
    st.title("📡 Market Intelligence")
    st.caption("Risk Metrics, Market Breadth & Positioning")

    tab_risk, tab_breadth, tab_cftc = st.tabs([
        "⚠️ Market Risk",
        "🌊 Market Breadth",
        "🐋 CFTC Position"
    ])

    # --- Tab 1: Market Risk ---
    with tab_risk:
        st.subheader("Market Implied Risk")
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

    # --- Tab 2: Market Breadth ---
    with tab_breadth:
        st.subheader("Market Breadth")
        path = os.path.join("MarketDashboard", "MarketBreadth")
        html_content, filename = get_latest_file_content(path, "market_breadth_*.html")
        if html_content:
            st.caption(f"Displaying Report: {filename}")
            components.html(html_content, height=2200, scrolling=True)
        else:
            st.warning("⚠️ Market Breadth report not found.")

    # --- Tab 3: CFTC Position ---
    with tab_cftc:
        st.subheader("CFTC Institutional Positioning")
        st.caption("Commitment of Traders (COT) Report - Smart Money vs Retail")
        path = "MarketDashboard"
        html_content, filename = get_latest_file_content(path, "cftc_pro_report*.html")
        if html_content:
            st.caption(f"📅 Report Date: {filename}")
            components.html(html_content, height=2200, scrolling=True)
        else:
            st.warning("⚠️ CFTC Report not found.")


# [PAGE] Stock Analytics (Consolidated with Tabs)
elif target_page == "美股數據 Stock":
    st.title("🇺🇸 US Stock Market Analytics")
    st.caption("Institutional Data, Heatmaps & Factor Analysis")

    # Define the Tabs
    tab_basket, tab_smart, tab_sp500, tab_sector, tab_ta, tab_earn, tab_insider, tab_squeeze, tab_dna, tab_vol = st.tabs(
        [
            "🧺 Thematic Basket",
            "🚀 Smart Money",
            "🔥 S&P 500",
            "🗺️ Sector",
            "🚦 TA Score",
            "📅 Earnings",
            "🕴️ Insider",
            "⚡ Short Squeeze",
            "🧬 Stock DNA",
            "📉 Volatility"
        ])

    # --- Tab 1: Thematic Basket ---
    with tab_basket:
        st.subheader("Thematic Basket Analysis")
        path = "ThematicBasket"
        html_content, filename = get_latest_file_content(path, "elite_dashboard_*.html")
        if html_content:
            st.caption(f"📅 Strategy Report: {filename}")
            components.html(html_content, height=6000, scrolling=True)
        else:
            st.warning("⚠️ No basket reports found.")

    # --- Tab 2: ETF Smart Money (LOCKED) ---
    with tab_smart:
        st.subheader("ETF Smart Money Tracker")
        # Check Access
        if check_access_or_show_teaser("ETF資金流 Smart Money",
                                       description="Track leveraged ETF flows to spot market reversals instantly. Don't fight the trend, ride the institutional wave."):

            path = "xETF"
            html_content, filename = get_latest_file_content(path, "ETF_Smart_Money_Report_*.html")
            if html_content:
                st.caption(f"📅 Report Date: {filename}")
                components.html(html_content, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No ETF Smart Money reports found.")

    # --- Tab 3: S&P 500 Heatmap ---
    with tab_sp500:
        st.subheader("S&P 500 Performance Heatmap (YTD)")
        path = "Stock"
        html_content, filename = get_latest_file_content(path, "sp500_clean_heatmap_*.html")
        if html_content:
            st.caption(f"📅 Report Date: {filename}")
            components.html(html_content, height=1600, scrolling=True)
        else:
            st.warning("⚠️ No S&P 500 Heatmap found.")

    # --- Tab 4: Sector Heatmap ---
    with tab_sector:
        st.subheader("Industry Sector Heatmap")
        path = "MarketDashboard"
        html_content, filename = get_latest_file_content(path, "sector_etf_heatmap_*.html")
        if html_content:
            st.caption(f"Displaying Report: {filename}")
            components.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Sector Heatmap not found.")

    # --- Tab 5: TA Score ---
    with tab_ta:
        st.subheader("Technical Analysis Score")
        sub_tab_us, sub_tab_hk = st.tabs(["US Market", "HK Market"])
        path = "Stock"

        with sub_tab_us:
            html_content, filename = get_latest_file_content(path, "TA_score_heatmap_*.html")
            if html_content:
                st.caption(f"📅 US Report Date: {filename}")
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning("⚠️ US TA Score Heatmap not found.")

        with sub_tab_hk:
            html_content_hk, filename_hk = get_latest_file_content(path, "HK_TA_score_heatmap_*.html")
            if html_content_hk:
                st.caption(f"📅 HK Report Date: {filename_hk}")
                components.html(html_content_hk, height=1200, scrolling=True)
            else:
                st.warning("⚠️ HK TA Score Heatmap not found.")

    # --- Tab 6: Earnings ---
    with tab_earn:
        st.subheader("Earnings Calendar Analysis")
        path = "Earnings"
        html_content, filename = get_latest_file_content(path)
        if html_content:
            st.caption(f"Displaying Report: {filename}")
            components.html(html_content, height=2500, scrolling=True)
        else:
            st.warning("⚠️ No earnings reports found.")

    # --- Tab 7: Insider Trading (LOCKED) ---
    with tab_insider:
        st.subheader("Insider Trading Activity")
        if check_access_or_show_teaser("內部交易 Insider",
                                       description="See what CEOs and CFOs are doing with their own money. Real-time cluster buying alerts."):

            path = "Insider"
            html_content, filename = get_latest_file_content(path, "Insider_Trading_Report_*.html")
            if html_content:
                st.caption(f"📅 Report Date: {filename}")
                components.html(html_content, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No Insider Trading reports found.")

    # --- Tab 8: Short Squeeze (LOCKED) ---
    with tab_squeeze:
        st.subheader("Short Squeeze Scanner")
        if check_access_or_show_teaser("挾淡倉 Short Squeeze",
                                       description="Identify the next GME/AMC before it explodes. High short interest + High borrow cost scanner."):

            path = "Short_squeeze"
            html_content, filename = get_latest_file_content(path, "Short_squeeze_*.html")
            if html_content:
                st.caption(f"📅 Report Date: {filename}")
                components.html(html_content, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No Short Squeeze reports found.")

    # --- Tab 9: Stock DNA (LOCKED) ---
    with tab_dna:
        st.subheader("Stock Factor DNA")
        if check_access_or_show_teaser("因子模型 Stock DNA",
                                       description="Discover the hidden factors driving stock prices using Fama-French models."):

            html_content = load_stock_dna_with_injection()
            if html_content and "HTML not found" not in html_content:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.error("FamaFrench/index.html not found")

    # --- Tab 10: Volatility Target (LOCKED) ---
    with tab_vol:
        st.subheader("Volatility Target Strategy")
        if check_access_or_show_teaser("波動率策略 Volatility Target",
                                       description="Access professional-grade volatility control strategies."):

            path = "VolTarget"
            html_content, filename = get_latest_file_content(path, "vol_tool_*.html")
            if html_content:
                st.caption(f"Displaying Report: {filename}")
                components.html(html_content, height=1500, scrolling=True)
            else:
                st.warning("⚠️ Volatility Tool not found.")

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

# [PAGE] Options (Consolidated Tabs)
elif target_page == "期權分析 Option":
    st.title("🎯 Options Analytics")
    st.caption("Flows, Heatmaps & Strategy Builder")

    tab_hk, tab_us, tab_strat = st.tabs([
        "🇭🇰 HK Option",
        "🇺🇸 US Option",
        "🛠️ Strategy"
    ])

    # --- Tab 1: HK Option ---
    with tab_hk:
        st.subheader("HK Option Market Analysis")
        path = "Option"
        search_pattern = "HK_Option_Market_*.html"
        html_content, filename = get_latest_file_content(path, search_pattern)
        if html_content:
            st.caption(f"📅 Report Date: {filename}")
            components.html(html_content, height=2000, scrolling=True)
        else:
            st.warning("⚠️ No HK Option reports found.")

    # --- Tab 2: US Option (LOCKED) ---
    with tab_us:
        st.subheader("US Option Strike Analysis")
        if check_access_or_show_teaser("美股期權 US Option",
                                       description="Follow the Smart Money. Real-time unusual options activity and gamma exposure levels."):

            path = "Option"
            search_pattern = "option_strike_*.html"
            html_content, filename = get_latest_file_content(path, search_pattern)
            if html_content:
                st.caption(f"📅 Report Date: {filename}")
                components.html(html_content, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No US Option reports found.")

    # --- Tab 3: Strategy (LOCKED) ---
    with tab_strat:
        st.subheader("Interactive Option Strategy Builder")
        if check_access_or_show_teaser("期權策略 Strategy",
                                       description="Quantitative Analysis & Strategy Performance."):

            # --- 用戶輸入區 (Copy from original block) ---
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                with c1:
                    ticker_input = st.text_input("Enter US Ticker", value="NVDA", help="e.g., TSLA, AAPL, NVDA",
                                                 key="strat_ticker").upper()
                with c2:
                    spread_width = st.number_input("Spread Width ($)", value=5, min_value=1, max_value=50,
                                                   key="strat_width")
                with c3:
                    otm_call_pct = st.number_input("Call OTM %", value=1.03, step=0.01, format="%.2f",
                                                   help="1.10 = 10% OTM", key="strat_call")
                with c4:
                    itm_put_pct = st.number_input("Put ITM %", value=0.97, step=0.01, format="%.2f",
                                                  help="0.90 = 10% OTM", key="strat_put")

                run_btn = st.button("🚀 Generate Strategy Dashboard", type="primary", use_container_width=True,
                                    key="strat_btn")

            # --- 執行邏輯 ---
            if run_btn and ticker_input:
                with st.status(f"Processing {ticker_input}...", expanded=True) as status:
                    # Step 1: 檢查/下載 CSV
                    status.write("📂 Checking local data cache...")
                    try:
                        df_hist, options_data, data_date = strategy_logic.get_local_data(ticker_input)
                        if df_hist is None:
                            status.update(label="Local Data Not Found", state="error")
                            st.error(f"Data not found. Please run data_updater.py first.")
                            st.stop()
                        status.write(f"✅ Loaded history data. Data Date: {data_date}")

                        # Step 2: 獲取期權鏈並生成 HTML
                        status.write("🔗 Calculating strategy payoffs...")
                        html_result, msg = strategy_logic.generate_strategy_html(ticker_input, spread_width, otm_call_pct, itm_put_pct)

                        if html_result:
                            status.update(label="Dashboard Generated!", state="complete")
                            st.markdown("---")
                            components.html(html_result, height=1400, scrolling=True)
                        else:
                            status.update(label="Generation Failed", state="error")
                            st.error(msg)
                    except Exception as e:
                        st.error(f"System Error: {e}")

# [PAGE] Future (Consolidated Tabs)
elif target_page == "期貨/牛熊 Future":
    st.title("🎢 Futures & Trends")
    st.caption("Volatility, Volume & Heavy Zones")

    tab_vol, tab_vp, tab_cbbc = st.tabs([
        "⚡ Intraday Volatility",
        "📊 Volume Profile",
        "🐻 CBBC Ladder"
    ])

    # --- Tab 1: Intraday Volatility ---
    with tab_vol:
        st.subheader("Intraday Volatility Analysis")
        html_path = os.path.join("MarketDashboard", "Intraday_Volatility.html")
        html_content = load_html_file(html_path)
        if html_content and "File not found" not in html_content:
            components.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("⚠️ 找不到 Intraday Volatility 報告")

    # --- Tab 2: Volume Profile (LOCKED) ---
    with tab_vp:
        st.subheader("Volume Profile Analysis")
        if check_access_or_show_teaser("成交分佈 Volume Profile",
                                       description="Professional grade Volume Profile analysis to identify key support and resistance levels."):

            path = "VP"
            html_content, filename = get_latest_file_content(path)
            if html_content:
                st.caption(f"Displaying Report: {filename}")
                components.html(html_content, height=1000, scrolling=True)
            else:
                st.warning("⚠️ 尚未部署 Volume Profile 模組 (VP 資料夾為空)")

    # --- Tab 3: CBBC Ladder (LOCKED) ---
    with tab_cbbc:
        st.subheader("HSI CBBC Heavy Zone")
        if check_access_or_show_teaser("牛熊重貨區 CBBC Ladder",
                                       description="Visualise the Bear/Bull contract heavy zones to predict market dealer hedging moves."):

            html_path = os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html")
            html_content = load_html_file(html_path)
            if html_content and "File not found" not in html_content:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning("⚠️ 尚未生成牛熊證分佈報告")


# [PAGE] My Portfolio
elif target_page == "實戰持倉 Portfolio":
    st.title("💼 Paris Picks")
    path = "Trade"

    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])

    # 檢查是否已登入 (檢查 Session State)
    is_vip = st.session_state.get("authentication_status", False)

    # --- Tab 1: Stock Journal (部分公開) ---
    with tab1:
        html_content, filename = get_latest_file_content(path, "trade_record_*.html")

        if html_content:
            st.caption(f"📅 Stock Report: {filename}")

            if is_vip:
                # [VIP 模式]：顯示完整高度 + 允許捲動
                components.html(html_content, height=1200, scrolling=True)
            else:
                # [免費模式]：顯示上半部預覽 (高度設小 + 禁止捲動)
                st.info("👀 Preview Mode: Showing top positions only.")
                # height=400 且 scrolling=False 確保只能看到頂部
                components.html(html_content, height=600, scrolling=False)

                # 顯示鎖定遮罩與登入按鈕
                st.markdown("---")
                # 這裡調用你的鎖定函數，若未登入會顯示 Login Form
                check_access_or_show_teaser(
                    "Stock Journal Full Access",
                    description="🔒 Sign in to unlock the full trade journal, entry/exit prices, and historical performance."
                )
        else:
            st.warning("⚠️ Trade Record HTML not found.")
            st.info("Please verify that the GitHub Action has run successfully.")

    # --- Tab 2: Option Desk (維持完全鎖定或根據你的需求調整) ---
    with tab2:
        # 如果你希望 Option Desk 也是同樣邏輯，可以複製上面的做法
        # 這裡示範保持原本的全鎖定邏輯 (如果未登入，直接擋住)

        if not is_vip:
            check_access_or_show_teaser(
                "Option Desk",
                description="🔒 VIP Access Only. Real-time option flow analysis and positions."
            )
        else:
            # VIP 才能看到這部分
            html_content_opt, filename_opt = get_latest_file_content(path, "option_record_*.html")
            if html_content_opt:
                st.caption(f"📅 Option Report: {filename_opt}")
                components.html(html_content_opt, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Option Record HTML not found.")
                st.info("Please verify `option_record_*.html` exists in `Trade` folder.")

# [PAGE] MT5 EA - Introduction
elif target_page == "EA 介紹 Introduction":
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
elif target_page == "工具資源 Resources":
    st.title("🔗 Trading Resources")
    html_path = os.path.join("Resources", "external_links.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.warning("⚠️ Resources file not found.")
        st.info(f"Please ensure `{html_path}` exists.")

elif target_page == "交易社群 Community":
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

# [PAGE] Education Hub (Refactored to external module)
elif target_page == "交易學院 Education":
    # Pass the helper functions to the module
    education_page.render_education_page(check_access_or_show_teaser, load_markdown_with_images)

# [PAGE] Membership (Sales Page)
elif target_page == "升級會員 VIP":
    # 標題仍保留在 Streamlit，方便 SEO 和結構，內容則用 HTML 渲染
    st.title("💎 升級機構級數據 Upgrade to Institutional Level")
    st.caption("停止猜測。像專業人士一樣，利用數據進行交易。")
    st.caption("Stop guessing. Start trading with data used by professionals.")

    # 定義 HTML 檔案路徑
    html_file_path = os.path.join("Community", "membership_pricing.html")

    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # 設定 height=1000 或更高，以確保卡片能完整顯示不需捲動
            components.html(html_content, height=1100, scrolling=True)
    else:
        st.error(f"⚠️ Membership page file not found at: {html_file_path}")
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