# 🗓️ TradingView 指標：ST Table 多時框分析表

<div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-bottom: 20px;">
    <h3 style="margin:0; color: #3B82F6;">🔐 指標權限獲取</h3>
    <p style="margin-top:10px; color: #e2e8f0;">
        此為 ParisTrader 內部專用指標。如需開通權限，請在 Discord 或 Telegram 聯繫 <strong>777</strong>。
    </p>
    <a href="https://www.tradingview.com/script/s4pUEDq2-ST-Table/" target="_blank">
        <button style="background-color:#3B82F6; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:bold;">
            前往 TradingView 收藏指標 ↗
        </button>
    </a>
</div>

---

## 🔍 指標功能簡介 (Executive Summary)

這是一個專為**期貨 (Futures)** 和 **差價合約 (CFD)** 交易者設計的儀表板工具。

它能幫助你在**單一圖表**上，同時監控 **6 個不同時間範圍**的價格走勢。系統會自動計算自定義的 **ST 值**（源自 ATR 和價格差異），並將結果以表格形式顯示在圖表角落。這讓你無需頻繁切換圖表，即可判斷「多時框共振」是否形成。



---

## ✨ 核心特徵 (Key Features)

### 1. 多時間範圍分析 (Multi-Timeframe Analysis)
不再需要開啟 6 個螢幕或切換 6 次視窗，ST Table 自動計算並顯示以下週期的趨勢狀態：
* **1 分鐘 (1m)**：極短線動能
* **3 分鐘 (3m)**：入場確認
* **5 分鐘 (5m)**：短線結構
* **15 分鐘 (15m)**：日內趨勢
* **1 小時 (1h)**：主要趨勢
* **4 小時 (4h)**：大級別方向

### 2. ST 值計算邏輯
* 該指標並非單純的移動平均線，而是基於 **ATR (平均真實波幅)** 與 **價格差異** 計算出的動態數值。
* 這對於比較不同時間解析度的短期價格行為特別有用，能過濾掉市場雜訊，顯示真實的波動方向。

---

## 🛠️ 如何應用於實戰？

1.  **趨勢確認**：當表格中從 1m 到 1h 全部顯示為 **綠色 (Bullish)** 或 **紅色 (Bearish)** 時，代表強烈趨勢形成，這是勝率最高的進場點。
2.  **背離警示**：如果 4h 和 1h 顯示上漲，但 1m 和 3m 轉為下跌，這代表短線回調 (Pullback) 正在發生，可等待短週期轉回與大週期一致時進場。
3.  **輔助四圖流**：此表格可完美配合我們的「四圖流」策略，作為螢幕空間不足時的最佳替代方案。

> **提示**：將此指標疊加在您的主圖表 (例如 M3 或 M5) 上，即可實現「一張圖看全貌」。