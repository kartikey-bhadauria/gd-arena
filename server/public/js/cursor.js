/**
 * GD Arena — Full-Website Cursor Interaction & Ambient Physics Engine
 * 
 * Features:
 * 1. Fluid Lerped Cursor Follower (Dot + Smooth Magnetic Ring)
 * 2. Full-Page Ambient Radial Spotlight Glow
 * 3. 3D Card Perspective Tilt & Dynamic Glare on Mouse Move
 * 4. Magnetic Attraction for Buttons, Badges, and Action Pills
 * 5. Interactive Click Wave Ripples & Soundwave Particles
 * 6. Responsive Fallback (Gracefully disables on touch / mobile devices)
 */

(function () {
  // Only activate on devices with fine pointer (mouse/trackpad)
  if (window.matchMedia('(pointer: coarse)').matches) {
    return;
  }

  // Create DOM Elements for Cursor and Ambient Glow
  const ambientGlow = document.createElement('div');
  ambientGlow.className = 'cursor-ambient-glow';
  document.body.appendChild(ambientGlow);

  const cursorDot = document.createElement('div');
  cursorDot.className = 'cursor-dot';
  document.body.appendChild(cursorDot);

  const cursorRing = document.createElement('div');
  cursorRing.className = 'cursor-ring';
  document.body.appendChild(cursorRing);

  // State
  const mouse = { x: -100, y: -100 };
  const ring = { x: -100, y: -100, targetX: -100, targetY: -100 };
  let isHovering = false;
  let isClicking = false;
  let activeHoverEl = null;

  // Track Mouse Movement
  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;

    ring.targetX = e.clientX;
    ring.targetY = e.clientY;

    // Position dot immediately
    cursorDot.style.transform = `translate3d(${mouse.x}px, ${mouse.y}px, 0)`;

    // Update full-page ambient spotlight (page coordinates)
    ambientGlow.style.setProperty('--cursor-x', `${e.clientX}px`);
    ambientGlow.style.setProperty('--cursor-y', `${e.clientY}px`);
  });

  // Mouse Down / Up Ripple Effects
  window.addEventListener('mousedown', (e) => {
    isClicking = true;
    cursorRing.classList.add('cursor-ring--clicking');
    createClickRipple(e.clientX, e.clientY);
  });

  window.addEventListener('mouseup', () => {
    isClicking = false;
    cursorRing.classList.remove('cursor-ring--clicking');
  });

  // Smooth Ring Lerp Animation Loop
  function animate() {
    // Lerp factor
    const ease = isHovering ? 0.22 : 0.15;
    ring.x += (ring.targetX - ring.x) * ease;
    ring.y += (ring.targetY - ring.y) * ease;

    const scale = isClicking ? 0.85 : isHovering ? 1.6 : 1;
    cursorRing.style.transform = `translate3d(${ring.x}px, ${ring.y}px, 0) scale(${scale})`;

    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);

  // Click Ripple Generator
  function createClickRipple(x, y) {
    const ripple = document.createElement('div');
    ripple.className = 'cursor-click-ripple';
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    document.body.appendChild(ripple);

    ripple.addEventListener('animationend', () => {
      ripple.remove();
    });
  }

  // Interactive Hover Targets detection
  function setupHoverListeners() {
    const interactiveSelectors = 'a, button, input, select, textarea, .btn-primary, .btn-secondary, .pill, .card, .card-surface, [role="button"], [tabindex="0"]';
    
    document.addEventListener('mouseover', (e) => {
      const target = e.target.closest(interactiveSelectors);
      if (target && !isHovering) {
        isHovering = true;
        activeHoverEl = target;
        cursorRing.classList.add('cursor-ring--active');
        if (target.matches('.btn-primary, .btn-secondary, button, a')) {
          cursorRing.classList.add('cursor-ring--button');
        }
      }
    });

    document.addEventListener('mouseout', (e) => {
      const target = e.target.closest(interactiveSelectors);
      if (target && target === activeHoverEl) {
        isHovering = false;
        activeHoverEl = null;
        cursorRing.classList.remove('cursor-ring--active', 'cursor-ring--button');
      }
    });
  }

  // 3D Card Subtle Physics & Glare Effect (Tamed & Damped)
  function setupCardTilt() {
    const cards = document.querySelectorAll('.card, .card-surface, .interactive-tilt, .persona-card');

    cards.forEach((card) => {
      if (getComputedStyle(card).position === 'static') {
        card.style.position = 'relative';
      }

      let glare = card.querySelector('.card-glare');
      if (!glare) {
        glare = document.createElement('div');
        glare.className = 'card-glare';
        card.appendChild(glare);
      }

      card.style.transition = 'transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease';

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        // Subtle gentle micro-tilt (max 1.8deg)
        const rotateX = ((y - centerY) / centerY) * -1.8;
        const rotateY = ((x - centerX) / centerX) * 1.8;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-3px)`;

        // Soft, subtle glare
        const glareX = (x / rect.width) * 100;
        const glareY = (y / rect.height) * 100;
        glare.style.background = `radial-gradient(circle 220px at ${glareX}% ${glareY}%, rgba(249, 157, 114, 0.08), transparent 70%)`;
        glare.style.opacity = '1';
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
        glare.style.opacity = '0';
      });
    });
  }

  // Magnetic Button Attraction Effect (Subtle Damping)
  function setupMagneticButtons() {
    const magnetics = document.querySelectorAll('.btn-primary, .btn-secondary, .magnetic-btn');

    magnetics.forEach((btn) => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        // Gentle subtle attraction
        btn.style.transform = `translate3d(${x * 0.08}px, ${y * 0.08}px, 0)`;
      });

      btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translate3d(0, 0, 0)';
        btn.style.transition = 'transform 0.3s cubic-bezier(0.25, 1, 0.5, 1)';
        setTimeout(() => {
          btn.style.transition = '';
        }, 300);
      });
    });
  }

  // Hide default cursor when active
  document.documentElement.classList.add('custom-cursor-active');

  // Initialize all listeners
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setupHoverListeners();
      setupCardTilt();
      setupMagneticButtons();
    });
  } else {
    setupHoverListeners();
    setupCardTilt();
    setupMagneticButtons();
  }

  // Re-run card tilt when dynamic content loads
  const observer = new MutationObserver(() => {
    setupCardTilt();
    setupMagneticButtons();
  });
  observer.observe(document.body, { childList: true, subtree: true });
})();
