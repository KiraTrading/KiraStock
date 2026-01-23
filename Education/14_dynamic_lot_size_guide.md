# 資金管理：動態手數風險計算機 (Excel Tool)

<div style="background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; margin-bottom: 20px;">
    <h3 style="margin:0; color: #10B981;">📥 工具下載</h3>
    <p style="margin-top:10px; color: #e2e8f0;">
        點擊下方按鈕下載 Excel 計算機，輸入您的帳戶淨值，自動獲取建議手數。
    </p>
    <a href="https://docs.google.com/spreadsheets/d/1u9kDBHrN1e6051pci_LTJTfbC5zJoygJ/edit?usp=sharing" target="_blank">
        <button style="background-color:#10B981; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:bold;">
            打開 Google Sheets 計算機 🧮
        </button>
    </a>
</div>

---

## 核心觀念導讀

### 1. 賬戶淨值 vs. 滿倉風險 (Equity vs. Margin Call Risk)

* **最大手數 (Max Lot)**：這是基於 1:500 槓桿計算出的「極限手數」。
* **建議手數 (Suggested Lot)**：這是基於風險控制計算出的「安全手數」。

> **⚠️ Paris 教學話術：**
> 「雖然系統允許你在 $1,000 美金時開 1.03 手黃金，但這等於是在『賭博』。只要市場反向波動一點點，賬戶就會強制平倉 (Margin Call)。所以我們一定要看『建議手數』，而非挑戰『最大手數』。」

### 2. 黃金 (XAU) 的高風險屬性

* **現價**：約 $4,817 (假設值)
* **合約價值**：標準手 (100 oz) 高達 $481,700。

> **⚠️ Paris 教學話術：**
> 「很多新手習慣做 0.1 手，但在現在的高金價下，0.1 手的波動非常劇烈。對於 $1,000 美金的小賬戶，**0.01 手** 才是最安全的起步點，這能讓你有足夠的空間承受波動。」

### 3. 產品規格差異 (HK50 vs. NAS100)

同樣的資金，不同產品的合約規格 (Contract Size) 差異巨大：

| 產品 | 建議手數 (範例) | 風險特徵 |
| :--- | :--- | :--- |
| **恆指 (HK50)** | 1.46 手 | 點值較小，可操作手數較大 |
| **納指 (NAS100)** | 0.19 手 | 波動大且點值高，必須縮小手數 |

> **⚠️ Paris 教學話術：**
> 「每一種產品的合約大小不同，千萬不要用做恆指的習慣去下納指或比特幣，否則風險會瞬間失控。」

---

### 如何使用此表格？

1.  **輸入淨值**：在 Excel 的黃色欄位輸入您目前的帳戶餘額 (例如 1000, 5000, 10000)。
2.  **查看建議**：表格會自動根據不同產品 (XAU, US30, NAS100, HK50) 顯示建議的開倉手數。
3.  **嚴格執行**：交易前請先查表，避免憑感覺下單。