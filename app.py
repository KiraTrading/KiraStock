import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import sys
import glob
import time
import base64
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from io import BytesIO
from datetime import datetime

maxMessageSize = 600

# Add Trade folder path
sys.path.append('Trade')
try:
    from Trade import trade_app
except ImportError:
    pass

# ==========================================
# 0. Strategy Helper Functions (Adapted for Offline)
# ==========================================
# Set Matplotlib style for consistency
plt.style.use('dark_background')


def get_base64_plot(fig):
    """Convert matplotlib figure to base64 string"""
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=80, transparent=True)
    img_buffer.seek(0)
    b64_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close(fig)
    return b64_str


def fmt_money(val_per_share):
    """Formats price as: $1.50 ($150)"""
    if isinstance(val_per_share, str): return val_per_share
    real_val = val_per_share * 100
    return f"${val_per_share:.2f} <b>(${real_val:,.0f})</b>"


def get_local_data(ticker):
    """
    Reads local data from 'Option/Option' folder.
    Fixed: Case sensitivity bug in JSON filename matching.
    """
    # [PATH] Points to E:\ALGO_Snake\Website\Option\Option
    folder_path = os.path.join("Option", "Option")
    ticker = ticker.upper()

    # --- 1. Search for Stock CSV ---
    csv_files = glob.glob(os.path.join(folder_path, f"{ticker}_*.csv"))

    # 這裡也要加上 .upper() 以防萬一，確保比對一致
    valid_csvs = [f for f in csv_files if os.path.basename(f).upper().startswith(f"{ticker}_")]

    if not valid_csvs:
        # Debug info: 顯示絕對路徑幫助除錯
        abs_path = os.path.abspath(folder_path)
        return None, None, f"Stock data not found in {abs_path}. Please run data_updater.py."

    latest_csv = max(valid_csvs, key=os.path.getctime)
    try:
        df_hist = pd.read_csv(latest_csv, index_col=0, parse_dates=True)
    except Exception as e:
        return None, None, f"Error reading CSV: {e}"

    # --- 2. Search for Options JSON ---
    # 這裡搜尋的是含有 _options_ 的檔案
    json_files = glob.glob(os.path.join(folder_path, f"{ticker}_options_*.json"))

    # [BUG FIX HERE]
    # 原本: .startswith(f"{ticker}_options_") -> 導致 "OPTIONS" 與 "options" 不匹配
    # 修正: .startswith(f"{ticker}_options_".upper()) -> 確保兩邊都是大寫
    prefix_check = f"{ticker}_options_".upper()
    valid_jsons = [f for f in json_files if os.path.basename(f).upper().startswith(prefix_check)]

    if not valid_jsons:
        # 找不到檔案時，回傳詳細錯誤
        return df_hist, None, f"Option JSON not found for {ticker} (Checked prefix: {prefix_check})"

    latest_json = max(valid_jsons, key=os.path.getctime)
    try:
        with open(latest_json, 'r') as f:
            options_data = json.load(f)
    except Exception as e:
        return df_hist, None, f"Error reading JSON: {e}"

    # Extract date from filename for display
    try:
        data_date = latest_json.rsplit('_', 1)[1].replace('.json', '')
    except:
        data_date = "Unknown"

    return df_hist, options_data, data_date


def generate_strategy_html(ticker, spread_width, otm_pct, itm_pct):
    """
    Replicates the logic of your original script but using offline data.
    """
    # 1. Load Data
    hist, options_raw, data_date = get_local_data(ticker)

    if hist is None:
        return None, f"Stock data missing for {ticker}."
    if options_raw is None:
        return None, f"Option data missing for {ticker}."

    current_price = hist['Close'].iloc[-1]

    # Trend Analysis
    try:
        sma_20 = hist['Close'].tail(20).mean()
        sma_50 = hist['Close'].tail(50).mean()

        if current_price > sma_20 and current_price > sma_50:
            trend_text = "Bullish (Uptrend)"
            trend_color = "#2ecc71"
            rec_text = "Focus on Bullish Zone"
        elif current_price < sma_20 and current_price < sma_50:
            trend_text = "Bearish (Downtrend)"
            trend_color = "#e74c3c"
            rec_text = "Focus on Bearish Zone"
        else:
            trend_text = "Consolidation"
            trend_color = "#f1c40f"
            rec_text = "Focus on Volatility"
    except:
        trend_text = "Unknown"
        trend_color = "#888"
        rec_text = "N/A"

    # 2. Process Data
    selected_dates = list(options_raw.keys())
    selected_dates.sort()

    master_data = {}

    for target_date in selected_dates:
        # Convert JSON list back to DataFrame to match your original logic
        try:
            calls = pd.DataFrame(options_raw[target_date]['calls'])
            puts = pd.DataFrame(options_raw[target_date]['puts'])
        except:
            continue

        if calls.empty or puts.empty:
            continue

        def get_option(df, target_strike):
            if df.empty: return None
            idx = (df['strike'] - target_strike).abs().idxmin()
            return df.iloc[idx]

        plot_range = np.linspace(current_price * 0.7, current_price * 1.3, 100)
        date_data = {}

        # --- REPLICATING YOUR ORIGINAL LOGIC EXACTLY ---

        # 1. Naked Call (nc)
        nc_row = get_option(calls, current_price * otm_pct)
        if nc_row is not None:
            cost = nc_row['lastPrice']
            payoff = [max(0, p - nc_row['strike']) - cost for p in plot_range]

            fig, ax = plt.subplots(figsize=(5, 3))
            # Set transparent background for web
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            # Dark mode axis
            ax.spines['bottom'].set_color('#ccc');
            ax.spines['top'].set_color('none')
            ax.spines['left'].set_color('#ccc');
            ax.spines['right'].set_color('none')
            ax.tick_params(axis='x', colors='#ccc');
            ax.tick_params(axis='y', colors='#ccc')

            ax.plot(plot_range, payoff, color='#2ecc71', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1)
            ax.axvline(current_price, color='#aaa', linestyle=':')

            date_data["nc_setup"] = f"Buy ${nc_row['strike']} Call"
            date_data["nc_cost"] = fmt_money(cost)
            date_data["nc_loss"] = fmt_money(cost)
            date_data["nc_gain"] = "Unlimited"
            date_data["nc_break"] = f"${(nc_row['strike'] + cost):.2f}"
            date_data["nc_img"] = get_base64_plot(fig)

        # 2. Bull Call Spread (cs)
        cs_long = get_option(calls, current_price)
        cs_short = get_option(calls, current_price + spread_width)
        if cs_long is not None and cs_short is not None:
            cost = max(0.01, cs_long['lastPrice'] - cs_short['lastPrice'])
            max_gain = (cs_short['strike'] - cs_long['strike']) - cost
            payoff = [(max(0, p - cs_long['strike']) - max(0, p - cs_short['strike'])) - cost for p in plot_range]

            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_alpha(0.0);
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc');
            ax.spines['top'].set_color('none');
            ax.spines['left'].set_color('#ccc');
            ax.spines['right'].set_color('none');
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#27ae60', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1);
            ax.axvline(current_price, color='#aaa', linestyle=':')

            date_data["cs_setup"] = f"Buy ${cs_long['strike']} / Sell ${cs_short['strike']} Call"
            date_data["cs_cost"] = fmt_money(cost)
            date_data["cs_loss"] = fmt_money(cost)
            date_data["cs_gain"] = fmt_money(max_gain)
            date_data["cs_break"] = f"${(cs_long['strike'] + cost):.2f}"
            date_data["cs_img"] = get_base64_plot(fig)

        # 3. Naked Put (np)
        np_row = get_option(puts, current_price * itm_pct)
        if np_row is not None:
            cost = np_row['lastPrice']
            payoff = [max(0, np_row['strike'] - p) - cost for p in plot_range]

            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_alpha(0.0);
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc');
            ax.spines['top'].set_color('none');
            ax.spines['left'].set_color('#ccc');
            ax.spines['right'].set_color('none');
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#e74c3c', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1);
            ax.axvline(current_price, color='#aaa', linestyle=':')

            date_data["np_setup"] = f"Buy ${np_row['strike']} Put"
            date_data["np_cost"] = fmt_money(cost)
            date_data["np_loss"] = fmt_money(cost)
            date_data["np_gain"] = fmt_money(np_row['strike'] - cost)
            date_data["np_break"] = f"${(np_row['strike'] - cost):.2f}"
            date_data["np_img"] = get_base64_plot(fig)

        # 4. Bear Put Spread (ps)
        ps_long = get_option(puts, current_price)
        ps_short = get_option(puts, current_price - spread_width)
        if ps_long is not None and ps_short is not None:
            cost = max(0.01, ps_long['lastPrice'] - ps_short['lastPrice'])
            max_gain = (ps_long['strike'] - ps_short['strike']) - cost
            payoff = [(max(0, ps_long['strike'] - p) - max(0, ps_short['strike'] - p)) - cost for p in plot_range]

            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_alpha(0.0);
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc');
            ax.spines['top'].set_color('none');
            ax.spines['left'].set_color('#ccc');
            ax.spines['right'].set_color('none');
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#c0392b', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1);
            ax.axvline(current_price, color='#aaa', linestyle=':')

            date_data["ps_setup"] = f"Buy ${ps_long['strike']} / Sell ${ps_short['strike']} Put"
            date_data["ps_cost"] = fmt_money(cost)
            date_data["ps_loss"] = fmt_money(cost)
            date_data["ps_gain"] = fmt_money(max_gain)
            date_data["ps_break"] = f"${(ps_long['strike'] - cost):.2f}"
            date_data["ps_img"] = get_base64_plot(fig)

        # 5. Straddle (st)
        atm_call = get_option(calls, current_price)
        atm_put = get_option(puts, current_price)
        if atm_call is not None and atm_put is not None:
            cost = atm_call['lastPrice'] + atm_put['lastPrice']
            strike = atm_call['strike']
            payoff = [(max(0, p - strike) + max(0, strike - p)) - cost for p in plot_range]

            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_alpha(0.0);
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc');
            ax.spines['top'].set_color('none');
            ax.spines['left'].set_color('#ccc');
            ax.spines['right'].set_color('none');
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#9b59b6', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1);
            ax.axvline(current_price, color='#aaa', linestyle=':')

            date_data["st_setup"] = f"Buy Call + Put (${strike})"
            date_data["st_cost"] = fmt_money(cost)
            date_data["st_loss"] = fmt_money(cost)
            date_data["st_gain"] = "Unlimited"
            date_data["st_break"] = f"${(strike - cost):.2f} / ${(strike + cost):.2f}"
            date_data["st_img"] = get_base64_plot(fig)

        master_data[target_date] = date_data

    # --- HTML ASSEMBLY (Using your exact HTML structure) ---
    json_data = json.dumps(master_data)
    options_html = "".join([f'<option value="{d}">{d}</option>' for d in selected_dates])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{ticker.upper()} Interactive Dashboard</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: transparent; margin: 0; padding: 20px; color: #e2e8f0; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}

            /* TOP BAR */
            .top-bar {{ background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-left: 5px solid #3b82f6; border: 1px solid rgba(255,255,255,0.1); }}
            .title-group h1 {{ margin: 0; font-size: 24px; color: #f8fafc; }}
            .title-group p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 0.9em; }}

            /* SELECTOR STYLING */
            .control-group {{ text-align: right; }}
            select {{ padding: 10px 15px; font-size: 16px; border-radius: 8px; border: 1px solid #475569; background: #1e293b; color: white; cursor: pointer; outline: none; font-weight: bold; }}
            select:hover {{ background: #334155; }}

            .rec-tag {{ display:inline-block; margin-top:5px; background: {trend_color}; color: #111827; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.8em; }}
            .assumption {{ background: rgba(251, 191, 36, 0.2); color: #fbbf24; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; border: 1px solid rgba(251, 191, 36, 0.4); margin-left:10px; }}

            /* LAYOUT */
            .section-title {{ display: flex; align-items: center; margin: 30px 0 15px 0; color: #e2e8f0; font-size: 1.4em; border-bottom: 1px solid #334155; padding-bottom: 10px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .single-col {{ max-width: 600px; margin: 0 auto; }}

            /* CARD STYLING */
            .card {{ background: rgba(30, 41, 59, 0.5); border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; transition: opacity 0.3s; border: 1px solid rgba(255,255,255,0.05); }}
            .card-header {{ padding: 12px 15px; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2); border-bottom: 1px solid rgba(255,255,255,0.05); }}
            .card-header h4 {{ margin: 0; color: #f1f5f9; }}
            .badge {{ font-size: 0.75em; background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 4px; color: #cbd5e1; }}
            .logic {{ padding: 8px 15px; background: rgba(255,255,255,0.02); font-size: 0.85em; color: #94a3b8; font-style: italic; border-bottom: 1px solid rgba(255,255,255,0.05); }}

            img {{ width: 100%; display: block; min-height: 200px; background: transparent; }}

            .stats {{ padding: 10px 15px; font-size: 0.9em; }}
            .stat-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed rgba(255,255,255,0.1); color: #cbd5e1; }}
            .setup-footer {{ background: rgba(0,0,0,0.3); color: #93c5fd; padding: 10px; text-align: center; font-size: 0.9em; font-weight: bold; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="top-bar">
                <div class="title-group">
                    <h1>📊 {ticker.upper()} Strategy Dashboard <span style="font-size:0.5em; color:#64748b; margin-left:10px;">Data: {data_date}</span></h1>
                    <p>Price: <strong>${current_price:.2f}</strong> <span class="assumption">⚠️ Cost: 1 Lot (100 Shares)</span></p>
                    <span class="rec-tag">{trend_text} - {rec_text}</span>
                </div>
                <div class="control-group">
                    <label style="display:block; font-size:0.8em; color:#94a3b8; margin-bottom:5px;">📅 Select Expiry:</label>
                    <select id="expirySelector" onchange="updateDashboard()">
                        {options_html}
                    </select>
                </div>
            </div>

            <div class="section-title">📈 Bullish Strategies</div>
            <div class="grid">
                <div class="card" style="border-top: 4px solid #2ecc71">
                    <div class="card-header"><h4>Naked Call</h4><span class="badge">Aggressive</span></div>
                    <div class="logic">Maximizes profit if stock rallies hard.</div>
                    <img id="img_nc" src="" />
                    <div class="stats">
                        <div class="stat-row"><span>Cost:</span> <strong id="val_nc_cost">-</strong></div>
                        <div class="stat-row"><span>Max Loss:</span> <strong style="color:#ef4444" id="val_nc_loss">-</strong></div>
                        <div class="stat-row"><span>Max Gain:</span> <strong style="color:#2ecc71" id="val_nc_gain">-</strong></div>
                        <div class="stat-row" style="border-bottom:none"><span>Breakeven:</span> <strong id="val_nc_break">-</strong></div>
                    </div>
                    <div class="setup-footer" id="txt_nc_setup">...</div>
                </div>

                <div class="card" style="border-top: 4px solid #2ecc71">
                    <div class="card-header"><h4>Bull Call Spread</h4><span class="badge">Conservative</span></div>
                    <div class="logic">Reduces cost & risk. Best for moderate rally.</div>
                    <img id="img_cs" src="" />
                    <div class="stats">
                        <div class="stat-row"><span>Cost:</span> <strong id="val_cs_cost">-</strong></div>
                        <div class="stat-row"><span>Max Loss:</span> <strong style="color:#ef4444" id="val_cs_loss">-</strong></div>
                        <div class="stat-row"><span>Max Gain:</span> <strong style="color:#2ecc71" id="val_cs_gain">-</strong></div>
                        <div class="stat-row" style="border-bottom:none"><span>Breakeven:</span> <strong id="val_cs_break">-</strong></div>
                    </div>
                    <div class="setup-footer" id="txt_cs_setup">...</div>
                </div>
            </div>

            <div class="section-title">📉 Bearish Strategies</div>
            <div class="grid">
                <div class="card" style="border-top: 4px solid #e74c3c">
                    <div class="card-header"><h4>Naked Put</h4><span class="badge">Aggressive</span></div>
                    <div class="logic">Maximizes profit if stock crashes hard.</div>
                    <img id="img_np" src="" />
                    <div class="stats">
                        <div class="stat-row"><span>Cost:</span> <strong id="val_np_cost">-</strong></div>
                        <div class="stat-row"><span>Max Loss:</span> <strong style="color:#ef4444" id="val_np_loss">-</strong></div>
                        <div class="stat-row"><span>Max Gain:</span> <strong style="color:#2ecc71" id="val_np_gain">-</strong></div>
                        <div class="stat-row" style="border-bottom:none"><span>Breakeven:</span> <strong id="val_np_break">-</strong></div>
                    </div>
                    <div class="setup-footer" id="txt_np_setup">...</div>
                </div>

                <div class="card" style="border-top: 4px solid #e74c3c">
                    <div class="card-header"><h4>Bear Put Spread</h4><span class="badge">Conservative</span></div>
                    <div class="logic">Cheaper way to bet on a drop.</div>
                    <img id="img_ps" src="" />
                    <div class="stats">
                        <div class="stat-row"><span>Cost:</span> <strong id="val_ps_cost">-</strong></div>
                        <div class="stat-row"><span>Max Loss:</span> <strong style="color:#ef4444" id="val_ps_loss">-</strong></div>
                        <div class="stat-row"><span>Max Gain:</span> <strong style="color:#2ecc71" id="val_ps_gain">-</strong></div>
                        <div class="stat-row" style="border-bottom:none"><span>Breakeven:</span> <strong id="val_ps_break">-</strong></div>
                    </div>
                    <div class="setup-footer" id="txt_ps_setup">...</div>
                </div>
            </div>

            <div class="section-title">💥 Volatility (Straddle)</div>
            <div class="single-col">
                <div class="card" style="border-top: 4px solid #9b59b6">
                    <div class="card-header"><h4>Long Straddle</h4><span class="badge">Big Move</span></div>
                    <div class="logic">Profit if stock explodes up OR crashes down.</div>
                    <img id="img_st" src="" />
                    <div class="stats">
                        <div class="stat-row"><span>Cost:</span> <strong id="val_st_cost">-</strong></div>
                        <div class="stat-row"><span>Max Loss:</span> <strong style="color:#ef4444" id="val_st_loss">-</strong></div>
                        <div class="stat-row"><span>Max Gain:</span> <strong style="color:#2ecc71" id="val_st_gain">-</strong></div>
                        <div class="stat-row" style="border-bottom:none"><span>Breakeven:</span> <strong id="val_st_break">-</strong></div>
                    </div>
                    <div class="setup-footer" id="txt_st_setup">...</div>
                </div>
            </div>

            <br><br>
        </div>

        <script>
            const strategiesData = {json_data};

            function updateDashboard() {{
                const selector = document.getElementById('expirySelector');
                const selectedDate = selector.value;
                const data = strategiesData[selectedDate];

                // Helper to update text and image
                const setTxt = (id, val) => {{
                    const el = document.getElementById(id);
                    if(el) el.innerHTML = val;
                }};
                const setImg = (id, b64) => {{
                    const el = document.getElementById(id);
                    if(el) el.src = "data:image/png;base64," + b64;
                }};

                if (data) {{
                    // 1. Naked Call
                    setTxt('val_nc_cost', data.nc_cost);
                    setTxt('val_nc_loss', data.nc_loss);
                    setTxt('val_nc_gain', data.nc_gain);
                    setTxt('val_nc_break', data.nc_break);
                    setTxt('txt_nc_setup', data.nc_setup);
                    setImg('img_nc', data.nc_img);

                    // 2. Bull Spread
                    setTxt('val_cs_cost', data.cs_cost);
                    setTxt('val_cs_loss', data.cs_loss);
                    setTxt('val_cs_gain', data.cs_gain);
                    setTxt('val_cs_break', data.cs_break);
                    setTxt('txt_cs_setup', data.cs_setup);
                    setImg('img_cs', data.cs_img);

                    // 3. Naked Put
                    setTxt('val_np_cost', data.np_cost);
                    setTxt('val_np_loss', data.np_loss);
                    setTxt('val_np_gain', data.np_gain);
                    setTxt('val_np_break', data.np_break);
                    setTxt('txt_np_setup', data.np_setup);
                    setImg('img_np', data.np_img);

                    // 4. Bear Spread
                    setTxt('val_ps_cost', data.ps_cost);
                    setTxt('val_ps_loss', data.ps_loss);
                    setTxt('val_ps_gain', data.ps_gain);
                    setTxt('val_ps_break', data.ps_break);
                    setTxt('txt_ps_setup', data.ps_setup);
                    setImg('img_ps', data.ps_img);

                    // 5. Straddle
                    setTxt('val_st_cost', data.st_cost);
                    setTxt('val_st_loss', data.st_loss);
                    setTxt('val_st_gain', data.st_gain);
                    setTxt('val_st_break', data.st_break);
                    setTxt('txt_st_setup', data.st_setup);
                    setImg('img_st', data.st_img);
                }}
            }}

            window.onload = updateDashboard;
        </script>
    </body>
    </html>
    """
    return html_content, "Success"


# ==========================================
# 🔐 Security Login System
# ==========================================


def check_access_or_show_teaser(page_name, teaser_image_url=None, description=None):
    """
    如果已登入 -> 返回 True
    如果未登入 -> 顯示該功能的銷售文案 (Teaser) + 登入/購買按鈕 -> 返回 False
    """
    if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
        return True

    # --- 未登入狀態下的 Teaser 介面 ---
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px; background: rgba(17, 24, 39, 0.6); border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3);">
        <h2 style="color: #60a5fa;">🔒 Locked Feature: {page_name}</h2>
        <p style="font-size: 1.2em; color: #e2e8f0; max-width: 600px; margin: 0 auto;">
            {description if description else "This institutional-grade tool is reserved for VIP members."}
        </p>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 30px 0;">
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔑 Member Login")
        with st.form(f"login_form_{page_name}"):
            email_input = st.text_input("Email", key=f"email_{page_name}")
            password_input = st.text_input("Password", type="password", key=f"pw_{page_name}")
            submit = st.form_submit_button("Login to Access", type="secondary", use_container_width=True)

            if submit:
                login_success = False
                # 這裡填入你的驗證邏輯
                try:
                    valid_emails = st.secrets["allowed_users"]["emails"]
                    correct_password = st.secrets["access_password"]
                    if email_input in valid_emails and password_input == correct_password:
                        st.session_state["authentication_status"] = True
                        st.session_state["user_email"] = email_input
                        st.success("Access Granted.")
                        login_success = True  # 標記為成功
                    else:
                        st.error("Invalid Credentials")
                except Exception as e:  # ⚠️ 修改這裡：只捕捉一般錯誤，不捕捉系統訊號
                    st.error(f"System Config Error: {e}")
                # ⚠️ 將 rerun 移到 try/except 外面執行
                if login_success:
                    time.sleep(0.5)
                    st.rerun()
    with c2:
        st.markdown("#### 🚀 Not a Member?")
        st.markdown("""
        <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #2563EB;">
            <p style="font-size: 0.9em; margin-bottom: 15px;">
                Unlock this tool and get full access to Stock DNA, Option Flows, and my personal trade portfolio.
            </p>
            <a href="https://parisprogram.uk/zh/member-dash/plans/" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: #fbbf24; color: black; border: none; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                    Get VIP Access Now
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 如果有預覽圖，可以放在下面 (Optional)
    if teaser_image_url:
        st.image(teaser_image_url, caption="Preview of Tool (Blur)", use_column_width=True)

    return False


# --- Main Program Logic ---
# Uncomment to enable login
# if not login_system():
#    st.stop()

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ParisTrader - Quant Trading & Market Analysis | 2026香港投資銀行學習",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. Custom CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;700&display=swap');

    .stApp {
        background: transparent !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', 'Microsoft JhengHei', sans-serif;
        color: #e2e8f0;
    }

    /* Navigation Font Optimization for Bilingual Headers */
    [data-testid="stSidebarNav"] span {
        font-size: 14px !important;
        white-space: nowrap;
    }
    .nav-link {
        font-size: 14px !important;
        padding: 8px 10px !important;
    }

    @media (min-width: 768.1px) {
        header { visibility: hidden !important; }
        [data-testid="stSidebarCollapseButton"] { display: none !important; }
        section[data-testid="stSidebar"] button { display: none !important; }
        [data-testid="stToolbar"], [data-testid="stHeaderActionElements"] { visibility: hidden !important; display: none !important; }
        #MainMenu { visibility: hidden !important; display: none !important; }
    }

    @media (max-width: 768px) {
        header { visibility: visible !important; background: transparent !important; }
        header button[kind="header"] {
            background-color: rgba(17, 24, 39, 0.6) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
        }
        .block-container {
            padding-top: 3rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.2rem !important; }
    }

    footer { visibility: hidden !important; display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }

    .fixed-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
        z-index: -1; 
        background-color: #020617;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
        -webkit-mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
    }

    .fixed-blobs {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
        z-index: -1;
        background: 
            radial-gradient(circle at 10% 10%, rgba(79, 70, 229, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 20%, rgba(14, 165, 233, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 30% 90%, rgba(16, 185, 129, 0.1) 0%, transparent 40%);
        filter: blur(60px); pointer-events: none;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827; 
        border-right: 1px solid #374151;
        z-index: 999999 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #F3F4F6 !important;
    }

    .metric-card {
        background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;
        padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .metric-card h4 { color: #94a3b8; font-size: 0.9em; text-transform: uppercase; margin: 0; }
    .metric-card h2 { color: #f8fafc; margin: 5px 0; font-size: 1.8em; }

    .profile-card {
        background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;
        padding: 25px; text-align: center;
    }

    .custom-footer {
        margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; color: #94a3b8; font-size: 0.8rem;
    }
    .custom-footer a { color: #60a5fa; text-decoration: none; margin: 0 10px; }
    .custom-footer a:hover { text-decoration: underline; }

    .legal-text {
        font-size: 0.95rem; line-height: 1.7; color: #e2e8f0; text-align: justify;
        background: rgba(255, 255, 255, 0.03); padding: 30px;
        border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .legal-text h3 { color: #f8fafc !important; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px; }
    .legal-text h4 { color: #e2e8f0 !important; margin-top: 20px; font-weight: bold; }
    .legal-text strong { color: #f8fafc !important; }
</style>

<div class="fixed-bg"></div>
<div class="fixed-blobs"></div>
""", unsafe_allow_html=True)


# ==========================================
# 3. Helper Functions
# ==========================================

def load_markdown_with_images(file_path):
    """
    讀取 Markdown 檔案，並自動將本地圖片路徑轉換為 Base64 編碼。
    修復了 PC 版圖片過大導致版面跑位的問題。
    """
    if not os.path.exists(file_path):
        return f"<div style='color:red'>⚠️ File not found: {file_path}</div>"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正則表達式：尋找 ![alt](path) 格式的圖片語法
    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    def replace_image_link(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # 檢查是否為本地路徑 (不包含 http 開頭)
        if not image_path.startswith('http') and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode()
                    ext = image_path.split('.')[-1].lower()
                    mime_type = f"image/{ext}"
                    if ext == 'svg': mime_type = "image/svg+xml"

                    # [關鍵修改]
                    # 1. 外層 div 加入 text-align: center 讓圖片在 PC 上置中
                    # 2. img 標籤改用 max-width: 100% (不強制拉伸，只限制最大寬度)
                    # 3. 加入 max-height: 600px 限制 PC 上圖片不要高過 600px，避免佔滿畫面
                    # 4. width: auto; height: auto 保持圖片原始比例
                    return (
                        f'<div style="width:100%; text-align: center; margin: 20px 0;">'
                        f'<img src="data:{mime_type};base64,{b64_string}" alt="{alt_text}" '
                        f'style="max-width: 100%; max-height: 800px; width: auto; height: auto; '
                        f'border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">'
                        f'</div>'
                    )
            except Exception as e:
                return f"⚠️ Image Load Error: {str(e)}"

        return match.group(0)

    # 執行替換
    enhanced_content = image_pattern.sub(replace_image_link, content)
    return enhanced_content


def load_weekly_analysis():
    file_path = os.path.join("WeeklyContent", "latest_analysis.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "⚠️ Weekly analysis not uploaded yet (File not found: WeeklyContent/latest_analysis.md)"


def load_html_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return f"<div style='padding:20px; color:red;'>⚠️ File not found: {file_path}</div>"


def load_stock_dna_with_injection():
    # 1. Get absolute paths to ensure it works from any directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "FamaFrench", "index.html")
    csv_factor_path = os.path.join(current_dir, "FamaFrench", "stock_factor_data.csv")
    csv_returns_path = os.path.join(current_dir, "FamaFrench", "stock_returns_data.csv")

    if not os.path.exists(html_path):
        return f"<div style='color:red'>HTML not found: {html_path}</div>"

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # ---------------------------------------------------------
    # 1. Inject Factor Data (Your original logic)
    # ---------------------------------------------------------
    if os.path.exists(csv_factor_path):
        with open(csv_factor_path, 'r', encoding='utf-8') as f:
            csv_data = f.read()
            # Clean up backticks just in case
            csv_data = csv_data.replace('`', '')

        # JS to inject: Create variable -> Parse variable -> Disable download
        injection_js = f"""
        var csvData = `{csv_data}`;
        Papa.parse(csvData, {{
            download: false, 
        """

        target_str = 'Papa.parse("stock_factor_data.csv", {'
        if target_str in html_content:
            html_content = html_content.replace(target_str, injection_js)

    # ---------------------------------------------------------
    # 2. Inject Returns Data (The NEW addition)
    # ---------------------------------------------------------
    if os.path.exists(csv_returns_path):
        with open(csv_returns_path, 'r', encoding='utf-8') as f:
            returns_data = f.read()
            returns_data = returns_data.replace('`', '')

        # JS to inject: Use a DIFFERENT variable name (returnsCSVData)
        injection_js_ret = f"""
        var returnsCSVData = `{returns_data}`;
        Papa.parse(returnsCSVData, {{
            download: false, 
        """

        target_str_ret = 'Papa.parse("stock_returns_data.csv", {'
        if target_str_ret in html_content:
            html_content = html_content.replace(target_str_ret, injection_js_ret)

    # ---------------------------------------------------------
    # 3. Global Cleanup
    # ---------------------------------------------------------
    # Since we injected 'download: false', we remove the original 'download: true'
    # to avoid syntax errors or conflicting keys in the JS object.
    html_content = html_content.replace('download: true,', '')

    return html_content


def load_options_strategy_dashboard():
    """
    Reads the options dashboard HTML and injects the JSON data
    directly into the script to avoid local file loading issues.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "Option", "options_dashboard.html")
    json_path = os.path.join(current_dir, "Option", "all_strategies_data.json")

    if not os.path.exists(html_path):
        return f"<div style='padding:20px; color:red;'>⚠️ HTML File not found: {html_path}</div>"

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()

        # We inject the JSON data as a global JS variable.
        # You may need to ensure your HTML script uses 'window.allStrategiesData'
        # instead of fetch('all_strategies_data.json').
        injection_js = f"<script>window.allStrategiesData = {json_data};</script>"

        if "<head>" in html_content:
            html_content = html_content.replace("<head>", f"<head>{injection_js}")
        else:
            html_content = injection_js + html_content

    return html_content


def get_latest_file_content(folder_path, pattern="*.html"):
    if not os.path.exists(folder_path):
        return None, f"Directory not found: {folder_path}"

    search_pattern = os.path.join(folder_path, pattern)
    list_of_files = glob.glob(search_pattern)

    if not list_of_files:
        return None, f"No files found matching {pattern}."

    latest_file = max(list_of_files, key=os.path.getctime)

    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return f.read(), os.path.basename(latest_file)
    except Exception as e:
        return None, str(e)


# ==========================================
# 4. Main App Interface (Mixed Navigation)
# ==========================================

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #374151; margin-bottom: 20px;'>
        <h2 style='color: #F3F4F6; margin:0; letter-spacing: 1px; font-weight: 700;'>ParisTrader</h2>
        <p style='color: #9CA3AF; font-size: 0.85em; margin-top:5px;'>Quant Research</p>
    </div>
    """, unsafe_allow_html=True)


    # -------------------------------------------------------------------------
    # IMPROVED NAVIGATION LOGIC (Fixing the Double-Click Bug)
    # -------------------------------------------------------------------------

    # 1. 定義 Callback 函數：當選單改變時，立即更新 URL
    def on_nav_change(key):
        # 獲取選單現在的選擇 (透過 key)
        if "main_nav_key" in st.session_state:
            new_selection = st.session_state["main_nav_key"]
            # 立即更新 URL，這樣下一次 Rerun 時讀取到的就是正確的 Page
            st.query_params["page"] = new_selection
            # 切換主頁面時，清除子頁面參數，避免邏輯衝突
            if "sub" in st.query_params:
                del st.query_params["sub"]


    # 2. Capture the URL params
    query_params = st.query_params
    url_main_page = query_params.get("page", "首頁 Home")  # Default to Home
    url_sub_page = query_params.get("sub", None)  # Capture sub-page

    # Define Main Menu Options (HK Style)
    main_options = [
        "首頁 Home",
        "研究專欄 Research",
        "大市情報 Intelligence",
        "實戰持倉 Portfolio",
        "美股數據 Stock",
        "期權分析 Option",
        "期貨/牛熊 Future",
        "自動交易 MT5 EA",
        "交易學院 Education",
        "交易社群 Community",
        "工具資源 Resources",
        "升級會員 VIP"
    ]

    # Determine default index for Main Menu based on URL
    # Support for legacy URLs (e.g., "Home" maps to "首頁 Home")
    try:
        # Try exact match first
        main_default_index = main_options.index(url_main_page)
    except ValueError:
        # Fallback: fuzzy match (e.g. url "Home" finds "首頁 Home")
        matches = [i for i, opt in enumerate(main_options) if url_main_page in opt]
        main_default_index = matches[0] if matches else 0

    # 3. Render the Main Sidebar Menu
    selected_nav = option_menu(
        menu_title="Navigation",
        options=main_options,
        icons=[
            "house", "globe", "search", "briefcase", "list-task", "layers",
            "graph-up-arrow", "robot", "mortarboard", "people-fill", "collection", "gem"
        ],
        menu_icon="compass",
        default_index=main_default_index,  # Sync with URL
        key="main_nav_key",  # 設定一個唯一的 key
        on_change=on_nav_change,  # 綁定回調函數
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#9CA3AF", "font-size": "15px"},
            "nav-link": {
                "font-size": "15px", "text-align": "left", "margin": "5px",
                "color": "#D1D5DB", "--hover-color": "#1F2937",
            },
            "nav-link-selected": {"background-color": "#2563EB", "color": "#FFFFFF", "font-weight": "600"},
        }
    )

    # 3. Handle Sub-Menus and Update URL for Sub-Pages
    target_page = selected_nav  # Default target is the main selection


    # --- Helper to handle sub-menu logic ---
    def handle_submenu(key_name, options, icons):
        # Calculate default index for sub-menu based on URL 'sub' param
        # Only if the main page matches the current selection
        default_sub_index = 0
        if (url_main_page in selected_nav) and (url_sub_page in options):
            default_sub_index = options.index(url_sub_page)
        # Robust check for partial matches in URL sub params
        elif (url_main_page in selected_nav) and url_sub_page:
            matches = [i for i, opt in enumerate(options) if url_sub_page in opt]
            if matches:
                default_sub_index = matches[0]

        selection = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            default_index=default_sub_index,
            styles={
                "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.03)",
                              "border-radius": "10px"},
                "nav-link": {"font-size": "14px", "margin": "3px", "--hover-color": "#374151"},
                "nav-link-selected": {"background-color": "#4B5563"},
            },
            key=key_name  # Unique key is important
        )
        return selection


    # --- Sub-menu Logic (HK Style) ---
    if selected_nav == "大市情報 Intelligence":
        st.caption("MARKET MODULES")
        target_page = handle_submenu(
            "sub_market",
            ["風險指標 Market Risk", "市寬 Market Breadth"],
            ["activity", "bar-chart-line"]
        )

    elif selected_nav == "美股數據 Stock":
        st.caption("STOCK RESEARCH")
        target_page = handle_submenu(
            "sub_stock",
            [
                "主題籃子 Thematic Basket",
                "ETF資金流 Smart Money",
                "標普熱力圖 S&P 500",  # 👈 確保這裡有逗號
                "板塊熱力圖 Sector Heatmap",  # 👈 確保這裡有逗號
                "業績公佈 Earnings",
                "內部交易 Insider",
                "挾淡倉 Short Squeeze",
                "因子模型 Stock DNA",
                "波動率策略 Volatility Target",  # 👈 這裡也要小心
                "標普熱力圖 S&P 500"  # (你原代碼最後多了一個重複的項目，如果不想要可以刪除這行)
            ],
            [
                "basket",  # Thematic Basket
                "graph-up-arrow",  # ETF Smart Money
                "fire",  # 👈 修正點：補上逗號！ (原本這裡漏了)
                "grid-3x3",  # 👈 修正點：補上逗號！
                "cash-coin",  # Earnings
                "people",  # Insider Trading
                "lightning-charge",  # Short Squeeze
                "radar",  # Stock DNA
                "bullseye",  # Volatility Target
                "fire"  # S&P 500 (對應上面的重複項)
            ]
        )

    elif selected_nav == "期貨/牛熊 Future":
        st.caption("FUTURES & TRENDS")
        target_page = handle_submenu(
            "sub_future",
            ["日內波幅 Volatility", "成交分佈 Volume Profile", "牛熊重貨區 CBBC Ladder"],
            ["bar-chart-steps", "lightning-charge", "distribute-vertical"]
        )

    elif selected_nav == "期權分析 Option":
        st.caption("DERIVATIVES ANALYTICS")
        target_page = handle_submenu(
            "sub_option",
            ["港股期權 HK Option", "美股期權 US Option", "期權策略 Strategy"],  # Added here
            ["currency-dollar", "globe-asia-australia", "cpu"]  # Added icon
        )

    elif selected_nav == "自動交易 MT5 EA":
        st.caption("AUTOMATED TRADING")
        target_page = handle_submenu(
            "sub_ea",
            ["EA 介紹 Introduction"],
            ["robot"]
        )

    # --- 4. Deep Linking: Update URL based on final selection ---

    # Case A: Sidebar item matches target (Home, Education, etc. - No sub-menu)
    # COMMENTED OUT TO FIX DOUBLE CLICK BUG (Handled by on_nav_change)
    # if selected_nav == target_page:
    #     if url_main_page != selected_nav or url_sub_page is not None:
    #         st.query_params["page"] = selected_nav
    #         # Remove 'sub' param if it exists, as this page has no sub-menu
    #         if "sub" in st.query_params:
    #             del st.query_params["sub"]
    #         # time.sleep(0.1) # Optional: sometimes helps with race conditions

    # Case B: Target is a sub-menu item
    if selected_nav != target_page:
        # Check if URL needs update
        if url_main_page != selected_nav or url_sub_page != target_page:
            st.query_params["page"] = selected_nav
            st.query_params["sub"] = target_page

    st.markdown("---")

    # ---------------------------------------------------------
    # ✨ 改良後的 VIP 升級按鈕 (Gold/Pulse Effect) - [已修復連結]
    # ---------------------------------------------------------
    st.markdown("""
        <style>
            /* 定義呼吸燈動畫 */
            @keyframes pulse-gold {
                0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
                100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
            }

            .vip-promo-card {
                background: linear-gradient(135deg, #B45309 0%, #F59E0B 50%, #D97706 100%);
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                margin-bottom: 20px;
                margin-top: 10px;
                border: 1px solid #FCD34D;
                animation: pulse-gold 2s infinite;
            }

            /* 修改重點：直接將 link 變成按鈕樣式，移除 button 標籤以修復點擊問題 */
            a.vip-button-link {
                display: block;
                width: 100%;
                background: #FFFFFF;
                color: #B45309 !important; /* 強制深金色文字 */
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: 800;
                cursor: pointer;
                margin-top: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                transition: transform 0.1s;
                text-decoration: none !important; /* 移除底線 */
                text-align: center;
                box-sizing: border-box; /* 確保 padding 不會撐破寬度 */
            }

            a.vip-button-link:hover {
                transform: scale(1.02);
                background: #FEF3C7;
                color: #92400E !important;
            }

            a.vip-button-link:visited, a.vip-button-link:active {
                color: #B45309 !important;
            }
        </style>

        <div class="vip-promo-card">
            <h3 style="color: #FFFFFF; margin:0; font-size: 18px; font-weight: 800; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
                👑 升級 VIP 會員
            </h3>
            <p style="color: #FEF3C7; font-size: 12px; margin: 8px 0; line-height: 1.4;">
                解鎖機構級數據 (Stock DNA)<br>
                & 實戰倉位 (Portfolio)
            </p>
            <a href="?page=升級會員 VIP" target="_self" class="vip-button-link">
                🚀 立即加入 (Join Now)
            </a>
        </div>
    """, unsafe_allow_html=True)

# Handle Legal from Footer (Special Case)
if url_main_page == "Legal" and selected_nav == "首頁 Home":
    target_page = "Legal"

# ==========================================
# 🔒 權限控制與銷售轉化中心
# ==========================================

# Updated keys to match HK Style names
locked_pages = [
    # "實戰持倉 Portfolio",  <-- REMOVED as per request to allow partial access
    "因子模型 Stock DNA",
    "ETF資金流 Smart Money",
    "內部交易 Insider",
    "挾淡倉 Short Squeeze",
    "波動率策略 Volatility Target",
    "美股期權 US Option",
    "成交分佈 Volume Profile",
    "期權策略 Strategy",
    "牛熊重貨區 CBBC Ladder"
]

# Updated keys for teaser content
teaser_content = {
    "因子模型 Stock DNA": "Discover the hidden factors driving stock prices using Fama-French models. Identify high-quality alpha before the market moves.",
    "ETF資金流 Smart Money": "Track leveraged ETF flows to spot market reversals instantly. Don't fight the trend, ride the institutional wave.",
    "內部交易 Insider": "See what CEOs and CFOs are doing with their own money. Real-time cluster buying alerts.",
    "挾淡倉 Short Squeeze": "Identify the next GME/AMC before it explodes. High short interest + High borrow cost scanner.",
    "美股期權 US Option": "Follow the Smart Money. Real-time unusual options activity and gamma exposure levels.",
    "港股期權 HK Option": "Advanced market scanner for HK derivatives. Visualise the heavy zones and institutional positioning.",
    "實戰持倉 Portfolio": "Access my personal trade journal. See exactly when I enter and exit positions in Stocks and Options.",
    "成交分佈 Volume Profile": "Professional grade Volume Profile analysis to identify key support and resistance levels.",
    "日內波幅 Volatility": "Monitor real-time volatility spikes to capture intraday momentum.",
    "牛熊重貨區 CBBC Ladder": "Visualise the Bear/Bull contract heavy zones to predict market dealer hedging moves.",
    "期權策略 Strategy": "Quantitative Analysis & Strategy Performance."
}

if target_page in locked_pages:
    desc = teaser_content.get(target_page, "Access professional-grade tools designed for serious traders.")
    if not check_access_or_show_teaser(target_page, description=desc):
        st.stop()

# --- Content Routing (Based on target_page) ---
# [PAGE] HOME
if target_page == "首頁 Home":
    col_main, col_profile = st.columns([0.7, 0.3], gap="large")

    with col_main:
        st.markdown("""
        <h1 style='color:white;'>Ex-Ibanker開發-首個機構級黑科技</h1>
        <h3 style='color:#94a3b8;'>美股期權策略|NQ HSI 金期貨自動交易EA </h3>
        <p style='font-size: 1.1em; color: #64748b;'>
        贏錢不可能只看圖表交易 ,持續盈利交易員必備學習資源平台!
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")

        components.html("""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
          {
          "symbols": [
            {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
            {"proName": "FOREXCOM:NSXUSD", "title": "US 100"},
            {"description": "Gold", "proName": "OANDA:XAUUSD"}
          ],
          "showSymbolLogo": true,
          "colorTheme": "dark",
          "isTransparent": true,
          "displayMode": "adaptive",
          "locale": "en"
          }
          </script>
        </div>
        """, height=100)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📺 網站使用教學")
        st.video("https://www.youtube.com/watch?v=qb3XtEPj8cA")

        st.markdown("<br>", unsafe_allow_html=True)

        st.link_button(
            label="📊 點擊閱讀：下周大市分析 (Weekly Market Analysis)",
            url="https://parisprogram.uk/zh/member/post/RPT-20260117202415071?hash=c2894152df242ddf36604b022a1fbf98fe6b210be085496dba758628c35ebbc4",
            type="primary",
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("🧠 Week Ahead")

        with st.container():
            analysis_content = load_weekly_analysis()
            with st.expander("📖 Click to expand/collapse full analysis", expanded=True):
                st.markdown(analysis_content)

    with col_profile:
        img_path = "static/profile.jpg"
        if not os.path.exists(img_path):
            img_src = "https://ui-avatars.com/api/?name=Paris+Trader&background=0D8ABC&color=fff&size=150"
        else:
            img_src = img_path

        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        if os.path.exists(img_path):
            st.image(img_path, width=120)
        else:
            st.image(img_src, width=120)

        st.markdown("""
            <h3 style="margin-top:10px; color:#F3F4F6;">Paris Trader</h3>
            <p style="color: #9CA3AF; font-size: 0.9em;">Ex-Ibank Quantitative Trader</p>
            <hr style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="text-align: left; font-size: 0.9em; line-height: 1.6; color: #e2e8f0;">
                專注於量化因子挖掘與程式化交易。擅長將複雜的金融模型轉化為可執行的實戰策略，並提供獨家 TradingView 指標與回測數據。
                <br><br>
                <b>擅長策略 Core Strategies:</b><br>
                • 美股多因子長短倉 (Multi-Factor L/S)<br>
                • 期貨NQ黃金HSI Scalping (Future Scalping)<br>
                • 美股期權異動簍略 (Unusual Options)<br>
            </p>
            <a href="https://t.me/ParisTrader" target="_blank" style="text-decoration: none;">
                <button style="background-color:#2563EB; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; width:100%; margin-top:10px; font-weight:bold;">
                    Contact Me
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

# [PAGE] Market Dashboard
elif target_page == "Market Dashboard":
    st.title("Market Dashboard")
    path = os.path.join("MarketDashboard", "main_auto", "output")
    html_content, filename = get_latest_file_content(path)

    if html_content:
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning("⚠️ No dashboard files found.")
        st.error(f"Error: {filename}")

# [PAGE] Research
elif target_page == "研究專欄 Research":
    st.title("🦅 Research Paper from Paris")
    st.caption("Institutional Perspectives on Daily Flows")

    # 1. 讀取所有 MD 檔
    files = sorted(glob.glob(os.path.join("DailyInsights", "*.md")), reverse=True)

    if not files:
        st.info("No insights published yet. Stay tuned.")
    else:
        # 2. 顯示邏輯 (Timeline 樣式)
        # 【修改點】：加入 enumerate 以獲取 index (i)
        for i, file_path in enumerate(files):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split('\n')
            title = lines[0].replace('# ', '')

            date_display = "Recent"
            body_start_index = 1
            for idx, line in enumerate(lines):
                if "**Date:**" in line:
                    date_display = line.replace("**Date:**", "").strip()
                    body_start_index = idx + 1
                    break

            body = "\n".join(lines[body_start_index:])

            with st.container():
                col_date, col_text = st.columns([1, 5])

                with col_date:
                    st.markdown(f"""
                    <div style="background: rgba(37, 99, 235, 0.2); padding: 5px; border-radius: 5px; text-align: center; border: 1px solid #3b82f6;">
                        <span style="font-size: 0.8em; color: #93c5fd; font-weight: bold;">{date_display}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with col_text:
                    # 【修改點】：只展開第一個 (i == 0)
                    is_expanded = (i == 0)
                    with st.expander(f"📄 {title}", expanded=is_expanded):
                        st.markdown(body)
                        st.markdown("---")

# [PAGE] Options Strategy Dashboard
elif target_page == "期權策略 Strategy":
    st.title("🛠️ Interactive Option Strategy Builder")
    st.caption("Analyze payoff diagrams for Calls, Puts, Spreads, and Straddles instantly.")

    # --- 用戶輸入區 ---
    with st.container():
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            ticker_input = st.text_input("Enter US Ticker", value="NVDA", help="e.g., TSLA, AAPL, NVDA").upper()
        with c2:
            spread_width = st.number_input("Spread Width ($)", value=5, min_value=1, max_value=50)
        with c3:
            otm_call_pct = st.number_input("Call OTM %", value=1.03, step=0.01, format="%.2f", help="1.10 = 10% OTM")
        with c4:
            itm_put_pct = st.number_input("Put ITM %", value=0.97, step=0.01, format="%.2f", help="0.90 = 10% OTM")

        run_btn = st.button("🚀 Generate Strategy Dashboard", type="primary", use_container_width=True)

    # --- 執行邏輯 ---
    if run_btn and ticker_input:
        with st.status(f"Processing {ticker_input}...", expanded=True) as status:

            # Step 1: 檢查/下載 CSV
            status.write("📂 Checking local data cache...")
            try:
                # 這裡呼叫上面定義的 get_local_data
                df_hist, options_data, data_date = get_local_data(ticker_input)

                if df_hist is None:
                    status.update(label="Local Data Not Found", state="error")
                    st.error(f"Data not found in Option/Option. Please run data_updater.py first.")
                    st.stop()

                status.write(f"✅ Loaded history data ({len(df_hist)} days). Data Date: {data_date}")

                # Step 2: 獲取期權鏈並生成 HTML
                status.write("🔗 Calculating strategy payoffs...")
                html_result, msg = generate_strategy_html(ticker_input, spread_width, otm_call_pct, itm_put_pct)

                if html_result:
                    status.update(label="Dashboard Generated!", state="complete")

                    # 顯示 HTML (使用 components)
                    st.markdown("---")
                    components.html(html_result, height=1400, scrolling=True)
                else:
                    status.update(label="Generation Failed", state="error")
                    st.error(msg)

            except Exception as e:
                st.error(f"System Error: {e}")

# [PAGE] Market Risk
elif target_page == "風險指標 Market Risk":
    st.title("⚠️ Market Implied Risk")
    path = "ImpliedParameters"

    html_content, filename = get_latest_file_content(path)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        fix_style = """
        <style>
            body {
                display: block !important;
                height: auto !important;
                min-height: 100vh;
                padding-top: 50px;
                background-color: #020617 !important;
            }
            .card { margin: 0 auto !important; }
        </style>
        """
        html_content = html_content.replace("<head>", "<head>" + fix_style)
        components.html(html_content, height=2200, scrolling=True)
    else:
        st.warning("⚠️ No risk reports found.")
        st.info("Please ensure `ImpliedParameters/implied_params_*.html` exists.")

# [PAGE] Market Breadth
elif target_page == "市寬 Market Breadth":
    st.title("🌊 Market Breadth")
    path = os.path.join("MarketDashboard", "MarketBreadth")
    html_content, filename = get_latest_file_content(path, "market_breadth_*.html")

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=2200, scrolling=True)
    else:
        st.warning("⚠️ Market Breadth report not found.")
        st.info(f"Please ensure `{path}` contains `market_breadth_*.html` files.")

# [PAGE] Industry Sector Heatmap
elif target_page == "板塊熱力圖 Sector Heatmap":
    st.title("🔥 Industry Sector Heatmap")
    st.caption("Daily Return Heatmap (Last 20 Days)")
    path = "MarketDashboard"
    pattern = "sector_etf_heatmap_*.html"
    html_content, filename = get_latest_file_content(path, pattern)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("⚠️ Sector Heatmap not found.")
        st.info(f"Please ensure `{path}/{pattern}` exists.")

# [PAGE] Earnings
elif target_page == "業績公佈 Earnings":
    st.title("📅 Earnings Calendar Analysis")
    path = "Earnings"
    html_content, filename = get_latest_file_content(path)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning("⚠️ No earnings reports found.")
        st.info("Please ensure there is an `Earnings` folder in the root directory containing .html files.")

# [PAGE] Stock DNA
elif target_page == "因子模型 Stock DNA":
    st.title("🧬 Stock Factor DNA")
    html_content = load_stock_dna_with_injection()
    if html_content and "HTML not found" not in html_content:
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.error("FamaFrench/index.html not found")

# [PAGE] S&P 500 Heatmap
elif target_page == "標普熱力圖 S&P 500":
    st.title("🔥 S&P 500 Performance Heatmap (YTD)")
    st.caption("Top 50 Best Performers - Daily Returns Tracking")

    # Assumes the script saves the file into the 'Stock' folder.
    # If the script runs in the root, change this to path = "."
    path = "Stock"

    # Look for files matching the new timestamped pattern
    html_content, filename = get_latest_file_content(path, "sp500_clean_heatmap_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        # Height is adjustable depending on how many rows (50 rows needs ~1500px)
        components.html(html_content, height=1600, scrolling=True)
    else:
        st.warning("⚠️ No S&P 500 Heatmap found.")
        st.info(f"Please run `sp500_ytd_ranking.py` and ensure the output is saved in `{path}` folder.")

# [PAGE] Thematic Basket
elif target_page == "主題籃子 Thematic Basket":
    st.title("🧺 Thematic Basket Analysis")
    path = "ThematicBasket"
    html_content, filename = get_latest_file_content(path, "elite_dashboard_*.html")

    if html_content:
        st.caption(f"📅 Strategy Report: {filename}")
        components.html(html_content, height=6000, scrolling=True)
    else:
        st.warning("⚠️ No basket reports found.")
        st.info(f"Checking path: {os.path.abspath(path)}")

# [PAGE] ETF Smart Money
elif target_page == "ETF資金流 Smart Money":
    st.title("🚀 ETF Smart Money Tracker")
    st.caption("Tracking Leveraged ETF Relative Volume Spikes")
    path = "xETF"
    html_content, filename = get_latest_file_content(path, "ETF_Smart_Money_Report_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No ETF Smart Money reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `ETF_Smart_Money_Report_*.html` files.")

# [PAGE] Insider Trading
elif target_page == "內部交易 Insider":
    st.title("🕴️ Insider Trading Activity")
    st.caption("Daily Cluster Buys & Significant Insider Transactions")
    path = "Insider"
    html_content, filename = get_latest_file_content(path, "Insider_Trading_Report_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Insider Trading reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `Insider_Trading_Report_*.html` files.")

# [PAGE] Short Squeeze
elif target_page == "挾淡倉 Short Squeeze":
    st.title("⚡ Short Squeeze Scanner")
    st.caption("Retail Hype & High Short Interest Candidates")
    path = "Short_squeeze"
    html_content, filename = get_latest_file_content(path, "Short_squeeze_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Short Squeeze reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `Short_squeeze_*.html` files.")

# [PAGE] Reddit Sentiment
elif target_page == "Reddit Sentiment":
    path = "Rddt"
    html_content, filename = get_latest_file_content(path, "reddit_scanner_*.html")

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Reddit reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `reddit_scanner_*.html` files.")

# [PAGE] Volatility Target
elif target_page == "波動率策略 Volatility Target":
    st.title("📉 Volatility Target Strategy")
    path = "VolTarget"
    html_content, filename = get_latest_file_content(path, "vol_tool_*.html")

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=1500, scrolling=True)
    else:
        st.warning("⚠️ Volatility Tool not found.")
        st.info("Please ensure `vol_tool_*.html` exists in the `VolTarget` folder.")

# [PAGE] US Option
elif target_page == "美股期權 US Option":
    st.title("US Option Strike Analysis")
    st.caption("Tracking Unusual Options Activity & Gamma Levels")
    path = "Option"
    search_pattern = "option_strike_*.html"
    html_content, filename = get_latest_file_content(path, search_pattern)

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No US Option reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `{search_pattern}` files.")

# [PAGE] HK Option
elif target_page == "港股期權 HK Option":
    st.title("HK Option Market Analysis")
    st.caption("Market Scanner, Stock Ranking & Heatmaps")
    path = "Option"
    search_pattern = "HK_Option_Market_*.html"
    html_content, filename = get_latest_file_content(path, search_pattern)

    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No HK Option reports found.")
        st.info(f"Please ensure `{path}` folder exists and contains `{search_pattern}` files.")

# [PAGE] Volume Profile
elif target_page == "成交分佈 Volume Profile":
    st.title("📊 Volume Profile Analysis")
    path = "VP"
    html_content, filename = get_latest_file_content(path)

    if html_content:
        st.caption(f"Displaying Report: {filename}")
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.warning("⚠️ 尚未部署 Volume Profile 模組 (VP 資料夾為空)")

# [PAGE] Future -> Intraday Volatility
elif target_page == "日內波幅 Volatility":
    st.title("⚡ Intraday Volatility Analysis")
    html_path = os.path.join("MarketDashboard", "Intraday_Volatility.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("⚠️ 找不到 Intraday Volatility 報告")
        st.info(f"請確認檔案 `{html_path}` 是否存在。")

# [PAGE] Future -> HSI CBBC Ladder
elif target_page == "牛熊重貨區 CBBC Ladder":
    st.title("🐻 HSI CBBC Heavy Zone (牛熊重貨區)")
    html_path = os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("⚠️ 尚未生成牛熊證分佈報告")
        st.info(f"請確認檔案 `{html_path}` 是否存在。")

# [PAGE] My Portfolio
elif target_page == "實戰持倉 Portfolio":
    st.title("💼 Paris Picks")
    path = "Trade"

    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])

    # 檢查是否已登入 (檢查 Session State)
    is_vip = st.session_state.get("authentication_status", False)

    # --- Tab 1: Stock Journal (部分公開) ---
    with tab1:
        html_content, filename = get_latest_file_content(path, "trade_record_*.html")

        if html_content:
            st.caption(f"📅 Stock Report: {filename}")

            if is_vip:
                # [VIP 模式]：顯示完整高度 + 允許捲動
                components.html(html_content, height=1200, scrolling=True)
            else:
                # [免費模式]：顯示上半部預覽 (高度設小 + 禁止捲動)
                st.info("👀 Preview Mode: Showing top positions only.")
                # height=400 且 scrolling=False 確保只能看到頂部
                components.html(html_content, height=600, scrolling=False)

                # 顯示鎖定遮罩與登入按鈕
                st.markdown("---")
                # 這裡調用你的鎖定函數，若未登入會顯示 Login Form
                check_access_or_show_teaser(
                    "Stock Journal Full Access",
                    description="🔒 Sign in to unlock the full trade journal, entry/exit prices, and historical performance."
                )
        else:
            st.warning("⚠️ Trade Record HTML not found.")
            st.info("Please verify that the GitHub Action has run successfully.")

    # --- Tab 2: Option Desk (維持完全鎖定或根據你的需求調整) ---
    with tab2:
        # 如果你希望 Option Desk 也是同樣邏輯，可以複製上面的做法
        # 這裡示範保持原本的全鎖定邏輯 (如果未登入，直接擋住)

        if not is_vip:
            check_access_or_show_teaser(
                "Option Desk",
                description="🔒 VIP Access Only. Real-time option flow analysis and positions."
            )
        else:
            # VIP 才能看到這部分
            html_content_opt, filename_opt = get_latest_file_content(path, "option_record_*.html")
            if html_content_opt:
                st.caption(f"📅 Option Report: {filename_opt}")
                components.html(html_content_opt, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Option Record HTML not found.")
                st.info("Please verify `option_record_*.html` exists in `Trade` folder.")

# [PAGE] MT5 EA - Introduction
elif target_page == "EA 介紹 Introduction":
    st.title("🤖 MT5 Expert Advisor")
    html_path = os.path.join("MT5EA", "ea_marketing.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=3000, scrolling=True)
    else:
        st.warning("⚠️ No marketing content found.")
        st.info("Please ensure `MT5EA/ea_marketing.html` exists.")


# [PAGE] LEGAL
elif target_page == "Legal":
    st.title("📜 Legal & Compliance")
    tab1, tab2, tab3 = st.tabs(["Disclaimer", "Privacy Policy", "Terms of Use"])
    with tab1:
        html = load_html_file(os.path.join("Legal", "disclaimer.html"))
        st.html(html)
    with tab2:
        html = load_html_file(os.path.join("Legal", "privacy.html"))
        st.html(html)
    with tab3:
        html = load_html_file(os.path.join("Legal", "terms.html"))
        st.html(html)

# [PAGE] Resources
elif target_page == "工具資源 Resources":
    st.title("🔗 Trading Resources")
    html_path = os.path.join("Resources", "external_links.html")
    html_content = load_html_file(html_path)
    if html_content and "File not found" not in html_content:
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.warning("⚠️ Resources file not found.")
        st.info(f"Please ensure `{html_path}` exists.")

elif target_page == "交易社群 Community":
    # 不顯示 Streamlit 預設標題，因為 HTML 裡已經有了

    html_file_path = os.path.join("Community", "community_promo.html")

    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # 使用 components.html 渲染，height 設定高一點以容納整個頁面
            # scrolling=True 讓用戶可以捲動
            components.html(html_content, height=1200, scrolling=True)
    else:
        st.error(f"⚠️ Community page file not found at: {html_file_path}")

# [PAGE] Education Hub
elif target_page == "交易學院 Education":
    st.title("🎓 Quant Academy")
    st.caption("Institutional Trading Knowledge & Strategies")

    # 1. 定義文章清單 (重新排序：EA(免費) -> 心法 -> 基礎 -> 系統 -> 期權 -> 量化)
    articles = {
        # --- 第一階段：MT5 自動化交易 (Free / Lead Magnet) ---
        "mt5_ea_install": {
            "title": "第01課 | [EA] 如何將 EA 安裝到 MT5",
            "file": "34_mt5_ea_installation.md",
            "icon": "📂",
            "desc": "新手必看！手把手教你將 .ex5 / .mq5 檔案正確放入 MT5 資料夾並啟動自動交易。"
        },
        "ea_manual": {
            "title": "第02課 | [EA] Paris摩打手 Assistant",
            "file": "4_mt5_ea_manual.md",
            "icon": "🤖",
            "desc": "告別手動算點數，隱形止損與一鍵反手神器。"
        },
        "fate_indicator": {
            "title": "第03課 | [EA] Fate 趨勢判定反轉系統",
            "file": "6_paris_fate_indicator_guide.md",
            "icon": "🧭",
            "desc": "整合波動率與動能的機構級圖表系統，自動繪製 TP/SL。"
        },
        "gold_excalibur": {
            "title": "第04課 | [EA] 黃金自動現金流馬丁策略",
            "file": "5_paris_gold_excalibur.md",
            "icon": "⚔️",
            "desc": "結合 Fate 趨勢引擎與 ATR 動態網格的機構級黃金策略。"
        },

        # --- 第二階段：交易員心法與認知 (Mindset - VIP) ---
        "trading_career_reality": {
            "title": "第05課 | [心法] 面對家人與孤獨的修煉 ",
            "file": "36_trading_career_reality.md",
            "icon": "🧗",
            "desc": "交易賺錢不過是思考和紀律的副產品。如何獲得家人的理解？交易員必須掌握的 8 大技能樹。"
        },
        "metal_lesson": {
            "title": "第06課 | [心法] 別讓情緒毀了你的交易 ",
            "file": "10_Mastering Trading Psychology.md",
            "icon": "🧠",
            "desc": "跳出情緒陷阱，用我的獨家心法和策略，讓你們交易更穩、更賺！"
        },
        "trading_psychology_focus": {
            "title": "第07課 | [心法] 千萬不要在玩牌的時候數錢 ",
            "file": "35_trading_psychology_no_peeking.md",
            "icon": "🃏",
            "desc": "為什麼越勤勞越輸錢？學會「設好離手」(Set & Forget)，利用 45 分鐘專注法則提高執行力。"
        },
        "four_hearts_discipline": {
            "title": "第08課 | [心法] 四心修煉與概率遊戲 ",
            "file": "37_four_hearts_discipline.md",
            "icon": "❤️",
            "desc": "耐心、細心、決心、狠心。為什麼高勝算入場前必須有止損？短線操作出錯的三大處理原則。"
        },
        "kung_fu_trading": {
            "title": "第09課 | [心法] 功夫兩個字，一橫一直 ",
            "file": "38_kung_fu_trading.md",
            "icon": "🥋",
            "desc": "為什麼交易系統只有兩個重點：入場信號與出場風控？贏家與輸家的區別。"
        },
        "day_trading_edge": {
            "title": "第10課 | [心法] 為什麼選擇日內交易 (Day Trade)？ ",
            "file": "39_day_trading_philosophy.md",
            "icon": "⚡",
            "desc": "為什麼大戶做不到 Day Trade 而散戶可以？這是你的 Edge。升跌不理，市場郁就得。"
        },

        # --- 第三階段：工欲善其事 (Setup & Risk - VIP) ---
        "tv_setup": {
            "title": "第11課 | [工具] TradingView 新手速成 Setup 🔒",
            "file": "11_TradingView Setup Guide.md",
            "icon": "⚙️",
            "desc": "從零開始 Setup，由買數據到安指標，快速搭建你的「四圖流」賺錢戰壇！"
        },
        "ib_hotkeys": {
            "title": "第12課 | [工具] IB TWS 快捷鍵 (Hotkeys) 設定 🔒",
            "file": "28_ib_hotkeys_setup.md",
            "icon": "⌨️",
            "desc": "炒極限期權必備！設定一鍵下單 (Buy/Sell)，告別手動輸入的延遲。"
        },
        "risk_sizing": {
            "title": "第13課 | [風控] 何為波動性「均注」？ ",
            "file": "8_volatility_sizing.md",
            "icon": "⚖️",
            "desc": "贏單常有卻輸在資金管理？學會 ATR 動態注碼，像機構一樣控盤。"
        },
        "risk_calculator": {
            "title": "第14課 | [風控] 動態手數風險計算機 (Excel) 🔒",
            "file": "14_dynamic_lot_size_guide.md",
            "icon": "🧮",
            "desc": "工具下載：根據淨值自動計算安全手數，一鍵看清 XAU 與 NAS100 的合約風險差異。"
        },
        "sharpe_ratio": {
            "title": "第15課 | [風控] 夏普比率 (Sharpe Ratio) ",
            "file": "41_sharpe_ratio_explained.md",
            "icon": "📊",
            "desc": "如何用數學分辨「運氣」與「實力」？拆解衡量策略效率的核心指標。"
        },

        # --- 第四階段：ParisTrader 核心系統 (System - VIP) ---
        "paris_manual": {
            "title": "第16課 | [系統] ParisTrader 獨家操作手冊 🔒",
            "file": "15_paris_system_manual.md",
            "icon": "📘",
            "desc": "完整收錄四圖流架構、ST/VV 核心指標詳解、進出場機制與實戰心法。"
        },
        "vp_tutorial": {
            "title": "第17課 | [指標] Volume Profile (VP) 日內實戰 🔒",
            "file": "13_Volume Profile Tutorial.md",
            "icon": "📊",
            "desc": "不看指標只看量？用 Fixed Range VP 找出機構成本區，捕捉開盤前 5 分鐘機會。"
        },
        "volume_v2": {
            "title": "第18課 | [指標] Volume v2 進階成交量分析 🔒",
            "file": "17_volume_indicator_v2.md",
            "icon": "📶",
            "desc": "獨家分解買賣量，結合 Supertrend 動態均線，自動標記 CC/PP 爆量信號。"
        },
        "vv_tutorial": {
            "title": "第19課 | [指標] VV 指標實戰：結合 ST 判斷趨勢 🔒",
            "file": "12_VV Indicator Tutorial.md",
            "icon": "📈",
            "desc": "學會觀察 VV 與 ST 的黃金交叉，利用多時框共振心法，精準捕捉進出場時機。"
        },
        "bull_diamond_strategy": {
            "title": "第20課 | [戰法] 交易前三問與鑽石指標 🔒",
            "file": "40_bull_diamond_strategy.md",
            "icon": "💎",
            "desc": "什麼是晨鑽/首鑽？如何避免 Reprinting？左側 vs 右側交易詳解。"
        },
        "st_table": {
            "title": "第21課 | [神器] ST Table 多時框趨勢監控 🔒",
            "file": "16_st_table_guide.md",
            "icon": "🗓️",
            "desc": "一眼看清 1m 至 4h 的趨勢方向！自定義 ST 值矩陣，專為期貨短線設計。"
        },
        "trend_table": {
            "title": "第22課 | [神器] Trend Table 全市場趨勢雷達 🔒",
            "file": "20_trend_table_guide.md",
            "icon": "🧭",
            "desc": "整合 EMA, VV, ST 三大系統。全綠/全紅代表最強共識！"
        },
        "trendtable_alert": {
            "title": "第23課 | [神器] TrendTable 自動 Alert 設定 🔒",
            "file": "33_trendtable_alert_setup.md",
            "icon": "🔔",
            "desc": "不想肉眼盯盤？教你如何在 TV 設定「全綠/全紅」的手機彈窗提示。"
        },
        "rsi_table": {
            "title": "第24課 | [神器] 14天 RSI 當炒表 (每日強勢股) 🔒",
            "file": "19_rsi_hot_table.md",
            "icon": "🔥",
            "desc": "每日掃描最強勢資產！一眼找出這幾天最易賺錢的標的 (Daily Chart 專用)。"
        },
        "tv_heatmap": {
            "title": "第25課 | [神器] 期貨動能熱力圖 (Heatmap) 🔒",
            "file": "7_tv_volume_heatmap.md",
            "icon": "🗺️",
            "desc": "一眼看穿大戶資金流向，監控全球 18 大資產 Z-Score。"
        },

        # --- 第五階段：期貨與衍生品基礎 (Futures - VIP) ---
        "cfd_basis": {
            "title": "第26課 | [期貨] Future vs CFD 差價計算機 🔒",
            "file": "18_cfd_basis_calculator.md",
            "icon": "💱",
            "desc": "解決看期貨做 CFD 的點差難題，一鍵換算對應點位。"
        },
        "basis_theory": {
            "title": "第27課 | [期貨] Basis (水位) 理論與手動換算 🔒",
            "file": "29_basis_theory_manual.md",
            "icon": "🌊",
            "desc": "為什麼牛牛的報價跟 CFD 不一樣？深入理解基差變動原理。"
        },
        "cbbc_street_map": {
            "title": "第28課 | [牛熊] 牛熊街貨圖與投行對沖 ",
            "file": "31_cbbc_street_map.md",
            "icon": "🎯",
            "desc": "為什麼「打靶」後市況會反轉？從投行 Delta Hedging 角度找大位 TP。"
        },

        # --- 第六階段：期權大師班 (Options - VIP) ---
        "option_pricing_101": {
            "title": "第29課 | [期權] Option Pricing 定價原理 🔒",
            "file": "21_option_pricing_101.md",
            "icon": "🎓",
            "desc": "投資班第一堂：拆解 BS Model，什麼是 IV？美式與歐式有何分別？"
        },
        "bs_model_excel": {
            "title": "第30課 | [期權] BS Model 定價計算機 (Excel) 🔒",
            "file": "27_bs_model_excel.md",
            "icon": "🧮",
            "desc": "輸入股價、行權價與 IV，一鍵計算期權理論價格與 Greeks，驗證報價是否合理。"
        },
        "bull_call": {
            "title": "第31課 | [期權] Bull Call Spread 實戰詳解 ",
            "file": "2_bull_call_spread.md",
            "icon": "🐂",
            "desc": "看對市卻輸錢？學會這個對沖策略，降低成本抗 Theta。"
        },
        "naked_long": {
            "title": "第32課 | [期權] Naked Long 的時間博弈 ",
            "file": "3_naked_long_strategy.md",
            "icon": "⏳",
            "desc": "為什麼橫盤不要買 Weekly？Python 數據回測告訴你真相。"
        },
        "option_t0_strategy": {
            "title": "第33課 | [期權] T0 實戰 - 風險回報最大化 🔒",
            "file": "22_option_t0_strategy.md",
            "icon": "🚀",
            "desc": "利用期權非線性特性，在單日內實現極致風險回報比的實戰技術。"
        },
        "itm_vs_otm": {
            "title": "第34課 | [期權] ITM vs OTM Put (Greeks解析) 🔒",
            "file": "23_itm_vs_otm_puts.md",
            "icon": "📐",
            "desc": "深度解析 Delta, Gamma, Theta 差異，與 QQQ 末日輪實戰心法。"
        },
        "iv_expected_move": {
            "title": "第35課 | [期權] IV 隱含波動率與預期波幅 🔒",
            "file": "45_iv_expected_move.md",
            "icon": "⚡",
            "desc": "公式詳解：如何用 IV 計算股票每日預期升跌幅，找出操盤手食糊位。"
        },
        "vol_crush": {
            "title": "第36課 | [期權] Vol Crush (波動率暴跌) 詳解 ",
            "file": "24_vol_crush_explained.md",
            "icon": "📉",
            "desc": "詳解財報後 IV Crush 現象與 Apple 實戰案例。"
        },
        "oi_settlement": {
            "title": "第37課 | [期權] OI 未平倉合約與 Max Pain 🔒",
            "file": "25_oi_settlement_logic.md",
            "icon": "📍",
            "desc": "為什麼結算日價格總是在某個範圍？看穿莊家最大痛點 (Max Pain)。"
        },
        "dividend_marking": {
            "title": "第38課 | [期權] 股息標記 (Dividend Marking) 🔒",
            "file": "26_dividend_marking.md",
            "icon": "🔖",
            "desc": "了解除息日如何影響遠期曲線 (Forward Curve) 與期權價值。"
        },

        # --- 第七階段：機構級量化 (Quant - VIP) ---
        "risk_monitor_guide": {
            "title": "第39課 | [量化] 大市雷達：識別見頂/見底 ",
            "file": "9_risk_dashboard_guide.md",
            "icon": "📟",
            "desc": "學會解讀 VIX, Skew 與 Z-Score，像機構一樣捕捉轉折點。"
        },
        "stock_dna": {
            "title": "第40課 | [量化] Stock DNA 因子分析儀 ",
            "file": "1_stock_dna_guide.md",
            "icon": "🧬",
            "desc": "如何使用 Fama-French 模型工具拆解持倉風險與屬性。"
        },
        "cftc_cot_report": {
            "title": "第41課 | [量化] CFTC COT 倉位報告解讀 🔒",
            "file": "42_cftc_cot_report.md",
            "icon": "🐋",
            "desc": "教你解讀 Commercials vs Speculators，看清大資金流向。"
        },
        "dispersion_trading": {
            "title": "第42課 | [量化] Dispersion Trading (分散度交易) 🔒",
            "file": "43_dispersion_trading.md",
            "icon": "⚖️",
            "desc": "投行波動率套利策略。利用期權定價錯位，無需預測方向也能獲利。"
        },
        "bergomi_model": {
            "title": "第43課 | [量化] Bergomi 模型與粗糙波動率 🔒",
            "file": "44_bergomi_model.md",
            "icon": "♾️",
            "desc": "高階數學：描述波動率動態與曲面微笑的模型。"
        },
        "totem_valuation": {
            "title": "第44課 | [量化] 投行揭秘：大戶的答案紙 Totem 🔒",
            "file": "30_totem_valuation.md",
            "icon": "🤫",
            "desc": "揭開投行如何利用 Totem 進行 OTC 衍生品估值與風控的內幕。"
        },
    }

    # 準備選單需要的標題列表和圖標列表
    options_titles = [data["title"] for data in articles.values()]
    options_icons = [data["icon"] for data in articles.values()]

    # 2. 建立兩欄佈局：左邊是文章列表，右邊是內容閱讀區
    col_list, col_content = st.columns([1, 2.5], gap="large")

    with col_list:
        st.markdown("### 📚 Article List")

        # 使用 option_menu 顯示文章列表
        selected_title = option_menu(
            menu_title=None,
            options=options_titles,  # 顯示中文標題
            icons=options_icons,  # 顯示對應圖標
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"background-color": "rgba(255,255,255,0.05)", "padding": "10px"},
                "nav-link": {"font-size": "14px", "margin": "5px", "text-align": "left"},
                "nav-link-selected": {"background-color": "#2563EB"},
                "icon": {"font-size": "18px"}
            }
        )

    with col_content:
        # 根據選中的 Title 找回對應的 Article 資料
        current_article = next((item for item in articles.values() if item["title"] == selected_title), None)

        if current_article:
            # === [權限檢查邏輯] ===
            # 如果標題包含 "🔒" 且用戶未登入 -> 顯示付費牆
            if "🔒" in current_article["title"]:
                # 使用你的全局 check_access_or_show_teaser 函數
                # 注意：這裡我們傳遞文章標題作為 page_name
                if not check_access_or_show_teaser(current_article['title'],
                                                   description=f"🔒 此教學為 VIP 專屬內容：{current_article['desc']}"):
                    # 如果返回 False，代表未登入，這裡直接停止渲染後續內容，讓 teaser 佔據右側
                    st.stop()

            # === [內容渲染] (免費或已解鎖) ===
            file_path = os.path.join("Education", current_article["file"])

            # 顯示標題頭
            st.markdown(f"""
            <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #2563EB; margin-bottom: 20px;">
                <h2 style="margin:0; color: white;">{current_article['icon']} {current_article['title'].replace(' 🔒', '')}</h2>
                <p style="margin-top:5px; color: #94a3b8;">{current_article['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

            # 使用 Base64 Loader 讀取內容
            content = load_markdown_with_images(file_path)
            st.markdown(content, unsafe_allow_html=True)

            # CTA (僅在免費文章底部顯示升級提示)
            if "🔒" not in current_article["title"]:
                st.divider()
                st.info("💡 喜歡這些自動化工具？ 升級 VIP 會員，解鎖後續 40+ 堂高階心法與策略教學。")
        else:
            st.error("Error loading article.")

# [PAGE] Membership (Sales Page)
elif target_page == "升級會員 VIP":
    # 標題仍保留在 Streamlit，方便 SEO 和結構，內容則用 HTML 渲染
    st.title("💎 升級機構級數據 Upgrade to Institutional Level")
    st.caption("停止猜測。像專業人士一樣，利用數據進行交易。")
    st.caption("Stop guessing. Start trading with data used by professionals.")

    # 定義 HTML 檔案路徑
    html_file_path = os.path.join("Community", "membership_pricing.html")

    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # 設定 height=1000 或更高，以確保卡片能完整顯示不需捲動
            components.html(html_content, height=1100, scrolling=True)
    else:
        st.error(f"⚠️ Membership page file not found at: {html_file_path}")
# ==========================================
# 5. Global Footer
# ==========================================
# [UPDATED] Added Legal link in footer
st.markdown("""
<div class="custom-footer">
    <p>
        © 2026 Paris Trader. All rights reserved.<br>
        <span style="font-size: 0.75rem; color: #6B7280;">
        Not financial advice · For informational and educational purposes only · I am not a licensed financial advisor in Hong Kong or any jurisdiction · Investments carry risk of total loss · Paris Trader accepts no liability.
        </span>
    </p>
    <p>
        <a href="https://t.me/algoparistrader" target="_blank">@ParisTrader on TG</a> | 
        <a href="?page=Legal" target="_self" style="color: #6B7280; text-decoration: none;">Legal & Compliance</a>
    </p>
</div>
""", unsafe_allow_html=True)
