/* ==========================================================================
   MIN pitpibool - CHART RENDERING ENGINE (REDESIGNED)
   Ultra-Modern Canvas Trading Charts with Glowing Neon & Space-Age Aesthetics
   ========================================================================== */

const COLORS = {
    bgStart: '#06050e',
    bgEnd: '#0a091e',
    grid: 'rgba(255, 255, 255, 0.015)',
    gridLine: 'rgba(255, 255, 255, 0.03)',
    
    // Neon Lights (Standard Trading Colors but glowing)
    green: '#00e676',      // Standard Trading Green (Bullish)
    greenGlow: 'rgba(0, 230, 118, 0.3)',
    red: '#ff1744',        // Standard Trading Red (Bearish)
    redGlow: 'rgba(255, 23, 68, 0.3)',
    cyan: '#00f2fe',       // Cyber Cyan (POC)
    cyanGlow: 'rgba(0, 242, 254, 0.4)',
    blue: '#4facfe',       // Electric Blue (VAL)
    purple: '#d946ef',     // Neon Purple (VWAP)
    purpleGlow: 'rgba(217, 70, 239, 0.4)',
    yellow: '#ffb703',     // Gold (Spike / Warnings)
    orange: '#ff5e00',     // Orange (Halt / Sell Wall)
    
    textPrimary: '#f8fafc',
    textSecondary: '#94a3b8',
    textDim: '#475569',
};

// --- Helper Utilities ---

function setupCanvasDPI(canvas) {
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    
    ctx.scale(dpr, dpr);
    return { width: rect.width, height: rect.height };
}

function getResponsiveChartLayout(W, H) {
    const compact = W < 640;
    const tablet = W >= 640 && W < 900;
    const sidePanel = compact ? 18 : tablet ? 120 : 200;
    const left = compact ? 34 : 50;
    const top = compact ? 50 : 60;
    const bottom = H - (compact ? 82 : 90);

    return {
        compact,
        tablet,
        chart: { left, top, right: W - sidePanel, bottom },
        volArea: { top: H - (compact ? 72 : 80), bottom: H - 20 },
        sidePanel,
    };
}

function fillBackground(ctx, w, h) {
    // Cyberpunk backlit glow effect (radial gradient in the center)
    const radial = ctx.createRadialGradient(w/2, h/2, 50, w/2, h/2, Math.max(w, h));
    radial.addColorStop(0, '#0c0a25');
    radial.addColorStop(0.5, '#070617');
    radial.addColorStop(1, COLORS.bgStart);
    ctx.fillStyle = radial;
    ctx.fillRect(0, 0, w, h);
}

function drawRoundedRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
}

function drawCandle(ctx, x, open, close, high, low, width) {
    const isGreen = close > open;
    const color = isGreen ? COLORS.green : COLORS.red;
    const glow = isGreen ? COLORS.greenGlow : COLORS.redGlow;
    const top = Math.min(open, close);
    const bottom = Math.max(open, close);
    const height = Math.max(bottom - top, 1.5);

    // Wick (thin glowing line)
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    ctx.shadowColor = color;
    ctx.shadowBlur = 4;
    ctx.beginPath();
    ctx.moveTo(x + width/2, high);
    ctx.lineTo(x + width/2, low);
    ctx.stroke();
    
    // Body (glowing capsule)
    ctx.fillStyle = color;
    ctx.shadowColor = glow;
    ctx.shadowBlur = 10;
    
    // Draw body
    ctx.fillRect(x + 1.5, top, width - 3, height);
    
    // Reset shadow
    ctx.shadowBlur = 0;
}

function drawVolumeBar(ctx, x, height, baseY, isGreen, width) {
    const color = isGreen ? COLORS.green : COLORS.red;
    const grad = ctx.createLinearGradient(x, baseY - height, x, baseY);
    grad.addColorStop(0, isGreen ? 'rgba(0, 230, 118, 0.4)' : 'rgba(255, 23, 68, 0.4)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    
    ctx.fillStyle = grad;
    ctx.fillRect(x + 1.5, baseY - height, width - 3, height);
    
    ctx.strokeStyle = isGreen ? 'rgba(0, 230, 118, 0.15)' : 'rgba(255, 23, 68, 0.15)';
    ctx.lineWidth = 1;
    ctx.strokeRect(x + 1.5, baseY - height, width - 3, height);
}

function drawGrid(ctx, chart) {
    const { left, top, right, bottom } = chart;
    ctx.strokeStyle = COLORS.gridLine;
    ctx.lineWidth = 0.5;

    // Horizontal Lines
    for (let i = 0; i <= 6; i++) {
        const y = top + (bottom - top) * i / 6;
        ctx.beginPath();
        ctx.moveTo(left, y);
        ctx.lineTo(right, y);
        ctx.stroke();
    }

    // Vertical Lines
    for (let i = 0; i <= 10; i++) {
        const x = left + (right - left) * i / 10;
        ctx.beginPath();
        ctx.moveTo(x, top);
        ctx.lineTo(x, bottom);
        ctx.stroke();
    }
}

function drawVolumeProfile(ctx, x, width, levels, chartTop, chartBottom, maxVol, color) {
    const numLevels = levels.length;
    const levelH = (chartBottom - chartTop) / numLevels;

    levels.forEach((vol, i) => {
        const barW = (vol / maxVol) * width;
        const y = chartTop + i * levelH;
        
        const grad = ctx.createLinearGradient(x, y, x + barW, y);
        grad.addColorStop(0, color + '55'); // transparent color
        grad.addColorStop(1, color + '03');
        
        ctx.fillStyle = grad;
        drawRoundedRect(ctx, x, y + 1.5, barW, levelH - 3, 3);
        ctx.fill();
        
        ctx.strokeStyle = color + '22';
        ctx.lineWidth = 0.8;
        ctx.stroke();
    });
}

function drawDashedLine(ctx, x1, y1, x2, y2, color, dashPattern = [6, 4]) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    ctx.setLineDash(dashPattern);
    ctx.shadowColor = color;
    ctx.shadowBlur = 4;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.shadowBlur = 0;
}

function drawBadge(ctx, text, x, y, color, align = 'left') {
    const canvasWidth = ctx.canvas.getBoundingClientRect().width || ctx.canvas.width;
    const canvasHeight = ctx.canvas.getBoundingClientRect().height || ctx.canvas.height;
    const compact = canvasWidth < 640;
    ctx.font = `bold ${compact ? 7.5 : 9}px "Outfit", "Noto Sans Thai", sans-serif`;
    const metrics = ctx.measureText(text);
    const padX = compact ? 5 : 7, padY = 4;
    const w = metrics.width + padX * 2;
    const h = compact ? 14 : 16;
    let lx = align === 'right' ? x - w : align === 'center' ? x - w / 2 : x;
    lx = Math.max(4, Math.min(lx, canvasWidth - w - 4));
    const cy = Math.max(h / 2 + 4, Math.min(y, canvasHeight - h / 2 - 4));
    
    // Glassmorphism Badge
    ctx.fillStyle = 'rgba(10, 10, 25, 0.85)';
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    ctx.shadowColor = color + '44';
    ctx.shadowBlur = 6;
    
    drawRoundedRect(ctx, lx, cy - h / 2, w, h, 4);
    ctx.fill();
    ctx.stroke();
    
    // Text inside
    ctx.fillStyle = color;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.shadowBlur = 0;
    ctx.fillText(text, lx + padX, cy);
}

function drawArrow(ctx, fromX, fromY, toX, toY, color) {
    const angle = Math.atan2(toY - fromY, toX - fromX);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.shadowColor = color;
    ctx.shadowBlur = 8;
    
    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();

    const headLen = 8;
    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle - Math.PI / 6), toY - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(toX - headLen * Math.cos(angle + Math.PI / 6), toY - headLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();
    
    ctx.shadowBlur = 0;
}

function drawGlassBox(ctx, x, y, w, h, borderColor) {
    ctx.fillStyle = 'rgba(8, 8, 20, 0.75)';
    ctx.strokeStyle = borderColor || 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    ctx.shadowColor = 'rgba(0,0,0,0.5)';
    ctx.shadowBlur = 20;
    
    drawRoundedRect(ctx, x, y, w, h, 12);
    ctx.fill();
    ctx.stroke();
    
    ctx.shadowBlur = 0;
}

// ==========================================================================
// STRATEGY 1: Post-Spike Reversal
// ==========================================================================
function drawChart1() {
    const canvas = document.getElementById('chart1');
    if (!canvas) return;
    const { width: W, height: H } = setupCanvasDPI(canvas);
    const ctx = canvas.getContext('2d');
    fillBackground(ctx, W, H);

    const { chart, volArea, compact } = getResponsiveChartLayout(W, H);
    drawGrid(ctx, chart);

    // Header Title
    ctx.font = '900 15px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.textPrimary;
    ctx.textAlign = 'left';
    ctx.fillText('กลยุทธ์ที่ 1: เข้าหลังหุ้น Spike แล้วร่วง (After Hours 18:00+)', chart.left, 35);

    // Setup Candle Data
    const o = [180, 200, 240, 290, 310, 280, 250, 225, 200, 185, 168, 168, 175, 185, 198];
    const c = [200, 240, 290, 310, 280, 250, 225, 200, 185, 168, 168, 175, 185, 198, 212];
    const h = [205, 245, 295, 320, 315, 285, 255, 230, 205, 190, 178, 178, 182, 202, 218];
    const l = [175, 195, 235, 285, 275, 245, 220, 195, 180, 162, 162, 165, 170, 180, 195];
    const v = [30, 45, 90, 85, 70, 55, 45, 40, 35, 30, 50, 40, 55, 60, 50];

    const minP = 140, maxP = 340;
    const priceToY = (p) => chart.top + (1 - (p - minP) / (maxP - minP)) * (chart.bottom - chart.top);
    const candleW = (chart.right - chart.left) / o.length;

    // Draw Candles & Volume
    o.forEach((_, i) => {
        const x = chart.left + i * candleW;
        drawCandle(ctx, x, priceToY(o[i]), priceToY(c[i]), priceToY(h[i]), priceToY(l[i]), candleW);
        
        const hVol = (v[i] / 100) * (volArea.bottom - volArea.top);
        drawVolumeBar(ctx, x, hVol, volArea.bottom, c[i] >= o[i], candleW);
    });

    // Volume Profile (Right side)
    const vpLevels = [10, 20, 45, 70, 90, 80, 60, 40, 35, 55, 75, 50, 25, 15];
    const prices = np_linspace(160, 320, vpLevels.length);
    const levelH = (chart.bottom - chart.top) / vpLevels.length;
    
    // Draw Volume Profile bars
    drawVolumeProfile(ctx, chart.right + 5, 65, vpLevels, chart.top, chart.bottom, 100, COLORS.cyan);

    // Draw lines
    const vahY = priceToY(275);
    const pocY = priceToY(225);
    const valY = priceToY(168);

    drawDashedLine(ctx, chart.left, vahY, chart.right + 75, vahY, COLORS.green);
    drawBadge(ctx, 'VAH แนวต้าน (2.75)', chart.right + 78, vahY, COLORS.green);

    drawDashedLine(ctx, chart.left, pocY, chart.right + 75, pocY, COLORS.cyan);
    drawBadge(ctx, 'POC เป้าหมาย (2.25)', chart.right + 78, pocY, COLORS.cyan);

    drawDashedLine(ctx, chart.left, valY, chart.right + 75, valY, COLORS.red);
    drawBadge(ctx, 'VAL จุดเข้าซื้อ (1.68)', chart.right + 78, valY, COLORS.red);

    // Annotations
    const entryX = chart.left + 10 * candleW + candleW/2;
    drawArrow(ctx, entryX - 25, valY + 30, entryX, valY + 4, COLORS.green);
    drawBadge(ctx, 'จุดเข้าซื้อ VAL', entryX - 70, valY + 35, COLORS.green);

    drawArrow(ctx, entryX + 20, pocY + 30, entryX + 45, pocY + 4, COLORS.cyan);
    drawBadge(ctx, 'เป้าหมายทำกำไร POC', entryX + 10, pocY + 40, COLORS.cyan);

    drawBadge(ctx, 'หุ้น Spike รุนแรง 🚀', chart.left + 2.5 * candleW, priceToY(310) - 20, COLORS.yellow, 'center');
    drawBadge(ctx, 'ราคาร่วงคายของ 📉', chart.left + 7 * candleW, priceToY(225) - 20, COLORS.red, 'center');

    // Time & Sales High-Tech Panel
    if (!compact) {
    const tsX = chart.right + 85, tsY = chart.bottom - 120;
    drawGlassBox(ctx, tsX, tsY, 110, 115, 'rgba(0, 242, 254, 0.15)');

    ctx.font = 'bold 9px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.cyan;
    ctx.textAlign = 'center';
    ctx.fillText('TIME & SALES', tsX + 55, tsY + 16);

    const tsData = [
        { t: '18:05:42', p: '1.69', v: '2,500', c: COLORS.green },
        { t: '18:05:39', p: '1.68', v: '8,000', c: COLORS.green },
        { t: '18:05:35', p: '1.68', v: '15,000', c: COLORS.green },
        { t: '18:05:30', p: '1.67', v: '3,200', c: COLORS.red },
        { t: '18:05:22', p: '1.68', v: '500', c: COLORS.green },
        { t: '18:05:15', p: '1.67', v: '10,000', c: COLORS.red },
    ];

    tsData.forEach((d, i) => {
        const rowY = tsY + 32 + i * 13;
        ctx.font = '8px "Outfit", monospace';
        ctx.fillStyle = COLORS.textSecondary;
        ctx.textAlign = 'left';
        ctx.fillText(d.t, tsX + 8, rowY);
        
        ctx.fillStyle = d.c;
        ctx.fillText(d.p, tsX + 54, rowY);
        
        ctx.fillStyle = COLORS.textPrimary;
        ctx.textAlign = 'right';
        ctx.fillText(d.v, tsX + 102, rowY);
    });
    }

    // Axis Labels
    ctx.font = '8px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.textDim;
    ctx.textAlign = 'right';
    for (let p = minP; p <= maxP; p += 40) {
        ctx.fillText(p.toFixed(0), chart.left - 8, priceToY(p) + 3);
    }
}

// ==========================================================================
// STRATEGY 2: Below VWAP Recovery
// ==========================================================================
function drawChart2() {
    const canvas = document.getElementById('chart2');
    if (!canvas) return;
    const { width: W, height: H } = setupCanvasDPI(canvas);
    const ctx = canvas.getContext('2d');
    fillBackground(ctx, W, H);

    const { chart, volArea, compact } = getResponsiveChartLayout(W, H);
    drawGrid(ctx, chart);

    ctx.font = '900 15px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.textPrimary;
    ctx.textAlign = 'left';
    ctx.fillText('กลยุทธ์ที่ 2: หุ้น Spike แล้วราคาหล่นมาใต้ VWAP', chart.left, 35);

    // Setup Candle Data
    const o = [110, 115, 130, 160, 180, 160, 145, 135, 125, 118, 120, 112, 108, 112, 107];
    const c = [115, 130, 160, 180, 160, 145, 135, 125, 118, 120, 112, 108, 112, 107, 110];
    const h = [118, 132, 165, 185, 182, 165, 148, 138, 128, 122, 122, 115, 114, 115, 112];
    const l = [108, 113, 128, 155, 158, 142, 132, 122, 116, 115, 110, 106, 106, 105, 105];
    const v = [20, 35, 75, 95, 70, 50, 40, 30, 25, 22, 20, 18, 25, 22, 20];

    const minP = 90, maxP = 200;
    const priceToY = (p) => chart.top + (1 - (p - minP) / (maxP - minP)) * (chart.bottom - chart.top);
    const candleW = (chart.right - chart.left) / o.length;

    // Draw Candles & Volume
    o.forEach((_, i) => {
        const x = chart.left + i * candleW;
        drawCandle(ctx, x, priceToY(o[i]), priceToY(c[i]), priceToY(h[i]), priceToY(l[i]), candleW);
        const hVol = (v[i] / 100) * (volArea.bottom - volArea.top);
        drawVolumeBar(ctx, x, hVol, volArea.bottom, c[i] >= o[i], candleW);
    });

    // VWAP Line (Neon Purple Tube)
    const vwap = [112, 118, 135, 150, 155, 152, 147, 142, 139, 137, 135, 134, 133, 132, 131];
    ctx.strokeStyle = COLORS.purple;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = COLORS.purpleGlow;
    ctx.shadowBlur = 10;
    ctx.beginPath();
    vwap.forEach((val, idx) => {
        const px = chart.left + idx * candleW + candleW/2;
        const py = priceToY(val);
        idx === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    });
    ctx.stroke();
    ctx.shadowBlur = 0; // Reset
    
    drawBadge(ctx, 'เส้น VWAP', chart.left + 5 * candleW, priceToY(vwap[5]) - 14, COLORS.purple);

    // Draw POC After Hours
    const pocY = priceToY(140);
    drawDashedLine(ctx, chart.left, pocY, chart.right + 75, pocY, COLORS.cyan);
    drawBadge(ctx, 'POC AH (1.40)', chart.right + 78, pocY, COLORS.cyan);

    // Current Price Glow Dot
    const curX = chart.left + 14 * candleW + candleW/2;
    const curY = priceToY(110);
    ctx.fillStyle = COLORS.yellow;
    ctx.shadowColor = COLORS.yellow;
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.arc(curX, curY, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    
    drawBadge(ctx, 'ราคาหลุดใต้ VWAP 📉', curX - 110, curY, COLORS.yellow);

    // Sell Wall line
    const swY = priceToY(165);
    drawDashedLine(ctx, chart.left, swY, chart.right + 75, swY, COLORS.orange);
    drawBadge(ctx, 'Sell Wall (1.65)', chart.right + 78, swY, COLORS.orange);

    // Distance arrow
    drawArrow(ctx, curX, curY - 5, curX, swY + 5, COLORS.orange);
    drawBadge(ctx, 'วัดระยะห่างแนวขายสะสม', curX - 60, (curY + swY)/2, COLORS.orange);

    // Order Book Level 2 high-tech panel
    if (!compact) {
    const obX = chart.right + 85, obY = chart.top + 10;
    drawGlassBox(ctx, obX, obY, 110, 130, 'rgba(217, 70, 239, 0.15)');

    ctx.font = 'bold 9px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.purple;
    ctx.textAlign = 'center';
    ctx.fillText('ORDER BOOK L2', obX + 55, obY + 16);

    const askPrices = ['1.68', '1.65', '1.60', '1.58'];
    const askSizes = ['5,200', '98,000', '12,000', '3,500'];
    const askBars = [15, 95, 25, 10]; // bars sizes

    askPrices.forEach((pr, i) => {
        const rowY = obY + 34 + i * 14;
        // background bar
        ctx.fillStyle = 'rgba(255, 0, 127, 0.12)';
        ctx.fillRect(obX + 65, rowY - 7, askBars[i] * 0.4, 11);
        
        ctx.font = '8px "Outfit", monospace';
        ctx.fillStyle = COLORS.red;
        ctx.textAlign = 'left';
        ctx.fillText(pr, obX + 8, rowY);
        
        ctx.fillStyle = COLORS.textPrimary;
        ctx.textAlign = 'right';
        ctx.fillText(askSizes[i], obX + 60, rowY);
    });

    // Sell Wall Marker
    ctx.strokeStyle = COLORS.yellow;
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 2]);
    ctx.strokeRect(obX + 4, obY + 43, 102, 17);
    ctx.setLineDash([]);

    // Bid Prices (Buyers)
    const bidPrices = ['1.10', '1.08'];
    const bidSizes = ['4,200', '8,000'];
    bidPrices.forEach((pr, i) => {
        const rowY = obY + 98 + i * 13;
        ctx.fillStyle = 'rgba(0, 255, 135, 0.12)';
        ctx.fillRect(obX + 65, rowY - 7, 20, 11);
        
        ctx.font = '8px "Outfit", monospace';
        ctx.fillStyle = COLORS.green;
        ctx.textAlign = 'left';
        ctx.fillText(pr, obX + 8, rowY);
        
        ctx.fillStyle = COLORS.textPrimary;
        ctx.textAlign = 'right';
        ctx.fillText(bidSizes[i], obX + 60, rowY);
    });
    }

    // Y Axis
    ctx.font = '8px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.textDim;
    ctx.textAlign = 'right';
    for (let p = minP; p <= maxP; p += 20) {
        ctx.fillText(p.toFixed(0), chart.left - 8, priceToY(p) + 3);
    }
}

// ==========================================================================
// STRATEGY 3: Scalper Uptrend
// ==========================================================================
function drawChart3() {
    const canvas = document.getElementById('chart3');
    if (!canvas) return;
    const { width: W, height: H } = setupCanvasDPI(canvas);
    const ctx = canvas.getContext('2d');
    fillBackground(ctx, W, H);

    const { chart, volArea, compact } = getResponsiveChartLayout(W, H);
    drawGrid(ctx, chart);

    ctx.font = '900 15px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.textPrimary;
    ctx.textAlign = 'left';
    ctx.fillText('กลยุทธ์ที่ 3: Scalper เทรดหุ้นขาขึ้น (ราคายืนเหนือ VWAP)', chart.left, 35);

    // Setup Candle Data
    const o = [90, 110, 130, 118, 115, 122, 128, 135, 132, 138, 145, 152, 148, 155, 162];
    const c = [110, 130, 118, 115, 122, 128, 135, 132, 138, 145, 152, 148, 155, 162, 168];
    const h = [113, 132, 132, 120, 125, 130, 138, 138, 140, 148, 155, 153, 158, 165, 172];
    const l = [88, 108, 115, 112, 113, 120, 125, 130, 130, 135, 142, 145, 145, 152, 160];
    const v = [40, 75, 55, 30, 45, 55, 60, 40, 50, 60, 65, 35, 55, 60, 50];

    const minP = 70, maxP = 180;
    const priceToY = (p) => chart.top + (1 - (p - minP) / (maxP - minP)) * (chart.bottom - chart.top);
    const candleW = (chart.right - chart.left) / o.length;

    // Draw Candles & Volume
    o.forEach((_, i) => {
        const x = chart.left + i * candleW;
        drawCandle(ctx, x, priceToY(o[i]), priceToY(c[i]), priceToY(h[i]), priceToY(l[i]), candleW);
        const hVol = (v[i] / 100) * (volArea.bottom - volArea.top);
        drawVolumeBar(ctx, x, hVol, volArea.bottom, c[i] >= o[i], candleW);
    });

    // VWAP Line (below candles)
    const vwap = [95, 108, 112, 113, 115, 118, 122, 124, 126, 130, 134, 136, 138, 141, 144];
    ctx.strokeStyle = COLORS.purple;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = COLORS.purpleGlow;
    ctx.shadowBlur = 10;
    ctx.beginPath();
    vwap.forEach((val, idx) => {
        const px = chart.left + idx * candleW + candleW/2;
        const py = priceToY(val);
        idx === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    });
    ctx.stroke();
    ctx.shadowBlur = 0;
    
    drawBadge(ctx, 'ราคาอยู่เหนือ VWAP ✓', chart.left + 8 * candleW, priceToY(vwap[8]) + 16, COLORS.purple);

    // Volume Profile on the right
    const vpLevels = [10, 20, 50, 70, 95, 80, 55, 35, 20, 10];
    drawVolumeProfile(ctx, chart.right + 5, 65, vpLevels, chart.top, chart.bottom, 100, COLORS.cyan);

    // Draw VAH support line
    const vahY = priceToY(130);
    drawDashedLine(ctx, chart.left, vahY, chart.right + 75, vahY, COLORS.green);
    drawBadge(ctx, 'VAH แนวรับ ห้ามหลุด! (1.30)', chart.right + 78, vahY, COLORS.green);

    // Draw POC line
    const pocY = priceToY(145);
    drawDashedLine(ctx, chart.left, pocY, chart.right + 75, pocY, COLORS.cyan);
    drawBadge(ctx, 'POC (1.45)', chart.right + 78, pocY, COLORS.cyan);

    // Entry point above VAH, near POC
    const entryX = chart.left + 10 * candleW + candleW/2;
    const entryY = priceToY(152);
    drawArrow(ctx, entryX - 20, entryY - 25, entryX, entryY - 4, COLORS.green);
    drawBadge(ctx, 'จุดเข้า: ยืนเหนือ VAH ใกล้ POC', entryX - 70, entryY - 30, COLORS.green);

    // Stop Loss at VAH
    ctx.fillStyle = COLORS.red;
    ctx.shadowColor = COLORS.red;
    ctx.shadowBlur = 10;
    ctx.beginPath();
    const slX = chart.left + 10 * candleW + candleW/2;
    ctx.arc(slX, vahY, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    drawBadge(ctx, '🛑 คัททันทีหากหลุด VAH', slX - 110, vahY + 16, COLORS.red);

    // Checklist Panel (Right)
    if (!compact) {
    const clX = chart.right + 85, clY = chart.bottom - 110;
    drawGlassBox(ctx, clX, clY, 110, 105, 'rgba(0, 255, 135, 0.15)');

    ctx.font = 'bold 9px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.green;
    ctx.textAlign = 'center';
    ctx.fillText('CHECKLIST', clX + 55, clY + 15);

    const checks = ['✓ เทรนด์ขึ้น', '✓ เหนือ VWAP', '✓ เคย Spike', '✓ Volume สูง', '✓ ยืนแนว VAH'];
    checks.forEach((ch, i) => {
        ctx.font = '8.5px "Outfit", "Noto Sans Thai", sans-serif';
        ctx.fillStyle = COLORS.textPrimary;
        ctx.textAlign = 'left';
        ctx.fillText(ch, clX + 10, clY + 32 + i * 13);
    });
    }

    // Y Axis
    ctx.font = '8px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.textDim;
    ctx.textAlign = 'right';
    for (let p = minP; p <= maxP; p += 20) {
        ctx.fillText(p.toFixed(0), chart.left - 8, priceToY(p) + 3);
    }
}

// ==========================================================================
// STRATEGY 4: HALT Play
// ==========================================================================
function drawChart4() {
    const canvas = document.getElementById('chart4');
    if (!canvas) return;
    const { width: W, height: H } = setupCanvasDPI(canvas);
    const ctx = canvas.getContext('2d');
    fillBackground(ctx, W, H);

    const { chart, volArea } = getResponsiveChartLayout(W, H);
    drawGrid(ctx, chart);

    ctx.font = '900 15px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.textPrimary;
    ctx.textAlign = 'left';
    ctx.fillText('กลยุทธ์ที่ 4: เทรดหลัง HALT (ราคายืนได้ 5-10 นาที)', chart.left, 35);

    // Candle data: pre-halt and post-halt
    const o_pre = [200, 220, 250, 280];
    const c_pre = [220, 250, 280, 320];
    const h_pre = [225, 255, 285, 325];
    const l_pre = [198, 218, 248, 275];
    const v_pre = [40, 60, 75, 95];

    const o_post = [340, 350, 345, 355, 350, 360, 370];
    const c_post = [350, 345, 355, 350, 360, 370, 380];
    const h_post = [360, 355, 358, 358, 365, 375, 385];
    const l_post = [335, 340, 342, 348, 348, 358, 368];
    const v_post = [90, 70, 65, 55, 60, 75, 80];

    const o = o_pre + [null, null] + o_post;
    const totalSlots = o_pre.length + 2 + o_post.length;
    const candleW = (chart.right - chart.left) / totalSlots;

    const minP = 170, maxP = 400;
    const priceToY = (p) => chart.top + (1 - (p - minP) / (maxP - minP)) * (chart.bottom - chart.top);

    // Draw pre-halt candles
    o_pre.forEach((_, i) => {
        const x = chart.left + i * candleW;
        drawCandle(ctx, x, priceToY(o_pre[i]), priceToY(c_pre[i]), priceToY(h_pre[i]), priceToY(l_pre[i]), candleW);
        const hVol = (v_pre[i] / 100) * (volArea.bottom - volArea.top);
        drawVolumeBar(ctx, x, hVol, volArea.bottom, true, candleW);
    });

    // Draw HALT zone
    const haltX1 = chart.left + o_pre.length * candleW;
    const haltX2 = haltX1 + 2 * candleW;
    
    const haltGrad = ctx.createLinearGradient(haltX1, chart.top, haltX2, chart.top);
    haltGrad.addColorStop(0, 'rgba(255, 94, 0, 0.04)');
    haltGrad.addColorStop(0.5, 'rgba(255, 94, 0, 0.15)');
    haltGrad.addColorStop(1, 'rgba(255, 94, 0, 0.04)');
    ctx.fillStyle = haltGrad;
    ctx.fillRect(haltX1, chart.top, 2 * candleW, chart.bottom - chart.top);

    // Halt boundaries
    drawDashedLine(ctx, haltX1, chart.top, haltX1, chart.bottom, COLORS.orange, [4, 4]);
    drawDashedLine(ctx, haltX2, chart.top, haltX2, chart.bottom, COLORS.orange, [4, 4]);
    
    ctx.font = 'bold 10px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.orange;
    ctx.textAlign = 'center';
    ctx.fillText('⏸ HALT', (haltX1 + haltX2)/2, chart.top + 30);
    ctx.font = '8px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillText('หยุดซื้อขาย', (haltX1 + haltX2)/2, chart.top + 42);

    // Draw post-halt candles
    o_post.forEach((_, i) => {
        const x = haltX2 + i * candleW;
        drawCandle(ctx, x, priceToY(o_post[i]), priceToY(c_post[i]), priceToY(h_post[i]), priceToY(l_post[i]), candleW);
        const hVol = (v_post[i] / 100) * (volArea.bottom - volArea.top);
        drawVolumeBar(ctx, x, hVol, volArea.bottom, c_post[i] >= o_post[i], candleW);
    });

    // Pre-halt close line
    const preCloseY = priceToY(320);
    drawDashedLine(ctx, chart.left, preCloseY, chart.right + 75, preCloseY, COLORS.yellow);
    drawBadge(ctx, 'ราคาปิดก่อน Halt (3.20)', chart.right + 78, preCloseY, COLORS.yellow);

    // Resumption check: stays above previous close
    ctx.font = 'bold 8.5px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.green;
    ctx.textAlign = 'center';
    ctx.fillText('ราคาหลัง Resume ยืนเหนือแท่งปิดได้ ✓', haltX2 + 3.5 * candleW, priceToY(330));
    ctx.font = '8px "Outfit", "Noto Sans Thai", sans-serif';
    ctx.fillStyle = COLORS.textSecondary;
    ctx.fillText('(รอสังเกตอาการ 5-10 นาที)', haltX2 + 3.5 * candleW, priceToY(330) + 12);

    // Volume Profile drawn on the halt candle (or resumption area)
    const vpLevels = [25, 80, 60, 40, 20, 10];
    drawVolumeProfile(ctx, haltX2 + 0.5 * candleW, 40, vpLevels, priceToY(380), priceToY(320), 100, COLORS.cyan);

    // Buy at POC of Halt candle
    const pocY = priceToY(345);
    drawDashedLine(ctx, chart.left, pocY, chart.right + 75, pocY, COLORS.cyan);
    drawBadge(ctx, 'POC แท่ง Halt (3.45)', chart.right + 78, pocY, COLORS.cyan);

    const buyX = haltX2 + candleW/2;
    drawArrow(ctx, buyX, priceToY(300), buyX, pocY + 4, COLORS.green);
    drawBadge(ctx, 'เข้าซื้อสะสมตรง POC', buyX - 55, priceToY(290), COLORS.green);

    // Warning Banner
    drawBadge(ctx, '⚠️ ห้าม FOMO!', (haltX1 + haltX2)/2, chart.top + 80, COLORS.red, 'center');

    // Y Axis
    ctx.font = '8px "Outfit", sans-serif';
    ctx.fillStyle = COLORS.textDim;
    ctx.textAlign = 'right';
    for (let p = minP; p <= maxP; p += 40) {
        ctx.fillText(p.toFixed(0), chart.left - 8, priceToY(p) + 3);
    }
}

// ==========================================================================
// INFOGRAPHIC MINI CHARTS
// ==========================================================================
function drawMiniCharts() {
    // Mini Chart 1
    const mc1 = document.getElementById('miniChart1');
    if (mc1) {
        mc1.innerHTML = '';
        const canvas = document.createElement('canvas');
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        mc1.appendChild(canvas);
        const { width: W, height: H } = setupCanvasDPI(canvas);
        const ctx = canvas.getContext('2d');
        fillBackground(ctx, W, H);
        
        ctx.strokeStyle = COLORS.red;
        ctx.lineWidth = 2;
        ctx.shadowColor = COLORS.redGlow;
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.moveTo(10, 15);
        ctx.lineTo(25, 10);
        ctx.lineTo(40, H - 20);
        ctx.lineTo(W - 40, H - 15);
        ctx.stroke();
        
        // arrow target
        drawArrow(ctx, W - 40, H - 15, W - 15, H/2, COLORS.green);
    }

    // Mini Chart 2
    const mc2 = document.getElementById('miniChart2');
    if (mc2) {
        mc2.innerHTML = '';
        const canvas = document.createElement('canvas');
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        mc2.appendChild(canvas);
        const { width: W, height: H } = setupCanvasDPI(canvas);
        const ctx = canvas.getContext('2d');
        fillBackground(ctx, W, H);
        
        // VWAP
        ctx.strokeStyle = COLORS.purple;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(10, 20);
        ctx.bezierCurveTo(W/3, 10, 2*W/3, H - 15, W - 10, H - 25);
        ctx.stroke();
        
        // Price
        ctx.strokeStyle = COLORS.yellow;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(10, 10);
        ctx.lineTo(35, 15);
        ctx.lineTo(W - 45, H - 10); // below VWAP
        ctx.stroke();
        
        // glow dot
        ctx.fillStyle = COLORS.yellow;
        ctx.beginPath(); ctx.arc(W - 45, H - 10, 3, 0, Math.PI*2); ctx.fill();
    }

    // Mini Chart 3
    const mc3 = document.getElementById('miniChart3');
    if (mc3) {
        mc3.innerHTML = '';
        const canvas = document.createElement('canvas');
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        mc3.appendChild(canvas);
        const { width: W, height: H } = setupCanvasDPI(canvas);
        const ctx = canvas.getContext('2d');
        fillBackground(ctx, W, H);
        
        ctx.strokeStyle = COLORS.green;
        ctx.lineWidth = 2.5;
        ctx.shadowColor = COLORS.greenGlow;
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.moveTo(10, H - 15);
        ctx.lineTo(W/3, H - 25);
        ctx.lineTo(2*W/3, 20);
        ctx.lineTo(W - 10, 10);
        ctx.stroke();
        ctx.shadowBlur = 0;
        
        // VWAP below
        ctx.strokeStyle = COLORS.purple;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(10, H - 8);
        ctx.lineTo(W - 10, H/2 + 10);
        ctx.stroke();
    }

    // Mini Chart 4
    const mc4 = document.getElementById('miniChart4');
    if (mc4) {
        mc4.innerHTML = '';
        const canvas = document.createElement('canvas');
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        mc4.appendChild(canvas);
        const { width: W, height: H } = setupCanvasDPI(canvas);
        const ctx = canvas.getContext('2d');
        fillBackground(ctx, W, H);
        
        // Pre-halt
        ctx.strokeStyle = COLORS.green;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(10, H - 10);
        ctx.lineTo(W/3 - 10, H/2 - 10);
        ctx.stroke();
        
        // Halt block
        ctx.fillStyle = 'rgba(255, 94, 0, 0.15)';
        ctx.fillRect(W/3 - 5, 5, 20, H - 10);
        
        // Post-halt
        ctx.strokeStyle = COLORS.green;
        ctx.beginPath();
        ctx.moveTo(W/3 + 20, H/3);
        ctx.lineTo(W - 10, 10);
        ctx.stroke();
    }
}

// Numpy-like linspace helper
function np_linspace(start, end, num) {
    const arr = [];
    const step = (end - start) / (num - 1);
    for (let i = 0; i < num; i++) {
        arr.push(start + step * i);
    }
    return arr;
}

// ==========================================================================
// INITIALIZATION
// ==========================================================================
function init() {
    drawChart1();
    drawChart2();
    drawChart3();
    drawChart4();
    drawMiniCharts();
    
    // Setup scroll observer for dynamic section fade-ins
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.strategy-section, .infographic-section').forEach(el => {
        observer.observe(el);
    });

    // Handle Window Resize (redraw charts)
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            drawChart1();
            drawChart2();
            drawChart3();
            drawChart4();
            drawMiniCharts();
        }, 250);
    });
}

// Listen to page load
window.addEventListener('DOMContentLoaded', () => {
    // Wait slightly for fonts to load so labels render nicely
    setTimeout(init, 250);
});
