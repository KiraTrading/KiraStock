import streamlit as st
import streamlit.components.v1 as components
import os
import utils

# --- Language & Translation Setup ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'zh'

translations = {
    "zh": {
        "page_title": "美股市場深度分析系統",
        "workflow_title": "🎯 交易工作流 (Workflow):",
        "workflow_step1": "宏觀、熱度與業績 (觀察板塊輪動、財報雷區與大市氣氛)",
        "workflow_step2": "選股與資金訊號 (在該板塊找尋強勢股/聰明錢/內部人)",
        "workflow_step3": "深度分析與執行 (進場前的價位與倉位確認)",
        "phase1_name": "1️⃣ 宏觀、熱度與業績 (Macro & Earnings)",
        "phase2_name": "2️⃣ 選股與資金訊號 (Screening & Flows)",
        "phase3_name": "3️⃣ 深度分析與執行 (Deep Dive & Execution)",
        "p1_info": "💡 **第一步：市場節奏與熱點？** 查看板塊輪動、標普熱力圖，並留意本週**業績公佈**帶來的波動風險。",
        "p1_tabs": ["🧺 概念籃子", "🗺️ 板塊輪動", "🔥 標普500", "📅 業績公佈"],
        "p1_headers": ["主題投組分析 (Thematic Basket)", "行業板塊熱力圖 (Sector Heatmap)",
                       "標普 500 表現熱力圖 (S&P 500 Map)", "財報行事曆分析 (Earnings Calendar)"],
        "p2_info": "💡 **第二步：誰在買？買什麼？** 追蹤 ETF 資金流、內部人交易，並結合技術評分篩選個股。",
        "p2_tabs": ["🚀 ETF資金流", "🚦 技術評分", "🕴️ 內部交易", "⚡ 挾淡倉"],
        "p2_headers": ["ETF 資金流追蹤 (Smart Money Tracker)", "技術分析評分 (Technical Analysis Score)",
                       "內部人士交易活動 (Insider Trading)", "短拉補/挾淡倉掃描 (Short Squeeze Scanner)"],
        "p3_info": "💡 **第三步：如何進場？買多少？** 使用 VP 尋找支撐壓力，用基因比較個股，最後用波動率計算倉位。",
        "p3_tabs": ["📊 VP價量分佈", "🧬 股票基因", "📉 波動率倉位"],
        "p3_headers": ["個股成交量分佈圖 (Volume Profile)", "股票因子基因 (Stock Factor DNA)",
                       "波動率目標控制策略 (Volatility Target)"],
        "err_not_found": "⚠️ 找不到報告 (Report not found).",
        "btn_show_report": "顯示報告"
    },
    "en": {
        "page_title": "US Market Deep Analysis System",
        "workflow_title": "🎯 Trading Workflow:",
        "workflow_step1": "Macro, Heat & Earnings (Observe sector rotation, earnings mines, and market sentiment)",
        "workflow_step2": "Screening & Flow Signals (Find strong stocks/Smart Money/Insiders)",
        "workflow_step3": "Deep Dive & Execution (Confirm entry levels and sizing)",
        "phase1_name": "1️⃣ Macro & Earnings",
        "phase2_name": "2️⃣ Screening & Flows",
        "phase3_name": "3️⃣ Deep Dive & Execution",
        "p1_info": "💡 **Step 1: Market Rhythm?** Check sector rotation, S&P heatmap, and watch out for **Earnings Volatility**.",
        "p1_tabs": ["🧺 Thematic Basket", "🗺️ Sector Rotation", "🔥 S&P 500", "📅 Earnings"],
        "p1_headers": ["Thematic Basket Analysis", "Sector Heatmap", "S&P 500 Performance Map",
                       "Earnings Calendar Analysis"],
        "p2_info": "💡 **Step 2: Who's Buying?** Track ETF flows, Insider trading, and filter stocks with Technical Scores.",
        "p2_tabs": ["🚀 ETF Flow", "🚦 TA Score", "🕴️ Insider", "⚡ Short Squeeze"],
        "p2_headers": ["ETF Smart Money Tracker", "Technical Analysis Score", "Insider Trading Activity",
                       "Short Squeeze Scanner"],
        "p3_info": "💡 **Step 3: How to Enter?** Use VP for levels, DNA for quality check, and Volatility for sizing.",
        "p3_tabs": ["📊 Volume Profile", "🧬 Stock DNA", "📉 Vol Target"],
        "p3_headers": ["Stock Volume Profile", "Stock Factor DNA", "Volatility Target Strategy"],
        "err_not_found": "⚠️ Report not found.",
        "btn_show_report": "Show Report"
    }
}


def t(key):
    return translations[st.session_state['language']].get(key, key)


def render_stock_page():
    # 頁面主標題
    st.title(t("page_title"))

    # Workflow HTML (Mixed static HTML with dynamic text)
    st.markdown(f"""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: black;'>
        <b style='color: black;'>{t('workflow_title')}</b> <br>
        <ol style='color: black; margin-top: 10px;'>
            <li><b>{t('workflow_step1').split('(')[0]}</b> ({t('workflow_step1').split('(')[1] if '(' in t('workflow_step1') else ''} ➡ </li>
            <li><b>{t('workflow_step2').split('(')[0]}</b> ({t('workflow_step2').split('(')[1] if '(' in t('workflow_step2') else ''} ➡ </li>
            <li><b>{t('workflow_step3').split('(')[0]}</b> ({t('workflow_step3').split('(')[1] if '(' in t('workflow_step3') else ''}</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # 定義三大階段
    phase_names = [t("phase1_name"), t("phase2_name"), t("phase3_name")]
    phase1, phase2, phase3 = st.tabs(phase_names)

    # =========================================================
    # Phase 1
    # =========================================================
    with phase1:
        st.info(t("p1_info"))
        p1_tabs = st.tabs(t("p1_tabs"))

        # --- Tab 1.1: Thematic Basket ---
        with p1_tabs[0]:
            st.subheader(t("p1_headers")[0])
            html_content, fn = utils.get_latest_file_content("ThematicBasket", "elite_dashboard_*.html")
            if html_content:
                st.caption(f"📅 Report: {fn}")
                components.html(html_content, height=6000, scrolling=True)
            else:
                st.warning(t("err_not_found"))

        # --- Tab 1.2: Sector Heatmap ---
        with p1_tabs[1]:
            st.subheader(t("p1_headers")[1])
            html_content, _ = utils.get_latest_file_content("MarketDashboard", "sector_etf_heatmap_*.html")
            if html_content:
                st.caption(t("btn_show_report"))
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning(t("err_not_found"))

        # --- Tab 1.3: S&P 500 Map ---
        with p1_tabs[2]:
            st.subheader(t("p1_headers")[2])
            html_content, _ = utils.get_latest_file_content("Stock", "sp500_clean_heatmap_*.html")
            if html_content:
                components.html(html_content, height=1600, scrolling=True)
            else:
                st.warning(t("err_not_found"))

        # --- Tab 1.4: Earnings ---
        with p1_tabs[3]:
            st.subheader(t("p1_headers")[3])
            html, _ = utils.get_latest_file_content("Earnings")
            if html:
                components.html(html, height=2500, scrolling=True)
            else:
                st.warning(t("err_not_found"))

    # =========================================================
    # Phase 2
    # =========================================================
    with phase2:
        st.info(t("p2_info"))
        p2_tabs = st.tabs(t("p2_tabs"))

        # --- Tab 2.1: ETF Flow ---
        with p2_tabs[0]:
            st.subheader(t("p2_headers")[0])
            if utils.check_access_or_show_teaser("ETF資金流 Smart Money",
                                                 description="Track leverage ETF flows to catch reversals."):
                html_content, _ = utils.get_latest_file_content("xETF", "ETF_Smart_Money_Report_*.html")
                if html_content:
                    components.html(html_content, height=2000, scrolling=True)
                else:
                    st.warning(t("err_not_found"))

        # --- Tab 2.2: TA Score ---
        with p2_tabs[1]:
            st.subheader(t("p2_headers")[1])
            if utils.check_access_or_show_teaser("技術評分 TA Score",
                                                 description="Composite technical score matrix."):
                sub_us, sub_hk = st.tabs(["🇺🇸 US Market", "🇭🇰 HK Market"])
                with sub_us:
                    html, _ = utils.get_latest_file_content("Stock", "TA_score_heatmap_*.html")
                    if html:
                        components.html(html, height=1200, scrolling=True)
                    else:
                        st.warning(t("err_not_found"))
                with sub_hk:
                    html_hk, _ = utils.get_latest_file_content("Stock", "HK_TA_score_heatmap_*.html")
                    if html_hk:
                        components.html(html_hk, height=1200, scrolling=True)
                    else:
                        st.warning(t("err_not_found"))

        # --- Tab 2.3: Insider ---
        with p2_tabs[2]:
            st.subheader(t("p2_headers")[2])
            if utils.check_access_or_show_teaser("內部交易 Insider",
                                                 description="See how CEOs/CFOs trade their own stock."):
                html, _ = utils.get_latest_file_content("Insider", "Insider_Trading_Report_*.html")
                if html:
                    components.html(html, height=2000, scrolling=True)
                else:
                    st.warning(t("err_not_found"))

        # --- Tab 2.4: Short Squeeze ---
        with p2_tabs[3]:
            st.subheader(t("p2_headers")[3])
            if utils.check_access_or_show_teaser("挾淡倉 Short Squeeze",
                                                 description="High Short Interest + High Borrow Fee Scanner."):
                html, _ = utils.get_latest_file_content("Short_squeeze", "Short_squeeze_*.html")
                if html:
                    components.html(html, height=2000, scrolling=True)
                else:
                    st.warning(t("err_not_found"))

    # =========================================================
    # Phase 3
    # =========================================================
    with phase3:
        st.info(t("p3_info"))
        p3_tabs = st.tabs(t("p3_tabs"))

        # --- Tab 3.1: VP ---
        with p3_tabs[0]:
            st.subheader(t("p3_headers")[0])
            if utils.check_access_or_show_teaser("Stock VP", description="Pro Volume Profile Dashboard."):
                html, filename = utils.get_latest_file_content("VP", "vp_dashboard_*.html")
                if html:
                    st.caption(f"📅 Date: {filename}")
                    components.html(html, height=1350, scrolling=True)
                else:
                    st.warning(t("err_not_found"))

        # --- Tab 3.2: Stock DNA ---
        with p3_tabs[1]:
            st.subheader(t("p3_headers")[1])
            if utils.check_access_or_show_teaser("因子模型 Stock DNA",
                                                 description="Discover hidden factors driving price."):
                html = utils.load_stock_dna_with_injection(os.getcwd())
                if html and "HTML not found" not in html:
                    components.html(html, height=1200, scrolling=True)
                else:
                    st.error("HTML not found: FamaFrench/index.html")

        # --- Tab 3.3: Vol Target ---
        with p3_tabs[2]:
            st.subheader(t("p3_headers")[2])
            if utils.check_access_or_show_teaser("波動率策略 Volatility Target",
                                                 description="Professional Volatility Control Strategy."):
                html, _ = utils.get_latest_file_content("VolTarget", "vol_tool_*.html")
                if html:
                    components.html(html, height=1500, scrolling=True)
                else:
                    st.warning(t("err_not_found"))