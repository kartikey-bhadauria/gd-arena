/**
 * GD Arena — High Performance Scroll Animation & Parallax Engine
 * 
 * Features:
 * 1. IntersectionObserver-based Scroll Reveals (Fade, Slide, Scale, Stagger)
 * 2. Viewport Scroll Progress Bar
 * 3. Animated Number Counters on Scroll Entry
 * 4. Dynamic Sticky Navbar Glass Morphism
 * 5. Floating Parallax Tilt on Scroll
 * 6. Floating Back-to-Top Action Pill
 */

(function () {
  'use strict';

  // 1. Create Top Scroll Progress Indicator
  const progressBar = document.createElement('div');
  progressBar.id = 'scroll-progress-bar';
  progressBar.className = 'scroll-progress-bar';
  document.body.appendChild(progressBar);

  // 2. Create Floating Back to Top Button
  const backToTopBtn = document.createElement('button');
  backToTopBtn.id = 'back-to-top-btn';
  backToTopBtn.className = 'back-to-top-btn';
  backToTopBtn.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="m18 15-6-6-6 6"/>
    </svg>
  `;
  backToTopBtn.setAttribute('aria-label', 'Scroll to top');
  document.body.appendChild(backToTopBtn);

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 3. Track Scroll Events (Progress Bar + Navbar + Back to Top)
  const header = document.querySelector('header');

  function onScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    
    // Progress Bar
    if (scrollHeight > 0) {
      const progress = (scrollTop / scrollHeight) * 100;
      progressBar.style.width = `${progress}%`;
    }

    // Header Morph
    if (header) {
      if (scrollTop > 20) {
        header.classList.add('header-scrolled');
      } else {
        header.classList.remove('header-scrolled');
      }
    }

    // Back to top visibility
    if (scrollTop > 450) {
      backToTopBtn.classList.add('show');
    } else {
      backToTopBtn.classList.remove('show');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // 4. Scroll Reveal Intersection Observer
  function setupScrollReveals() {
    // Automatically select sections, cards, steps, and explicitly marked reveal items
    const elementsToReveal = document.querySelectorAll(
      'section, .card, .card-surface, .reveal-up, .reveal-left, .reveal-right, .reveal-scale, .stagger-item, h2, .persona-card, .faq-item'
    );

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          
          // Trigger number counter if attached
          if (entry.target.hasAttribute('data-counter') && !entry.target.classList.contains('counted')) {
            animateCounter(entry.target);
          }

          // Trigger counters inside the revealed element
          entry.target.querySelectorAll('[data-counter]:not(.counted)').forEach(animateCounter);

          // Once revealed, unobserve for optimal GPU performance
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    elementsToReveal.forEach((el, index) => {
      // Clean, elegant upward reveal for all content
      if (!el.classList.contains('reveal-left') && !el.classList.contains('reveal-right') && !el.classList.contains('reveal-scale') && !el.classList.contains('reveal-up')) {
        el.classList.add('reveal-up');
      }

      // Smooth subtle stagger for cards in grids
      const parent = el.parentElement;
      if (parent && (parent.classList.contains('grid') || parent.classList.contains('stagger-container'))) {
        const siblingIndex = Array.from(parent.children).indexOf(el);
        el.style.transitionDelay = `${(siblingIndex % 4) * 60}ms`;
      }

      observer.observe(el);
    });
  }

  // 5. High-Precision Number Counter Animation
  function animateCounter(el) {
    el.classList.add('counted');
    const targetText = el.getAttribute('data-counter') || el.innerText;
    const match = targetText.match(/^([^\d]*)(\d+(?:\.\d+)?)([^\d]*)$/);
    if (!match) return;

    const prefix = match[1] || '';
    const targetValue = parseFloat(match[2]);
    const suffix = match[3] || '';
    const isDecimal = match[2].includes('.');
    const duration = 1600; // ms
    const startTime = performance.now();

    function update(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // easeOutExpo function
      const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const currentValue = targetValue * ease;

      el.innerText = `${prefix}${isDecimal ? currentValue.toFixed(1) : Math.floor(currentValue)}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.innerText = targetText;
      }
    }

    requestAnimationFrame(update);
  }

  // 6. Text Word-by-Word Split and Reveal Engine
  function setupTextWordReveals() {
    const textElements = document.querySelectorAll('.text-reveal-words, .hero-headline');
    textElements.forEach(el => {
      // Don't re-split if already split
      if (el.querySelector('.word-span')) return;

      const words = el.innerText.trim().split(/\s+/);
      el.innerHTML = words.map((word, i) => {
        return `<span class="word-span" style="transition-delay: ${i * 45}ms">${word} </span>`;
      }).join('');
    });

    // Also initialize hero text rotator if present
    setupHeroTextRotator();
  }

  // 7. Dynamic Hero Subtitle Text Rotator
  function setupHeroTextRotator() {
    const rotator = document.getElementById('heroRotatingText');
    if (!rotator) return;

    const phrases = [
      "Group Discussions",
      "Technical 1-on-1 Interviews",
      "Instant Speech Barge-In",
      "Campus Placement Rounds"
    ];

    let currentIdx = 0;
    setInterval(() => {
      rotator.classList.add('swap-out');
      setTimeout(() => {
        currentIdx = (currentIdx + 1) % phrases.length;
        rotator.textContent = phrases[currentIdx];
        rotator.classList.remove('swap-out');
        rotator.classList.add('swap-in');
        setTimeout(() => {
          rotator.classList.remove('swap-in');
        }, 50);
      }, 350);
    }, 3200);
  }

  // Initialize Engine
  function initEngine() {
    setupTextWordReveals();
    setupScrollReveals();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEngine);
  } else {
    initEngine();
  }
})();
