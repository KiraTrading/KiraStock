# ⚖️ 期權教學：ITM vs OTM Put (Greeks 解析)

<iframe width="100%" height="450" src="https://www.youtube.com/embed/CI8dbI6HUII?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

## 主題:比較同月到期的價內 (ITM) 與價外 (OTM) 看跌期權 (Put)
**核心問題：** 如果股價下跌 10%，兩者在 Greeks 和方向性玩法上有何差異？

---

## 1. Greeks (希臘字母) 差異分析

### **Delta ($\Delta$)：對價格變動的敏感度**
* **定義**：衡量期權價格對標的資產價格變動的敏感度。
* **比較**：ITM Put 通常具有**更高**的 Delta。
* **實戰意義**：ITM Put 會隨著標的股票價格的變化而經歷更大的價格變動。如果股票下跌 10%，ITM Put 的絕對價值增加金額通常會多於 OTM Put。

### **Gamma ($\Gamma$)：Delta 的加速度**
* **定義**：代表 Delta 隨標的資產價格變動而變動的速率。
* **比較**：ITM Put 的 Gamma 通常較高（接近 ATM 時最高）。
* **實戰意義**：隨著股價下跌，ITM Put 的 Gamma 會導致其 Delta 比 OTM Put 的 Delta 增長得更快。這意味著 ITM Put 對價格進一步下跌的敏感度將大於 OTM Put。

### **Theta ($\Theta$)：時間值損耗**
* **定義**：衡量期權價值的時間衰減率。
* **比較**：ITM Put 通常具有**較低**的 Theta。
* **原因**：因為 ITM 期權包含內在價值 (Intrinsic Value)，而 OTM 期權全由時間價值組成。
* **實戰意義**：隨著時間推移，ITM Put 價值的下降速度比 OTM Put 慢。

### **Vega ($v$)：對波動率的敏感度**
* **定義**：量化期權價格對隱含波動率 (IV) 變化的敏感度。
* **比較**：兩者通常都有正 Vega。
* **實戰意義**：波動性增加通常會增加兩者的價值。
    * *特別注意*：如果你預期股價在**非常短時間內大幅波動**（暴跌），OTM Option 的百分比漲幅 (ROI) 可能會高於 ITM，因為 OTM 的基數較低。

---

## 2. 方向性玩法總結

* **獲利機率**：如果股票下跌 10%，ITM Put 比 OTM Put 更有利可圖且更穩健。
    * **ITM Put**：由於執行價較高，已經具有內在價值（In-the-money），獲利機會更高。
    * **OTM Put**：需要股價**大幅下跌**並跌破執行價才能產生內在價值。如果跌幅不夠深，OTM 即使方向對也可能沒肉食。

---

## 📝 Paris 實戰心法

### **策略選擇**
1.  **OTM (價外)**：必須要**大插 (暴跌) 入價**才會賺最多 (High Risk, High Reward)。如果是慢跌 (陰跌)，OTM 會輸死時間值 (Theta)。
2.  **遠期期權**：時間值扣得較慢，適合波段。

### **極限權操作 (QQQ 玩 NQ)**
* **標的**：正常來說，玩極限權就用 **QQQ** (納指 ETF) 來操作 **NQ** (納指期貨) 的波動。
* **選價技巧 (即日權)**：
    * 假設 QQQ 現價 **385**。
    * **Call**：選最近的價外一檔 -> **386 Call**。
    * **Put**：選最近的價外一檔 -> **384 Put**。
* **進出紀律**：
    * **一入就要郁 (動)**：進場後價格必須立刻發動。
    * **唔郁即走**：如果價格停滯，立刻離場，不可以戀戰。
    * **倉位控制**：不可以大 Size All-in。
* **進場條件**：一定要配合 **四圖流 (M1, M3, M5, M15)**，且 **VV 指標方向齊全** + **有 TP 目標** + **無 Data Pending**。
* **止盈 (TP)**：
    * TP1：必食 (重倉出場)。
    * TP2：輕倉 (輕鬆坐，博更大利潤)。