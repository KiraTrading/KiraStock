# 🔔 工具教學：TrendTable 全自動 Alert 設定

<iframe width="100%" height="450" src="https://www.youtube.com/embed/n2sIx_QvInI?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

## 執行摘要
本影片針對 **TrendTable (趨勢表)** 指標進行了更新說明，特別是 H1/H4 大方向的邏輯優化。為了讓學員不需要時刻盯盤，講者演示了如何在 TradingView 上設置 **Alert (快訊)**，當 M1 至 H4 所有時框方向一致（全綠或全紅）時，自動發送手機 App 推播或 Email 通知。

---

## 重點摘要 (Key Takeaways)

### 1. 指標更新與準備
* **指標選擇**：請確保您使用的是最新版的 **TrendTable v1**。
* **圖表週期**：建議在 **M1 (1分鐘圖)** 上進行設定。
    * **原因**：系統會每分鐘 (每根 K 線收盤) 偵測一次是否「齊色」。

### 2. 設定步驟 (Step-by-Step)
1.  **新增快訊**：點擊 TradingView 上方的「鬧鐘」圖示或右鍵選擇 `Add Alert`。
2.  **Condition (條件)**：
    * 第一欄選擇：**Multi-Timeframe Trend Table v1** (您的指標名稱)。
    * 第二欄選擇：
        * **All Bullish (全部向上/全綠)**：做多信號。
        * **All Bearish (全部向下/全紅)**：做空信號。
3.  **Trigger (觸發頻率)**：
    * 選擇 **Once per bar close (K線收盤觸發)**。
    * **重要**：這代表每分鐘結束時 (第 60 秒)，如果確認所有時框都同色，才會發出信號，避免盤中閃爍的假信號。
4.  **Alert Actions (通知方式)**：
    * 勾選 **Notify in App**：手機 TradingView App 會彈出通知。
    * 勾選 **Play Sound**：電腦版會發出聲音 (可自選聲音與時長)。
    * (選填) Send Email / Webhook。
5.  **Alert Name & Message**：
    * **Name**：命名為 `GC All Up` (黃金全綠) 或 `GC All Down`。
    * **Message**：可以自定義訊息，例如 `Gold TrendTable All Green! Buy Signal`。

### 3. 實戰應用
* **雙向設定**：建議同時設定兩個 Alert，一個監測 **All Up**，一個監測 **All Down**。
* **免盯盤**：設定完成後，您可以去忙別的事，等到手機收到 `GC All Up` 通知時，再打開圖表確認進場機會。

---

## 總結
透過 Alert 功能，將 TrendTable 從「視覺輔助工具」升級為「半自動信號發送器」。
* **M1 圖表** -> **Once per bar close** -> **All Up / All Down**。