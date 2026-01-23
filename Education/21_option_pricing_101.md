# 摘要：投資班第一堂 - 期權定價 (Option Pricing)

<iframe width="100%" height="450" src="https://www.youtube.com/embed/x-Pxgt4EHko?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>



---

## 摘要
本影片是期權投資課程的第一堂，講者使用計算機網頁演示了期權定價的基本原理。重點講解了影響期權價格 (Premium) 的核心變量：正股價格 (Spot Price)、行權價 (Strike Price)、引伸波幅 (Implied Volatility)、到期日 (Days to Expiry) 以及無風險利率。此外，也簡要區分了美式期權 (American) 與歐式期權 (European) 的行權差異。

---

## 重點 

### 1. 期權價格的組成與計算
* **核心變量**：講者透過網頁計算機輸入不同參數，展示期權價格的變化。
    * **Spot Price (現價)**：標的資產當前的價格。
    * **Strike Price (行權價)**：合約約定的買賣價格。
    * **Implied Volatility (IV)**：引伸波幅。IV 越高，代表市場預期未來波動越大，期權價格 (Premium) 通常越貴。
    * **Time to Expiry**：距離到期的時間。時間越長，期權變成價內 (ITM) 的機會越大，因此時間價值 (Time Value) 越高。

### 2. 希臘字母 (Greeks) 初探
* **Delta ($\Delta$)**：
    * 定義：衡量期權價格對正股價格變動的敏感度。
    * 數值意義：Delta 接近 1 (或 100%) 代表該期權價格變動幾乎與正股同步（深度價內）；Delta 接近 0.5 (或 50%) 通常是價平 (ATM) 期權。
    * 機率解讀：Delta 也常被視為期權在到期時成為價內 (ITM) 的機率。
* **Theta ($\Theta$)**：
    * 代表時間價值的流逝 (Time Decay)。隨著到期日臨近，期權的時間價值會加速歸零。

### 3. 期權類型：美式 vs. 歐式
* **American Style (美式)**：
    * **特點**：買方可以在到期日之前的**任何時間**行權 (Exercise)。
    * **市場**：香港大部分股票期權、美股期權多為美式。
* **European Style (歐式)**：
    * **特點**：買方**只能在到期日當天**行權。
    * **市場**：通常指數期權 (如恒指期權) 多為歐式。

### 4. 價內 (ITM) vs. 價外 (OTM)
* **In-the-Money (價內)**：具有內在價值 (Intrinsic Value) 的期權。
    * Call: 現價 > 行權價。
    * Put: 現價 < 行權價。
* **Out-of-the-Money (價外)**：沒有內在價值，僅剩時間價值的期權。

---

## 總結
期權定價並非隨機，而是由數學模型 (如 Black-Scholes Model) 計算得出。理解這些變量（特別是 IV 和時間）如何影響價格，是進行期權交易的基礎。