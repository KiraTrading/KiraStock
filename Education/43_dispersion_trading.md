# ⚖️ 期權進階：Dispersion Trading (分散度交易)

**核心觀點**：這是股票期權交易部門 (Prop Desk) 常見的一種交易策略。核心在於利用市場的「不完全定價」，在無需預測股票漲跌的情況下賺取 Alpha。



---

## 1. 什麼是分散度交易 (Dispersion Trading)？

分散度交易是指利用股票期權 **相對定價不一 (Relative Mispricing)** 的空缺，進行跨式交易。

* **本質**：它是一種 **波動率套利 (Volatility Arbitrage)**。
* **原理**：利用期權定價模型（如 Black-Scholes）計算出理論價格，當發現市場價格 (Market Price) 與理論價格 (Model Price) 出現顯著偏離時，就存在套利空間。

---

## 2. 具體操作流程

這通常涉及「一長一短 (Long/Short)」的對沖操作：

1.  **尋找錯位 (Identify Mispricing)**：
    * 找出同一股票不同 **履約月份 (Expiration)** 或不同 **行使價 (Strike)** 的期權合約。
    * 
    * 觀察其隱含波動率 (IV) 的曲面，尋找異常凸起或凹陷的地方。

2.  **建立部位 (Execution)**：
    * **買入 (Long)**：定價相對低（IV 低估）的期權。
    * **賣出 (Short)**：定價相對高（IV 高估）的期權。
    * *目標*：保持 Delta Neutral (方向中性)，只交易 Vega (波動率) 或 Gamma。

3.  **獲利方式 (Profit Taking)**：
    * **收斂 (Mean Reversion)**：等待市場情緒冷靜，定價差異收窄時平倉。
    * **實現波動 (Realized Volatility)**：利用實際波動率的變化，賺取 Gamma Scalping 的利潤。

---

## 3. Paris 進階筆記：指數 vs 個股

在華爾街，最經典的 Dispersion Trading 其實是 **「指數 vs 成份股」** 的博弈：

* **Short Index Volatility (做空指數期權)**：因為指數期權通常會有溢價 (Overpriced)，隱含相關性 (Implied Correlation) 往往被高估。
* **Long Single Stock Volatility (做多個股期權)**：買入成份股的期權作為保護。
* **獲利邏輯**：
    * 如果個股各自亂跳（分散度高），指數本身可能不動（因為互相抵消）。
    * 這時候你 Long 的個股期權會賺錢（因為波動大），而你 Short 的指數期權也會賺錢（因為指數沒動，賺時間值）。

---

## 4. 總結

這種策略利用了期權定價模型和相對定價的市場不完全特徵。
* **優點**：無需預測股票走勢 (Directionless)。
* **缺點**：計算複雜，對模型依賴度高，且需要動態對沖 (Dynamic Hedging)。
* **結論**：這是專業交易員從「賭方向」進化到「賭數學」的重要里程碑。