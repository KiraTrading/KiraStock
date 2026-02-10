import streamlit as st
import streamlit.components.v1 as components
import os
import utils


def render_stock_page():
    # 頁面主標題
    st.title("美股市場分析")
    st.caption("機構數據、熱力圖與因子分析")

    # [已更新] 定義 Tab 名稱 (全中文介面)
    tab_names = [
        "🧺 概念籃子", "🚀 ETF", "🔥 標普500", "🗺️ 板塊輪動", "🚦 技術評分",
        "📅 業績", "🕴️ 內部交易", "⚡ 挾淡倉", "🧬 股票基因", "📉 波動定倉位", "📊 VP"
    ]

    # 建立 Tabs
    tab_basket, tab_smart, tab_sp500, tab_sector, tab_ta, tab_earn, tab_insider, tab_squeeze, tab_dna, tab_vol, tab_vp = st.tabs(
        tab_names)

    # --- Tab 1: 主題投組 ---
    with tab_basket:
        st.subheader("主題投組分析 (Thematic Basket Analysis)")
        html_content, fn = utils.get_latest_file_content("ThematicBasket", "elite_dashboard_*.html")
        if html_content:
            st.caption(f"📅 策略報告: {fn}")
            components.html(html_content, height=6000, scrolling=True)
        else:
            st.warning("⚠️ 找不到投組報告 (No basket reports found).")

    # --- Tab 2: ETF 聰明錢 ---
    with tab_smart:
        st.subheader("ETF 資金流追蹤 (Smart Money Tracker)")
        # 注意：權限 Key 維持原樣以確保資料庫對應，但描述已中文化
        if utils.check_access_or_show_teaser("ETF資金流 Smart Money",
                                             description="追蹤槓桿 ETF 資金流向，即時捕捉市場反轉訊號。順勢而為，跟隨機構大戶資金浪潮。"):
            html_content, _ = utils.get_latest_file_content("xETF", "ETF_Smart_Money_Report_*.html")
            if html_content:
                components.html(html_content, height=2000, scrolling=True)
            else:
                st.warning("⚠️ 找不到 ETF 資金流報告。")

    # --- Tab 3: S&P 500 熱力圖 ---
    with tab_sp500:
        st.subheader("標普 500 表現熱力圖 (年初至今)")
        html_content, _ = utils.get_latest_file_content("Stock", "sp500_clean_heatmap_*.html")
        if html_content:
            components.html(html_content, height=1600, scrolling=True)
        else:
            st.warning("⚠️ 找不到 S&P 500 熱力圖。")

    # --- Tab 4: 板塊熱力圖 ---
    with tab_sector:
        st.subheader("行業板塊熱力圖 (Sector Heatmap)")
        html_content, _ = utils.get_latest_file_content("MarketDashboard", "sector_etf_heatmap_*.html")
        if html_content:
            st.caption("顯示報告")
            components.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("⚠️ 找不到板塊熱力圖。")

    # --- Tab 5: 技術評分 ---
    with tab_ta:
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

    # --- Tab 6: 業績公佈 ---
    with tab_earn:
        st.subheader("財報行事曆分析 (Earnings Calendar)")
        html, _ = utils.get_latest_file_content("Earnings")
        if html:
            components.html(html, height=2500, scrolling=True)
        else:
            st.warning("⚠️ 找不到財報報告。")

    # --- Tab 7: 內部交易 ---
    with tab_insider:
        st.subheader("內部人士交易活動 (Insider Trading)")
        if utils.check_access_or_show_teaser("內部交易 Insider",
                                             description="查看 CEO 和 CFO 如何操作自家股票。即時叢集買入 (Cluster Buying) 警示。"):
            html, _ = utils.get_latest_file_content("Insider", "Insider_Trading_Report_*.html")
            if html:
                components.html(html, height=2000, scrolling=True)
            else:
                st.warning("⚠️ 找不到內部交易報告。")

    # --- Tab 8: 挾淡倉 ---
    with tab_squeeze:
        st.subheader("短拉補/挾淡倉掃描 (Short Squeeze Scanner)")
        if utils.check_access_or_show_teaser("挾淡倉 Short Squeeze",
                                             description="在爆發前識別下一個 GME/AMC。高沽空比率 + 高借貸成本掃描。"):
            html, _ = utils.get_latest_file_content("Short_squeeze", "Short_squeeze_*.html")
            if html:
                components.html(html, height=2000, scrolling=True)
            else:
                st.warning("⚠️ 找不到挾淡倉報告。")

    # --- Tab 9: 股票基因 ---
    with tab_dna:
        st.subheader("股票因子基因 (Stock Factor DNA)")
        if utils.check_access_or_show_teaser("因子模型 Stock DNA",
                                             description="利用 Fama-French 模型發掘驅動股價的隱藏因子。"):
            html = utils.load_stock_dna_with_injection(os.getcwd())
            if html and "HTML not found" not in html:
                components.html(html, height=1200, scrolling=True)
            else:
                st.error("找不到 FamaFrench/index.html")

    # --- Tab 10: 波動率策略 ---
    with tab_vol:
        st.subheader("波動率目標控制策略 (Volatility Target)")
        if utils.check_access_or_show_teaser("波動率策略 Volatility Target",
                                             description="獲取專業級波動率控制策略工具。"):
            html, _ = utils.get_latest_file_content("VolTarget", "vol_tool_*.html")
            if html:
                components.html(html, height=1500, scrolling=True)
            else:
                st.warning("⚠️ 找不到波動率工具。")

    # --- Tab 11: 價量分佈 ---
    with tab_vp:
        st.subheader("個股成交量分佈圖 (Volume Profile)")
        st.caption("支撐與壓力位及 SFP 策略背景分析")

        # 使用現有的權限檢查 Key: "Stock VP"
        if utils.check_access_or_show_teaser("Stock VP",
                                             description="專業級價量分佈 (Volume Profile) 儀表板，含 SFP 策略及關鍵價位識別。"):
            # 在 'VP' 資料夾中尋找 'vp_dashboard_*.html'
            html, filename = utils.get_latest_file_content("VP", "vp_dashboard_*.html")

            if html:
                st.caption(f"📅 數據生成時間: {filename}")
                components.html(html, height=1350, scrolling=True)
            else:
                st.warning("⚠️ 找不到價量分佈儀表板 (請先執行生成腳本)。")