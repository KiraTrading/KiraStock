# 🧮 工具下載：Black-Scholes 期權定價計算機 (Excel)

<div style="background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; margin-bottom: 20px;">
    <h3 style="margin:0; color: #10B981;">📥 工具下載</h3>
    <p style="margin-top:10px; color: #e2e8f0;">
        這是一個專業的 Excel 宏 (Macro) 工具，用於計算期權理論價格與希臘字母 (Greeks)。
    </p>
    <a href="https://drive.google.com/drive/folders/1fXBMl5NNyw6SegME-wg8lSYtiiM5dLqu?usp=sharing" target="_blank">
        <button style="background-color:#10B981; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:bold;">
            前往 Google Drive 下載 📂
        </button>
    </a>
</div>

---

## 🔍 功能介紹

這個 Excel 工具基於 **Black-Scholes 模型**，是期權交易員必備的計算神器。

### 1. 核心計算功能
只需輸入以下 5 個參數，即可得出期權的 **理論價格 (Theoretical Price)**：
* **Spot Price** (正股現價)
* **Strike Price** (行權價)
* **Volatility** (波動率 / IV)
* **Risk-Free Rate** (無風險利率)
* **Time to Maturity** (到期時間)

### 2. 希臘字母 (Greeks) 自動生成
除了價格，工具還會自動計算所有關鍵風險指標：
* **Delta ($\Delta$)**：方向性風險。
* **Gamma ($\Gamma$)**：Delta 的加速度。
* **Theta ($\Theta$)**：時間損耗值。
* **Vega ($v$)**：波動率敏感度。
* **Rho ($\rho$)**：利率敏感度。

### 3. 實戰應用
* **尋找錯價**：當市場報價 (Market Price) 遠高於 Excel 算出的理論價時，可能代表該期權被高估 (Overpriced)，適合做空 (Short)。
* **模擬分析**：你可以調整「波動率」或「時間」參數，預演如果明天 IV 暴跌或時間流逝，你的持倉價值會變成多少。

> **注意**：此檔案為 `.xlsm` 格式 (啟用巨集的工作簿)，開啟時請允許執行巨集 (Enable Macros) 以確保計算功能正常運作。