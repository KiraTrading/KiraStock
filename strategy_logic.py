import os
import glob
import json
import base64
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set Matplotlib style for consistency
plt.style.use('dark_background')

# ==========================================
# Strategy Helper Functions
# ==========================================

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
    """
    # [PATH] Points to Option/Option folder
    folder_path = os.path.join("Option", "Option")
    ticker = ticker.upper()

    # --- 1. Search for Stock CSV ---
    csv_files = glob.glob(os.path.join(folder_path, f"{ticker}_*.csv"))
    valid_csvs = [f for f in csv_files if os.path.basename(f).upper().startswith(f"{ticker}_")]

    if not valid_csvs:
        abs_path = os.path.abspath(folder_path)
        return None, None, f"Stock data not found in {abs_path}. Please run data_updater.py."

    latest_csv = max(valid_csvs, key=os.path.getctime)
    try:
        df_hist = pd.read_csv(latest_csv, index_col=0, parse_dates=True)
    except Exception as e:
        return None, None, f"Error reading CSV: {e}"

    # --- 2. Search for Options JSON ---
    json_files = glob.glob(os.path.join(folder_path, f"{ticker}_options_*.json"))
    prefix_check = f"{ticker}_options_".upper()
    valid_jsons = [f for f in json_files if os.path.basename(f).upper().startswith(prefix_check)]

    if not valid_jsons:
        return df_hist, None, f"Option JSON not found for {ticker} (Checked prefix: {prefix_check})"

    latest_json = max(valid_jsons, key=os.path.getctime)
    try:
        with open(latest_json, 'r') as f:
            options_data = json.load(f)
    except Exception as e:
        return df_hist, None, f"Error reading JSON: {e}"

    try:
        data_date = latest_json.rsplit('_', 1)[1].replace('.json', '')
    except:
        data_date = "Unknown"

    return df_hist, options_data, data_date


def generate_strategy_html(ticker, spread_width, otm_pct, itm_pct):
    """
    Main logic to generate the strategy dashboard HTML.
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

        # 1. Naked Call (nc)
        nc_row = get_option(calls, current_price * otm_pct)
        if nc_row is not None:
            cost = nc_row['lastPrice']
            payoff = [max(0, p - nc_row['strike']) - cost for p in plot_range]

            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc')
            ax.spines['top'].set_color('none')
            ax.spines['left'].set_color('#ccc')
            ax.spines['right'].set_color('none')
            ax.tick_params(axis='x', colors='#ccc')
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
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc')
            ax.spines['top'].set_color('none')
            ax.spines['left'].set_color('#ccc')
            ax.spines['right'].set_color('none')
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#27ae60', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1)
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
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc')
            ax.spines['top'].set_color('none')
            ax.spines['left'].set_color('#ccc')
            ax.spines['right'].set_color('none')
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#e74c3c', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1)
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
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc')
            ax.spines['top'].set_color('none')
            ax.spines['left'].set_color('#ccc')
            ax.spines['right'].set_color('none')
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#c0392b', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1)
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
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.spines['bottom'].set_color('#ccc')
            ax.spines['top'].set_color('none')
            ax.spines['left'].set_color('#ccc')
            ax.spines['right'].set_color('none')
            ax.tick_params(colors='#ccc')

            ax.plot(plot_range, payoff, color='#9b59b6', linewidth=2)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) > 0), color='green', alpha=0.1)
            ax.fill_between(plot_range, payoff, 0, where=(np.array(payoff) < 0), color='red', alpha=0.1)
            ax.axhline(0, color='#888', lw=1)
            ax.axvline(current_price, color='#aaa', linestyle=':')

            date_data["st_setup"] = f"Buy Call + Put (${strike})"
            date_data["st_cost"] = fmt_money(cost)
            date_data["st_loss"] = fmt_money(cost)
            date_data["st_gain"] = "Unlimited"
            date_data["st_break"] = f"${(strike - cost):.2f} / ${(strike + cost):.2f}"
            date_data["st_img"] = get_base64_plot(fig)

        master_data[target_date] = date_data

    # --- HTML ASSEMBLY ---
    json_data = json.dumps(master_data)
    options_html = "".join([f'<option value="{d}">{d}</option>' for d in selected_dates])

    # Note: I'm keeping the long HTML string here as requested by "upto return html_content"
    # Ideally this HTML could also be in a template file, but this is fine for now.
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