/**
 * Procedural Web Audio API Synthesizer & Equalizer Visualizer
 * Zero external audio files required
 */

(function () {
  let audioCtx = null;
  let isMuted = false;

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  window.playAudioTone = function (freq, type = 'sine', duration = 0.15, volume = 0.1) {
    if (isMuted) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, ctx.currentTime);

      gain.gain.setValueAtTime(volume, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  };

  window.playAlarmSound = function () {
    if (isMuted) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      // Urgent cyber siren: 880Hz -> 440Hz -> 880Hz
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      osc.frequency.linearRampToValueAtTime(440, ctx.currentTime + 0.15);
      osc.frequency.linearRampToValueAtTime(880, ctx.currentTime + 0.3);

      gain.gain.setValueAtTime(0.12, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.45);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.45);
    } catch (e) {}
  };

  window.playSuccessChime = function () {
    if (isMuted) return;
    // Major triad: C5 (523Hz), E5 (659Hz), G5 (784Hz)
    [523.25, 659.25, 783.99].forEach((freq, idx) => {
      setTimeout(() => {
        window.playAudioTone(freq, 'sine', 0.4, 0.08);
      }, idx * 120);
    });
  };

  window.toggleAudioMute = function () {
    isMuted = !isMuted;
    const btn = document.getElementById('audio-toggle-btn');
    if (btn) {
      btn.classList.toggle('muted', isMuted);
    }
    return isMuted;
  };
})();
