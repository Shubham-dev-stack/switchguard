/**
 * Performance Overview Canvas Area Chart
 * Draws smooth cubic bezier curves with gradient fill and data points
 */

(function () {
  let canvas, ctx;
  let activeRange = '24h';

  const datasets = {
    '1h': [82, 85, 78, 88, 92, 90, 89, 94, 91, 95],
    '6h': [70, 75, 72, 80, 85, 78, 88, 91, 87, 93],
    '24h': [65, 72, 68, 79, 84, 76, 88, 92, 89, 96],
    '7d': [60, 68, 75, 70, 82, 85, 80, 89, 91, 95]
  };

  function initChart() {
    canvas = document.getElementById('perf-area-chart');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    // Time toggle buttons
    const btns = document.querySelectorAll('.time-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        btns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeRange = btn.getAttribute('data-range') || '24h';
        drawChart();
      });
    });

    window.addEventListener('resize', resizeAndDraw);
    resizeAndDraw();
  }

  function resizeAndDraw() {
    if (!canvas) return;
    const parent = canvas.parentElement;
    canvas.width = parent.clientWidth || 380;
    canvas.height = 110;
    drawChart();
  }

  function drawChart() {
    if (!ctx || !canvas) return;
    const w = canvas.width;
    const h = canvas.height;
    const data = datasets[activeRange] || datasets['24h'];

    ctx.clearRect(0, 0, w, h);

    // Subtle horizontal grid lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let y = 20; y < h; y += 30) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    const min = 50;
    const max = 100;
    const range = max - min;
    const step = w / (data.length - 1);

    // Gradient fill
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, 'rgba(0, 240, 255, 0.35)');
    grad.addColorStop(0.6, 'rgba(0, 255, 157, 0.15)');
    grad.addColorStop(1, 'transparent');

    ctx.beginPath();
    data.forEach((val, i) => {
      const x = i * step;
      const y = h - ((val - min) / range) * (h * 0.75) - 10;
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        const prevX = (i - 1) * step;
        const prevY = h - ((data[i - 1] - min) / range) * (h * 0.75) - 10;
        const midX = (prevX + x) / 2;
        const midY = (prevY + y) / 2;
        ctx.quadraticCurveTo(prevX, prevY, midX, midY);
      }
    });

    const lastX = w;
    const lastY = h - ((data[data.length - 1] - min) / range) * (h * 0.75) - 10;
    ctx.lineTo(lastX, lastY);

    // Stroke
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#00f0ff';
    ctx.shadowBlur = 8;
    ctx.stroke();

    // Fill under
    ctx.lineTo(w, h);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.shadowBlur = 0;
    ctx.fill();

    // Draw active dot at current peak
    const peakIdx = 6;
    const peakX = peakIdx * step;
    const peakY = h - ((data[peakIdx] - min) / range) * (h * 0.75) - 10;

    ctx.beginPath();
    ctx.arc(peakX, peakY, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#00ff9d';
    ctx.shadowColor = '#00ff9d';
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.shadowBlur = 0;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChart);
  } else {
    initChart();
  }
})();
