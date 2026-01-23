# 影片摘要：TradingView 新手入門與設定教學

<iframe width="100%" height="450" src="https://www.youtube.com/embed/Zovrw2tvzAI?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

## 執行摘要
本影片是針對 ParisTrader 用戶的 TradingView 基礎設置教學。講者詳細演示了從零開始建立觀察清單 (Watchlist)、購買即時數據 (Real-time Data)、選擇合適的訂閱方案，到如何安裝並設置專用的交易指標（如 Fate, Double Tap, Trend Table 等）。影片重點在於確保用戶能夠正確配置「四圖流」操作環境（M1, M3, M5, M15）。

---

## 重點摘要 (Key Takeaways)

### 1. 建立觀察清單 (Watchlist) 與 Ticker 代號
* 建議清空預設清單，重新加入常用交易品種：
    * **黃金期貨 (Gold)**：代號 `GC1!` (COMEX Gold Futures)
    * **納斯達克指數期貨 (Nasdaq)**：代號 `NQ1!` (CME Nasdaq 100 Futures)
    * **恆生指數期貨 (HSI)**：代號 `HK50` 或 `HSI1!`
    * **其他**：如 `HK2X` 等自訂品種。

### 2. 購買即時數據 (Real-time Data)
* **重要性**：新手常會看到數據延遲 (Delayed) 的標示，必須購買數據包才能進行即時交易。
* **購買路徑**：TradingView 訂閱頁面 -> Extra Data。
* **推薦購買項目**：
    * **CME Group**：包含 NQ (納指)、GC (黃金) 等美期數據。
    * **Hong Kong Futures Exchange (HKFE)**：包含恆指數據（費用約 $4 美元）。

### 3. 訂閱方案選擇 (Plan Selection)
講者分析了不同方案對應此策略的適用性：
* **Essential (入門版)**：
    * 限制：每分頁 2 個圖表、5 個指標。
    * 評價：**最低門檻**。對於資金有限的新手，這是最基本的起步方案。
* **Plus (升級版)**：
    * 優勢：每分頁 4 個圖表。適合想要在一個螢幕同時看 M1/M3/M5/M15 的人。
* **Premium (高級版)**：
    * 優勢：每分頁 8 個圖表，且支援更長時間的 Backtest (回測) 數據（Essential/Plus 會有回測時間限制）。
    * 評價：講者個人使用此方案，方便多圖表監控。

### 4. 指標安裝與設定 (Indicators Setup)
* **安裝位置**：指標位於「技術指標 (Indicators)」 -> 「僅限邀請 (Invite-only scripts)」。
* **核心指標清單**：
    * `Fate神指標` / `Fate Back-Testing`
    * `RSI Table` (當炒表，僅適用於日線圖)
    * `Trend Table` (趨勢表，全綠燈代表強勢)
    * `VBE` / `VV` (Volume Indicator)
    * `WTF` (用於橫行盤整市況)
* **故障排除**：如果指標顯示紅色感嘆號或錯誤，請嘗試重新整理 (Refresh) 或刪除指標後重新加入。

### 5. 圖表佈局策略 (Chart Layout)
講者建議的標準監控配置（四圖流）：
* **M1 (1分鐘圖)**：加載 `Fate神指標` + `VV` (Volume)。這是極短線進出的核心。
* **M3 (3分鐘圖)**：加載 `Fate神指標` 指標 + `VV`。
* **M5 / M15 (5分鐘/15分鐘圖)**：同樣加載 `Fate神指標` 相關指標，用於確認更大級別趨勢。
* **Trend Table**：建議設置為 Small size，用來監控多週期趨勢（例如看到所有時區皆為綠色，即為強勢做多信號）。

---

## 總結與小撇步
1. **使用電腦版 App**：強烈建議下載 TradingView Desktop App，而非使用瀏覽器網頁版。電腦版可以保存多個分頁佈局，且切換商品時不用重新加載指標，效率更高。
2. **保存佈局 (Save Layout)**：設定好所有指標和參數後，記得點擊右上角保存並命名（例如 "GC Setup"），避免下次開啟要重來。
3. **權限開通**：如果剛獲得指標授權卻看不到，請在指標視窗按 F5 或重啟軟體。