# 💱 TradingView 工具：Future Versus CFD Basis Calculator

<div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-bottom: 20px;">
    <h3 style="margin:0; color: #3B82F6;">🔐 指標權限獲取</h3>
    <p style="margin-top:10px; color: #e2e8f0;">
        此為內部專用計算工具。如需開通權限，請在 Discord 或 Telegram 私訊助手 <strong>777</strong>。
    </p>
    <a href="https://www.tradingview.com/script/xGztPMNA-Future-Versus-CFD-Basis-Calculator/" target="_blank">
        <button style="background-color:#3B82F6; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:bold;">
            前往 TradingView 收藏指標 ↗
        </button>
    </a>
</div>

---

## 🔍 為什麼需要這個工具？

許多交易員習慣看 **期貨圖表** (如 GC 黃金期貨、NQ 納指期貨) 進行分析，因為期貨有成交量與機構單。但下單時卻是在 **CFD 平台** (如 XAUUSD、NAS100) 操作。

**痛點**：期貨與現貨之間永遠存在一個 **價差 (Basis)**。
* 例如：GC 期貨是 2650，XAUUSD 現貨可能是 2645。
* 當你分析期貨會漲到 2660 時，你在 CFD 軟體該掛 TP 多少？手動計算非常麻煩且容易出錯。

---

## ✨ 核心功能 (Key Features)

此指標會在圖表上直接顯示一個乾淨、可自訂的表格：
![TV指標畫面](Education/images/cfd_calculator.png)
### 1. 自動計算基差 (Basis Calculation)
* 即時顯示 **期貨價格 (Future)** 與 **現貨價格 (Spot)** 的差異。
* **顏色編碼**：
    * 🟢 **綠色**：正基差 (期貨 > 現貨)
    * 🔴 **紅色**：負基差 (期貨 < 現貨)

### 2. 目標價一鍵換算 (CFD Equivalent)
這是最強大的功能！
* 你只需設定 **期貨的目標價格 (Target Price)**。
* 系統會根據當前的基差，自動計算出 **「等值的 CFD 價格」**。
* **應用場景**：你在 NQ 期貨看到阻力位是 18500，輸入此數字，指標告訴你 CFD 的 TP 應該設在 18485。

### 3. 支援主流交易對
目前預設支援兩大熱門商品：
* **黃金**：XAUUSD (現貨) / GC (期貨)
* **納指**：NAS100 (現貨) / NQ (期貨)

---

## 🛠️ 如何使用？

1.  **新增指標**：將其加入圖表。
2.  **選擇商品**：從設定中選擇你要交易的對 (XAUUSD/GC 或 NAS100/NQ)。
3.  **輸入目標**：將「Target Price」調整為你分析出的期貨目標價。
4.  **查看結果**：直接看表格中的 "CFD Equiv." 數值，這就是你在 MT4/MT5 要掛單的價格。
5.  **調整位置**：你可以自由設定表格在圖表上的位置 (左上、右下等)，以免遮擋 K 線。



> **適合對象**：看期貨圖表做單，但資金放在 CFD 券商的交易者。