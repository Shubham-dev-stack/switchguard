/**
 * Multi-Tab Command Console: Discord War Room, Sentry Trace, Git Diff & Audit Ledger
 */

(function () {
  let activeTab = 'discord';
  let isSimulating = false;

  function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-tab');
        switchTab(target);
      });
    });
  }

  window.switchTab = function (tabId) {
    activeTab = tabId;
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
    });
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.toggle('active', content.id === `tab-${tabId}`);
    });
    if (window.playAudioTone) window.playAudioTone(700, 'sine', 0.05, 0.04);
  };

  window.runInteractiveSimulation = function () {
    if (isSimulating) return;
    isSimulating = true;

    // Switch to discord tab
    window.switchTab('discord');

    // 1. Trigger Alarm & Outage State
    if (window.playAlarmSound) window.playAlarmSound();
    if (window.trigger3DOutage) window.trigger3DOutage();
    if (window.setSparklineOutage) window.setSparklineOutage();

    // Update KPI values to Outage Mode
    const pill = document.getElementById('status-pill');
    const pillText = document.getElementById('status-pill-text');
    if (pill && pillText) {
      pill.className = 'status-pill outage-active';
      pillText.textContent = '🔴 P0 OUTAGE ACTIVE';
    }

    const errElem = document.getElementById('metric-error-rate');
    if (errElem) {
      errElem.textContent = '100.0%';
      errElem.style.color = 'var(--red-plasma)';
    }

    const finElem = document.getElementById('metric-financial-risk');
    if (finElem) {
      finElem.textContent = '$450,000.00 USD';
      finElem.style.color = 'var(--red-plasma)';
    }

    const triggerBtn = document.getElementById('trigger-chaos-btn');
    if (triggerBtn) {
      triggerBtn.disabled = true;
      triggerBtn.classList.add('running');
      triggerBtn.innerHTML = '<span>⚡ Auto-Healing in Progress...</span>';
    }

    // Step 1: Discord Alert Message (0.5s)
    setTimeout(() => {
      appendDiscordMessage({
        bot: true,
        author: 'SwitchGuard Commander',
        tag: 'BOT',
        avatar: '🛡️',
        embed: {
          color: 'red',
          title: '🚨 [P0 Critical] Production Incident Detected',
          service: 'checkout-service',
          description: '**Sentry Alert:** `ZeroDivisionError: float division by zero`\n**Blast Radius:** 100% of checkout traffic impacted\n**Financial Risk:** $450,000.00 USD revenue exposure\n**SLA Deadline:** MTTR countdown started (30m target)',
          time: 'Just now'
        }
      });
      if (window.playAudioTone) window.playAudioTone(440, 'triangle', 0.2, 0.1);
    }, 600);

    // Step 2: Diagnostics & Patch Proposed (2.2s)
    setTimeout(() => {
      appendDiscordMessage({
        bot: true,
        author: 'SwitchGuard Fixer',
        tag: 'BOT',
        avatar: '🛠️',
        embed: {
          color: 'amber',
          title: '🛠️ Autonomous Hotfix Synthesized & Verified',
          service: 'checkout-service',
          description: '**Root Cause:** Promotion zero-total division at line 24 of `checkout.py`.\n**Pytest Regression Suite:** 3/3 tests passed (0.10s).\n**Action Required:** Human approval gate invoked.',
          time: '1m ago',
          showApproveBtn: true
        }
      });
      if (window.playAudioTone) window.playAudioTone(587, 'sine', 0.15, 0.08);
    }, 2400);

    // Step 3: Human Approval & Deployment (4.8s)
    setTimeout(() => {
      // Simulate Shubham approving
      appendDiscordMessage({
        bot: false,
        author: 'Shubham',
        tag: 'SRE Lead',
        avatar: '👤',
        content: '**Approve** — Verified patch on staging. Deploy immediately.'
      });
      if (window.playAudioTone) window.playAudioTone(659, 'sine', 0.1, 0.05);

      // Disable approve button
      const btn = document.getElementById('inline-approve-btn');
      if (btn) {
        btn.disabled = true;
        btn.textContent = '✔ Approved by @Shubham';
        btn.style.background = 'rgba(0, 255, 157, 0.2)';
      }
    }, 4500);

    // Step 4: Resolution & Chime (6.2s)
    setTimeout(() => {
      appendDiscordMessage({
        bot: true,
        author: 'SwitchGuard Commander',
        tag: 'BOT',
        avatar: '🛡️',
        embed: {
          color: 'green',
          title: '✅ Incident INC-502 Resolved in 2m 51s',
          service: 'checkout-service',
          description: '**Status:** Production restored. Service latency: 18.4ms.\n**Audit Ledger:** Block #4 cryptographically sealed (SHA-256).\n**Blameless Postmortem:** Compiled and available in 1-click.',
          time: 'Just now'
        }
      });

      // Recover 3D, sparklines, and KPIs
      if (window.resolve3DOutage) window.resolve3DOutage();
      if (window.setSparklineRecovered) window.setSparklineRecovered();
      if (window.playSuccessChime) window.playSuccessChime();

      if (pill && pillText) {
        pill.className = 'status-pill resolved-clean';
        pillText.textContent = '🟢 ALL SYSTEMS OPERATIONAL';
      }

      if (errElem) {
        errElem.textContent = '0.0%';
        errElem.style.color = 'var(--green-emerald)';
      }

      if (finElem) {
        finElem.textContent = '$0.00 USD';
        finElem.style.color = 'var(--text-primary)';
      }

      if (triggerBtn) {
        triggerBtn.disabled = false;
        triggerBtn.classList.remove('running');
        triggerBtn.innerHTML = '<span>⚡ Trigger Chaos Outage</span>';
      }

      isSimulating = false;
    }, 6200);
  };

  function appendDiscordMessage(msg) {
    const stream = document.getElementById('discord-message-stream');
    if (!stream) return;

    const row = document.createElement('div');
    row.className = 'discord-msg-row';

    let html = `
      <div class="discord-avatar">${msg.avatar}</div>
      <div class="discord-content">
        <div class="discord-header">
          <span class="discord-author">${msg.author}</span>
          ${msg.tag ? `<span class="discord-tag">${msg.tag}</span>` : ''}
          <span class="discord-timestamp">Today at ${new Date().toLocaleTimeString()}</span>
        </div>
    `;

    if (msg.content) {
      html += `<div class="discord-body">${msg.content}</div>`;
    }

    if (msg.embed) {
      html += `
        <div class="discord-embed embed-${msg.embed.color}">
          <div class="embed-title">${msg.embed.title}</div>
          <div class="embed-desc">${msg.embed.description.replace(/\n/g, '<br/>')}</div>
          ${msg.embed.showApproveBtn ? `
            <div class="embed-actions">
              <button class="discord-action-btn" id="inline-approve-btn" onclick="this.disabled=true; this.textContent='✔ Approved';">
                ✔ Approve & Deploy Hotfix
              </button>
            </div>
          ` : ''}
        </div>
      `;
    }

    html += `</div>`;
    row.innerHTML = html;
    stream.appendChild(row);

    // Scroll to bottom
    stream.scrollTop = stream.scrollHeight;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTabs);
  } else {
    initTabs();
  }
})();
