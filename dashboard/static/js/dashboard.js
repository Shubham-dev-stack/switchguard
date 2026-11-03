/**
 * SwitchGuard CyberDeck Dashboard Logic & Web Audio Synthesizer
 */

(function () {
  // Web Audio API Synthesizer (Zero external sound files needed!)
  let audioCtx = null;
  let soundEnabled = true;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();
    }
  }

  function playTone(freq, type = 'sine', duration = 0.12, volume = 0.1) {
    if (!soundEnabled) return;
    try {
      initAudio();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(volume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  function playAlertAlarm() {
    playTone(880, 'sawtooth', 0.18, 0.15);
    setTimeout(() => playTone(587, 'sawtooth', 0.22, 0.12), 150);
  }

  function playSuccessChime() {
    playTone(523.25, 'sine', 0.15, 0.08); // C5
    setTimeout(() => playTone(659.25, 'sine', 0.15, 0.08), 100); // E5
    setTimeout(() => playTone(783.99, 'sine', 0.25, 0.1), 200);  // G5
  }

  // Audio Toggle Button
  const audioBtn = document.getElementById('audio-toggle-btn');
  if (audioBtn) {
    audioBtn.addEventListener('click', () => {
      soundEnabled = !soundEnabled;
      audioBtn.style.color = soundEnabled ? 'var(--cyan-primary)' : 'var(--text-muted)';
      if (soundEnabled) playTone(440, 'sine', 0.1);
    });
  }

  // Terminal Streamer
  const terminalLogs = document.getElementById('terminal-logs');
  function addLog(text, type = 'info') {
    if (!terminalLogs) return;
    const now = new Date();
    const tStr = now.toISOString().substring(11, 19) + ' UTC';
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.innerHTML = `<span class="timestamp">[${tStr}]</span> ${text}`;
    terminalLogs.appendChild(entry);
    terminalLogs.scrollTop = terminalLogs.scrollHeight;
    playTone(1200, 'sine', 0.03, 0.02);
  }

  // Interactive Chaos Simulation Runner
  let isResolving = false;
  const chaosBtn = document.getElementById('trigger-chaos-btn');
  const statusPill = document.getElementById('status-pill');
  const statusPillText = document.getElementById('status-pill-text');
  const errorRateEl = document.getElementById('metric-error-rate');
  const financialRiskEl = document.getElementById('metric-financial-risk');
  const mttrEl = document.getElementById('metric-mttr');

  function simulateIncident() {
    if (isResolving) return;
    isResolving = true;

    // Phase 1: Trigger Outage
    playAlertAlarm();
    window.SwitchGuardTopology.setIncidentState(true);
    statusPill.className = 'status-pill active-p0';
    statusPillText.textContent = '🚨 P0 OUTAGE: checkout-service';
    errorRateEl.textContent = '100.0%';
    errorRateEl.style.color = 'var(--red-plasma)';
    financialRiskEl.textContent = '$45,000 USD';

    terminalLogs.innerHTML = '';
    addLog('🚨 [P0 ALERT] Sentry Telemetry: ZeroDivisionError detected on checkout-service', 'err');
    addLog('📊 Blast Radius Triage: 100% promo orders failing. Tier-1 service impacted.', 'warn');
    addLog('🛡️ SwitchGuard Commander: Opening War Room #incident-war-room in Discord', 'agent');

    // Phase 2: Agent Dispatches (after 1.5s)
    setTimeout(() => {
      addLog('🔍 SwitchGuard Investigator: Searching workspace for calculate_order_total...', 'info');
      addLog('📁 Located failing frame: demo-service/checkout.py line 24', 'agent');
      addLog('🎯 Root Cause Isolated: savings_ratio = round(subtotal / net_total, 2) when net_total == 0.0', 'err');
    }, 1500);

    // Phase 3: Patch & Regression Testing (after 3.5s)
    setTimeout(() => {
      addLog('🛠️ SwitchGuard Fixer: Synthesized guard clause -> if net_total == 0.0: savings_ratio = 1.0', 'agent');
      addLog('🧪 Executing pytest demo-service/test_checkout.py on host...', 'info');
      addLog('✅ Pytest Suite: 3 passed in 0.10s (100% green verification)', 'succ');
      addLog('⚠️ Human-in-the-Loop Gate: Awaiting confirmation from @Shubham in chat...', 'warn');
    }, 3500);

    // Phase 4: Human Signoff & Resolution (after 5.5s)
    setTimeout(() => {
      playSuccessChime();
      addLog('👤 Operator @Shubham: "Approve" granted in Discord War Room', 'agent');
      addLog('🚀 Production Hotfix Deployed & Verified. Service Latency: 18ms', 'succ');
      addLog('📑 Postmortem INC-502 automatically compiled and cryptographically sealed.', 'agent');

      // Update UI to Resolved State
      window.SwitchGuardTopology.setIncidentState(false);
      statusPill.className = 'status-pill resolved-clean';
      statusPillText.textContent = '🟢 ALL SYSTEMS OPERATIONAL';
      errorRateEl.textContent = '0.0%';
      errorRateEl.style.color = 'var(--green-emerald)';
      financialRiskEl.textContent = '$0.00 USD';
      mttrEl.textContent = '2m 51s';

      isResolving = false;
    }, 5500);
  }

  if (chaosBtn) {
    chaosBtn.addEventListener('click', simulateIncident);
  }

  // Postmortem Modal Dialog
  const postmortemBtn = document.getElementById('view-postmortem-btn');
  const postmortemModal = document.getElementById('postmortem-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  if (postmortemBtn && postmortemModal) {
    postmortemBtn.addEventListener('click', () => {
      postmortemModal.classList.add('active');
      playTone(600, 'sine', 0.08);
    });
  }

  if (modalCloseBtn && postmortemModal) {
    modalCloseBtn.addEventListener('click', () => {
      postmortemModal.classList.remove('active');
      playTone(400, 'sine', 0.08);
    });
  }

  // Close modal when clicking overlay background
  if (postmortemModal) {
    postmortemModal.addEventListener('click', (e) => {
      if (e.target === postmortemModal) {
        postmortemModal.classList.remove('active');
      }
    });
  }

  // Initial welcome logs
  addLog('🛡️ SwitchGuard CyberDeck Engine Initialized [v1.0.0]', 'info');
  addLog('📡 Listening on Switch Core PostgreSQL Message Bus (Port 49744)', 'info');
  addLog('🤖 Squad Active: Commander, Investigator, Fixer bridged to Discord', 'agent');
})();
