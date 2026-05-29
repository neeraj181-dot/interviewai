/* =============================================
   InterviewAI Premium — main.js v2.0
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initAlerts();
  initCounters();
  initProgressBars();
  initTyping();
  initTimer();
  initParticles();
  initAvatarUpload();
  initSearchFilter();
  initTheme();
});

/* ── Sidebar ── */
function initSidebar() {
  const btn = document.getElementById('hamburger');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (!btn || !sidebar) return;
  btn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
  });
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  });
}

/* ── Auto-dismiss alerts ── */
function initAlerts() {
  document.querySelectorAll('.alert-neon').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s, transform 0.5s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-8px)';
      setTimeout(() => el.remove(), 500);
    }, 4500);
  });
}

/* ── Animated counters ── */
function initCounters() {
  const els = document.querySelectorAll('[data-count]');
  if (!els.length) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseFloat(el.getAttribute('data-count'));
      const suffix = el.getAttribute('data-suffix') || '';
      const isFloat = String(target).includes('.');
      const duration = 1200;
      const start = performance.now();
      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const val = target * ease;
        el.textContent = (isFloat ? val.toFixed(1) : Math.floor(val)) + suffix;
        if (progress < 1) requestAnimationFrame(tick);
        else el.textContent = (isFloat ? target.toFixed(1) : target) + suffix;
      }
      requestAnimationFrame(tick);
      observer.unobserve(el);
    });
  }, { threshold: 0.3 });
  els.forEach(el => observer.observe(el));
}

/* ── Progress bars ── */
function initProgressBars() {
  document.querySelectorAll('.progress-fill[data-width]').forEach(bar => {
    const target = bar.getAttribute('data-width');
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = target; }, 300);
  });
  document.querySelectorAll('.xp-bar-fill[data-width]').forEach(bar => {
    const target = bar.getAttribute('data-width');
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = target; }, 500);
  });
}

/* ── Typing effect ── */
function initTyping() {
  const el = document.getElementById('typingText');
  if (!el) return;
  const texts = ['Python Developer', 'Django Engineer', 'Web Developer', 'Full Stack Dev', 'Software Engineer'];
  let ti = 0, ci = 0, deleting = false;
  function tick() {
    const cur = texts[ti];
    el.textContent = deleting ? cur.slice(0, ci - 1) : cur.slice(0, ci + 1);
    deleting ? ci-- : ci++;
    if (!deleting && ci === cur.length) { deleting = true; setTimeout(tick, 1600); return; }
    if (deleting && ci === 0) { deleting = false; ti = (ti + 1) % texts.length; }
    setTimeout(tick, deleting ? 55 : 95);
  }
  tick();
}

/* ── Interview timer ── */
function initTimer() {
  const el = document.getElementById('interviewTimer');
  if (!el) return;
  let secs = parseInt(el.getAttribute('data-start') || '0');
  const limit = parseInt(el.getAttribute('data-limit') || '0');
  setInterval(() => {
    secs++;
    const m = String(Math.floor(secs / 60)).padStart(2, '0');
    const s = String(secs % 60).padStart(2, '0');
    el.textContent = `${m}:${s}`;
    if (limit > 0) {
      const remaining = limit - secs;
      el.classList.toggle('warning', remaining <= 120 && remaining > 60);
      el.classList.toggle('danger', remaining <= 60);
    }
  }, 1000);
}

/* ── Particle canvas ── */
function initParticles() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; };
  resize();
  window.addEventListener('resize', resize);
  const N = 55;
  const pts = Array.from({ length: N }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    r: Math.random() * 1.8 + 0.4,
    a: Math.random() * 0.35 + 0.08,
  }));
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pts.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width)  p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,212,255,${p.a})`;
      ctx.fill();
    });
    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 110) {
          ctx.beginPath();
          ctx.moveTo(pts[i].x, pts[i].y);
          ctx.lineTo(pts[j].x, pts[j].y);
          ctx.strokeStyle = `rgba(0,212,255,${0.07 * (1 - d / 110)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
}

/* ── Avatar drag-and-drop upload ── */
function initAvatarUpload() {
  const zone = document.getElementById('avatarZone');
  const input = document.getElementById('avatarInput');
  const preview = document.getElementById('avatarPreview');
  if (!zone || !input) return;

  zone.addEventListener('click', () => input.click());
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      input.files = e.dataTransfer.files;
      showPreview(file);
    }
  });
  input.addEventListener('change', () => {
    if (input.files[0]) showPreview(input.files[0]);
  });

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = e => {
      if (preview) {
        preview.innerHTML = `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`;
      }
    };
    reader.readAsDataURL(file);
  }
}

/* ── History search filter ── */
function initSearchFilter() {
  const input = document.getElementById('historySearch');
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    document.querySelectorAll('.history-row[data-cat]').forEach(row => {
      row.style.display = row.getAttribute('data-cat').toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

/* ── Theme accent ── */
function initTheme() {
  const accent = document.body.getAttribute('data-accent');
  if (accent && accent !== '#00d4ff') {
    document.documentElement.style.setProperty('--cyan', accent);
    document.documentElement.style.setProperty('--cyan-dim', accent + '26');
    document.documentElement.style.setProperty('--cyan-glow', accent + '66');
    document.documentElement.style.setProperty('--border', accent + '1f');
    document.documentElement.style.setProperty('--border-hover', accent + '59');
    document.documentElement.style.setProperty('--glass', accent + '0a');
  }
}

/* ── Confetti celebration ── */
function launchConfetti() {
  const colors = ['#00d4ff','#00ff88','#ff6b9d','#ffd700','#7b68ee'];
  for (let i = 0; i < 80; i++) {
    const el = document.createElement('div');
    el.className = 'confetti-piece';
    el.style.cssText = `
      left: ${Math.random() * 100}vw;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      width: ${Math.random() * 8 + 4}px;
      height: ${Math.random() * 8 + 4}px;
      border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
      animation-duration: ${Math.random() * 2 + 2}s;
      animation-delay: ${Math.random() * 1}s;
    `;
    document.body.appendChild(el);
    el.addEventListener('animationend', () => el.remove());
  }
}

/* ── Level select modal ── */
function openLevelModal(slug, name, color) {
  const modal = document.getElementById('levelModal');
  if (!modal) return;
  modal.querySelector('.modal-cat-name').textContent = name;
  modal.querySelectorAll('.level-btn').forEach(btn => {
    btn.onclick = () => {
      window.location.href = `/interview/start/${slug}/?difficulty=${btn.getAttribute('data-level')}`;
    };
  });
  modal.style.display = 'flex';
  setTimeout(() => modal.classList.add('open'), 10);
}
function closeLevelModal() {
  const modal = document.getElementById('levelModal');
  if (!modal) return;
  modal.classList.remove('open');
  setTimeout(() => { modal.style.display = 'none'; }, 300);
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLevelModal(); });
