/**
 * SwitchGuard Interactive Microservice Topology Canvas
 * Visualizes service mesh status, dependency links, and real-time failure cascades.
 */

window.SwitchGuardTopology = (function () {
  const canvas = document.getElementById('topology-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width, height;
  function resize() {
    width = canvas.width = canvas.parentElement.clientWidth;
    height = canvas.height = canvas.parentElement.clientHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  // Topology Nodes
  const nodes = [
    { id: 'checkout', label: 'checkout-service', x: 0.22, y: 0.5, status: 'unhealthy', rps: 150, tier: 1 },
    { id: 'payment', label: 'payment-gateway', x: 0.50, y: 0.28, status: 'healthy', rps: 120, tier: 1 },
    { id: 'db', label: 'postgres-primary', x: 0.78, y: 0.35, status: 'healthy', rps: 450, tier: 1 },
    { id: 'redis', label: 'redis-cache', x: 0.58, y: 0.75, status: 'healthy', rps: 900, tier: 2 }
  ];

  // Dependency Connections
  const links = [
    { from: 'checkout', to: 'payment' },
    { from: 'checkout', to: 'redis' },
    { from: 'payment', to: 'db' }
  ];

  // Animated Data Packets
  const packets = [];
  for (let i = 0; i < 8; i++) {
    packets.push({
      linkIndex: i % links.length,
      progress: Math.random(),
      speed: 0.006 + Math.random() * 0.004
    });
  }

  let isOutage = true; // Initial demo state: P0 Outage active

  function setIncidentState(outageActive) {
    isOutage = outageActive;
    const checkoutNode = nodes.find(n => n.id === 'checkout');
    if (checkoutNode) {
      checkoutNode.status = outageActive ? 'unhealthy' : 'healthy';
    }
  }

  let tick = 0;
  function render() {
    tick++;
    ctx.clearRect(0, 0, width, height);

    // 1. Draw Links & Animated Packets
    links.forEach((link, idx) => {
      const fromNode = nodes.find(n => n.id === link.from);
      const toNode = nodes.find(n => n.id === link.to);

      const x1 = fromNode.x * width;
      const y1 = fromNode.y * height;
      const x2 = toNode.x * width;
      const y2 = toNode.y * height;

      // Draw connection line
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = isOutage && link.from === 'checkout'
        ? 'rgba(255, 0, 85, 0.3)'
        : 'rgba(56, 189, 248, 0.2)';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 6]);
      ctx.lineDashOffset = -tick * 0.5;
      ctx.stroke();
      ctx.setLineDash([]);
    });

    // 2. Draw Moving Data Laser Packets
    packets.forEach(pkt => {
      pkt.progress += pkt.speed;
      if (pkt.progress >= 1) pkt.progress = 0;

      const link = links[pkt.linkIndex];
      const fromNode = nodes.find(n => n.id === link.from);
      const toNode = nodes.find(n => n.id === link.to);

      const px = fromNode.x * width + (toNode.x * width - fromNode.x * width) * pkt.progress;
      const py = fromNode.y * height + (toNode.y * height - fromNode.y * height) * pkt.progress;

      ctx.beginPath();
      ctx.arc(px, py, 3, 0, Math.PI * 2);
      ctx.fillStyle = isOutage && link.from === 'checkout' ? '#FF0055' : '#00F0FF';
      ctx.shadowBlur = 10;
      ctx.shadowColor = ctx.fillStyle;
      ctx.fill();
      ctx.shadowBlur = 0;
    });

    // 3. Draw Service Nodes
    nodes.forEach(node => {
      const nx = node.x * width;
      const ny = node.y * height;
      const isRed = node.status === 'unhealthy';
      const nodeColor = isRed ? '#FF0055' : '#00FF9D';
      const glowColor = isRed ? 'rgba(255, 0, 85, 0.5)' : 'rgba(0, 255, 157, 0.4)';

      // Pulsating Outer Halo
      const pulseSize = 18 + Math.sin(tick * 0.08) * 4;
      ctx.beginPath();
      ctx.arc(nx, ny, pulseSize + 6, 0, Math.PI * 2);
      ctx.fillStyle = glowColor;
      ctx.globalAlpha = 0.25;
      ctx.fill();
      ctx.globalAlpha = 1.0;

      // Inner Core Circle
      ctx.beginPath();
      ctx.arc(nx, ny, 16, 0, Math.PI * 2);
      ctx.fillStyle = '#0D1117';
      ctx.strokeStyle = nodeColor;
      ctx.lineWidth = 2.5;
      ctx.shadowBlur = 14;
      ctx.shadowColor = nodeColor;
      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Status Indicator Dot
      ctx.beginPath();
      ctx.arc(nx, ny, 5, 0, Math.PI * 2);
      ctx.fillStyle = nodeColor;
      ctx.fill();

      // Service Label & Metrics
      ctx.fillStyle = '#FFFFFF';
      ctx.font = '600 12px Plus Jakarta Sans, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(node.label, nx, ny + 32);

      ctx.fillStyle = isRed ? '#FF7B72' : '#7EE787';
      ctx.font = '10px Fira Code, monospace';
      ctx.fillText(isRed ? '500 ERROR (100%)' : `${node.rps} RPS • HEALTHY`, nx, ny + 46);
    });

    requestAnimationFrame(render);
  }

  render();

  return {
    setIncidentState
  };
})();
