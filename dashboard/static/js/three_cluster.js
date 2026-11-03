/**
 * SwitchGuard 3D Holographic Microservice Cluster
 * Built with Three.js (WebGL, OrbitControls, 3D Curves, Particle Streams, Dynamic Lighting)
 * Awwwards / ThreeUI Standard
 */

(function () {
  let scene, camera, renderer, controls;
  let container, canvas;
  let nodes = {};
  let dataPackets = [];
  let curves = [];
  let shockwaveRing = null;
  let ambientLight, pointLight;
  let isOutage = false;
  let animFrameId;

  const SERVICES = [
    { id: 'checkout', name: 'checkout-service', pos: [-5, 1, 0], rps: 150, port: 8081, tier: 1 },
    { id: 'payment', name: 'payment-gateway', pos: [0, 3, 2], rps: 120, port: 8082, tier: 1 },
    { id: 'postgres', name: 'postgres-primary', pos: [5, 0, -1], rps: 450, port: 5432, tier: 1 },
    { id: 'redis', name: 'redis-cache', pos: [0, -3, -1], rps: 900, port: 6379, tier: 2 }
  ];

  const CONNECTIONS = [
    { from: 'checkout', to: 'payment' },
    { from: 'checkout', to: 'redis' },
    { from: 'payment', to: 'postgres' },
    { from: 'payment', to: 'redis' }
  ];

  function init() {
    container = document.getElementById('three-cluster-container');
    if (!container) return;

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 360;

    // 1. Scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x06080f, 0.035);

    // 2. Camera
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 4, 14);

    // 3. Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);
    canvas = renderer.domElement;

    // 4. OrbitControls
    if (typeof THREE.OrbitControls !== 'undefined') {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.enableZoom = true;
      controls.minDistance = 6;
      controls.maxDistance = 25;
      controls.maxPolarAngle = Math.PI / 2 + 0.15; // Don't go too far under floor
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.6;
    }

    // 5. Lighting
    ambientLight = new THREE.AmbientLight(0x0a192f, 2.5);
    scene.add(ambientLight);

    pointLight = new THREE.PointLight(0x00f0ff, 3.0, 50);
    pointLight.position.set(0, 6, 4);
    scene.add(pointLight);

    // 6. Subsurface Ground Grid
    const gridHelper = new THREE.GridHelper(24, 24, 0x00f0ff, 0x112233);
    gridHelper.position.y = -4;
    gridHelper.material.opacity = 0.25;
    gridHelper.material.transparent = true;
    scene.add(gridHelper);

    // 7. Core Central Gyroscope Rings
    createGyroscopeCore();

    // 8. Service Nodes & Connections
    buildServiceNodes();
    buildConnectionTunnels();
    createShockwaveRing();

    // 9. Resize listener
    window.addEventListener('resize', onWindowResize);

    // 10. Start loop
    animate();
  }

  function createGyroscopeCore() {
    const group = new THREE.Group();
    group.name = 'gyroscope';

    const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.15 });
    const ring1 = new THREE.Mesh(new THREE.TorusGeometry(3.5, 0.02, 16, 64), ringMat1);
    group.add(ring1);

    const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x8b5cf6, wireframe: true, transparent: true, opacity: 0.12 });
    const ring2 = new THREE.Mesh(new THREE.TorusGeometry(4.2, 0.02, 16, 64), ringMat2);
    ring2.rotation.x = Math.PI / 3;
    group.add(ring2);

    scene.add(group);
  }

  function buildServiceNodes() {
    SERVICES.forEach(svc => {
      const nodeGroup = new THREE.Group();
      nodeGroup.position.set(svc.pos[0], svc.pos[1], svc.pos[2]);

      // Inner glowing core
      const coreGeo = new THREE.SphereGeometry(0.55, 32, 32);
      const coreMat = new THREE.MeshStandardMaterial({
        color: 0x00f0ff,
        emissive: 0x00a8cc,
        emissiveIntensity: 0.6,
        roughness: 0.2,
        metalness: 0.8
      });
      const coreMesh = new THREE.Mesh(coreGeo, coreMat);
      nodeGroup.add(coreMesh);

      // Outer wireframe halo
      const haloGeo = new THREE.IcosahedronGeometry(0.85, 1);
      const haloMat = new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        wireframe: true,
        transparent: true,
        opacity: 0.35
      });
      const haloMesh = new THREE.Mesh(haloGeo, haloMat);
      haloMesh.name = 'halo';
      nodeGroup.add(haloMesh);

      // Orbital indicator ring
      const ringGeo = new THREE.RingGeometry(0.95, 1.05, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0x00ff9d,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.4
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.rotation.x = Math.PI / 2;
      ringMesh.name = 'ring';
      nodeGroup.add(ringMesh);

      // 2D Canvas Billboard Label
      const labelSprite = createTextSprite(svc.name, "HEALTHY • " + svc.rps + " RPS");
      labelSprite.position.set(0, 1.25, 0);
      labelSprite.name = 'label';
      nodeGroup.add(labelSprite);

      scene.add(nodeGroup);
      nodes[svc.id] = {
        group: nodeGroup,
        core: coreMesh,
        halo: haloMesh,
        ring: ringMesh,
        label: labelSprite,
        data: svc
      };
    });
  }

  function createTextSprite(title, subtitle, isError = false) {
    const canvas = document.createElement('canvas');
    canvas.width = 300;
    canvas.height = 80;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = isError ? 'rgba(255, 0, 85, 0.85)' : 'rgba(10, 18, 32, 0.85)';
    ctx.strokeStyle = isError ? '#ff0055' : 'rgba(0, 240, 255, 0.5)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(4, 4, 292, 72, 8);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 22px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.fillText(title, 150, 34);

    ctx.font = '14px "JetBrains Mono", monospace';
    ctx.fillStyle = isError ? '#ffccd5' : '#00ff9d';
    ctx.fillText(subtitle, 150, 60);

    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(spriteMat);
    sprite.scale.set(2.8, 0.75, 1);
    return sprite;
  }

  function buildConnectionTunnels() {
    CONNECTIONS.forEach(conn => {
      const fromNode = nodes[conn.from].group.position;
      const toNode = nodes[conn.to].group.position;

      // Arc curve in 3D
      const mid = new THREE.Vector3().addVectors(fromNode, toNode).multiplyScalar(0.5);
      mid.y += 0.8; // subtle curve arc upward

      const curve = new THREE.CatmullRomCurve3([fromNode, mid, toNode]);
      curves.push(curve);

      // Line geometry
      const points = curve.getPoints(50);
      const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
      const lineMat = new THREE.LineBasicMaterial({
        color: 0x00f0ff,
        transparent: true,
        opacity: 0.22,
        linewidth: 1
      });
      const line = new THREE.Line(lineGeo, lineMat);
      scene.add(line);

      // Add animated packets along curve
      for (let i = 0; i < 3; i++) {
        const pGeo = new THREE.SphereGeometry(0.08, 12, 12);
        const pMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff });
        const packet = new THREE.Mesh(pGeo, pMat);
        scene.add(packet);
        dataPackets.push({
          mesh: packet,
          curve: curve,
          progress: i * 0.33,
          speed: 0.004 + Math.random() * 0.003
        });
      }
    });
  }

  function createShockwaveRing() {
    const geo = new THREE.RingGeometry(0.5, 0.7, 32);
    const mat = new THREE.MeshBasicMaterial({
      color: 0xff0055,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.0
    });
    shockwaveRing = new THREE.Mesh(geo, mat);
    shockwaveRing.rotation.x = Math.PI / 2;
    scene.add(shockwaveRing);
  }

  function onWindowResize() {
    if (!container || !renderer || !camera) return;
    const width = container.clientWidth;
    const height = container.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }

  function animate(timestamp) {
    animFrameId = requestAnimationFrame(animate);

    const time = timestamp ? timestamp * 0.001 : 0;

    // Rotate controls
    if (controls) controls.update();

    // Rotate core gyroscope
    const gyro = scene.getObjectByName('gyroscope');
    if (gyro) {
      gyro.rotation.y = time * 0.15;
      gyro.rotation.x = Math.sin(time * 0.1) * 0.1;
    }

    // Animate nodes halos & rings
    Object.values(nodes).forEach(n => {
      n.halo.rotation.y = time * 0.4;
      n.halo.rotation.x = time * 0.3;
      n.ring.rotation.z = -time * 0.5;
    });

    // Animate data laser packets
    dataPackets.forEach(p => {
      p.progress += p.speed;
      if (p.progress > 1) p.progress = 0;
      const pos = p.curve.getPointAt(p.progress);
      p.mesh.position.copy(pos);
      p.mesh.material.color.setHex(isOutage ? 0xff0055 : 0x00f0ff);
    });

    // Outage shockwave pulse
    if (isOutage && shockwaveRing) {
      shockwaveRing.position.copy(nodes['checkout'].group.position);
      const pulse = (time * 2.5) % 1;
      shockwaveRing.scale.set(1 + pulse * 4.5, 1 + pulse * 4.5, 1);
      shockwaveRing.material.opacity = (1 - pulse) * 0.8;
    } else if (shockwaveRing) {
      shockwaveRing.material.opacity = 0;
    }

    renderer.render(scene, camera);
  }

  // Public Event Hooks
  window.trigger3DOutage = function () {
    isOutage = true;
    if (ambientLight) ambientLight.color.setHex(0x330a15);
    if (pointLight) pointLight.color.setHex(0xff0055);

    // Turn checkout red
    const checkout = nodes['checkout'];
    if (checkout) {
      checkout.core.material.color.setHex(0xff0055);
      checkout.core.material.emissive.setHex(0xff0033);
      checkout.halo.material.color.setHex(0xff0055);
      checkout.ring.material.color.setHex(0xff0055);

      // Replace label
      checkout.group.remove(checkout.label);
      checkout.label = createTextSprite('checkout-service', 'CRITICAL • 100% ERROR', true);
      checkout.label.position.set(0, 1.25, 0);
      checkout.group.add(checkout.label);
    }
  };

  window.resolve3DOutage = function () {
    isOutage = false;
    if (ambientLight) ambientLight.color.setHex(0x0a192f);
    if (pointLight) pointLight.color.setHex(0x00ff9d);

    const checkout = nodes['checkout'];
    if (checkout) {
      checkout.core.material.color.setHex(0x00ff9d);
      checkout.core.material.emissive.setHex(0x00b870);
      checkout.halo.material.color.setHex(0x00ff9d);
      checkout.ring.material.color.setHex(0x00ff9d);

      checkout.group.remove(checkout.label);
      checkout.label = createTextSprite('checkout-service', 'RESTORED • 18ms', false);
      checkout.label.position.set(0, 1.25, 0);
      checkout.group.add(checkout.label);
    }
  };

  window.reset3DNodes = function () {
    isOutage = false;
    if (ambientLight) ambientLight.color.setHex(0x0a192f);
    if (pointLight) pointLight.color.setHex(0x00f0ff);

    Object.values(nodes).forEach(n => {
      n.core.material.color.setHex(0x00f0ff);
      n.core.material.emissive.setHex(0x00a8cc);
      n.halo.material.color.setHex(0x00f0ff);
      n.ring.material.color.setHex(0x00ff9d);

      n.group.remove(n.label);
      n.label = createTextSprite(n.data.name, 'HEALTHY • ' + n.data.rps + ' RPS', false);
      n.label.position.set(0, 1.25, 0);
      n.group.add(n.label);
    });
  };

  // Auto-init on DOM loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
