# 📊 TradingView 指標：成交量指標 v2 (Volume Analysis Tool)

<div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-bottom: 20px;">
    <h3 style="margin:0; color: #3B82F6;">📥 獲取指標</h3>
    <p style="margin-top:10px; color: #e2e8f0;">
        此指標為非覆蓋式 (放在副圖)，專為深入了解成交量動態的交易者設計。
    </p>
    <a href="https://www.tradingview.com/script/zLRrU2PO/" target="_blank">
        <button style="background-color:#3B82F6; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:bold;">
            前往 TradingView 收藏指標 ↗
        </button>
    </a>
</div>

---

## 🔍 指標功能詳解

這不僅僅是普通的成交量柱，它將買賣力道**可視化分解**，並結合了趨勢濾網。

### 1. 買賣成交量分解 (Breakdown)
傳統成交量只看總量，此指標將其拆解：
* **🟢 綠色柱狀圖**：代表 **買入成交量** (Buy Volume)。
* **🔴 紅色柱狀圖**：代表 **賣出成交量** (Sell Volume)。
* **堆疊顯示**：兩者堆疊在一起，讓你一眼看出當前 K 線是「實買」還是「實賣」主導。

### 2. Supertrend 智能整合
系統內建 15 週期基於 ATR 的 Supertrend 來檢測趨勢變化：
* **動態調整**：成交量移動平均線的長度，會根據最近一次 Supertrend 交叉以來的 K 線數量自動調整。
* **無趨勢時**：若無明顯趨勢，則回退至標準的 10 週期 SMA。

### 3. 爆量信號 (Volume Spikes)
當成交量出現異常激增時，系統會自動標記，幫助你識別機構進場點：
* **🟣 CC 信號 (紫色)**：當成交量超過 Supertrend SMA 的 **2倍** 時觸發。
* **🔵 PP 信號 (藍色)**：當成交量超過 Supertrend SMA 的 **2倍** 時觸發。
* **視覺提示**：信號會以「量」標籤直接標記在成交量水平上。

### 4. GC1! 黃金期貨專屬優化
* 如果你在看 **GC1! (黃金期貨)** 的 **1分鐘 (1m)** 圖表，指標會自動添加一條位於 **100** 的水平線。
* **用途**：標記黃金短線交易的關鍵成交量閾值，超過此線往往代表動能爆發。

---

## 🛠️ 如何使用？

1.  **安裝**：將指標添加到你的圖表（它會顯示在下方副圖）。
2.  **設定**：你可以調整「平均成交量K線數」來自定義黃色 SMA 參考線。
3.  **實戰觀察**：
    * **看壓力**：觀察綠色與紅色柱的比例，判斷市場是多頭強還是空頭強。
    * **抓爆發**：尋找 **CC (紫色)** 和 **PP (藍色)** 信號，這通常發生在趨勢啟動或反轉的關鍵時刻。
    * **黃金短打**：做黃金期貨時，留意 1m 圖是否突破 100 量能線。

> **適用對象**：短線交易者 (Scalpers)、日內交易者 (Day Traders) 以及專注於量價分析 (VSA) 的分析師。