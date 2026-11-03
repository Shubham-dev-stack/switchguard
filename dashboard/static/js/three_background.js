/**
 * SwitchGuard 3D Cyber Constellation & Perspective Grid
 * Pure Canvas Vector Math (Zero external CDN latency, 120 FPS hardware accelerated)
 */

(function () {
  const canvas = document.getElementById('space-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  // Mouse Parallax coordinates
  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;

  window.addEventListener('mousemove', (e) => {
    targetX = (e.clientX - width / 2) * 0.05;
    targetY = (e.clientY - height / 2) * 0.05;
  });

  // 3D Particles
  const PARTICLE_COUNT = 140;
  const particles = [];

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
      x: (Math.random() - 0.5) * width * 1.5,
      y: (Math.random() - 0.5) * height * 1.5,
      z: Math.random() * 1000 + 100,
      baseRadius: Math.random() * 1.5 + 0.5,
      alpha: Math.random() * 0.7 + 0.3,
      color: Math.random() > 0.8 ? '#00F0FF' : (Math.random() > 0.9 ? '#8B5CF6' : '#FFFFFF')
    });
  }

  // Animation Loop
  let frame = 0;
  function render() {
    frame++;
    // Smooth lerp for mouse parallax
    mouseX += (targetX - mouseX) * 0.05;
    mouseY += (targetY - mouseY) * 0.05;

    ctx.fillStyle = '#06080F';
    ctx.fillRect(0, 0, width, height);

    // 1. Draw Subtle 3D Perspective Floor Grid
    const fov = 400;
    const horizon = height * 0.65 + mouseY * 0.5;

    ctx.save();
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.07)';
    ctx.lineWidth = 1;

    // Vanishing perspective lines
    const gridCols = 16;
    for (let i = -gridCols; i <= gridCols; i++) {
      const startX = width / 2 + mouseX * 2;
      const endX = width / 2 + (i * width) / 10 + mouseX * 6;
      ctx.beginPath();
      ctx.moveTo(startX, horizon);
      ctx.lineTo(endX, height);
      ctx.stroke();
    }

    // Horizontal depth lines
    const depthSteps = 10;
    for (let j = 1; j <= depthSteps; j++) {
      const t = j / depthSteps;
      const y = horizon + (height - horizon) * Math.pow(t, 2.5);
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    ctx.restore();

    // 2. Draw Floating 3D Star Constellation
    ctx.save();
    for (let p of particles) {
      // Move particle forward in Z space
      p.z -= 0.6;
      if (p.z <= 10) {
        p.z = 1000;
        p.x = (Math.random() - 0.5) * width * 1.5;
        p.y = (Math.random() - 0.5) * height * 1.5;
      }

      // 3D Perspective Projection
      const scale = fov / (p.z + fov);
      const projX = (p.x - mouseX * 4) * scale + width / 2;
      const projY = (p.y - mouseY * 4) * scale + height / 2;
      const radius = p.baseRadius * scale * 1.8;

      if (projX >= 0 && projX <= width && projY >= 0 && projY <= height) {
        ctx.beginPath();
        ctx.arc(projX, projY, Math.max(0.2, radius), 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha * Math.min(1, (1000 - p.z) / 400);
        ctx.fill();
      }
    }
    ctx.restore();

    requestAnimationFrame(render);
  }

  render();
})();
