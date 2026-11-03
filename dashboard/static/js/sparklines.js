/**
 * Real-time SVG & Canvas Sparklines with Bezier Splines and Gradient Fill
 * Awwwards / Linear Telemetry Standard
 */

(function () {
  const sparklines = {};

  function initSparklines() {
    const configs = [
      { id: 'mtta-sparkline', color: '#00f0ff', points: [12, 11, 13, 12, 12, 11, 12, 12, 11, 12] },
      { id: 'mttr-sparkline', color: '#00ff9d', points: [171, 165, 172, 169, 171, 170, 168, 171] },
      { id: 'error-rate-sparkline', color: '#00ff9d', points: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], isDynamic: true },
      { id: 'financial-risk-sparkline', color: '#ffb800', points: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], isDynamic: true }
    ];

    configs.forEach(cfg => {
      const canvas = document.getElementById(cfg.id);
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      sparklines[cfg.id] = {
        canvas: canvas,
        ctx: ctx,
        color: cfg.color,
        data: [...cfg.points],
        maxPoints: 30,
        isDynamic: cfg.isDynamic || false
      };
      drawSparkline(sparklines[cfg.id]);
    });

    // Start subtle pulse loop for live feel
    setInterval(updateBackgroundJitter, 800);
  }

  function drawSparkline(spark) {
    const { canvas, ctx, color, data } = spark;
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    if (data.length < 2) return;

    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = (max - min) || 1;

    // Gradient fill
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, color + '55');
    grad.addColorStop(1, 'transparent');

    const step = w / (data.length - 1);

    ctx.beginPath();
    data.forEach((val, i) => {
      const x = i * step;
      const y = h - ((val - min) / range) * (h * 0.75) - (h * 0.12);
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        // Smooth quadratic curve
        const prevX = (i - 1) * step;
        const prevY = h - ((data[i - 1] - min) / range) * (h * 0.75) - (h * 0.12);
        const midX = (prevX + x) / 2;
        const midY = (prevY + y) / 2;
        ctx.quadraticCurveTo(prevX, prevY, midX, midY);
      }
    });

    const lastX = (data.length - 1) * step;
    const lastY = h - ((data[data.length - 1] - min) / range) * (h * 0.75) - (h * 0.12);
    ctx.lineTo(lastX, lastY);

    // Stroke
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = color;
    ctx.shadowBlur = 8;
    ctx.stroke();

    // Fill under curve
    ctx.lineTo(lastX, h);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.shadowBlur = 0;
    ctx.fill();

    // Pulse dot at current head
    ctx.beginPath();
    ctx.arc(lastX, lastY, 3.5, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = color;
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.shadowBlur = 0;
  }

  function updateBackgroundJitter() {
    // Subtle breathing on MTTA and MTTR
    ['mtta-sparkline', 'mttr-sparkline'].forEach(id => {
      const spark = sparklines[id];
      if (!spark) return;
      const last = spark.data[spark.data.length - 1];
      const jitter = (Math.random() - 0.5) * 0.6;
      spark.data.push(Math.max(1, last + jitter));
      if (spark.data.length > 20) spark.data.shift();
      drawSparkline(spark);
    });
  }

  window.setSparklineOutage = function () {
    const errSpark = sparklines['error-rate-sparkline'];
    if (errSpark) {
      errSpark.color = '#ff0055';
      errSpark.data = [0, 0, 5, 20, 65, 98, 100, 100, 100, 100];
      drawSparkline(errSpark);
    }

    const finSpark = sparklines['financial-risk-sparkline'];
    if (finSpark) {
      finSpark.color = '#ff0055';
      finSpark.data = [0, 0, 50000, 150000, 320000, 450000, 450000, 450000];
      drawSparkline(finSpark);
    }
  };

  window.setSparklineRecovered = function () {
    const errSpark = sparklines['error-rate-sparkline'];
    if (errSpark) {
      errSpark.color = '#00ff9d';
      errSpark.data = [100, 95, 70, 35, 10, 0, 0, 0, 0, 0];
      drawSparkline(errSpark);
    }

    const finSpark = sparklines['financial-risk-sparkline'];
    if (finSpark) {
      finSpark.color = '#00ff9d';
      finSpark.data = [450000, 400000, 250000, 90000, 0, 0, 0, 0];
      drawSparkline(finSpark);
    }
  };

  window.resetSparklines = function () {
    const errSpark = sparklines['error-rate-sparkline'];
    if (errSpark) {
      errSpark.color = '#00ff9d';
      errSpark.data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
      drawSparkline(errSpark);
    }

    const finSpark = sparklines['financial-risk-sparkline'];
    if (finSpark) {
      finSpark.color = '#ffb800';
      finSpark.data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
      drawSparkline(finSpark);
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSparklines);
  } else {
    initSparklines();
  }
})();
