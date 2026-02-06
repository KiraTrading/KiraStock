import streamlit as st
from streamlit_option_menu import option_menu
import os

def render_education_page(check_access_func, load_markdown_func):
    """
    Renders the Education page.
    Requires passing the security check function and markdown loader function from main app.
    """
    st.title("🎓 Quant Academy")
    st.caption("Institutional Trading Knowledge & Strategies")

    # 1. 定義文章清單 (Moved from app.py)
    articles = {
        # --- 第一階段：MT5 自動化交易 (Free / Lead Magnet) ---
        "mt5_ea_install": {
            "title": "第01課 | [EA] 如何將 EA 安裝到 MT5",
            "file": "34_mt5_ea_installation.md",
            "icon": "📂",
            "desc": "新手必看！手把手教你將 .ex5 / .mq5 檔案正確放入 MT5 資料夾並啟動自動交易。"
        },
        "ea_manual": {
            "title": "第02課 | [EA] Paris摩打手 Assistant",
            "file": "4_mt5_ea_manual.md",
            "icon": "🤖",
            "desc": "告別手動算點數，隱形止損與一鍵反手神器。"
        },
        "fate_indicator": {
            "title": "第03課 | [EA] Fate 趨勢判定反轉系統",
            "file": "6_paris_fate_indicator_guide.md",
            "icon": "🧭",
            "desc": "整合波動率與動能的機構級圖表系統，自動繪製 TP/SL。"
        },
        "gold_excalibur": {
            "title": "第04課 | [EA] 黃金自動現金流馬丁策略",
            "file": "5_paris_gold_excalibur.md",
            "icon": "⚔️",
            "desc": "結合 Fate 趨勢引擎與 ATR 動態網格的機構級黃金策略。"
        },

        # --- 第二階段：交易員心法與認知 (Mindset - VIP) ---
        "trading_career_reality": {
            "title": "第05課 | [心法] 面對家人與孤獨的修煉 ",
            "file": "36_trading_career_reality.md",
            "icon": "🧗",
            "desc": "交易賺錢不過是思考和紀律的副產品。如何獲得家人的理解？交易員必須掌握的 8 大技能樹。"
        },
        "metal_lesson": {
            "title": "第06課 | [心法] 別讓情緒毀了你的交易 ",
            "file": "10_Mastering Trading Psychology.md",
            "icon": "🧠",
            "desc": "跳出情緒陷阱，用我的獨家心法和策略，讓你們交易更穩、更賺！"
        },
        "trading_psychology_focus": {
            "title": "第07課 | [心法] 千萬不要在玩牌的時候數錢 ",
            "file": "35_trading_psychology_no_peeking.md",
            "icon": "🃏",
            "desc": "為什麼越勤勞越輸錢？學會「設好離手」(Set & Forget)，利用 45 分鐘專注法則提高執行力。"
        },
        "four_hearts_discipline": {
            "title": "第08課 | [心法] 四心修煉與概率遊戲 ",
            "file": "37_four_hearts_discipline.md",
            "icon": "❤️",
            "desc": "耐心、細心、決心、狠心。為什麼高勝算入場前必須有止損？短線操作出錯的三大處理原則。"
        },
        "kung_fu_trading": {
            "title": "第09課 | [心法] 功夫兩個字，一橫一直 ",
            "file": "38_kung_fu_trading.md",
            "icon": "🥋",
            "desc": "為什麼交易系統只有兩個重點：入場信號與出場風控？贏家與輸家的區別。"
        },
        "day_trading_edge": {
            "title": "第10課 | [心法] 為什麼選擇日內交易 (Day Trade)？ ",
            "file": "39_day_trading_philosophy.md",
            "icon": "⚡",
            "desc": "為什麼大戶做不到 Day Trade 而散戶可以？這是你的 Edge。升跌不理，市場郁就得。"
        },

        # --- 第三階段：工欲善其事 (Setup & Risk - VIP) ---
        "tv_setup": {
            "title": "第11課 | [工具] TradingView 新手速成 Setup 🔒",
            "file": "11_TradingView Setup Guide.md",
            "icon": "⚙️",
            "desc": "從零開始 Setup，由買數據到安指標，快速搭建你的「四圖流」賺錢戰壇！"
        },
        "ib_hotkeys": {
            "title": "第12課 | [工具] IB TWS 快捷鍵 (Hotkeys) 設定 🔒",
            "file": "28_ib_hotkeys_setup.md",
            "icon": "⌨️",
            "desc": "炒極限期權必備！設定一鍵下單 (Buy/Sell)，告別手動輸入的延遲。"
        },
        "risk_sizing": {
            "title": "第13課 | [風控] 何為波動性「均注」？ ",
            "file": "8_volatility_sizing.md",
            "icon": "⚖️",
            "desc": "贏單常有卻輸在資金管理？學會 ATR 動態注碼，像機構一樣控盤。"
        },
        "risk_calculator": {
            "title": "第14課 | [風控] 動態手數風險計算機 (Excel) 🔒",
            "file": "14_dynamic_lot_size_guide.md",
            "icon": "🧮",
            "desc": "工具下載：根據淨值自動計算安全手數，一鍵看清 XAU 與 NAS100 的合約風險差異。"
        },
        "sharpe_ratio": {
            "title": "第15課 | [風控] 夏普比率 (Sharpe Ratio) ",
            "file": "41_sharpe_ratio_explained.md",
            "icon": "📊",
            "desc": "如何用數學分辨「運氣」與「實力」？拆解衡量策略效率的核心指標。"
        },

        # --- 第四階段：ParisTrader 核心系統 (System - VIP) ---
        "paris_manual": {
            "title": "第16課 | [系統] ParisTrader 獨家操作手冊 🔒",
            "file": "15_paris_system_manual.md",
            "icon": "📘",
            "desc": "完整收錄四圖流架構、ST/VV 核心指標詳解、進出場機制與實戰心法。"
        },
        "vp_tutorial": {
            "title": "第17課 | [指標] Volume Profile (VP) 日內實戰 🔒",
            "file": "13_Volume Profile Tutorial.md",
            "icon": "📊",
            "desc": "不看指標只看量？用 Fixed Range VP 找出機構成本區，捕捉開盤前 5 分鐘機會。"
        },
        "volume_v2": {
            "title": "第18課 | [指標] Volume v2 進階成交量分析 🔒",
            "file": "17_volume_indicator_v2.md",
            "icon": "📶",
            "desc": "獨家分解買賣量，結合 Supertrend 動態均線，自動標記 CC/PP 爆量信號。"
        },
        "vv_tutorial": {
            "title": "第19課 | [指標] VV 指標實戰：結合 ST 判斷趨勢 🔒",
            "file": "12_VV Indicator Tutorial.md",
            "icon": "📈",
            "desc": "學會觀察 VV 與 ST 的黃金交叉，利用多時框共振心法，精準捕捉進出場時機。"
        },
        "bull_diamond_strategy": {
            "title": "第20課 | [戰法] 交易前三問與鑽石指標 🔒",
            "file": "40_bull_diamond_strategy.md",
            "icon": "💎",
            "desc": "什麼是晨鑽/首鑽？如何避免 Reprinting？左側 vs 右側交易詳解。"
        },
        "st_table": {
            "title": "第21課 | [神器] ST Table 多時框趨勢監控 🔒",
            "file": "16_st_table_guide.md",
            "icon": "🗓️",
            "desc": "一眼看清 1m 至 4h 的趨勢方向！自定義 ST 值矩陣，專為期貨短線設計。"
        },
        "trend_table": {
            "title": "第22課 | [神器] Trend Table 全市場趨勢雷達 🔒",
            "file": "20_trend_table_guide.md",
            "icon": "🧭",
            "desc": "整合 EMA, VV, ST 三大系統。全綠/全紅代表最強共識！"
        },
        "trendtable_alert": {
            "title": "第23課 | [神器] TrendTable 自動 Alert 設定 🔒",
            "file": "33_trendtable_alert_setup.md",
            "icon": "🔔",
            "desc": "不想肉眼盯盤？教你如何在 TV 設定「全綠/全紅」的手機彈窗提示。"
        },
        "rsi_table": {
            "title": "第24課 | [神器] 14天 RSI 當炒表 (每日強勢股) 🔒",
            "file": "19_rsi_hot_table.md",
            "icon": "🔥",
            "desc": "每日掃描最強勢資產！一眼找出這幾天最易賺錢的標的 (Daily Chart 專用)。"
        },
        "tv_heatmap": {
            "title": "第25課 | [神器] 期貨動能熱力圖 (Heatmap) 🔒",
            "file": "7_tv_volume_heatmap.md",
            "icon": "🗺️",
            "desc": "一眼看穿大戶資金流向，監控全球 18 大資產 Z-Score。"
        },

        # --- 第五階段：期貨與衍生品基礎 (Futures - VIP) ---
        "cfd_basis": {
            "title": "第26課 | [期貨] Future vs CFD 差價計算機 🔒",
            "file": "18_cfd_basis_calculator.md",
            "icon": "💱",
            "desc": "解決看期貨做 CFD 的點差難題，一鍵換算對應點位。"
        },
        "basis_theory": {
            "title": "第27課 | [期貨] Basis (水位) 理論與手動換算 🔒",
            "file": "29_basis_theory_manual.md",
            "icon": "🌊",
            "desc": "為什麼牛牛的報價跟 CFD 不一樣？深入理解基差變動原理。"
        },
        "cbbc_street_map": {
            "title": "第28課 | [牛熊] 牛熊街貨圖與投行對沖 ",
            "file": "31_cbbc_street_map.md",
            "icon": "🎯",
            "desc": "為什麼「打靶」後市況會反轉？從投行 Delta Hedging 角度找大位 TP。"
        },

        # --- 第六階段：期權大師班 (Options - VIP) ---
        "option_pricing_101": {
            "title": "第29課 | [期權] Option Pricing 定價原理 🔒",
            "file": "21_option_pricing_101.md",
            "icon": "🎓",
            "desc": "投資班第一堂：拆解 BS Model，什麼是 IV？美式與歐式有何分別？"
        },
        "bs_model_excel": {
            "title": "第30課 | [期權] BS Model 定價計算機 (Excel) 🔒",
            "file": "27_bs_model_excel.md",
            "icon": "🧮",
            "desc": "輸入股價、行權價與 IV，一鍵計算期權理論價格與 Greeks，驗證報價是否合理。"
        },
        "bull_call": {
            "title": "第31課 | [期權] Bull Call Spread 實戰詳解 ",
            "file": "2_bull_call_spread.md",
            "icon": "🐂",
            "desc": "看對市卻輸錢？學會這個對沖策略，降低成本抗 Theta。"
        },
        "naked_long": {
            "title": "第32課 | [期權] Naked Long 的時間博弈 ",
            "file": "3_naked_long_strategy.md",
            "icon": "⏳",
            "desc": "為什麼橫盤不要買 Weekly？Python 數據回測告訴你真相。"
        },
        "option_t0_strategy": {
            "title": "第33課 | [期權] T0 實戰 - 風險回報最大化 🔒",
            "file": "22_option_t0_strategy.md",
            "icon": "🚀",
            "desc": "利用期權非線性特性，在單日內實現極致風險回報比的實戰技術。"
        },
        "itm_vs_otm": {
            "title": "第34課 | [期權] ITM vs OTM Put (Greeks解析) 🔒",
            "file": "23_itm_vs_otm_puts.md",
            "icon": "📐",
            "desc": "深度解析 Delta, Gamma, Theta 差異，與 QQQ 末日輪實戰心法。"
        },
        "iv_expected_move": {
            "title": "第35課 | [期權] IV 隱含波動率與預期波幅 🔒",
            "file": "45_iv_expected_move.md",
            "icon": "⚡",
            "desc": "公式詳解：如何用 IV 計算股票每日預期升跌幅，找出操盤手食糊位。"
        },
        "vol_crush": {
            "title": "第36課 | [期權] Vol Crush (波動率暴跌) 詳解 ",
            "file": "24_vol_crush_explained.md",
            "icon": "📉",
            "desc": "詳解財報後 IV Crush 現象與 Apple 實戰案例。"
        },
        "oi_settlement": {
            "title": "第37課 | [期權] OI 未平倉合約與 Max Pain 🔒",
            "file": "25_oi_settlement_logic.md",
            "icon": "📍",
            "desc": "為什麼結算日價格總是在某個範圍？看穿莊家最大痛點 (Max Pain)。"
        },
        "dividend_marking": {
            "title": "第38課 | [期權] 股息標記 (Dividend Marking) 🔒",
            "file": "26_dividend_marking.md",
            "icon": "🔖",
            "desc": "了解除息日如何影響遠期曲線 (Forward Curve) 與期權價值。"
        },

        # --- 第七階段：機構級量化 (Quant - VIP) ---
        "risk_monitor_guide": {
            "title": "第39課 | [量化] 大市雷達：識別見頂/見底 ",
            "file": "9_risk_dashboard_guide.md",
            "icon": "📟",
            "desc": "學會解讀 VIX, Skew 與 Z-Score，像機構一樣捕捉轉折點。"
        },
        "stock_dna": {
            "title": "第40課 | [量化] Stock DNA 因子分析儀 ",
            "file": "1_stock_dna_guide.md",
            "icon": "🧬",
            "desc": "如何使用 Fama-French 模型工具拆解持倉風險與屬性。"
        },
        "cftc_cot_report": {
            "title": "第41課 | [量化] CFTC COT 倉位報告解讀 🔒",
            "file": "42_cftc_cot_report.md",
            "icon": "🐋",
            "desc": "教你解讀 Commercials vs Speculators，看清大資金流向。"
        },
        "dispersion_trading": {
            "title": "第42課 | [量化] Dispersion Trading (分散度交易) 🔒",
            "file": "43_dispersion_trading.md",
            "icon": "⚖️",
            "desc": "投行波動率套利策略。利用期權定價錯位，無需預測方向也能獲利。"
        },
        "bergomi_model": {
            "title": "第43課 | [量化] Bergomi 模型與粗糙波動率 🔒",
            "file": "44_bergomi_model.md",
            "icon": "♾️",
            "desc": "高階數學：描述波動率動態與曲面微笑的模型。"
        },
        "totem_valuation": {
            "title": "第44課 | [量化] 投行揭秘：大戶的答案紙 Totem 🔒",
            "file": "30_totem_valuation.md",
            "icon": "🤫",
            "desc": "揭開投行如何利用 Totem 進行 OTC 衍生品估值與風控的內幕。"
        },
        "daily_chart_scorecard": {
            "title": "第45課 | [量化] 日圖計分表：將盤感數據化 📝",
            "file": "45_Daily_Chart_Scorecard.md",
            "icon": "✅",
            "desc": "學會將主觀的圖表分析轉化為客觀的數據評分，建立機械化的進場標準，拒絕情緒交易。"
        },
        "factor_mri": {
            "title": "第46課 | [量化] 市場 MRI：解讀 Pure Factor Z-Score 🧬",
            "file": "46_factor_mri.md",
            "icon": "📊",
            "desc": "教你如何透過「因子 Z-Score」看穿大市漲跌背後的資金流向，識別板塊輪動與避險模式。"
        },
    }

    # 準備選單需要的標題列表和圖標列表
    options_titles = [data["title"] for data in articles.values()]
    options_icons = [data["icon"] for data in articles.values()]

    # 2. 建立兩欄佈局：左邊是文章列表，右邊是內容閱讀區
    col_list, col_content = st.columns([1, 2.5], gap="large")

    with col_list:
        st.markdown("### 📚 Article List")

        # 使用 option_menu 顯示文章列表
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
        # 根據選中的 Title 找回對應的 Article 資料
        current_article = next((item for item in articles.values() if item["title"] == selected_title), None)

        if current_article:
            # === [權限檢查邏輯] ===
            # 如果標題包含 "🔒" 且用戶未登入 -> 顯示付費牆
            if "🔒" in current_article["title"]:
                # 使用傳入的 check_access_func (即 check_access_or_show_teaser)
                if not check_access_func(current_article['title'],
                                                   description=f"🔒 此教學為 VIP 專屬內容：{current_article['desc']}"):
                    # 如果返回 False，代表未登入，這裡直接停止渲染後續內容
                    return # Stop execution of this function

            # === [內容渲染] (免費或已解鎖) ===
            file_path = os.path.join("Education", current_article["file"])

            # 顯示標題頭
            st.markdown(f"""
            <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #2563EB; margin-bottom: 20px;">
                <h2 style="margin:0; color: white;">{current_article['icon']} {current_article['title'].replace(' 🔒', '')}</h2>
                <p style="margin-top:5px; color: #94a3b8;">{current_article['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

            # 使用傳入的 load_markdown_func 讀取內容
            content = load_markdown_func(file_path)
            st.markdown(content, unsafe_allow_html=True)

            # CTA (僅在免費文章底部顯示升級提示)
            if "🔒" not in current_article["title"]:
                st.divider()
                st.info("💡 喜歡這些自動化工具？ 升級 VIP 會員，解鎖後續 40+ 堂高階心法與策略教學。")
        else:
            st.error("Error loading article.")