# ⌨️ 工具教學：IB TWS 快捷鍵 (Hotkeys) 設定

<iframe width="100%" height="450" src="https://www.youtube.com/embed/Jw44yAj106s?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

## 摘要
在極限期權 (如 0DTE 末日輪) 的交易中，速度就是金錢。本影片演示了如何在 Interactive Brokers (IB) 的 TWS 交易平台中設定 **快捷鍵 (Hotkeys)**。透過設定 F3 (買入) 和 F4 (賣出)，交易者可以省略手動輸入價格和數量的時間，實現「一鍵下單」，這對於捕捉稍縱即逝的突破行情至關重要。

---

## 重點

### 1. 為什麼需要快捷鍵？
* **手動下單的痛點**：傳統下單需要點擊 Bid/Ask，輸入價格，輸入數量，再點傳送。這在劇烈波動的行情中太慢了。
* **極限操作需求**：當價格突破關鍵位 (Breakout) 時，往往只有幾秒鐘的進場窗口。快捷鍵能讓你瞬間成交。

### 2. IB TWS 設定步驟 (Step-by-Step)
1.  **進入設定**：點擊 TWS 上方的 `File` -> `Global Configuration` -> `Hotkeys`。
2.  **選擇功能**：
    * **Buy (買入)**：設定為 `F3` (或其他你順手的鍵)。
    * **Sell (賣出)**：設定為 `F4`。
3.  **自訂參數 (Customize)**：
    * **Size (數量)**：設定為 `Absolute` (絕對值)，例如每次 `3` 張 (Default Size = 3)。
    * **Order Type (訂單類型)**：
        * 建議設定為 `LMT` (限價單) 以控制滑點。
        * 或者設定為 `MKT` (市價單) 以確保成交（視個人風格）。
    * **Limit Price (限價)**：可以設定為 `Ask + 0.05` (買入時) 或 `Bid - 0.05` (賣出時)，以增加成交機率但又不如市價單般被動。
    * **Transmit the order instantaneously**：**務必勾選**。這代表按下按鍵後「直接送出」，不會再彈出確認視窗 (Don't show confirmation)。

### 3. 實戰操作演示
* **Option Chain (期權鏈)**：打開 QQQ 或 SPY 的期權鏈。
* **選定合約**：點擊你想交易的行權價 (Strike)。
* **一鍵進場**：看到訊號 (如 VV 轉向)，手指按下 `F3`，系統立即以預設的 3 張單買入。
* **一鍵離場**：看到 TP 到達或止損位，手指按下 `F4`，系統立即賣出平倉。

---

## ⚠️ Paris 實戰叮嚀

* **測試**：設定好後，請務必先在 **Paper Trading (模擬倉)** 測試，確保按鍵邏輯符合預期，避免在真倉按錯導致因快得慢。
* **數量控制**：在設定 Default Size 時要小心，不要設得太大 (如 100 張)，以免誤觸鍵盤造成巨大損失。