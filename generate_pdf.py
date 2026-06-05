import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Ensure matplotlib uses Tahoma for Thai text if available
import matplotlib.font_manager as fm
from matplotlib import rcParams

# Custom modern colors for dark neon theme
COLORS = {
    'bg': '#0f172a',        # Deep navy/slate
    'grid': '#1e293b',      # Slate
    'text': '#f8fafc',      # Off-white
    'text_dim': '#94a3b8',  # Slate gray
    'cyan': '#06b6d4',      # Cyan
    'teal': '#0d9488',      # Teal
    'green': '#10b981',     # Emerald Green (Bullish)
    'red': '#f43f5e',       # Rose Red (Bearish)
    'yellow': '#eab308',    # Gold
    'purple': '#a855f7',    # Purple (VWAP)
    'orange': '#f97316',    # Orange
}

# Add Tahoma to matplotlib
try:
    tahoma_font = fm.FontProperties(fname='C:\\Windows\\Fonts\\tahoma.ttf')
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Tahoma', 'DejaVu Sans', 'Arial']
except Exception as e:
    print(f"Warning setting matplotlib font: {e}")

def draw_candles(ax, o, c, h, l, width=0.6):
    for i in range(len(o)):
        is_green = c[i] >= o[i]
        color = COLORS['green'] if is_green else COLORS['red']
        # Wick
        ax.plot([i, i], [l[i], h[i]], color=color, linewidth=1.5, zorder=2)
        # Body
        bottom = min(o[i], c[i])
        height = max(abs(o[i] - c[i]), 0.05)
        ax.bar(i, height, width, bottom=bottom, color=color, edgecolor=color, zorder=3)

def draw_volume_profile(ax, start_x, max_width, prices, volumes, color):
    max_v = max(volumes)
    level_h = (max(prices) - min(prices)) / len(prices)
    for p, v in zip(prices, volumes):
        w = (v / max_v) * max_width
        # Draw horizontal bars
        ax.barh(p, w, left=start_x, height=level_h*0.8, color=color, alpha=0.3, edgecolor=color, linewidth=0.5, zorder=1)

def draw_arrow(ax, from_x, from_y, to_x, to_y, color, head_width=0.2, head_length=15):
    ax.annotate('', xy=(to_x, to_y), xytext=(from_x, from_y),
                arrowprops=dict(arrowstyle="->", color=color, lw=2, mutation_scale=15), zorder=4)

def draw_label(ax, text, x, y, bg_color, text_color, fontsize=10, ha='left'):
    ax.text(x, y, text, color=text_color, fontname='Tahoma', fontsize=fontsize, fontweight='bold',
            bbox=dict(facecolor=bg_color, edgecolor='none', boxstyle='round,pad=0.3'),
            ha=ha, va='center', zorder=5)

# --- CHART GENERATION FUNCTIONS ---

def generate_logo():
    fig, ax = plt.subplots(figsize=(7, 2), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    
    # Stylized logo trendline
    ax.plot([0.5, 1.0, 1.5, 2.0, 2.5], [0.8, 1.8, 1.2, 2.5, 2.8], color=COLORS['teal'], linewidth=4, zorder=1)
    ax.scatter([2.5], [2.8], color=COLORS['cyan'], s=150, zorder=2, edgecolors=COLORS['text'], linewidths=1.5)
    
    # Text
    ax.text(3.0, 1.6, 'MIN', fontname='Tahoma', fontsize=44, fontweight='bold', color=COLORS['cyan'], va='center')
    ax.text(3.0, 0.7, 'pitpibool', fontname='Tahoma', fontsize=24, color=COLORS['text'], va='center')
    
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 3.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('temp_logo.png', dpi=300, facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()

def generate_chart1():
    # Strategy 1: Post-Spike Reversal
    fig, (ax, ax_vol) = plt.subplots(2, 1, figsize=(8, 5.5), gridspec_kw={'height_ratios': [4, 1]}, facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax_vol.set_facecolor(COLORS['bg'])
    
    # Candle data: spike then drop
    o = [2.8, 3.0, 3.5, 4.2, 4.4, 4.0, 3.7, 3.4, 3.2, 3.05, 2.8, 2.8, 2.85, 2.95, 3.1]
    c = [3.0, 3.5, 4.2, 4.4, 4.0, 3.7, 3.4, 3.2, 3.05, 2.9, 2.8, 2.85, 2.95, 3.1, 3.2]
    h = [3.05, 3.55, 4.3, 4.5, 4.42, 4.05, 3.75, 3.45, 3.25, 3.1, 2.95, 2.9, 2.98, 3.12, 3.25]
    l = [2.75, 2.98, 3.45, 4.15, 3.95, 3.65, 3.35, 3.15, 3.0, 2.85, 2.75, 2.75, 2.82, 2.92, 3.08]
    
    v = [30, 45, 90, 85, 70, 55, 45, 40, 35, 30, 50, 40, 55, 60, 50]
    
    draw_candles(ax, o, c, h, l)
    
    # Volume bars
    for i in range(len(v)):
        color = COLORS['green'] if c[i] >= o[i] else COLORS['red']
        ax_vol.bar(i, v[i], width=0.6, color=color, alpha=0.7)
    
    # Volume profile on the right
    prices = np.linspace(2.7, 4.5, 12)
    volumes = [10, 25, 60, 85, 50, 40, 30, 25, 35, 45, 20, 10]
    draw_volume_profile(ax, len(o)-0.5, 3.5, prices, volumes, COLORS['cyan'])
    
    # VAH, POC, VAL lines
    ax.axhline(y=3.9, color=COLORS['green'], linestyle='--', linewidth=1.2)
    draw_label(ax, 'VAH แนวต้าน (3.90)', len(o) + 3.2, 3.9, '#10b98122', COLORS['green'], fontsize=8, ha='right')
    
    ax.axhline(y=3.3, color=COLORS['cyan'], linestyle='--', linewidth=1.2)
    draw_label(ax, 'POC เป้าหมาย (3.30)', len(o) + 3.2, 3.3, '#06b6d422', COLORS['cyan'], fontsize=8, ha='right')
    
    ax.axhline(y=2.8, color=COLORS['red'], linestyle='--', linewidth=1.2)
    draw_label(ax, 'VAL จุดเข้าซื้อ (2.80)', len(o) + 3.2, 2.8, '#f43f5e22', COLORS['red'], fontsize=8, ha='right')
    
    # Annotations (no emojis)
    draw_arrow(ax, 2, 4.8, 2, 4.3, COLORS['yellow'])
    draw_label(ax, 'หุ้น Spike ขึ้นสูง', 2, 4.9, '#eab30822', COLORS['yellow'], fontsize=9, ha='center')
    
    draw_label(ax, 'ราคาร่วงเยอะ', 6, 3.9, '#f43f5e11', COLORS['red'], fontsize=9, ha='center')
    
    # Entry and Exit target arrows
    draw_arrow(ax, 10.5, 2.4, 10.5, 2.75, COLORS['green'])
    draw_label(ax, 'จุดเข้าซื้อตรง VAL', 10.5, 2.2, '#10b98133', COLORS['green'], fontsize=10, ha='center')
    
    draw_arrow(ax, 12, 2.6, 13.5, 3.2, COLORS['cyan'])
    draw_label(ax, 'เป้าหมาย POC', 12, 2.4, '#06b6d433', COLORS['cyan'], fontsize=10, ha='center')
    
    # Styling
    ax.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax.set_xlim(-1, len(o) + 3.5)
    ax.set_ylim(2.5, 5.2)
    ax.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax.set_title('กลยุทธ์ที่ 1: Post-Spike Reversal (After Hours 18:00+)', color=COLORS['cyan'], fontname='Tahoma', fontsize=12, fontweight='bold', pad=15)
    
    # Vol axis styling
    ax_vol.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax_vol.set_xlim(-1, len(o) + 3.5)
    ax_vol.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax_vol.set_xlabel('แท่งเทียน 5 นาที (After Hours)', color=COLORS['text_dim'], fontname='Tahoma', fontsize=9)
    
    # Hide top axis spines
    for sp in ['top', 'right', 'left', 'bottom']:
        ax.spines[sp].set_color(COLORS['grid'])
        ax_vol.spines[sp].set_color(COLORS['grid'])
        
    plt.tight_layout()
    plt.savefig('temp_chart1.png', dpi=300, facecolor=COLORS['bg'])
    plt.close()

def generate_chart2():
    # Strategy 2: Below VWAP Recovery
    fig, (ax, ax_vol) = plt.subplots(2, 1, figsize=(8, 5.5), gridspec_kw={'height_ratios': [4, 1]}, facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax_vol.set_facecolor(COLORS['bg'])
    
    # Candle data: spike then fall below VWAP
    o = [2.0, 2.1, 2.4, 2.9, 3.2, 2.9, 2.6, 2.4, 2.25, 2.15, 2.2, 2.1, 2.05, 2.15, 2.08]
    c = [2.1, 2.4, 2.9, 3.2, 2.9, 2.6, 2.4, 2.25, 2.15, 2.2, 2.1, 2.05, 2.15, 2.08, 2.12]
    h = [2.15, 2.45, 2.95, 3.3, 3.25, 2.95, 2.65, 2.45, 2.3, 2.25, 2.25, 2.15, 2.18, 2.2, 2.16]
    l = [1.98, 2.08, 2.38, 2.85, 2.85, 2.55, 2.35, 2.2, 2.1, 2.1, 2.05, 2.0, 2.02, 2.05, 2.05]
    
    v = [25, 40, 80, 95, 75, 55, 45, 35, 30, 28, 25, 22, 30, 28, 26]
    
    draw_candles(ax, o, c, h, l)
    
    # VWAP line (purple curved)
    vwap = [2.05, 2.15, 2.4, 2.65, 2.75, 2.7, 2.6, 2.52, 2.48, 2.45, 2.42, 2.4, 2.38, 2.37, 2.36]
    ax.plot(vwap, color=COLORS['purple'], linewidth=2.5, label='VWAP', zorder=4)
    draw_label(ax, 'เส้น VWAP', 5, 2.75, '#a855f722', COLORS['purple'], fontsize=8)
    
    # Volume bars
    for i in range(len(v)):
        color = COLORS['green'] if c[i] >= o[i] else COLORS['red']
        ax_vol.bar(i, v[i], width=0.6, color=color, alpha=0.7)
        
    # Draw POC Line
    ax.axhline(y=2.5, color=COLORS['cyan'], linestyle='--', linewidth=1.2)
    draw_label(ax, 'POC After Hours (2.50)', len(o)-0.5, 2.5, '#06b6d422', COLORS['cyan'], fontsize=8, ha='right')
    
    # Current Price marker
    cur_idx = 14
    cur_p = c[cur_idx]
    ax.scatter([cur_idx], [cur_p], color=COLORS['yellow'], s=100, zorder=5, edgecolors=COLORS['text'])
    draw_label(ax, 'ราคาปัจจุบัน (ใต้ VWAP)', cur_idx - 1, cur_p + 0.15, '#eab30822', COLORS['yellow'], fontsize=9, ha='right')
    
    # Sell Wall in Order Book representation on the right
    ax.axhline(y=2.9, color=COLORS['orange'], linestyle=':', linewidth=1.5)
    draw_label(ax, 'Sell Wall หนาแน่นที่สุด (2.90)', len(o)-0.5, 2.9, '#f9731622', COLORS['orange'], fontsize=8, ha='right')
    
    # Distance arrow
    draw_arrow(ax, cur_idx, cur_p + 0.05, cur_idx, 2.85, COLORS['orange'])
    draw_label(ax, 'วัดระยะห่างแนวคนรอขาย', cur_idx - 4.5, (cur_p + 2.9)/2, '#f9731611', COLORS['orange'], fontsize=9)
    
    # Spike annotation
    draw_label(ax, 'เคย Spike มาก่อน', 3, 3.4, '#eab30822', COLORS['yellow'], fontsize=9, ha='center')
    
    # Styling
    ax.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax.set_xlim(-1, len(o) + 1)
    ax.set_ylim(1.8, 3.6)
    ax.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax.set_title('กลยุทธ์ที่ 2: หุ้น Spike แล้วราคาหล่นมาใต้ VWAP', color=COLORS['cyan'], fontname='Tahoma', fontsize=12, fontweight='bold', pad=15)
    
    ax_vol.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax_vol.set_xlim(-1, len(o) + 1)
    ax_vol.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax_vol.set_xlabel('แท่งเทียน 5 นาที', color=COLORS['text_dim'], fontname='Tahoma', fontsize=9)
    
    for sp in ['top', 'right', 'left', 'bottom']:
        ax.spines[sp].set_color(COLORS['grid'])
        ax_vol.spines[sp].set_color(COLORS['grid'])
        
    plt.tight_layout()
    plt.savefig('temp_chart2.png', dpi=300, facecolor=COLORS['bg'])
    plt.close()

def generate_chart3():
    # Strategy 3: Scalper Uptrend
    fig, (ax, ax_vol) = plt.subplots(2, 1, figsize=(8, 5.5), gridspec_kw={'height_ratios': [4, 1]}, facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax_vol.set_facecolor(COLORS['bg'])
    
    # Candle data: clear uptrend
    o = [1.5, 1.8, 2.2, 2.0, 1.95, 2.05, 2.15, 2.25, 2.2, 2.3, 2.4, 2.5, 2.45, 2.55, 2.65]
    c = [1.8, 2.2, 2.0, 1.95, 2.05, 2.15, 2.25, 2.2, 2.3, 2.4, 2.5, 2.45, 2.55, 2.65, 2.7]
    h = [1.85, 2.25, 2.22, 2.05, 2.1, 2.18, 2.28, 2.28, 2.33, 2.43, 2.53, 2.52, 2.58, 2.68, 2.75]
    l = [1.48, 1.78, 1.95, 1.9, 1.93, 2.03, 2.13, 2.18, 2.18, 2.28, 2.38, 2.42, 2.43, 2.53, 2.62]
    
    v = [50, 85, 60, 40, 55, 65, 70, 45, 60, 70, 75, 40, 65, 70, 60]
    
    draw_candles(ax, o, c, h, l)
    
    # VWAP line (purple curved, below candles)
    vwap = [1.55, 1.78, 1.9, 1.93, 1.98, 2.05, 2.12, 2.15, 2.19, 2.25, 2.32, 2.36, 2.4, 2.45, 2.5]
    ax.plot(vwap, color=COLORS['purple'], linewidth=2.5, label='VWAP', zorder=4)
    draw_label(ax, 'ราคายืนเหนือ VWAP ✓', 12, 2.35, '#a855f722', COLORS['purple'], fontsize=8)
    
    # Volume profile on right
    prices = np.linspace(1.8, 2.7, 10)
    volumes = [15, 30, 65, 90, 80, 50, 40, 30, 20, 10]
    draw_volume_profile(ax, len(o)-0.5, 3, prices, volumes, COLORS['cyan'])
    
    # VAH Line (Support)
    ax.axhline(y=2.15, color=COLORS['green'], linestyle='--', linewidth=1.5)
    draw_label(ax, 'VAH แนวรับสำคัญ ห้ามหลุด! (2.15)', len(o) + 2.5, 2.15, '#10b98122', COLORS['green'], fontsize=8, ha='right')
    
    # POC Line
    ax.axhline(y=2.35, color=COLORS['cyan'], linestyle='--', linewidth=1.2)
    draw_label(ax, 'POC (2.35)', len(o) + 2.5, 2.35, '#06b6d422', COLORS['cyan'], fontsize=8, ha='right')
    
    # Entry Point (above VAH, near POC)
    entry_idx = 10
    entry_p = c[entry_idx]
    draw_arrow(ax, entry_idx - 2, entry_p + 0.2, entry_idx, entry_p, COLORS['green'])
    draw_label(ax, 'เข้าเมื่อยืนเหนือ VAH และใกล้ POC', entry_idx - 5, entry_p + 0.25, '#10b98133', COLORS['green'], fontsize=9)
    
    # Stop-Loss
    ax.scatter([entry_idx], [2.15], color=COLORS['red'], marker='x', s=100, linewidths=2.5, zorder=5)
    draw_label(ax, 'STOP LOSS หากหลุด VAH', entry_idx - 5.5, 2.05, '#f43f5e22', COLORS['red'], fontsize=9)
    
    # Volume bars
    for i in range(len(v)):
        color = COLORS['green'] if c[i] >= o[i] else COLORS['red']
        ax_vol.bar(i, v[i], width=0.6, color=color, alpha=0.7)
        
    # Spike annotation
    draw_label(ax, 'เคย Spike สูงมาก่อน', 1.5, 2.35, '#eab30822', COLORS['yellow'], fontsize=9, ha='center')
    
    # Styling
    ax.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax.set_xlim(-1, len(o) + 3.0)
    ax.set_ylim(1.3, 3.0)
    ax.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax.set_title('กลยุทธ์ที่ 3: Scalper เทรดหุ้นเทรนด์ขาขึ้น (เหนือ VWAP)', color=COLORS['cyan'], fontname='Tahoma', fontsize=12, fontweight='bold', pad=15)
    
    ax_vol.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax_vol.set_xlim(-1, len(o) + 3.0)
    ax_vol.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax_vol.set_xlabel('แท่งเทียน 5 นาที', color=COLORS['text_dim'], fontname='Tahoma', fontsize=9)
    
    for sp in ['top', 'right', 'left', 'bottom']:
        ax.spines[sp].set_color(COLORS['grid'])
        ax_vol.spines[sp].set_color(COLORS['grid'])
        
    plt.tight_layout()
    plt.savefig('temp_chart3.png', dpi=300, facecolor=COLORS['bg'])
    plt.close()

def generate_chart4():
    # Strategy 4: HALT Play
    fig, (ax, ax_vol) = plt.subplots(2, 1, figsize=(8, 5.5), gridspec_kw={'height_ratios': [4, 1]}, facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax_vol.set_facecolor(COLORS['bg'])
    
    # Pre-halt candles (4 candles)
    o_pre = [3.0, 3.2, 3.5, 3.8]
    c_pre = [3.2, 3.5, 3.8, 4.2]
    h_pre = [3.25, 3.55, 3.85, 4.3]
    l_pre = [2.98, 3.18, 3.48, 3.75]
    v_pre = [40, 60, 75, 95]
    
    # Post-halt candles (7 candles)
    o_post = [4.4, 4.5, 4.45, 4.55, 4.5, 4.6, 4.7]
    c_post = [4.5, 4.45, 4.55, 4.5, 4.6, 4.7, 4.8]
    h_post = [4.6, 4.55, 4.58, 4.58, 4.65, 4.75, 4.85]
    l_post = [4.35, 4.4, 4.42, 4.48, 4.48, 4.58, 4.68]
    v_post = [90, 70, 65, 55, 60, 75, 80]
    
    # Combine with halt gap (index 4 and 5 represent the gap)
    o = o_pre + [np.nan, np.nan] + o_post
    c = c_pre + [np.nan, np.nan] + c_post
    h = h_pre + [np.nan, np.nan] + h_post
    l = l_pre + [np.nan, np.nan] + l_post
    
    # Draw pre-halt
    for i in range(len(o_pre)):
        draw_candles(ax, [o_pre[i]], [c_pre[i]], [h_pre[i]], [l_pre[i]])
        ax_vol.bar(i, v_pre[i], width=0.6, color=COLORS['green'], alpha=0.7)
        
    # Draw HALT zone
    ax.axvspan(4, 5, color='#ff91001c', zorder=1)
    ax.text(4.5, 3.5, '⏸ HALT\nหยุดซื้อขาย', color=COLORS['orange'], fontname='Tahoma', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)
    
    # Draw post-halt
    for i in range(len(o_post)):
        idx = i + 6
        draw_candles(ax, [o_post[i]], [c_post[i]], [h_post[i]], [l_post[i]])
        color = COLORS['green'] if c_post[i] >= o_post[i] else COLORS['red']
        ax_vol.bar(idx, v_post[i], width=0.6, color=color, alpha=0.7)
        
    # Pre-halt close line
    pre_close = c_pre[-1]
    ax.axhline(y=pre_close, color=COLORS['yellow'], linestyle=':', linewidth=1.5)
    draw_label(ax, 'ราคาปิดแท่งก่อน Halt (4.20)', len(o)-0.5, pre_close, '#eab30822', COLORS['yellow'], fontsize=8, ha='right')
    
    # Resumption check
    ax.text(8.5, 4.3, 'ราคาหลัง Halt ยืนเหนือแท่งปิดได้\n(รอสังเกตอาการ 5-10 นาที)', color=COLORS['green'], fontname='Tahoma', fontsize=8, ha='center', va='center',
            bbox=dict(facecolor='#10b9811c', edgecolor='none', boxstyle='round,pad=0.4'))
    
    # Volume Profile
    prices = np.linspace(4.2, 4.8, 6)
    volumes = [30, 85, 60, 40, 20, 10]
    draw_volume_profile(ax, 6.5, 2, prices, volumes, COLORS['cyan'])
    
    # Buy at POC
    pocPrice = 4.45
    ax.axhline(y=pocPrice, color=COLORS['cyan'], linestyle='--', linewidth=1.2)
    draw_label(ax, 'POC ของแท่ง Halt (4.45)', len(o)-0.5, pocPrice, '#06b6d422', COLORS['cyan'], fontsize=8, ha='right')
    
    draw_arrow(ax, 7.5, 4.0, 7.5, 4.4, COLORS['green'])
    draw_label(ax, 'ซื้อตอนราคาย่อตัวลงมาถึง POC', 7.5, 3.8, '#10b98133', COLORS['green'], fontsize=9, ha='center')
    
    # Warning Label
    draw_label(ax, 'ห้าม FOMO!', 4.5, 4.8, '#f43f5e33', COLORS['red'], fontsize=11, ha='center')
    
    # Styling
    ax.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax.set_xlim(-1, len(o) + 1)
    ax.set_ylim(2.6, 5.2)
    ax.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax.set_title('กลยุทธ์ที่ 4: เทรดหลัง HALT (ราคายืนได้ 5-10 นาที)', color=COLORS['cyan'], fontname='Tahoma', fontsize=12, fontweight='bold', pad=15)
    
    ax_vol.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.5)
    ax_vol.set_xlim(-1, len(o) + 1)
    ax_vol.tick_params(colors=COLORS['text_dim'], labelsize=9)
    ax_vol.set_xlabel('แท่งเทียน 5 นาที', color=COLORS['text_dim'], fontname='Tahoma', fontsize=9)
    
    for sp in ['top', 'right', 'left', 'bottom']:
        ax.spines[sp].set_color(COLORS['grid'])
        ax_vol.spines[sp].set_color(COLORS['grid'])
        
    plt.tight_layout()
    plt.savefig('temp_chart4.png', dpi=300, facecolor=COLORS['bg'])
    plt.close()

# --- PDF GENERATION WITH REPORTLAB ---

def build_pdf_document():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.lib import colors
    from reportlab.lib import fonts
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # 1. Register TTF fonts
    font_path = "C:\\Windows\\Fonts\\tahoma.ttf"
    font_bold_path = "C:\\Windows\\Fonts\\tahomabd.ttf"
    
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Tahoma', font_path))
    else:
        print("Error: Tahoma font not found!")
        sys.exit(1)
        
    if os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont('Tahoma-Bold', font_bold_path))
    else:
        # Fallback if bold tahoma isn't found
        pdfmetrics.registerFont(TTFont('Tahoma-Bold', font_path))
        
    # 2. Register font mappings for paraparser bold/italic tags
    fonts.addMapping('Tahoma', 0, 0, 'Tahoma')
    fonts.addMapping('Tahoma', 1, 0, 'Tahoma-Bold')
    fonts.addMapping('Tahoma-Bold', 0, 0, 'Tahoma-Bold')
    fonts.addMapping('Tahoma-Bold', 1, 0, 'Tahoma-Bold')
    
    pdf_filename = 'MIN_pitpibool_Trading_Plan.pdf'
    
    # Setup document
    margin = 40
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    # Setup styles
    styles = getSampleStyleSheet()
    
    # Custom styles using Tahoma for Thai support
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Tahoma-Bold',
        fontSize=26,
        leading=34,
        textColor=colors.HexColor('#06b6d4'),
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Tahoma',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    author_style = ParagraphStyle(
        'CoverAuthor',
        parent=styles['Normal'],
        fontName='Tahoma',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#cbd5e1'),
        alignment=TA_CENTER,
        spaceAfter=60
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Tahoma-Bold',
        fontSize=16,
        leading=22,
        textColor=colors.HexColor('#06b6d4'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Tahoma-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#eab308'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Tahoma',
        fontSize=9.5,
        leading=15,
        textColor=colors.HexColor('#cbd5e1'),
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=5
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Tahoma',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#f43f5e'),
        spaceBefore=5,
        spaceAfter=5
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Tahoma',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#cbd5e1')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Tahoma-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#f8fafc'),
        alignment=TA_CENTER
    )

    story = []
    
    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 20))
    
    # Logo
    logo_img = Image('temp_logo.png', width=5.5*inch, height=1.57*inch)
    story.append(logo_img)
    story.append(Spacer(1, 30))
    
    # Title
    story.append(Paragraph('คู่มือแผนเทรดโอกาสชนะสูง', title_style))
    story.append(Paragraph('4 กลยุทธ์การเทรดหุ้น US Penny Stocks สำหรับ Scalper', subtitle_style))
    
    # Author / Credit
    story.append(Paragraph('ผู้จัดเตรียมแผนเทรด: <b>พิตรพิบูล คำซองเมือง</b>', author_style))
    story.append(Spacer(1, 15))
    
    # Intro box
    intro_html = (
        "<b>บทนำ:</b> คู่มือนี้จัดทำขึ้นโดยแบรนด์ <b>MIN pitpibool</b> เพื่อรวบรวมแผนและกลยุทธ์ "
        "การเทรดหุ้นเก็งกำไรสหรัฐฯ (US Penny Stocks) ที่มีโอกาสชนะสูง (High Win-Rate) โดยอาศัย "
        "การวิเคราะห์ทางเทคนิคขั้นสูง (Technical Analysis) ร่วมกับเครื่องมือตรวจวัดแรงซื้อขายแบบเรียลไทม์ "
        "เช่น Volume Profile, VWAP, Order Book Level 2 และ Time & Sales เพื่อช่วยในการประเมินจุดเข้าซื้อ "
        "และจุดทำกำไรที่มีประสิทธิภาพสูงสุดและควบคุมความเสี่ยงอย่างเป็นระบบ"
    )
    story.append(Paragraph(intro_html, body_style))
    story.append(PageBreak())
    
    # --- PAGE 2: STRATEGY 1 ---
    story.append(Paragraph('กลยุทธ์ที่ 1: Post-Spike Reversal (After Hours 18:00+)', h1_style))
    
    desc_1 = (
        "<b>แนวคิดและหลักการ:</b> กลยุทธ์นี้ใช้สำหรับดักซื้อหุ้นเทรดนอกเวลาปกติ (After Hours) "
        "หลังเวลา 18:00 น. โดยรอให้หุ้นที่มีการวิ่งขึ้นรุนแรง (Spike) และมีการย่อตัวลงมามากๆ (Deep Pullback) "
        "จากนั้นวิเคราะห์โดยการลากเส้น <b>Volume Profile</b> ตั้งแต่ช่วง After Hours จนถึงเวลาปัจจุบัน "
        "เพื่อหาจุดเข้าซื้อที่มีความได้เปรียบสูงและมีนัยสำคัญทางสถิติ"
    )
    story.append(Paragraph(desc_1, body_style))
    
    story.append(Paragraph('เกณฑ์การเข้าซื้อและเป้าหมาย:', h2_style))
    story.append(Paragraph('• <b>จุดเข้าซื้อ (Entry):</b> รอจังหวะราคาย่อตัวแตะแนว <b>VAL (Value Area Low)</b> จาก Volume Profile', bullet_style))
    story.append(Paragraph('• <b>เป้าหมายราคา (Target):</b> ขายทำกำไรที่แนว <b>POC (Point of Control)</b> ซึ่งเป็นราคาที่มีปริมาณการเทรดหนาแน่นที่สุด', bullet_style))
    story.append(Paragraph('• <b>เครื่องมือตรวจวัด (Confirmation):</b> ดูหน้าต่าง <b>Time & Sales</b> ควบคู่ไปด้วย เพื่อยืนยันว่ามีปริมาณการซื้อ (Buy Volume) ไหลเข้าสู้ที่แนวรับอย่างแท้จริง', bullet_style))
    
    story.append(Spacer(1, 5))
    chart1_img = Image('temp_chart1.png', width=6.2*inch, height=4.2*inch)
    story.append(chart1_img)
    story.append(PageBreak())
    
    # --- PAGE 3: STRATEGY 2 ---
    story.append(Paragraph('กลยุทธ์ที่ 2: Below VWAP Recovery', h1_style))
    
    desc_2 = (
        "<b>แนวคิดและหลักการ:</b> ใช้เทรดหุ้นที่เคย Spike สูงมาก่อนในวันปัจจุบัน แต่ราคาปัจจุบันกลับร่วงหล่นลงมา "
        "ต่ำกว่าเส้นเฉลี่ยน้ำหนักการซื้อขาย <b>VWAP (Volume Weighted Average Price)</b> จุดเด่นของกลยุทธ์นี้คือ "
        "การหาจุดฟื้นตัวจากใต้เส้น VWAP โดยอาศัยแรงขายที่ใกล้หมดแรง (Exhaustion)"
    )
    story.append(Paragraph(desc_2, body_style))
    
    story.append(Paragraph('เกณฑ์การเข้าซื้อและเป้าหมาย:', h2_style))
    story.append(Paragraph('• <b>การวิเคราะห์แนวรับ:</b> ลากเส้น <b>Volume Profile</b> ดูเฉพาะแนว <b>POC After Hours</b> จนถึงเวลาล่าสุดของวัน', bullet_style))
    story.append(Paragraph('• <b>เครื่องมือตรวจวัด (Confirmation):</b> ตรวจสอบตาราง <b>Order Book Level 2</b> เพื่อดูราคาที่มีปริมาณหุ้นรอขายหนาแน่นที่สุด (Sell Wall)', bullet_style))
    story.append(Paragraph('• <b>จุดสังเกตสำคัญ:</b> ประเมินว่า Sell Wall ก้อนใหญ่ดังกล่าวอยู่ห่างจากราคาปัจจุบันมากแค่ไหน หาก Sell Wall อยู่ห่างและ POC อยู่ด้านบน แสดงว่ามีพื้นที่ให้ราคาดีดตัวกลับ (Recovery Room) กว้างเพียงพอให้เก็งกำไรได้', bullet_style))
    
    story.append(Spacer(1, 5))
    chart2_img = Image('temp_chart2.png', width=6.2*inch, height=4.2*inch)
    story.append(chart2_img)
    story.append(PageBreak())
    
    # --- PAGE 4: STRATEGY 3 ---
    story.append(Paragraph('กลยุทธ์ที่ 3: Scalper เทรดหุ้นเทรนด์ขาขึ้น', h1_style))
    
    desc_3 = (
        "<b>แนวคิดและหลักการ:</b> เป็นกลยุทธ์สำหรับนักสเกลเปอร์ (Scalper) เน้นเทรดตามเทรนด์ขาขึ้นความเร็วสูง (Momentum Follow) "
        "โดยคัดเฉพาะหุ้นที่มีปริมาณการซื้อขายหนาแน่นพิเศษ (High Volume) และเคยมีพฤติกรรม Spike มาก่อนหน้านี้"
    )
    story.append(Paragraph(desc_3, body_style))
    
    story.append(Paragraph('เกณฑ์การเข้าซื้อและเป้าหมาย:', h2_style))
    story.append(Paragraph('• <b>เงื่อนไขหลัก (Uptrend Criteria):</b> ราคาปัจจุบันต้องยืนเหนือเส้น <b>VWAP</b> ได้อย่างมั่นคง ยืนยันแนวโน้มขาขึ้น', bullet_style))
    story.append(Paragraph('• <b>การหาจุดเข้า (Entry):</b> วิเคราะห์ Volume Profile เพื่อดูแนว <b>VAH (Value Area High)</b> และหาระยะห่างจากแนว <b>POC</b> เข้าซื้อเมื่อราคายืนเหนือ VAH และอยู่ใกล้หรือห่างจาก POC พอเหมาะ', bullet_style))
    story.append(Paragraph('• <b>การตัดขาดทุน (Stop Loss):</b> จุดเข้าต้องใกล้แนวรับสำคัญ <b>ราคาห้ามหลุดแนว VAH</b> เป็นอันขาด หากราคาหลุดเส้น VAH ให้ตัดขาดทุนทันที (Strict Stop-Loss)', bullet_style))
    
    story.append(Spacer(1, 5))
    chart3_img = Image('temp_chart3.png', width=6.2*inch, height=4.2*inch)
    story.append(chart3_img)
    story.append(PageBreak())
    
    # --- PAGE 5: STRATEGY 4 ---
    story.append(Paragraph('กลยุทธ์ที่ 4: เทรดหลัง HALT (ระบบหยุดซื้อขายชั่วคราว)', h1_style))
    
    desc_4 = (
        "<b>แนวคิดและหลักการ:</b> หุ้น Penny Stock สหรัฐฯ มักถูกตลาดหยุดซื้อขายชั่วคราว (Volatility Halt) "
        "เนื่องจากราคาเคลื่อนไหวรวดเร็วเกินไป กลยุทธ์นี้จะดักซื้อในจังหวะ Resumption (เปิดเทรดใหม่อีกครั้ง) "
        "โดยตั้งอยู่บนความมีระเบียบวินัยขั้นสูง"
    )
    story.append(Paragraph(desc_4, body_style))
    
    story.append(Paragraph('เกณฑ์การเข้าซื้อและเป้าหมาย:', h2_style))
    story.append(Paragraph('• <b>เงื่อนไขเวลา:</b> หลังจากการกลับมาซื้อขาย (Resume) ราคาต้องสามารถยืนอยู่เหนือราคาปิดของแท่งเทียนก่อนหน้า (Pre-Halt Close) ได้นาน <b>5-10 นาที</b>', bullet_style))
    story.append(Paragraph('• <b>ข้อควรระวังหลัก:</b> <b>ห้าม FOMO (Fear of Missing Out)</b> ไล่ซื้อราคาเปิดเด็ดขาด ให้ใจเย็นๆ รอจังหวะย่อตัว', bullet_style))
    story.append(Paragraph('• <b>การหาจุดเข้า (Entry):</b> ลากเส้น Volume Profile บนแท่งเทียนกราฟ 5 นาทีที่เกิดการ HALT พอดี แล้วตั้งซื้อเมื่อราคาย่อตัวลงมาถึงแนว <b>POC</b> ของแท่งนั้น', bullet_style))
    story.append(Paragraph('• <b>เครื่องมือตรวจวัด (Confirmation):</b> ดูตาราง <b>Order Book Level 2</b> เพื่อตรวจสอบว่าราคาส่วนใหญ่เป็นสีเขียว (บวกตลอดเวลา) และมีแรงรับซื้อต่อเนื่อง', bullet_style))
    
    story.append(Spacer(1, 5))
    chart4_img = Image('temp_chart4.png', width=6.2*inch, height=4.2*inch)
    story.append(chart4_img)
    story.append(PageBreak())
    
    # --- PAGE 6: SUMMARY TABLE & DISCLAIMER ---
    story.append(Paragraph('ตารางสรุปแผนเทรดด่วน (Trading Cheat Sheet)', h1_style))
    story.append(Spacer(1, 10))
    
    # Summary Table data
    headers = [
        Paragraph('<b>กลยุทธ์</b>', table_header_style),
        Paragraph('<b>เงื่อนไขสำคัญ</b>', table_header_style),
        Paragraph('<b>จุดเข้าซื้อ (Entry)</b>', table_header_style),
        Paragraph('<b>เป้าหมาย (Target)</b>', table_header_style),
        Paragraph('<b>จุดออก/Stop Loss</b>', table_header_style)
    ]
    
    row1 = [
        Paragraph('<b>1. Post-Spike Reversal</b>', table_cell_style),
        Paragraph('เทรด After Hours 18:00+ หุ้น Spike แล้วย่อตัวลึก', table_cell_style),
        Paragraph('แนวรับ VAL ช่วง After Hours', table_cell_style),
        Paragraph('แนวต้าน POC', table_cell_style),
        Paragraph('ดู Time & Sales ยืนยันแรงซื้อ', table_cell_style)
    ]
    
    row2 = [
        Paragraph('<b>2. Below VWAP</b>', table_cell_style),
        Paragraph('ราคาปัจจุบันหลุดใต้เส้น VWAP หลังเคยวิ่งขึ้นสูง', table_cell_style),
        Paragraph('ใต้ VWAP โดยเช็คแนว POC After Hours', table_cell_style),
        Paragraph('แนว POC ด้านบน', table_cell_style),
        Paragraph('เช็ค Order Book L2 ระยะห่างจาก Sell Wall', table_cell_style)
    ]
    
    row3 = [
        Paragraph('<b>3. Scalper ขาขึ้น</b>', table_cell_style),
        Paragraph('เทรนด์ขึ้นเหนือ VWAP มี Volume ซื้อขายสูงมาก', table_cell_style),
        Paragraph('เหนือนแนว VAH และใกล้แนว POC', table_cell_style),
        Paragraph('POC และเป้าหมายตามความเร่ง', table_cell_style),
        Paragraph('<b>คัททันทีถ้าหลุดแนว VAH</b>', table_cell_style)
    ]
    
    row4 = [
        Paragraph('<b>4. HALT Play</b>', table_cell_style),
        Paragraph('หุ้นกลับมาเทรดหลัง Halt และยืนได้ 5-10 นาที', table_cell_style),
        Paragraph('ตั้งรับที่แนว POC ของแท่งกราฟ 5 นาทีช่วงที่ Halt', table_cell_style),
        Paragraph('ตามเป้าหมายโมเมนตัมบวก', table_cell_style),
        Paragraph('<b>ห้าม FOMO!</b> คัทหากหลุดราคาปิดแท่งก่อน Halt', table_cell_style)
    ]
    
    data = [headers, row1, row2, row3, row4]
    
    # 6.5 inches total width
    t = Table(data, colWidths=[1.2*inch, 1.6*inch, 1.4*inch, 1.1*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0d9488')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#1e293b'), colors.HexColor('#0f172a')]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 25))
    
    # Brand Footer Note
    story.append(Paragraph('พัฒนาภายใต้มาตรฐานระบบการเทรดโดยแบรนด์: <b>MIN pitpibool</b>', ParagraphStyle('BrandText', parent=body_style, textColor=colors.HexColor('#06b6d4'), alignment=TA_CENTER)))
    story.append(Spacer(1, 15))
    
    # Warning callout
    warning_text = (
        "<b>คำเตือนความเสี่ยง (Risk Disclaimer):</b> การเทรดหุ้นเก็งกำไรขนาดเล็ก (US Penny Stocks) "
        "มีความผันผวนสูงมากและมีความเสี่ยงสูงในการสูญเสียเงินลงทุน คู่มือและแผนเทรดนี้มีวัตถุประสงค์เพื่อใช้เป็น "
        "แนวทางศึกษาวิเคราะห์ทางสถิติและเทคนิคเท่านั้น ผู้เทรดควรประเมินความเสี่ยงและกำหนดจุดตัดขาดทุน (Stop Loss) "
        "อย่างเคร่งครัดทุกครั้งก่อนส่งคำสั่งซื้อขาย"
    )
    
    # Callout box styled as a single cell table
    callout_data = [[Paragraph(warning_text, callout_style)]]
    callout_table = Table(callout_data, colWidths=[6.5*inch])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f43f5e15')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f43f5e33')),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table)
    
    # Background and Page number canvas draws
    def add_page_decorations(canvas, doc):
        canvas.saveState()
        # Draw background color for all pages
        canvas.setFillColor(colors.HexColor('#0a0f1d')) # Very dark navy background
        canvas.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
        
        # Header/Footer
        canvas.setFont('Tahoma', 8)
        canvas.setFillColor(colors.HexColor('#64748b'))
        canvas.drawString(40, A4[1] - 25, "MIN pitpibool • High Win-Rate Trading Plan")
        canvas.drawRightString(A4[0] - 40, 20, f"หน้า {doc.page}")
        canvas.drawCentredString(A4[0] / 2, 20, "การลงทุนมีความเสี่ยง ควรศึกษาข้อมูลก่อนการลงทุน")
        canvas.restoreState()
        
    doc.build(story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)

if __name__ == '__main__':
    print("Generating MIN pitpibool Logo...")
    generate_logo()
    print("Generating Chart 1...")
    generate_chart1()
    print("Generating Chart 2...")
    generate_chart2()
    print("Generating Chart 3...")
    generate_chart3()
    print("Generating Chart 4...")
    generate_chart4()
    print("Assembling PDF Document...")
    build_pdf_document()
    
    # Clean up temp files
    temp_files = ['temp_logo.png', 'temp_chart1.png', 'temp_chart2.png', 'temp_chart3.png', 'temp_chart4.png']
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
    print("Success! Generated MIN_pitpibool_Trading_Plan.pdf")
