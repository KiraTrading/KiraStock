# 📊 [教學] 日圖計分表 (Daily Chart Scorecard)

> **核心理念**：拒絕情緒交易，用量化思維定義市場方向。  
> **Core Philosophy**: Don't guess. Quantify.

🎬 **完整教學影片 (Video Tutorial)**: [【交易教學】獨家「日圖計分表」大公開！](https://youtu.be/s4dqpWtwqFs)

---

## 1. 系統邏輯 (System Logic)

本計分表旨在將主觀的圖表型態轉化為客觀的數值 (`Score`)。我們不預測未來，只評估當下的優勢。

- **正分 (+)**：市場動能偏多 $\rightarrow$ **Long Bias**
- **負分 (-)**：市場動能偏空 $\rightarrow$ **Short Bias**
- **零分 (0)**：市場缺乏方向 $\rightarrow$ **Neutral / Range**

---

## 2. 計分標準 (Scoring Metrics)

請在每日開盤前 (Pre-market)，針對關注商品 (e.g., `XAUUSD`, `NQ`, `HSI`) 進行評分。

| 維度 (Dimension) | 判斷標準 (Criteria) | 得分 (Score) | 備註 (Notes) |
| :--- | :--- | :---: | :--- |
| **A. 趨勢 Trend**<br>*(權重 40%)* | `Price > 20MA` 且均線 **向上** | **+2** | 多頭趨勢確立 |
| | `Price > 20MA` 但均線 **走平** | **+1** | 震盪偏多 |
| | `Price < 20MA` 但均線 **走平** | **-1** | 震盪偏空 |
| | `Price < 20MA` 且均線 **向下** | **-2** | 空頭趨勢確立 |
| **B. 型態 Price Action**<br>*(權重 30%)* | 創新高 + 底底高 (`HH` + `HL`) | **+2** | 強勢多頭結構 |
| | 包含線 (`Inside Bar`) / 盤整 | **0** | 動能暫停 |
| | 創新低 + 頂頂低 (`LL` + `LH`) | **-2** | 強勢空頭結構 |
| **C. 關鍵位 Key Levels**<br>*(權重 20%)* | 突破關鍵阻力 (`Breakout`) | **+1** | 突破買入訊號 |
| | 處於區間中間 (`Mid-Range`) | **0** | 無明確訊號 |
| | 跌破關鍵支撐 (`Breakdown`) | **-1** | 跌破賣出訊號 |
| **D. 動能 Momentum**<br>*(權重 10%)* | `RSI > 50` (強勢區) | **+1** | 動能向上 |
| | `RSI < 50` (弱勢區) | **-1** | 動能向下 |

---

## 3. 決策矩陣 (Decision Matrix)

計算 **總分 (Total Score)**，並依據下表執行交易策略。

| 總分區間 (Score) | 市場狀態 (State) | 交易策略 (Strategy) | 倉位 (Sizing) |
| :---: | :---: | :--- | :--- |
| **+4 ~ +6** | 🔥 **強多頭** | **Long Only**<br>回調即買點，激進進場 | `Full Size` |
| **+1 ~ +3** | 📈 **震盪偏多** | **Dip Buy**<br>需等待關鍵位支撐確認 | `Half Size` |
| **0** | ⚖️ **盤整** | **No Trade / Range**<br>休息，或高拋低吸 | `Observation` |
| **-1 ~ -3** | 📉 **震盪偏空** | **Sell Rally**<br>需等待關鍵位阻力確認 | `Half Size` |
| **-4 ~ -6** | ❄️ **強空頭** | **Short Only**<br>反彈即空點，激進進場 | `Full Size` |

---

## 4. 風控原則 (Risk Management)

1.  **逆勢禁令 (No Counter-Trend)**：
    - `Score >= +4` 時，**禁止做空 (No Short)**。
    - `Score <= -4` 時，**禁止做多 (No Long)**。
2.  **止損設定 (Hard Stop)**：
    - 所有交易必須設定硬止損。
    - 建議參考 `ATR` 或 `Previous Candle High/Low`。
3.  **例外處理 (News Events)**：
    - 若遇重大數據公佈 (e.g., NFP, FOMC)，計分表暫時失效，以 **Price Action** 為主。

---

> **© 2026 ParisTrader (Jacky Ho)** > *Disclaimer: 本文件僅供教學與策略邏輯分享，不構成任何投資建議。*