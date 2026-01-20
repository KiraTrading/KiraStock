# MT5 神器：ParisTrader Assistant (手動交易輔助面板)

**Category:** Trading Tools | **Version:** 1.0

你是否厭倦了被 Broker『掃 Stop』？或者每次交易黃金，都要用計算機把 TP/SL 加入入場價？
**停！別再用 MT5 內建的笨重介面了。**

今天我要介紹一個改變你操盤節奏的神器 —— **ParisTrader Assistant**。

![EA 示意圖](Education/images/EA_ass.jpg)
---

## 為什麼你需要這個工具？

你還在手動算點數嗎？你還在擔心止損被券商偷看嗎？
ParisTrader Assistant v1.0 正式發布，三大核心功能解決你的痛點：

### ✅ 1. 直覺式美金風控 (Dollar Distance)
做 XAUUSD 不用再換算 Points！
* **痛點：** 黃金 2030.50 入場，止損要設 500 points 還是 50 pips？算錯就爆倉。
* **解法：** 想設 $5 止損？直接輸入 `5.0`。面板自動幫你搞定距離，**所見即所得**。

### ✅ 2. 隱形止損模式 (Hidden Mode)
* **痛點：** 券商看到你的 SL 在 2025，故意把價格打到 2024.99 掃你出場然後反彈。
* **解法：** 開啟 **`HIDDEN: ON`**，EA 將隱藏你的真實 SL/TP。券商看到的只有開倉價，沒有止損單。EA 在本地端監控，觸價即平。**防掃單、防獵殺。**

### ✅ 3. 動態戰術管理 (Tactical Buttons)
* **🔄 一鍵反手 (Rev)：** 發現看錯市？按一下，多單全平，反手做空。
* **🚀 一鍵加倍 (x2)：** 趨勢確認，獲利加倉神器。
* **🛠️ 一鍵修改 (UPDATE)：** 開單後想改止損？面板輸入新數字，一鍵更新所有持倉。

> **不用寫 Code，不用複雜設定，直接掛載即用。**

---

## 🖥️ 面板操作手冊 (User Manual)

ParisTrader Manual Trading Panel 是一個專為 MT5 設計的介面。載入後，面板將出現在圖表左上角。

### 1. 編輯框 (Edit Boxes) - 設定你的戰術
| 欄位 | 說明 | 預設值 |
| :--- | :--- | :--- |
| **Lot Size** | 單筆交易的手數。 | 0.1 |
| **SL($)** | 止損距離 (以美元計)。設 `0` 為無止損。 | 5.1 |
| **TP($)** | 止盈距離 (以美元計)。設 `0` 為無止盈。 | 10.0 |
| **Multi Count** | 連續下單次數 (配合 Multi 按鈕)。 | 10 |
| **Multi Lot** | 連續下單每筆的手數。 | 0.1 |

### 2. 核心按鈕 (Action Buttons)
* **BUY / SELL**: 立即開倉。系統會自動計算 SL/TP 價位。
    * *提示：若開啟 Hidden Mode，止損單不會傳送給券商。*
* **UPDATE SL/TP**: 覺得止損太近？在 `SL($)` 輸入新數字，按此按鈕，**所有持倉** 的止損立即更新。
* **HIDDEN: ON/OFF**: 切換隱藏模式。
    * 🟢 **ON (綠色)**: 本地監控，Broker 看不到止損。
    * 🔴 **OFF**: 傳統模式，止損單直接傳給 Broker。

### 3. 進階戰術按鈕 (Pro Features)
* **Multi BUY / SELL**: 機關槍模式。
    * *場景：* 你想下 1.0 手，但想拆成 10 張 0.1 手單 (方便分批出場)。設定 `Multi Count=10`，按一下搞定。
* **Close Buy / Close Sell**: 只平多單 或 只平空單。
    * *場景：* 對沖鎖倉時，只想解開獲利的一邊。
* **Rev (反轉)**: 淨倉位反手。
    * *場景：* 數據公佈，方向做反。按一下，平掉所有多單，反手開等量空單。
* **x2 (加倍)**: 勝率加倉。
    * *場景：* 浮盈加倉 (Pyramiding)。對現有持倉複製一倍。

---

## ⚙️ 安裝與設定 (Installation)

1.  **下載 EA 檔案** (`.ex5`) 並放入 MT5 的 `MQL5/Experts` 資料夾。
2.  **重啟 MT5** 或右鍵點擊「導航器」刷新。
3.  將 EA 拖曳到圖表 (建議 XAUUSD)。
4.  **輸入參數設定 (Inputs)：**
    * `InpStartLot`: 預設手數 (0.1)
    * `InpSL_Dollar` / `InpTP_Dollar`: 預設止損盈距離
    * `InpScale`: 面板縮放比例 (建議筆電設 1.5 - 2.0)
5.  **重要檢查：** 請確保 MT5 上方的 **"Algo Trading"** 按鈕已開啟 (綠色)。

---

## ⚠️ 注意事項 (Important Notes)

1.  **Magic Number:** 預設為 `888938`。EA 只會管理此 Magic Number 的訂單，不會干擾你其他的 EA 或手動單。
2.  **隱藏模式風險:** 在 `HIDDEN: ON` 模式下，止損是由你的電腦 (MT5 端) 觸發的。**如果你的電腦斷網、斷電或 MT5 關閉，止損將失效！** 建議使用 VPS 掛機。
3.  **帳戶類型:** 僅支援 **Hedging (對沖)** 帳戶。

---

### 👇 索取試用 / Get Access
這款工具目前僅開放給 VIP 社群成員使用。如想試用1個月,請即DM我!

**DM me on Telegram:**  [@Ho777ggg](https://t.me/Ho777ggg)