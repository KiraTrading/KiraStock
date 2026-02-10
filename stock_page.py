import streamlit as st
import streamlit.components.v1 as components
import os
import utils


def render_stock_page():
    # 頁面主標題
    st.title("美股市場深度分析系統")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
        <b>🎯 交易工作流 (Workflow):</b> <br>
        1. <b>宏觀、熱度與業績</b> (觀察板塊輪動、財報雷區與大市氣氛) ➡ 
        2. <b>選股與資金訊號</b> (在該板塊找尋強勢股/聰明錢/內部人) ➡ 
        3. <b>深度分析與執行</b> (進場前的價位與倉位確認)
    </div>
    """, unsafe_allow_html=True)

    # 定義三大階段
    phase_names = [
        "1️⃣ 宏觀、熱度與業績 (Macro & Earnings)",
        "2️⃣ 選股與資金訊號 (Screening & Flows)",
        "3️⃣ 深度分析與執行 (Deep Dive & Execution)"
    ]

    phase1, phase2, phase3 = st.tabs(phase_names)

    # =========================================================
    # Phase 1: 宏觀定方向 (看板塊、看大市、看業績日程)
    # =========================================================
    with phase1:
        st.info("💡 **第一步：市場節奏與熱點？** 查看板塊輪動、標普熱力圖，並留意本週**業績公佈**帶來的波動風險。")

        # [已更新] 將 "業績公佈" 加入此區塊
        p1_tabs = st.tabs(["🧺 概念籃子", "🗺️ 板塊輪動", "🔥 標普500", "📅 業績公佈"])

        # --- Tab 1.1: 主題投組 ---
        with p1_tabs[0]:
            st.subheader("主題投組分析 (Thematic Basket)")
            html_content, fn = utils.get_latest_file_content("ThematicBasket", "elite_dashboard_*.html")
            if html_content:
                st.caption(f"📅 策略報告: {fn}")
                components.html(html_content, height=6000, scrolling=True)
            else:
                st.warning("⚠️ 找不到投組報告 (No basket reports found).")

        # --- Tab 1.2: 板塊熱力圖 ---
        with p1_tabs[1]:
            st.subheader("行業板塊熱力圖 (Sector Heatmap)")
            html_content, _ = utils.get_latest_file_content("MarketDashboard", "sector_etf_heatmap_*.html")
            if html_content:
                st.caption("顯示報告")
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.warning("⚠️ 找不到板塊熱力圖。")

        # --- Tab 1.3: S&P 500 熱力圖 ---
        with p1_tabs[2]:
            st.subheader("標普 500 表現熱力圖 (S&P 500 Map)")
            html_content, _ = utils.get_latest_file_content("Stock", "sp500_clean_heatmap_*.html")
            if html_content:
                components.html(html_content, height=1600, scrolling=True)
            else:
                st.warning("⚠️ 找不到 S&P 500 熱力圖。")

        # --- Tab 1.4: 業績公佈 (Moved Here) ---
        with p1_tabs[3]:
            st.subheader("財報行事曆分析 (Earnings Calendar)")
            html, _ = utils.get_latest_file_content("Earnings")
            if html:
                components.html(html, height=2500, scrolling=True)
            else:
                st.warning("⚠️ 找不到財報報告。")

    # =========================================================
    # Phase 2: 選股找訊號 (聰明錢、技術面、內部人)
    # =========================================================
    with phase2:
        st.info("💡 **第二步：誰在買？買什麼？** 追蹤 ETF 資金流、內部人交易，並結合技術評分篩選個股。")

        # [已更新] 移除業績，剩下 4 個選股工具
        p2_tabs = st.tabs(["🚀 ETF資金流", "🚦 技術評分", "🕴️ 內部交易", "⚡ 挾淡倉"])

        # --- Tab 2.1: ETF 聰明錢 ---
        with p2_tabs[0]:
            st.subheader("ETF 資金流追蹤 (Smart Money Tracker)")
            if utils.check_access_or_show_teaser("ETF資金流 Smart Money",
                                                 description="追蹤槓桿 ETF 資金流向，即時捕捉市場反轉訊號。"):
                html_content, _ = utils.get_latest_file_content("xETF", "ETF_Smart_Money_Report_*.html")
                if html_content:
                    components.html(html_content, height=2000, scrolling=True)
                else:
                    st.warning("⚠️ 找不到 ETF 資金流報告。")

        # --- Tab 2.2: 技術評分 ---
        with p2_tabs[1]:
            st.subheader("技術分析評分 (Technical Analysis Score)")
            sub_us, sub_hk = st.tabs(["🇺🇸 美股市場", "🇭🇰 港股市場"])
            with sub_us:
                html, _ = utils.get_latest_file_content("Stock", "TA_score_heatmap_*.html")
                if html:
                    components.html(html, height=1200, scrolling=True)
                else:
                    st.warning("⚠️ 找不到美股報告。")
            with sub_hk:
                html_hk, _ = utils.get_latest_file_content("Stock", "HK_TA_score_heatmap_*.html")
                if html_hk:
                    components.html(html_hk, height=1200, scrolling=True)
                else:
                    st.warning("⚠️ 找不到港股報告。")

        # --- Tab 2.3: 內部交易 ---
        with p2_tabs[2]:
            st.subheader("內部人士交易活動 (Insider Trading)")
            if utils.check_access_or_show_teaser("內部交易 Insider",
                                                 description="查看 CEO 和 CFO 如何操作自家股票。"):
                html, _ = utils.get_latest_file_content("Insider", "Insider_Trading_Report_*.html")
                if html:
                    components.html(html, height=2000, scrolling=True)
                else:
                    st.warning("⚠️ 找不到內部交易報告。")

        # --- Tab 2.4: 挾淡倉 ---
        with p2_tabs[3]:
            st.subheader("短拉補/挾淡倉掃描 (Short Squeeze Scanner)")
            if utils.check_access_or_show_teaser("挾淡倉 Short Squeeze",
                                                 description="高沽空比率 + 高借貸成本掃描。"):
                html, _ = utils.get_latest_file_content("Short_squeeze", "Short_squeeze_*.html")
                if html:
                    components.html(html, height=2000, scrolling=True)
                else:
                    st.warning("⚠️ 找不到挾淡倉報告。")

    # =========================================================
    # Phase 3: 深度分析與執行 (保持不變)
    # =========================================================
    with phase3:
        st.info("💡 **第三步：如何進場？買多少？** 使用 VP 尋找支撐壓力，用基因比較個股，最後用波動率計算倉位。")

        p3_tabs = st.tabs(["📊 VP價量分佈", "🧬 股票基因", "📉 波動率倉位"])

        # --- Tab 3.1: 價量分佈 (VP) ---
        with p3_tabs[0]:
            st.subheader("個股成交量分佈圖 (Volume Profile)")
            if utils.check_access_or_show_teaser("Stock VP", description="專業級價量分佈儀表板。"):
                html, filename = utils.get_latest_file_content("VP", "vp_dashboard_*.html")
                if html:
                    st.caption(f"📅 數據生成時間: {filename}")
                    components.html(html, height=1350, scrolling=True)
                else:
                    st.warning("⚠️ 找不到價量分佈儀表板。")

        # --- Tab 3.2: 股票基因 ---
        with p3_tabs[1]:
            st.subheader("股票因子基因 (Stock Factor DNA)")
            if utils.check_access_or_show_teaser("因子模型 Stock DNA", description="發掘驅動股價的隱藏因子。"):
                html = utils.load_stock_dna_with_injection(os.getcwd())
                if html and "HTML not found" not in html:
                    components.html(html, height=1200, scrolling=True)
                else:
                    st.error("找不到 FamaFrench/index.html")

        # --- Tab 3.3: 波動率策略 ---
        with p3_tabs[2]:
            st.subheader("波動率目標控制策略 (Volatility Target)")
            if utils.check_access_or_show_teaser("波動率策略 Volatility Target",
                                                 description="獲取專業級波動率控制策略工具。"):
                html, _ = utils.get_latest_file_content("VolTarget", "vol_tool_*.html")
                if html:
                    components.html(html, height=1500, scrolling=True)
                else:
                    st.warning("⚠️ 找不到波動率工具。")