# 🧬 第46課 | [量化] 市場 MRI：解讀 Pure Factor Z-Score

> **核心理念**：指數升跌只是表象，因子 (Factor) 才是資金流動的真實軌跡。  
> **Core Philosophy**: Don't just watch the Index. Watch the Flow.

---

## 1. 這張圖表是什麼？ (The Dashboard)

很多散戶只看熱力圖 (Heatmap) 知道哪隻股票升，但量化交易員看的是 **Pure Factor (純因子表現)**。這張圖表經過數學處理 (Z-Score)，剔除了大市本身的漲跌，直接告訴你：**聰明錢 (Smart Money) 今天到底在買什麼屬性？賣什麼屬性？**

* **紅色長條 (Red Bar)**：資金正在**撤離**的風格（被拋售）。
* **綠色長條 (Green Bar)**：資金正在**湧入**的風格（被追捧）。
* **數值 (Z-Score)**：代表強弱程度。
    * `> +2.0`：極度擁擠 (Overbought)，小心回調。
    * `< -2.0`：極度恐慌 (Oversold)，可能有反彈或崩盤。

---

## 2. 案例分析 A：防禦性輪動 (Defensive Rotation)
*(參考圖一：有綠有紅，分化明顯)*

!
**📊 盤面解讀：**
* **Momentum (動能股) Z: -2.59** 🟥
    * **解讀**：這是最危險的訊號！前期升得最勁的強勢股正在被機構無情獲利了結 (Profit Taking)。千萬不要去接「高位回調」的股票。
* **Sentiment (情緒股) Z: -1.97** 🟥
    * **解讀**：散戶最愛的網紅股 (Meme Stocks) 正在退潮。
* **Shareholder Yield (股東回報) Z: +1.79** 🟩
    * **解讀**：資金沒有離場，而是「搬家」了。它們躲進了**高股息、高回購**的防禦板塊。

> **💡 交易策略**：這是典型的 **Risk Off (避險模式)**。
> * ❌ **Stop Longing Breakouts**：停止追漲殺跌。
> * ✅ **Rotate to Value**：如果非要買，只能買保險、能源等現金流強的公司。

---

## 3. 案例分析 B：系統性拋售 (Systematic Sell-off)
*(參考圖二：全紅，無一倖免)*

!
**📊 盤面解讀：**
* **全紅 (All Red)**：
    * **解讀**：留意圖中連 `Low Vol` (低波動) 和 `Value` (價值) 都是負分。這代表市場發生了 **流動性危機 (Liquidity Event)**。
* **Sentiment (情緒) Z: -2.23** 🟥
    * **解讀**：投機資金徹底崩潰，散戶投降 (Capitulation)。
* **Low Vol (低波動) Z: -0.29** 🟧
    * **解讀**：它雖然是負分，但跌得最少。這不是因為它強，只是因為它「抗跌」。

> **💡 交易策略**：這是 **Cash is King (現金為王)** 的時刻。
> * ❌ **Don't Buy the Dip**：不要撈底！當連防禦股都在跌，代表機構在「無差別變現」以應付保證金 (Margin Call)。
> * ✅ **Short / Hedge**：這是做空大市 (Short Beta) 的最佳時機。

---

## 4. 因子字典 (Factor Dictionary)

看不懂英文術語？這裡有對照表：

| 因子 (Factor) | 代表意義 (Meaning) | 對應股票例子 |
| :--- | :--- | :--- |
| **Momentum** | **動能**：過去 12 個月漲幅最強的股票。 | `NVDA`, `SMCI` |
| **Sentiment** | **情緒**：散戶討論度高、沽空比率高的股票。 | `GME`, `TSLA` (部分時期) |
| **Growth** | **成長**：高收入增長、高估值 (High PE)。 | `AMD`, `CRWD` |
| **High Beta** | **高波**：波動率大於大市，攻擊型。 | `TQQQ`, `SOXL` |
| **Value** | **價值**：被低估、低 PE/PB 的股票。 | `INTC`, `F` |
| **Shareholder Yield** | **股東回報**：高股息 + 大量回購股票。 | `AAPL`, `XOM`, `KO` |
| **Low Vol** | **低波**：股價像心電圖一樣平穩。 | `JNJ`, `WM` |

---

## 5. 實戰應用：如何放進你的 Routine？

每天開市前 (Pre-market) 看一眼這個儀表板：

1.  **若 Momentum < -2.0**：當天禁止使用「突破策略」(Breakout Strategy)。
2.  **若 High Beta > Value**：大市處於進攻模式，可以加大槓桿。
3.  **若 Shareholder Yield 獨強**：大市處於防守模式，減少操作頻率，轉向防守。

---

> **© 2026 ParisTrader (Jacky Ho)** > *Disclaimer: 因子數據僅供參考，歷史回測不代表未來表現。*