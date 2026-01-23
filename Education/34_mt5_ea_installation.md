# 📂 工具教學：如何將 EA 安裝到 MT5

<iframe width="100%" height="450" src="https://www.youtube.com/embed/5cZwqK4psOA?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

**影片標題：** 如何將EA file安裝到MT5上!
**頻道：** ParisTrader (巴黎炒家)

---

## 執行摘要
本影片演示了將 Expert Advisor (EA) 程式檔案安裝到 MetaTrader 5 (MT5) 平台的標準流程。無論是您購買的 EA 或是自製的程式，都必須經過正確的「放置檔案」與「權限開啟」步驟才能運作。

---

## 安裝步驟重點 (Step-by-Step)

### 1. 放置檔案
1.  **複製檔案**：先複製您的 EA 檔案 (通常是 `.ex5` 或 `.mq5` 格式)。
2.  **開啟數據資料夾**：在 MT5 左上角選單點擊 `File (文件)` -> `Open Data Folder (打開數據文件夾)`。
3.  **進入路徑**：雙擊 `MQL5` 資料夾 -> 雙擊 `Experts` 資料夾。
4.  **貼上**：將檔案貼上到 `Experts` 資料夾中 (建議可以新建一個資料夾分類，例如 `Paris_EA`)。
5.  **刷新**：回到 MT5 介面，在左側 `Navigator (導航)` 面板的 `Experts` 上按右鍵 -> `Refresh (刷新)`。您應該能看到剛貼上的 EA。

### 2. 啟動 EA
1.  **開啟圖表**：打開您要交易的商品圖表 (例如 XAUUSD)。
2.  **拖曳 EA**：從 `Navigator` 將 EA 拖曳到圖表上。
3.  **允許交易**：
    * 在彈出的設定視窗中，切換到 `Common (常用)` 分頁。
    * **務必勾選** `Allow Algo Trading (允許自動交易)`。
4.  **全局開關**：
    * 檢查 MT5 上方工具列的 `Algo Trading` 按鈕。
    * 確保它顯示為 **綠色 (播放圖示)**，而不是 紅色 (停止)。

### 3. 確認狀態
* 查看圖表右上角，應該會出現 EA 的名稱與一個 **「藍色帽子」** 圖示。
    * 🎩 **藍色帽子** = 運作正常。
    * 🧢 **灰色帽子** = EA 被禁用 (請檢查 Algo Trading 按鈕)。