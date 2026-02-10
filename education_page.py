import streamlit as st
from streamlit_option_menu import option_menu
import os


def render_winning_roadmap():
    """
    Renders the 7-Step Winning Roadmap content (Traditional Chinese Version).
    """
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%); padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid #3b82f6;">
        <h2 style="color: white; margin:0; text-align:center;">🦅 Alpha 獲利方程式：七步成詩</h2>
        <p style="color: #bfdbfe; text-align:center; margin-top:5px;">如何系統化運用 ParisTrader 工具尋找致勝交易 (SOP)。</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 1
    with st.expander("第一步：觀天測市 (宏觀大勢) 🌧️☀️", expanded=True):
        st.markdown("""
        **目標：** 判斷當下應該積極進攻 (Risk-On) 還是防守現金 (Risk-Off)。

        * **前往：** `📡 Market Radar (大市雷達)`
        * **檢查：** `⚠️ Risk Meter (恐慌指數)`
            * 🟢 **低風險 (Low Risk)：** 綠燈，放心買入。
            * 🔴 **高風險 (High Risk)：** 現金為王，切勿強行交易。
        * **檢查：** `🌊 Market Breadth (市場寬度)`
            * 大部分股票都在漲嗎？如果只有 NVDA 在升但其他都在跌，這是假升市。
        """)

    # Step 2
    with st.expander("第二步：尋找水流 (板塊輪動) 🌊", expanded=False):
        st.markdown("""
        **目標：** 順勢而為，資金流向哪裡，我們就去哪裡。

        * **前往：** `🦅 US Stock Market Analytics (美股獵人)`
        * **檢查：** `🚀 Smart Money (ETF)`
            * 觀察哪些板塊正在獲得資金流入。
        * **檢查：** `🗺️ Sector Heatmap`
            * 識別當日最強勢的板塊龍頭。
        """)

    # Step 3
    with st.expander("第三步：鎖定目標 (個股篩選) 🎯", expanded=False):
        st.markdown("""
        **目標：** 萬中選一，找出跑得最快的馬。

        * **前往：** `🦅 US Stock Market Analytics`
        * **檢查：** `🚦 TA Score`
            * 尋找動量評分 (Momentum Score) **> 70** 的股票。
            * 參考 FATE神指標 生成的 **TP (止盈)** 與 **SL (止損)** 位置。
        * **檢查：** `🕴️ Insider (內部交易)`
            * CEO 有沒有自己掏錢買股票？這是最強的信心投票。
        """)

    # Step 4
    with st.expander("第四步：驗明正身 (基本面 DNA) 🧬", expanded=False):
        st.markdown("""
        **目標：** 避開「老千股」與破產風險。

        * **前往：** `🦅 US Stock Market Analytics` -> `🧬 Stock DNA`
        * **動作：** 輸入你的股票代碼 (Ticker)。
            * **質量因子 (Quality Factor)：** 必須及格。除非你是做即日鮮，否則避開「垃圾級」股票。
            * **價值因子 (Value Factor)：** 股價是否嚴重高估？
        * *法則：* 高動量 + 高質量 = **Alpha (超額回報)**。
        """)

    # Step 5
    with st.expander("第五步：狙擊入場 (籌碼分佈 VP) 🔫", expanded=False):
        st.markdown("""
        **目標：** 精準打擊，絕不追高。

        * **前往：** `🦅 US Stock Market Analytics` -> `📊 Stock VP`
        * **SFP 假跌破策略 (Swing Failure Pattern)：**
            1.  尋找下方的 **藍色支撐線**。
            2.  等待股價跌 **穿** 該線。
            3.  **當股價重新收盤站回該線上方時買入。** (這就是淡友被挾的時刻)。
        * **目標：** 上方的 **紅色阻力線**。
        """)

    # Step 6
    with st.expander("第六步：確認訊號 (期權異動) 🐳", expanded=False):
        st.markdown("""
        **目標：** 看看「大戶 (Whales)」是否與你看法一致，並快速制定期權策略。

        * **前往：** `🎯 Option Flow (期權佈局)`
        * **檢查：** `Unusual Activity (異動)`
            * 有大戶在買入 Call 嗎？
        * **檢查：** `Gamma Levels`
            * 上方是否有 "Call Wall" 形成磁鐵效應？
        * **實戰佈局：** `🛠️ Strategy Simulator (策略模擬器)`
            * **自動生成：** 根據你的看好/看淡方向，一鍵生成對應的期權組合（如 Bull Call Spread）。
            * **智能選股：** 系統會自動篩選最合適的 **行使價 (Strike)** 與 **到期日 (Expiry)**。
            * **可視化決策：** 實時查看 **Payoff Diagram (損益圖)** 與 **Breakeven Point (盈虧平衡點)**，確保在進場前對風險回報比瞭然於胸，實現更快、更專業的交易決策。
        """)

    # Step 7
    with st.expander("第七步：名師驗證 (專家觀點) 👨‍🏫", expanded=False):
        st.markdown("""
        **目標：** 與專業操盤手的部署進行對齊。

        * **前往：** `每日復盤`
            * 閱讀每日分析，檢查自己是否有盲點。
        * **前往：** `實戰持倉`
            * 看看 Paris 是在做多、做空，還是正在對沖。
        """)

    st.info(
        "💡 **Pro Tip:** 交易是 **80% 的等待** 加上 **20% 的執行**。耐心等待上述 7 個步驟中至少符合 5 個，勝率將大幅提升。")


def render_education_page(check_access_func, load_markdown_func):
    """
    Renders the Education page with Tabs.
    Requires passing the security check function and markdown loader function from main app.
    """
    st.title("🎓 量化交易學院 (Quant Academy)")
    st.caption("Institutional Trading Knowledge & Strategies")

    # Define Tabs
    tab_roadmap, tab_edu, tab_video = st.tabs(["🚀 致勝地圖 (Roadmap)", "📚 知識庫 (Articles)", "🎥 影片教學 (Videos)"])

    # --- TAB 1: Roadmap ---
    with tab_roadmap:
        render_winning_roadmap()

    # --- TAB 2: Knowledge Base (Articles) ---
    with tab_edu:
        # 1. 定義文章清單
        articles = {
            # --- 第一階段：MT5 自動化交易 (Free / Lead Magnet) ---
            "mt5_ea_install": {
                "title": "第01課 | [EA] 躺平交易第一步：MT5 EA 安裝全攻略",
                "file": "34_mt5_ea_installation.md",
                "icon": "📂",
                "desc": "無需編程知識，手把手教你啟動自動交易引擎，讓電腦為你 24 小時打工。"
            },
            "ea_manual": {
                "title": "第02課 | [EA] 告別手忙腳亂：Paris 摩打手輔助系統",
                "file": "4_mt5_ea_manual.md",
                "icon": "🤖",
                "desc": "秒速下單、隱形止損、一鍵反手。將你的手速提升至機構交易員水平。"
            },
            "fate_indicator": {
                "title": "第03課 | [EA] 趨勢導航：Fate 系統自動繪製買賣點",
                "file": "6_paris_fate_indicator_guide.md",
                "icon": "🧭",
                "desc": "不要再憑感覺畫線。讓 Fate 系統透過波動率運算，告訴你精準的 TP/SL 位置。"
            },
            "gold_excalibur": {
                "title": "第04課 | [EA] 黃金現金流：Excalibur 自動馬丁策略",
                "file": "5_paris_gold_excalibur.md",
                "icon": "⚔️",
                "desc": "專為 XAUUSD 設計的動態網格策略，在震盪市中自動收割點數。"
            },

            # --- 第二階段：交易員心法與認知 (Mindset - VIP) ---
            "trading_career_reality": {
                "title": "第05課 | [心法] 全職交易的真相：如何面對家人與孤獨 ",
                "file": "36_trading_career_reality.md",
                "icon": "🧗",
                "desc": "交易不是賭博，是一門生意。如何建立正確的預期，並獲得家人的支持？"
            },
            "metal_lesson": {
                "title": "第06課 | [心法] 鋼鐵心態：如何戒掉「手多」與「追單」 ",
                "file": "10_Mastering Trading Psychology.md",
                "icon": "🧠",
                "desc": "跳出情緒陷阱。為什麼你總是在最低點止損？學會像機器人一樣執行交易。"
            },
            "trading_psychology_focus": {
                "title": "第07課 | [心法] 懶人交易法：設好離手 (Set & Forget) ",
                "file": "35_trading_psychology_no_peeking.md",
                "icon": "🃏",
                "desc": "為什麼越勤勞越輸錢？學會這一招，減少 80% 因盯盤而犯的低級錯誤。"
            },
            "four_hearts_discipline": {
                "title": "第08課 | [心法] 概率思維：連續虧損後的心理重建 ",
                "file": "37_four_hearts_discipline.md",
                "icon": "❤️",
                "desc": "耐心、細心、決心、狠心。接受虧損是交易的一部分，才能捕捉下一波大行情。"
            },
            "kung_fu_trading": {
                "title": "第09課 | [心法] 功夫哲學：交易只有一橫一直 ",
                "file": "38_kung_fu_trading.md",
                "icon": "🥋",
                "desc": "贏家站著，輸家躺下。簡化你的交易系統，專注於唯一的重點：盈虧比。"
            },
            "day_trading_edge": {
                "title": "第10課 | [心法] 散戶優勢：為何日內交易能戰勝大戶？ ",
                "file": "39_day_trading_philosophy.md",
                "icon": "⚡",
                "desc": "大戶船大難轉彎，散戶船小好調頭。利用「靈活性」成為市場中的游擊隊。"
            },
            "risk_adjusted_return": {
                "title": "第11課 | [心法] 散戶覺醒：拒絕「一年十倍」的賭徒陷阱",
                "file": "47_risk_adjusted_return.md",
                "icon": "🛡️",
                "desc": "為何上班族不應追求暴利？了解 Risk-Adjusted Return 與機構選股思維。"
            },

            # --- 第三階段：工欲善其事 (Setup & Risk - VIP) ---
            "tv_setup": {
                "title": "第12課 | [工具] 打造你的戰情室：TradingView 專業設定 🔒",
                "file": "11_TradingView Setup Guide.md",
                "icon": "⚙️",
                "desc": "別用預設圖表交易！從零開始搭建「四圖流」監控系統，一眼看穿市場全貌。"
            },
            "ib_hotkeys": {
                "title": "第13課 | [工具] 極速下單：IB TWS 快捷鍵設定攻略 🔒",
                "file": "28_ib_hotkeys_setup.md",
                "icon": "⌨️",
                "desc": "炒末日輪必備！設定一鍵 Buy/Sell，比散戶快 2 秒進場，滑價也能變利潤。"
            },
            "risk_sizing": {
                "title": "第14課 | [風控] 拒絕爆倉：ATR 動態注碼管理 ",
                "file": "8_volatility_sizing.md",
                "icon": "⚖️",
                "desc": "為什麼你的止損總是太窄？學會根據市場波動率調整倉位，像基金經理一樣控盤。"
            },
            "risk_calculator": {
                "title": "第15課 | [風控] 保命神器：動態手數計算機 (Excel) 🔒",
                "file": "14_dynamic_lot_size_guide.md",
                "icon": "🧮",
                "desc": "工具下載：輸入淨值與止損點，自動計算安全手數。交易納指、黃金必備。"
            },
            "sharpe_ratio": {
                "title": "第16課 | [風控] 賺錢是運氣還是實力？Sharpe Ratio 詳解 ",
                "file": "41_sharpe_ratio_explained.md",
                "icon": "📊",
                "desc": "如何分辨「運氣好的賭徒」與「穩定的交易員」？用數學驗證你的策略能否長存。"
            },

            # --- 第四階段：ParisTrader 核心系統 (System - VIP) ---
            "paris_manual": {
                "title": "第17課 | [系統] ParisTrader 實戰手冊：四圖流操盤法 🔒",
                "file": "15_paris_system_manual.md",
                "icon": "📘",
                "desc": "完整收錄我的核心系統：如何結合 ST/VV 指標，在單邊行情中吃到最長的一段。"
            },
            "vp_tutorial": {
                "title": "第18課 | [指標] 尋找大戶成本區：Volume Profile (VP) 實戰 🔒",
                "file": "13_Volume Profile Tutorial.md",
                "icon": "📊",
                "desc": "價格會騙人，成交量不會。找出機構的「吸籌區」與「派發區」，精準抄底逃頂。"
            },
            "volume_v2": {
                "title": "第19課 | [指標] 識破假突破：Volume v2 買賣盤分析 🔒",
                "file": "17_volume_indicator_v2.md",
                "icon": "📶",
                "desc": "獨家指標：將成交量拆解為「主動買」與「主動賣」，一眼識破主力誘多誘空。"
            },
            "vv_tutorial": {
                "title": "第20課 | [指標] 捕捉暴漲前夕：VV 與 ST 的黃金交叉 🔒",
                "file": "12_VV Indicator Tutorial.md",
                "icon": "📈",
                "desc": "學會觀察波動率 (VV) 與趨勢 (ST) 的共振點，在行情發動的第一秒進場。"
            },
            "bull_diamond_strategy": {
                "title": "第21課 | [戰法] 鑽石形態：高勝率右側交易策略 🔒",
                "file": "40_bull_diamond_strategy.md",
                "icon": "💎",
                "desc": "什麼是「晨鑽」訊號？如何利用這套戰法，在回調結束時精準切入。"
            },
            "st_table": {
                "title": "第22課 | [神器] 趨勢儀表板：ST Table 多時框監控 🔒",
                "file": "16_st_table_guide.md",
                "icon": "🗓️",
                "desc": "不用切換圖表，一眼看清 1m 到 4h 的趨勢方向，順勢交易必備工具。"
            },
            "trend_table": {
                "title": "第23課 | [神器] 全市場雷達：Trend Table 搵食訊號 🔒",
                "file": "20_trend_table_guide.md",
                "icon": "🧭",
                "desc": "自動掃描全市場。當 EMA, VV, ST 同時亮綠燈，就是最強的「全共識」進場點。"
            },
            "trendtable_alert": {
                "title": "第24課 | [神器] 盯盤救星：設定 TrendTable 手機警報 🔒",
                "file": "33_trendtable_alert_setup.md",
                "icon": "🔔",
                "desc": "上班族必學！如何讓 TradingView 自動監控，訊號出現直接推送到手機。"
            },
            "rsi_table": {
                "title": "第25課 | [神器] 短線爆發力：RSI 當炒股掃描 🔒",
                "file": "19_rsi_hot_table.md",
                "icon": "🔥",
                "desc": "每日掃描 RSI 強勢區資產。一眼找出這幾天資金最集中、最易炒作的標的。"
            },
            "tv_heatmap": {
                "title": "第26課 | [神器] 資金流向圖：期貨動能 Heatmap 🔒",
                "file": "7_tv_volume_heatmap.md",
                "icon": "🗺️",
                "desc": "一眼看穿全球資金在買什麼？利用 Z-Score 找出當日最強與最弱的板塊。"
            },

            # --- 第五階段：期貨與衍生品基礎 (Futures - VIP) ---
            "cfd_basis": {
                "title": "第27課 | [期貨] 差價陷阱：Future vs CFD 換算攻略 🔒",
                "file": "18_cfd_basis_calculator.md",
                "icon": "💱",
                "desc": "解決看期貨做 CFD 的點差難題，避免因為「水位」問題而被掃止損。"
            },
            "basis_theory": {
                "title": "第28課 | [期貨] 水位理論：為何牛牛報價跟期貨不同？ 🔒",
                "file": "29_basis_theory_manual.md",
                "icon": "🌊",
                "desc": "深入理解基差 (Basis) 變動原理，利用轉倉期捕捉套利空間。"
            },
            "cbbc_street_map": {
                "title": "第29課 | [牛熊] 屠牛殺熊：解讀街貨圖與投行對沖 🔒",
                "file": "31_cbbc_street_map.md",
                "icon": "🎯",
                "desc": "為什麼「打靶」後市況會反轉？從投行 Delta Hedging 角度，預測莊家的殺跌目標價。"
            },

            # --- 第六階段：期權大師班 (Options - VIP) ---
            "option_pricing_101": {
                "title": "第30課 | [期權] 拒絕做水魚！拆解 BS Model 定價原理 🔒",
                "file": "21_option_pricing_101.md",
                "icon": "🎓",
                "desc": "別被莊家報價忽悠。學會分辨期權是「平」還是「貴」，只在值博率高時出手。"
            },
            "bs_model_excel": {
                "title": "第31課 | [期權] 定價計算機：一鍵算出合理期權價 (Excel) 🔒",
                "file": "27_bs_model_excel.md",
                "icon": "🧮",
                "desc": "工具下載：輸入股價與 IV，立即知道莊家有沒有「食價」。"
            },
            "bull_call": {
                "title": "第32課 | [期權] 降低成本：Bull Call Spread 實戰攻略 ",
                "file": "2_bull_call_spread.md",
                "icon": "🐂",
                "desc": "看對市卻輸時間值？學會價差策略，用低成本博取倍數回報。"
            },
            "naked_long": {
                "title": "第33課 | [期權] 買 Call 必死？Naked Long 的生存法則 ",
                "file": "3_naked_long_strategy.md",
                "icon": "⏳",
                "desc": "為什麼橫盤不要買 Weekly？Python 數據回測告訴你，何時才適合「單邊下注」。"
            },
            "option_t0_strategy": {
                "title": "第34課 | [期權] T+0 戰法：利用 Gamma 暴漲賺快錢 🔒",
                "file": "22_option_t0_strategy.md",
                "icon": "🚀",
                "desc": "利用期權非線性特性，在單日內實現極致風險回報比的即日鮮技術。"
            },
            "itm_vs_otm": {
                "title": "第35課 | [期權] 價內 vs 價外：末日輪選股心法 🔒",
                "file": "23_itm_vs_otm_puts.md",
                "icon": "📐",
                "desc": "深度解析 Delta 與 Gamma。想博十倍回報，該選哪一個行使價 (Strike)？"
            },
            "iv_expected_move": {
                "title": "第36課 | [期權] 預測波幅：如何用 IV 算出目標價？ 🔒",
                "file": "45_iv_expected_move.md",
                "icon": "⚡",
                "desc": "莊家已經把答案寫在 IV 裡了。學會公式，計算股票今日的「預期最高/最低點」。"
            },
            "vol_crush": {
                "title": "第37課 | [期權] 避開 IV Crush：財報季生存指南 ",
                "file": "24_vol_crush_explained.md",
                "icon": "📉",
                "desc": "為什麼業績大升，你的 Call 卻輸錢？詳解波動率暴跌現象與對策。"
            },
            "oi_settlement": {
                "title": "第38課 | [期權] 最大痛點：利用 OI 預測結算價 🔒",
                "file": "25_oi_settlement_logic.md",
                "icon": "📍",
                "desc": "為什麼股價總是在某個區間結算？看穿莊家 Max Pain，跟著莊家收租。"
            },
            "dividend_marking": {
                "title": "第39課 | [期權] 除息陷阱：股息如何影響期權價格 🔒",
                "file": "26_dividend_marking.md",
                "icon": "🔖",
                "desc": "了解 Forward Curve。別讓股息除淨導致你的 Put/Call 莫名虧損。"
            },

            # --- 第七階段：機構級量化 (Quant - VIP) ---
            "risk_monitor_guide": {
                "title": "第40課 | [量化] 逃頂訊號：Risk Dashboard 使用指南 ",
                "file": "9_risk_dashboard_guide.md",
                "icon": "📟",
                "desc": "學會解讀 VIX, Skew 與 Z-Score。在大跌發生前，識別市場的恐慌訊號。"
            },
            "stock_dna": {
                "title": "第41課 | [量化] 揀股黑科技：Stock DNA 因子掃描 ",
                "file": "1_stock_dna_guide.md",
                "icon": "🧬",
                "desc": "如何使用 Fama-French 模型，拆解股票的「基因」，找出被低估的優質股。"
            },
            "cftc_cot_report": {
                "title": "第42課 | [量化] 跟蹤聰明錢：CFTC 倉位報告實戰 🔒",
                "file": "42_cftc_cot_report.md",
                "icon": "🐋",
                "desc": "每週更新。教你解讀 Commercials (大戶) 持倉，看穿長線資金流向。"
            },
            "dispersion_trading": {
                "title": "第43課 | [量化] 投行秘技：Dispersion Trading (分散度交易) 🔒",
                "file": "43_dispersion_trading.md",
                "icon": "⚖️",
                "desc": "無需預測方向也能賺錢？揭秘投行如何利用指數與個股的波動率錯價進行套利。"
            },
            "bergomi_model": {
                "title": "第44課 | [量化] 波動率模型：Bergomi Model 簡介 🔒",
                "file": "44_bergomi_model.md",
                "icon": "♾️",
                "desc": "高階視角：描述波動率動態與微笑曲線的數學模型，適合量化發燒友。"
            },
            "totem_valuation": {
                "title": "第45課 | [量化] 大戶的答案紙：Totem 估值揭秘 🔒",
                "file": "30_totem_valuation.md",
                "icon": "🤫",
                "desc": "揭開投行如何利用 Totem 服務，為 OTC 衍生品進行定價與風控。"
            },
            "daily_chart_scorecard": {
                "title": "第46課 | [量化] 拒絕憑感覺：日圖計分表 (Scorecard) 📝",
                "file": "45_Daily_Chart_Scorecard.md",
                "icon": "✅",
                "desc": "將盤感數據化。建立一套機械化的進場標準，分數不夠絕不出手。"
            },
            "factor_mri": {
                "title": "第47課 | [量化] 市場 MRI：用因子 Z-Score 看穿板塊輪動 🧬",
                "file": "46_factor_mri.md",
                "icon": "📊",
                "desc": "資金正在流向價值股還是成長股？用數據識別當下的市場主線。"
            },
        }

        # 2. 建立兩欄佈局：左邊是文章列表，右邊是內容閱讀區
        col_list, col_content = st.columns([1, 2.5], gap="large")

        with col_list:
            st.markdown("### 📚 文章列表 (Article List)")

            # 準備選單需要的標題列表和圖標列表
            options_titles = [data["title"] for data in articles.values()]
            options_icons = [data["icon"] for data in articles.values()]

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
                        st.stop()  # 停止渲染

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

    # --- TAB 3: Video Tutorials ---
    with tab_video:
        st.subheader("📺 影片教學 (Video Tutorials)")
        st.video("https://www.youtube.com/watch?v=qb3XtEPj8cA")
        st.caption("網站使用教學 (Walkthrough)")

        st.markdown("---")
        st.info("🔥 更多實戰影片將陸續上架，涵蓋 EA 安裝演示與期權操作實錄。")