import streamlit as st
from streamlit_option_menu import option_menu
import os

# --- Language Setup ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'zh'

translations = {
    "zh": {
        "page_title": "🎓 量化交易學院 (Quant Academy)",
        "page_caption": "Institutional Trading Knowledge & Strategies",
        "tabs": ["🚀 致勝地圖 (Roadmap)", "📚 知識庫 (Articles)", "🎥 影片教學 (Videos)"],
        "roadmap_header": "🦅 Alpha 獲利方程式：七步成詩",
        "roadmap_sub": "如何系統化運用 Kira 的工具尋找致勝交易 (SOP)。",
        "video_sub": "網站使用教學 (Walkthrough)",
        "video_info": "🔥 更多實戰影片將陸續上架，涵蓋 EA 安裝演示與期權操作實錄。",
        "article_list": "📚 文章列表 (Article List)",
        "vip_locked": "🔒 此教學為 VIP 專屬內容",
        "cta": "💡 喜歡這些自動化工具？ 升級 VIP 會員，解鎖後續 40+ 堂高階心法與策略教學。"
    },
    "en": {
        "page_title": "🎓 Quant Trading Academy",
        "page_caption": "Institutional Trading Knowledge & Strategies",
        "tabs": ["🚀 Winning Roadmap", "📚 Knowledge Base", "🎥 Video Tutorials"],
        "roadmap_header": "🦅 The Alpha Formula: 7-Step Roadmap",
        "roadmap_sub": "Systematic SOP to find winning trades.",
        "video_sub": "Platform Walkthrough",
        "video_info": "🔥 More videos on EA installation and Options trading coming soon.",
        "article_list": "📚 Article List",
        "vip_locked": "🔒 VIP Content Only",
        "cta": "💡 Like these tools? Upgrade to VIP to unlock 40+ advanced lessons."
    }
}


def t(key):
    return translations[st.session_state['language']].get(key, key)


def render_winning_roadmap():
    """
    Renders the 7-Step Winning Roadmap content.
    """
    is_zh = st.session_state['language'] == 'zh'

    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%); padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid #3b82f6;">
        <h2 style="color: white; margin:0; text-align:center;">{t('roadmap_header')}</h2>
        <p style="color: #bfdbfe; text-align:center; margin-top:5px;">{t('roadmap_sub')}</p>
    </div>
    """, unsafe_allow_html=True)

    if is_zh:
        # --- Chinese Version ---
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

        with st.expander("第二步：尋找水流 (板塊輪動) 🌊", expanded=False):
            st.markdown("""
            **目標：** 順勢而為，資金流向哪裡，我們就去哪裡。
            * **前往：** `🦅 US Stock Market Analytics (美股獵人)`
            * **檢查：** `🚀 Smart Money (ETF)` - 觀察哪些板塊正在獲得資金流入。
            * **檢查：** `🗺️ Sector Heatmap` - 識別當日最強勢的板塊龍頭。
            """)

        with st.expander("第三步：鎖定目標 (個股篩選) 🎯", expanded=False):
            st.markdown("""
            **目標：** 萬中選一，找出跑得最快的馬。
            * **前往：** `🦅 US Stock Market Analytics`
            * **檢查：** `🚦 TA Score` - 尋找動量評分 (Momentum Score) **> 70** 的股票。
            * **檢查：** `🕴️ Insider (內部交易)` - CEO 有沒有自己掏錢買股票？這是最強的信心投票。
            """)

        with st.expander("第四步：驗明正身 (基本面 DNA) 🧬", expanded=False):
            st.markdown("""
            **目標：** 避開「老千股」與破產風險。
            * **前往：** `🦅 US Stock Market Analytics` -> `🧬 Stock DNA`
            * **動作：** 輸入你的股票代碼 (Ticker)。
                * **質量因子 (Quality Factor)：** 必須及格。
                * **價值因子 (Value Factor)：** 股價是否嚴重高估？
            """)

        with st.expander("第五步：狙擊入場 (籌碼分佈 VP) 🔫", expanded=False):
            st.markdown("""
            **目標：** 精準打擊，絕不追高。
            * **前往：** `🦅 US Stock Market Analytics` -> `📊 Stock VP`
            * **SFP 假跌破策略 (Swing Failure Pattern)：**
                1. 尋找下方的 **藍色支撐線**。
                2. 等待股價跌 **穿** 該線。
                3. **當股價重新收盤站回該線上方時買入。**
            """)

        with st.expander("第六步：確認訊號 (期權異動) 🐳", expanded=False):
            st.markdown("""
            **目標：** 看看「大戶 (Whales)」是否與你看法一致，並快速制定期權策略。
            * **前往：** `🎯 Option Flow (期權佈局)`
            * **檢查：** `Unusual Activity` (有大戶在買入 Call 嗎？)
            * **實戰佈局：** `🛠️ Strategy Simulator` - 自動生成對應的期權組合與損益圖。
            """)

        with st.expander("第七步：名師驗證 (專家觀點) 👨‍🏫", expanded=False):
            st.markdown("""
            **目標：** 與專業操盤手的部署進行對齊。
            * **前往：** `每日復盤` - 閱讀每日分析。
            * **前往：** `實戰持倉` - 看看 Kira 是在做多、做空，還是正在對沖。
            """)

        st.info(
            "💡 **Pro Tip:** 交易是 **80% 的等待** 加上 **20% 的執行**。耐心等待上述 7 個步驟中至少符合 5 個，勝率將大幅提升。")

    else:
        # --- English Version ---
        with st.expander("Step 1: Macro View (Risk On/Off) 🌧️☀️", expanded=True):
            st.markdown("""
            **Goal:** Determine if we should be Risk-On (Aggressive) or Risk-Off (Defensive).
            * **Go To:** `📡 Market Radar`
            * **Check:** `⚠️ Risk Meter`
                * 🟢 **Low Risk:** Green light, safe to buy.
                * 🔴 **High Risk:** Cash is King, do not force trades.
            * **Check:** `🌊 Market Breadth`
                * Are stocks rising broadly? If only NVDA is up but others are down, it's a fake rally.
            """)

        with st.expander("Step 2: Flow Check (Sector Rotation) 🌊", expanded=False):
            st.markdown("""
            **Goal:** Follow the trend. Go where the money flows.
            * **Go To:** `🦅 Stock Hunter`
            * **Check:** `🚀 Smart Money (ETF)` - See which sectors are getting inflows.
            * **Check:** `🗺️ Sector Heatmap` - Identify today's strongest sector leaders.
            """)

        with st.expander("Step 3: Target Lock (Stock Screening) 🎯", expanded=False):
            st.markdown("""
            **Goal:** Pick the fastest horse.
            * **Go To:** `🦅 Stock Hunter`
            * **Check:** `🚦 TA Score` - Look for Momentum Score **> 70**.
            * **Check:** `🕴️ Insider` - Is the CEO buying their own stock?
            """)

        with st.expander("Step 4: Due Diligence (Fundamental DNA) 🧬", expanded=False):
            st.markdown("""
            **Goal:** Avoid "Junk" stocks and bankruptcy risk.
            * **Go To:** `🦅 Stock Hunter` -> `🧬 Stock DNA`
            * **Action:** Enter Ticker.
                * **Quality Factor:** Must pass. Avoid junk unless day trading.
                * **Value Factor:** Is it severely overvalued?
            """)

        with st.expander("Step 5: Sniper Entry (Volume Profile) 🔫", expanded=False):
            st.markdown("""
            **Goal:** Precision strike. Never chase highs.
            * **Go To:** `🦅 Stock Hunter` -> `📊 Stock VP`
            * **SFP Strategy (Swing Failure Pattern):**
                1. Locate the **Blue Support Line** below.
                2. Wait for price to break **below** it.
                3. **Buy when price closes back ABOVE the line.** (Short squeeze moment).
            """)

        with st.expander("Step 6: Confirm Signal (Option Flow) 🐳", expanded=False):
            st.markdown("""
            **Goal:** Check if Whales agree with you.
            * **Go To:** `🎯 Option Flow`
            * **Check:** `Unusual Activity` (Are whales buying Calls?)
            * **Action:** `🛠️ Strategy Simulator` - Generate spreads and payoff diagrams instantly.
            """)

        with st.expander("Step 7: Expert Validation 👨‍🏫", expanded=False):
            st.markdown("""
            **Goal:** Align with professional positioning.
            * **Go To:** `Daily Recap` - Read daily analysis.
            * **Go To:** `Portfolio` - Is Kira Long, Short, or Hedging?
            """)

        st.info(
            "💡 **Pro Tip:** Trading is **80% Waiting** + **20% Execution**. Wait for at least 5 of these 7 steps to align, and your win rate will skyrocket.")


def render_education_page(check_access_func, load_markdown_func):
    """
    Renders the Education page with Tabs.
    Requires passing the security check function and markdown loader function from main app.
    """

    # --- CSS Styles ---
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 20px;
            font-weight: bold;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
             color: #2563EB;
             border-bottom-color: #2563EB;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title(t("page_title"))
    st.caption(t("page_caption"))

    # Define Tabs
    tab_roadmap, tab_edu, tab_video = st.tabs(t("tabs"))

    # --- TAB 1: Roadmap ---
    with tab_roadmap:
        render_winning_roadmap()

    # --- TAB 2: Knowledge Base (Articles) ---
    with tab_edu:
        is_zh = st.session_state['language'] == 'zh'

        # Define articles with conditional titles/desc based on language
        articles = {
            # --- Phase 1: MT5 (Free) ---
            "mt5_ea_install": {
                "title": "第01課 | [EA] 躺平交易第一步：MT5 EA 安裝全攻略" if is_zh else "Lesson 01 | [EA] Setup Guide: MT5 EA Installation",
                "file": "34_mt5_ea_installation.md",
                "icon": "📂",
                "desc": "無需編程知識，手把手教你啟動自動交易引擎。" if is_zh else "No coding needed. Step-by-step guide to starting your auto-trading engine."
            },
            "ea_manual": {
                "title": "第02課 | [EA] 告別手忙腳亂：Kira 摩打手輔助系統" if is_zh else "Lesson 02 | [EA] Kira Assistant System Manual",
                "file": "4_mt5_ea_manual.md",
                "icon": "🤖",
                "desc": "秒速下單、隱形止損、一鍵反手。" if is_zh else "Fast execution, hidden SL, one-click reverse."
            },
            "fate_indicator": {
                "title": "第03課 | [EA] 趨勢導航：Fate 系統自動繪製買賣點" if is_zh else "Lesson 03 | [EA] Fate Trend Indicator Guide",
                "file": "6_paris_fate_indicator_guide.md",
                "icon": "🧭",
                "desc": "讓 Fate 系統透過波動率運算，告訴你精準的 TP/SL 位置。" if is_zh else "Let Fate system calculate precise TP/SL levels using volatility models."
            },
            "gold_excalibur": {
                "title": "第04課 | [EA] 黃金現金流：Excalibur 自動馬丁策略" if is_zh else "Lesson 04 | [EA] Gold Excalibur Strategy",
                "file": "5_paris_gold_excalibur.md",
                "icon": "⚔️",
                "desc": "專為 XAUUSD 設計的動態網格策略。" if is_zh else "Dynamic grid strategy designed specifically for XAUUSD."
            },

            # --- Phase 2: Mindset (VIP) ---
            "trading_career_reality": {
                "title": "第05課 | [心法] 全職交易的真相：如何面對家人與孤獨" if is_zh else "Lesson 05 | [Mindset] Trading Career Reality",
                "file": "36_trading_career_reality.md",
                "icon": "🧗",
                "desc": "交易不是賭博，是一門生意。" if is_zh else "Trading is a business, not gambling. Managing expectations."
            },
            "metal_lesson": {
                "title": "第06課 | [心法] 鋼鐵心態：如何戒掉「手多」與「追單」" if is_zh else "Lesson 06 | [Mindset] Iron Discipline",
                "file": "10_Mastering Trading Psychology.md",
                "icon": "🧠",
                "desc": "學會像機器人一樣執行交易。" if is_zh else "How to stop overtrading and execute like a robot."
            },
            "trading_psychology_focus": {
                "title": "第07課 | [心法] 懶人交易法：設好離手 (Set & Forget)" if is_zh else "Lesson 07 | [Mindset] Set & Forget Method",
                "file": "35_trading_psychology_no_peeking.md",
                "icon": "🃏",
                "desc": "減少 80% 因盯盤而犯的低級錯誤。" if is_zh else "Reduce 80% of errors caused by watching charts all day."
            },
            "four_hearts_discipline": {
                "title": "第08課 | [心法] 概率思維：連續虧損後的心理重建" if is_zh else "Lesson 08 | [Mindset] Probability Thinking",
                "file": "37_four_hearts_discipline.md",
                "icon": "❤️",
                "desc": "接受虧損是交易的一部分。" if is_zh else "Accepting losses as part of the game to catch the next big wave."
            },
            "kung_fu_trading": {
                "title": "第09課 | [心法] 功夫哲學：交易只有一橫一直" if is_zh else "Lesson 09 | [Mindset] Kung Fu Philosophy",
                "file": "38_kung_fu_trading.md",
                "icon": "🥋",
                "desc": "專注於唯一的重點：盈虧比。" if is_zh else "Simplify your system. Focus on Risk:Reward."
            },
            "day_trading_edge": {
                "title": "第10課 | [心法] 散戶優勢：為何日內交易能戰勝大戶？" if is_zh else "Lesson 10 | [Mindset] The Retail Edge",
                "file": "39_day_trading_philosophy.md",
                "icon": "⚡",
                "desc": "利用「靈活性」成為市場中的游擊隊。" if is_zh else "Using agility to beat institutional whales."
            },
            "risk_adjusted_return": {
                "title": "第11課 | [心法] 散戶覺醒：拒絕「一年十倍」的賭徒陷阱" if is_zh else "Lesson 11 | [Mindset] Risk-Adjusted Returns",
                "file": "47_risk_adjusted_return.md",
                "icon": "🛡️",
                "desc": "了解機構選股思維。" if is_zh else "Understand institutional selection logic over gambling for 10x."
            },

            # --- Phase 3: Setup & Risk (VIP) ---
            "tv_setup": {
                "title": "第12課 | [工具] 打造戰情室：TradingView 專業設定 🔒" if is_zh else "Lesson 12 | [Tools] Pro TradingView Setup 🔒",
                "file": "11_TradingView Setup Guide.md",
                "icon": "⚙️",
                "desc": "從零開始搭建「四圖流」監控系統。" if is_zh else "Build your 'Quad-Chart' monitoring system from scratch."
            },
            "ib_hotkeys": {
                "title": "第13課 | [工具] 極速下單：IB TWS 快捷鍵設定攻略 🔒" if is_zh else "Lesson 13 | [Tools] IB TWS Hotkeys Guide 🔒",
                "file": "28_ib_hotkeys_setup.md",
                "icon": "⌨️",
                "desc": "比散戶快 2 秒進場。" if is_zh else "Enter trades 2 seconds faster than the crowd."
            },
            "risk_sizing": {
                "title": "第14課 | [風控] 拒絕爆倉：ATR 動態注碼管理" if is_zh else "Lesson 14 | [Risk] ATR Position Sizing",
                "file": "8_volatility_sizing.md",
                "icon": "⚖️",
                "desc": "學會根據市場波動率調整倉位。" if is_zh else "Adjust position size dynamically based on volatility."
            },
            "risk_calculator": {
                "title": "第15課 | [風控] 保命神器：動態手數計算機 (Excel) 🔒" if is_zh else "Lesson 15 | [Risk] Dynamic Lot Calculator 🔒",
                "file": "14_dynamic_lot_size_guide.md",
                "icon": "🧮",
                "desc": "自動計算安全手數。" if is_zh else "Auto-calculate safe lot sizes for Gold/Nasdaq."
            },
            "sharpe_ratio": {
                "title": "第16課 | [風控] 賺錢是運氣還是實力？Sharpe Ratio 詳解" if is_zh else "Lesson 16 | [Risk] Sharpe Ratio Explained",
                "file": "41_sharpe_ratio_explained.md",
                "icon": "📊",
                "desc": "用數學驗證你的策略能否長存。" if is_zh else "Mathematically verify if your strategy is sustainable."
            },

            # --- Phase 4: System (VIP) ---
            "paris_manual": {
                "title": "第17課 | [系統] KiraTrader 實戰手冊：四圖流操盤法 🔒" if is_zh else "Lesson 17 | [System] Kira Manual: Quad-Chart Method 🔒",
                "file": "15_paris_system_manual.md",
                "icon": "📘",
                "desc": "在單邊行情中吃到最長的一段。" if is_zh else "Catch the longest trend in one-sided markets."
            },
            "vp_tutorial": {
                "title": "第18課 | [指標] 尋找大戶成本區：Volume Profile (VP) 實戰 🔒" if is_zh else "Lesson 18 | [Indicator] Volume Profile Mastery 🔒",
                "file": "13_Volume Profile Tutorial.md",
                "icon": "📊",
                "desc": "找出機構的「吸籌區」與「派發區」。" if is_zh else "Identify institutional accumulation and distribution zones."
            },
            "volume_v2": {
                "title": "第19課 | [指標] 識破假突破：Volume v2 買賣盤分析 🔒" if is_zh else "Lesson 19 | [Indicator] Volume v2 Buying/Selling 🔒",
                "file": "17_volume_indicator_v2.md",
                "icon": "📶",
                "desc": "將成交量拆解為「主動買」與「主動賣」。" if is_zh else "Breakdown volume into Aggressive Buy vs Sell."
            },
            "vv_tutorial": {
                "title": "第20課 | [指標] 捕捉暴漲前夕：VV 與 ST 的黃金交叉 🔒" if is_zh else "Lesson 20 | [Indicator] VV & ST Golden Cross 🔒",
                "file": "12_VV Indicator Tutorial.md",
                "icon": "📈",
                "desc": "在行情發動的第一秒進場。" if is_zh else "Enter at the very first second of a trend burst."
            },
            "bull_diamond_strategy": {
                "title": "第21課 | [戰法] 鑽石形態：高勝率右側交易策略 🔒" if is_zh else "Lesson 21 | [Strategy] Bull Diamond Setup 🔒",
                "file": "40_bull_diamond_strategy.md",
                "icon": "💎",
                "desc": "在回調結束時精準切入。" if is_zh else "Precise entry at the end of a pullback."
            },
            "st_table": {
                "title": "第22課 | [神器] 趨勢儀表板：ST Table 多時框監控 🔒" if is_zh else "Lesson 22 | [Tool] ST Trend Dashboard 🔒",
                "file": "16_st_table_guide.md",
                "icon": "🗓️",
                "desc": "一眼看清 1m 到 4h 的趨勢方向。" if is_zh else "Visualize trend direction from 1m to 4h at a glance."
            },
            "trend_table": {
                "title": "第23課 | [神器] 全市場雷達：Trend Table 搵食訊號 🔒" if is_zh else "Lesson 23 | [Tool] Trend Table Scanner 🔒",
                "file": "20_trend_table_guide.md",
                "icon": "🧭",
                "desc": "EMA, VV, ST 同時亮綠燈，最強共識點。" if is_zh else "Strongest consensus when EMA, VV, and ST all turn green."
            },
            "trendtable_alert": {
                "title": "第24課 | [神器] 盯盤救星：設定 TrendTable 手機警報 🔒" if is_zh else "Lesson 24 | [Tool] Setting Mobile Alerts 🔒",
                "file": "33_trendtable_alert_setup.md",
                "icon": "🔔",
                "desc": "訊號出現直接推送到手機。" if is_zh else "Push signals directly to your phone."
            },
            "rsi_table": {
                "title": "第25課 | [神器] 短線爆發力：RSI 當炒股掃描 🔒" if is_zh else "Lesson 25 | [Tool] RSI Hot Scanner 🔒",
                "file": "19_rsi_hot_table.md",
                "icon": "🔥",
                "desc": "一眼找出這幾天資金最集中的標的。" if is_zh else "Find assets with the most capital concentration."
            },
            "tv_heatmap": {
                "title": "第26課 | [神器] 資金流向圖：期貨動能 Heatmap 🔒" if is_zh else "Lesson 26 | [Tool] Global Volume Heatmap 🔒",
                "file": "7_tv_volume_heatmap.md",
                "icon": "🗺️",
                "desc": "利用 Z-Score 找出最強與最弱的板塊。" if is_zh else "Use Z-Score to find strongest/weakest sectors."
            },

            # --- Phase 5: Futures (VIP) ---
            "cfd_basis": {
                "title": "第27課 | [期貨] 差價陷阱：Future vs CFD 換算攻略 🔒" if is_zh else "Lesson 27 | [Futures] CFD vs Futures Basis 🔒",
                "file": "18_cfd_basis_calculator.md",
                "icon": "💱",
                "desc": "解決看期貨做 CFD 的點差難題。" if is_zh else "Solve the spread/pricing issue when trading CFDs."
            },
            "basis_theory": {
                "title": "第28課 | [期貨] 水位理論：為何牛牛報價跟期貨不同？ 🔒" if is_zh else "Lesson 28 | [Futures] Basis Theory 🔒",
                "file": "29_basis_theory_manual.md",
                "icon": "🌊",
                "desc": "深入理解基差 (Basis) 變動原理。" if is_zh else "Understanding Basis fluctuations and arbitrage."
            },
            "cbbc_street_map": {
                "title": "第29課 | [牛熊] 屠牛殺熊：解讀街貨圖與投行對沖 🔒" if is_zh else "Lesson 29 | [CBBC] Street Map & Hedging 🔒",
                "file": "31_cbbc_street_map.md",
                "icon": "🎯",
                "desc": "預測莊家的殺跌目標價。" if is_zh else "Predict dealer targets using Delta Hedging logic."
            },

            # --- Phase 6: Options (VIP) ---
            "option_pricing_101": {
                "title": "第30課 | [期權] 拒絕做水魚！拆解 BS Model 定價原理 🔒" if is_zh else "Lesson 30 | [Options] BS Model Pricing 101 🔒",
                "file": "21_option_pricing_101.md",
                "icon": "🎓",
                "desc": "只在值博率高時出手。" if is_zh else "Trade only when the odds and pricing are in your favor."
            },
            "bs_model_excel": {
                "title": "第31課 | [期權] 定價計算機：一鍵算出合理期權價 (Excel) 🔒" if is_zh else "Lesson 31 | [Options] Pricing Calculator 🔒",
                "file": "27_bs_model_excel.md",
                "icon": "🧮",
                "desc": "立即知道莊家有沒有「食價」。" if is_zh else "Instantly know if the dealer is overcharging."
            },
            "bull_call": {
                "title": "第32課 | [期權] 降低成本：Bull Call Spread 實戰攻略" if is_zh else "Lesson 32 | [Options] Bull Call Spread Strategy",
                "file": "2_bull_call_spread.md",
                "icon": "🐂",
                "desc": "用低成本博取倍數回報。" if is_zh else "Low cost, high multiple returns."
            },
            "naked_long": {
                "title": "第33課 | [期權] 買 Call 必死？Naked Long 的生存法則" if is_zh else "Lesson 33 | [Options] Naked Long Survival Guide",
                "file": "3_naked_long_strategy.md",
                "icon": "⏳",
                "desc": "何時才適合「單邊下注」。" if is_zh else "When is it safe to bet directionally?"
            },
            "option_t0_strategy": {
                "title": "第34課 | [期權] T+0 戰法：利用 Gamma 暴漲賺快錢 🔒" if is_zh else "Lesson 34 | [Options] T+0 Gamma Scalping 🔒",
                "file": "22_option_t0_strategy.md",
                "icon": "🚀",
                "desc": "極致風險回報比的即日鮮技術。" if is_zh else "High R:R intraday scalping using Gamma."
            },
            "itm_vs_otm": {
                "title": "第35課 | [期權] 價內 vs 價外：末日輪選股心法 🔒" if is_zh else "Lesson 35 | [Options] ITM vs OTM Selection 🔒",
                "file": "23_itm_vs_otm_puts.md",
                "icon": "📐",
                "desc": "想博十倍回報，該選哪一個行使價？" if is_zh else "Which strike to pick for 10x returns?"
            },
            "iv_expected_move": {
                "title": "第36課 | [期權] 預測波幅：如何用 IV 算出目標價？ 🔒" if is_zh else "Lesson 36 | [Options] IV Expected Move 🔒",
                "file": "45_iv_expected_move.md",
                "icon": "⚡",
                "desc": "計算股票今日的「預期最高/最低點」。" if is_zh else "Calculate today's expected High/Low using IV."
            },
            "vol_crush": {
                "title": "第37課 | [期權] 避開 IV Crush：財報季生存指南" if is_zh else "Lesson 37 | [Options] Avoiding IV Crush",
                "file": "24_vol_crush_explained.md",
                "icon": "📉",
                "desc": "詳解波動率暴跌現象與對策。" if is_zh else "Understanding Volatility Crush during earnings."
            },
            "oi_settlement": {
                "title": "第38課 | [期權] 最大痛點：利用 OI 預測結算價 🔒" if is_zh else "Lesson 38 | [Options] Max Pain & OI Settlement 🔒",
                "file": "25_oi_settlement_logic.md",
                "icon": "📍",
                "desc": "看穿莊家 Max Pain，跟著莊家收租。" if is_zh else "Predict settlement price using Max Pain logic."
            },
            "dividend_marking": {
                "title": "第39課 | [期權] 除息陷阱：股息如何影響期權價格 🔒" if is_zh else "Lesson 39 | [Options] Dividend Trap 🔒",
                "file": "26_dividend_marking.md",
                "icon": "🔖",
                "desc": "別讓股息除淨導致你的 Put/Call 莫名虧損。" if is_zh else "Don't let dividends kill your option position."
            },

            # --- Phase 7: Quant (VIP) ---
            "risk_monitor_guide": {
                "title": "第40課 | [量化] 逃頂訊號：Risk Dashboard 使用指南" if is_zh else "Lesson 40 | [Quant] Risk Dashboard Guide",
                "file": "9_risk_dashboard_guide.md",
                "icon": "📟",
                "desc": "在大跌發生前，識別市場的恐慌訊號。" if is_zh else "Identify panic signals before the crash."
            },
            "stock_dna": {
                "title": "第41課 | [量化] 揀股黑科技：Stock DNA 因子掃描" if is_zh else "Lesson 41 | [Quant] Stock DNA Factor Scan",
                "file": "1_stock_dna_guide.md",
                "icon": "🧬",
                "desc": "拆解股票的「基因」，找出被低估的優質股。" if is_zh else "Decode stock DNA to find undervalued gems."
            },
            "cftc_cot_report": {
                "title": "第42課 | [量化] 跟蹤聰明錢：CFTC 倉位報告實戰 🔒" if is_zh else "Lesson 42 | [Quant] CFTC COT Report Analysis 🔒",
                "file": "42_cftc_cot_report.md",
                "icon": "🐋",
                "desc": "看穿 Commercials (大戶) 長線資金流向。" if is_zh else "Follow the long-term money flow of Commercials."
            },
            "dispersion_trading": {
                "title": "第43課 | [量化] 投行秘技：Dispersion Trading (分散度交易) 🔒" if is_zh else "Lesson 43 | [Quant] Dispersion Trading 🔒",
                "file": "43_dispersion_trading.md",
                "icon": "⚖️",
                "desc": "利用指數與個股的波動率錯價進行套利。" if is_zh else "Arbitrage using Index vs Stock volatility mispricing."
            },
            "bergomi_model": {
                "title": "第44課 | [量化] 波動率模型：Bergomi Model 簡介 🔒" if is_zh else "Lesson 44 | [Quant] Bergomi Model Intro 🔒",
                "file": "44_bergomi_model.md",
                "icon": "♾️",
                "desc": "描述波動率動態與微笑曲線的數學模型。" if is_zh else "Mathematical model for volatility dynamics and smile."
            },
            "totem_valuation": {
                "title": "第45課 | [量化] 大戶的答案紙：Totem 估值揭秘 🔒" if is_zh else "Lesson 45 | [Quant] Totem Valuation 🔒",
                "file": "30_totem_valuation.md",
                "icon": "🤫",
                "desc": "為 OTC 衍生品進行定價與風控。" if is_zh else "Pricing and risk management for OTC derivatives."
            },
            "daily_chart_scorecard": {
                "title": "第46課 | [量化] 拒絕憑感覺：日圖計分表 (Scorecard) 📝" if is_zh else "Lesson 46 | [Quant] Daily Chart Scorecard 📝",
                "file": "45_Daily_Chart_Scorecard.md",
                "icon": "✅",
                "desc": "將盤感數據化。分數不夠絕不出手。" if is_zh else "Systematize your intuition. No score, no trade."
            },
            "factor_mri": {
                "title": "第47課 | [量化] 市場 MRI：用因子 Z-Score 看穿板塊輪動 🧬" if is_zh else "Lesson 47 | [Quant] Market MRI (Factor Z-Score) 🧬",
                "file": "46_factor_mri.md",
                "icon": "📊",
                "desc": "用數據識別當下的市場主線。" if is_zh else "Identify the current market narrative using data."
            },
        }

        col_list, col_content = st.columns([1, 2.5], gap="large")

        with col_list:
            st.markdown(f"### {t('article_list')}")

            options_titles = [data["title"] for data in articles.values()]
            options_icons = [data["icon"] for data in articles.values()]

            selected_title = option_menu(
                menu_title=None,
                options=options_titles,
                icons=options_icons,
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
            current_article = next((item for item in articles.values() if item["title"] == selected_title), None)

            if current_article:
                # Permission Check
                # Important: check_access_func expects the TITLE.
                # Since we translated the title, we must ensure the '🔒' symbol is present in English titles too.
                if "🔒" in current_article["title"] or "Lock" in current_article["title"]:
                    if not check_access_func(current_article['title'],
                                             description=f"{t('vip_locked')}: {current_article['desc']}"):
                        st.stop()

                file_path = os.path.join("Education", current_article["file"])

                st.markdown(f"""
                <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #2563EB; margin-bottom: 20px;">
                    <h2 style="margin:0; color: white;">{current_article['icon']} {current_article['title'].replace(' 🔒', '')}</h2>
                    <p style="margin-top:5px; color: #94a3b8;">{current_article['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

                content = load_markdown_func(file_path)
                st.markdown(content, unsafe_allow_html=True)

                if "🔒" not in current_article["title"]:
                    st.divider()
                    st.info(t("cta"))
            else:
                st.error("Error loading article.")

    # --- TAB 3: Video Tutorials ---
    with tab_video:
        st.subheader(t("tabs")[2])
        st.video("https://www.youtube.com/")
        st.caption(t("video_sub"))
        st.markdown("---")
        st.info(t("video_info"))