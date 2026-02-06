import streamlit as st
import streamlit.components.v1 as components
import os
import utils


def render_stock_page():
    st.title("🇺🇸 US Stock Market Analytics")
    st.caption("Institutional Data, Heatmaps & Factor Analysis")

    # [UPDATED] Define the Tabs (Added "Stock VP" at the end)
    tab_basket, tab_smart, tab_sp500, tab_sector, tab_ta, tab_earn, tab_insider, tab_squeeze, tab_dna, tab_vol, tab_vp = st.tabs(
        ["🧺 Thematic Basket", "🚀 Smart Money", "🔥 S&P 500", "🗺️ Sector", "🚦 TA Score",
         "📅 Earnings", "🕴️ Insider", "⚡ Short Squeeze", "🧬 Stock DNA", "📉 Volatility", "📊 Stock VP"])

    # --- Tab 1: Thematic Basket ---
    with tab_basket:
        st.subheader("Thematic Basket Analysis")
        html_content, fn = utils.get_latest_file_content("ThematicBasket", "elite_dashboard_*.html")
        if html_content:
            st.caption(f"📅 Strategy Report: {fn}")
            components.html(html_content, height=6000, scrolling=True)
        else:
            st.warning("⚠️ No basket reports found.")

    # --- Tab 2: ETF Smart Money ---
    with tab_smart:
        st.subheader("ETF Smart Money Tracker")
        if utils.check_access_or_show_teaser("ETF資金流 Smart Money",
                                             description="Track leveraged ETF flows to spot market reversals instantly. Don't fight the trend, ride the institutional wave."):
            html_content, _ = utils.get_latest_file_content("xETF", "ETF_Smart_Money_Report_*.html")
            if html_content:
                components.html(html_content, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No ETF Smart Money reports found.")

    # --- Tab 3: S&P 500 Heatmap ---
    with tab_sp500:
        st.subheader("S&P 500 Performance Heatmap (YTD)")
        html_content, _ = utils.get_latest_file_content("Stock", "sp500_clean_heatmap_*.html")
        if html_content:
            components.html(html_content, height=1600, scrolling=True)
        else:
            st.warning("⚠️ No S&P 500 Heatmap found.")

    # --- Tab 4: Sector Heatmap ---
    with tab_sector:
        st.subheader("Industry Sector Heatmap")
        html_content, _ = utils.get_latest_file_content("MarketDashboard", "sector_etf_heatmap_*.html")
        if html_content:
            st.caption("Displaying Report")
            components.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Sector Heatmap not found.")

    # --- Tab 5: TA Score ---
    with tab_ta:
        st.subheader("Technical Analysis Score")
        sub_us, sub_hk = st.tabs(["US Market", "HK Market"])
        with sub_us:
            html, _ = utils.get_latest_file_content("Stock", "TA_score_heatmap_*.html")
            if html:
                components.html(html, height=1200, scrolling=True)
            else:
                st.warning("⚠️ US Report not found.")
        with sub_hk:
            html_hk, _ = utils.get_latest_file_content("Stock", "HK_TA_score_heatmap_*.html")
            if html_hk:
                components.html(html_hk, height=1200, scrolling=True)
            else:
                st.warning("⚠️ HK Report not found.")

    # --- Tab 6: Earnings ---
    with tab_earn:
        st.subheader("Earnings Calendar Analysis")
        html, _ = utils.get_latest_file_content("Earnings")
        if html:
            components.html(html, height=2500, scrolling=True)
        else:
            st.warning("⚠️ No earnings reports found.")

    # --- Tab 7: Insider Trading ---
    with tab_insider:
        st.subheader("Insider Trading Activity")
        if utils.check_access_or_show_teaser("內部交易 Insider",
                                             description="See what CEOs and CFOs are doing with their own money. Real-time cluster buying alerts."):
            html, _ = utils.get_latest_file_content("Insider", "Insider_Trading_Report_*.html")
            if html:
                components.html(html, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No Insider Trading reports found.")

    # --- Tab 8: Short Squeeze ---
    with tab_squeeze:
        st.subheader("Short Squeeze Scanner")
        if utils.check_access_or_show_teaser("挾淡倉 Short Squeeze",
                                             description="Identify the next GME/AMC before it explodes. High short interest + High borrow cost scanner."):
            html, _ = utils.get_latest_file_content("Short_squeeze", "Short_squeeze_*.html")
            if html:
                components.html(html, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No Short Squeeze reports found.")

    # --- Tab 9: Stock DNA ---
    with tab_dna:
        st.subheader("Stock Factor DNA")
        if utils.check_access_or_show_teaser("因子模型 Stock DNA",
                                             description="Discover the hidden factors driving stock prices using Fama-French models."):
            html = utils.load_stock_dna_with_injection(os.getcwd())
            if html and "HTML not found" not in html:
                components.html(html, height=1200, scrolling=True)
            else:
                st.error("FamaFrench/index.html not found")

    # --- Tab 10: Volatility Target ---
    with tab_vol:
        st.subheader("Volatility Target Strategy")
        if utils.check_access_or_show_teaser("波動率策略 Volatility Target",
                                             description="Access professional-grade volatility control strategies."):
            html, _ = utils.get_latest_file_content("VolTarget", "vol_tool_*.html")
            if html:
                components.html(html, height=1500, scrolling=True)
            else:
                st.warning("⚠️ Volatility Tool not found.")

    # --- [NEW] Tab 11: Stock VP ---
    with tab_vp:
        st.subheader("Individual Stock Volume Profile")
        st.caption("Support & Resistance Levels with Strategy Context")

        # Check permission (Optional: You can remove the 'if' check if you want it free for all)
        if utils.check_access_or_show_teaser("Stock VP",
                                             description="Professional Volume Profile dashboard with SFP strategy and key level identification."):
            # Looks for 'vp_dashboard_*.html' inside the 'VP' folder
            html, filename = utils.get_latest_file_content("VP", "vp_dashboard_*.html")

            if html:
                st.caption(f"📅 Data Generated: {filename}")
                # Increased height to accommodate the strategy section and table
                components.html(html, height=1350, scrolling=True)
            else:
                st.warning("⚠️ No Stock VP dashboard found. (Please run the generator script first)")