# 期權實戰：Bull Call Spread (牛市價差策略)

**Category:** Derivatives Strategy | **Level:** Intermediate

有沒有試過買 Call 看對了方向（股票升了），但最後還是輸錢？
**因為你輸給了「時間 (Theta)」和「波幅回調 (IV Crush)」。**

如果有人願意替你支付部分入場費，甚至幫你分擔時間損耗，好不好？這就是今期的 **Call Spread**。

---

## 什麼是 Call Spread？

假設你想租一層樓開 Party (看升 HSI)，租金要 $10,000 (買入 Call 的成本)。
但你覺得自己用不完這麼大的空間，於是你把其中的一個房間「分租」給別人，收回 $4,000 (賣出較遠價的 Call)。

**結果：** 你的實際成本降到了 $6,000。只要房價升值，你賺錢的起點 (Break-even point) 就比別人低！
當然 In return，你無法使用整間房子，使用空間有限 (賺錢的天花板有限)。

---

## 實戰操作 (The Math) —— HSI 27000 案例

**場景：** HSI 現在 27,000，目標看升到 27,600。

### 1. 賭徒做法 (Naked Long Call)
* **動作：** 買入 1月 27000 Call，付出權利金 500點。
* **打和點 (Break-even)：** 27000 + 500 = **27500**。
* **風險：** HSI 1月 Expiry 升到 27400，中間你唔走，你仍然會輸錢！

### 2. 聰明人做法 (Bull Call Spread)
* **動作 A (進攻)：** 買入 27000 Call (付出 500點)。
* **動作 B (防守/收租)：** 賣出 27600 Call (收回 200點)。
* **淨成本 (Net Debit)：** 500 - 200 = **300點**。
* **打和點 (Break-even)：** 27000 + 300 = **27300**。

> **結論：** HSI 只要升到 27300 你就開始賺了（比賭徒早了 200 點）。
> **代價：** 如果 HSI 飛升到 28000，你的利潤在 27600 就封頂了。

所以問下自己：「你是想穩穩地賺 300點，還是想賭那個很少發生的 1000點大升浪？」

---

## 為什麼它是「防禦性」武器？

1.  **抵銷 Theta (時間值)：** 你買的 Call 在貶值，但你賣出的 Call 也在貶值（賺錢）。賣出的那張 Call 幫你抵銷了每天的時間損耗。
2.  **抵銷 Vega (引伸波幅)：** 如果大市突然平靜下來 (IV Drop)，Naked Call 會大虧，但 Spread 因為一買一賣，受傷較輕。

> *"Making less mistakes rather than trying to hit beautiful shots."*
> 每次大戶輸大錢，永遠唔係睇錯邊，而係無做好風險管理，長期慢慢盈利比不穩定地大上大落好。

---

## IB 開戶與保證金迷思 (The Margin Myth)

很多新手（特別是學生）去 IB/牛牛開 Short Call，看到保證金要十幾萬港幣就嚇跑了。

**真相：Spread 不需要「Short 的保證金」。**

* **單頭 Short (Naked Short)：** 風險無限，IB 要求極高保證金（HKD 160,000+）。
* **Spread (價差策略)：** 當你在 IB 用「組合單 (Combo)」下單時，系統知道你手上有一張 Long Call 做保護。因為你的最大虧損已經鎖定，所以 **IB 不會收你 Short 的保證金**。

**實戰算數：大期 (HSI) vs 細期 (MHI)**

| 合約類型 | 策略 | 入場費 (假設淨權利金 300點) | 點評 |
| :--- | :--- | :--- | :--- |
| **大期 HSI** | Bull Call Spread | 300 x $50 = **HKD 15,000** | 心理壓力大，輸一次沒半個月糧。 |
| **細期 MHI** | Bull Call Spread | 300 x $10 = **HKD 3,000** | **<推薦>** 適合大部分谷友，負擔得起。 |

---

## 手機實戰操作 (IBKR Mobile)

錢的問題解決了，但操作有兩個陷阱：
1.  **必須是 Margin Account (保證金帳戶)**：Cash Account 做不到 Spread。
2.  **必須用 Strategy Builder (策略構建器)**：不能分開兩張單下 (Legging in)，否則會被拒單。

### 步驟教學：

**Step 1: 搜尋 MHI，選擇期權**
![IB 搜尋畫面](Education/images/mhi_step1.jpg)


**Step 2: 開啟策略構建器**
選擇第一隻 Strike (例如 Long 27000 Call)，然後點擊下方的「策略構建器」或「增加股票邊」。

**Step 3: 選擇兩隻腳 (Legs)**
* **Leg 1:** 買入 (Buy) 27000 Call
* **Leg 2:** 賣出 (Sell) 27400 Call
![IB 策略構建畫面](Education/images/mhi_step2.jpg)


**Step 4: 確認風險與下單**
改完之後你會見到 Net Debit (例如 148 點)。
* **Max Loss:** 權利金 HKD 1,480 (148 * 10)
* **Max Profit:** HKD 2,513
* **打和點:** 27148.26

![IB 風險分析畫面](Education/images/mhi_risk.jpg)


---

## 懶人包結論

1.  **錢的問題：** 不要玩大期 HSI，玩 **細期 MHI**。入場費大約 HKD 3,000，輸光也就是輸這 3000，不會負債。
2.  **帳戶問題：** 必須開 **Margin Account**。
3.  **操作問題：** 一定要用 **Strategy Builder** 將兩隻腳綁在一起下單。

