// Landing Page Interactive Features & FAQ Accordions

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Scroll animations via IntersectionObserver
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.scroll-fade').forEach(el => observer.observe(el));
});

window.toggleFaq = function(cardEl) {
  const content = cardEl.querySelector('.faq-content');
  const icon = cardEl.querySelector('[data-lucide="chevron-down"]');
  if (content) {
    content.classList.toggle('hidden');
    if (icon) {
      icon.classList.toggle('rotate-180');
    }
  }
};
