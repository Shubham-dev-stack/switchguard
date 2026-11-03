/**
 * 3D Holographic Wireframe Globe
 * Uses Three.js to render a rotating cyber globe in the Global Protection widget
 */

(function () {
  let scene, camera, renderer, globeGroup;
  let animId;

  function initGlobe() {
    const container = document.getElementById('globe-canvas-container');
    if (!container) return;

    const size = container.clientWidth || 120;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.z = 4.2;

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(size, size);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    globeGroup = new THREE.Group();

    // 1. Wireframe sphere
    const sphereGeo = new THREE.SphereGeometry(1.4, 18, 14);
    const sphereMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.35
    });
    const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
    globeGroup.add(sphereMesh);

    // 2. Inner glow core
    const coreGeo = new THREE.SphereGeometry(1.25, 16, 16);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x0b192c,
      transparent: true,
      opacity: 0.85
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    globeGroup.add(coreMesh);

    // 3. Glowing orbital rings
    const ringGeo = new THREE.RingGeometry(1.6, 1.65, 32);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00ff9d,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.4
    });
    const ringMesh = new THREE.Mesh(ringGeo, ringMat);
    ringMesh.rotation.x = Math.PI / 2.5;
    globeGroup.add(ringMesh);

    // 4. City marker beacons (dots on globe)
    const markerCoords = [
      { lat: 37, lon: -122 }, // SF
      { lat: 51, lon: 0 },    // London
      { lat: 19, lon: 72 },   // Mumbai
      { lat: 35, lon: 139 },  // Tokyo
      { lat: -33, lon: 151 }  // Sydney
    ];

    markerCoords.forEach(c => {
      const phi = (90 - c.lat) * (Math.PI / 180);
      const theta = (c.lon + 180) * (Math.PI / 180);
      const x = -(1.42 * Math.sin(phi) * Math.cos(theta));
      const z = 1.42 * Math.sin(phi) * Math.sin(theta);
      const y = 1.42 * Math.cos(phi);

      const dotGeo = new THREE.SphereGeometry(0.05, 8, 8);
      const dotMat = new THREE.MeshBasicMaterial({ color: 0x00ff9d });
      const dot = new THREE.Mesh(dotGeo, dotMat);
      dot.position.set(x, y, z);
      globeGroup.add(dot);
    });

    scene.add(globeGroup);

    animate();
  }

  function animate() {
    animId = requestAnimationFrame(animate);
    if (globeGroup) {
      globeGroup.rotation.y += 0.008;
      globeGroup.rotation.x = 0.2;
    }
    renderer.render(scene, camera);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlobe);
  } else {
    initGlobe();
  }
})();
