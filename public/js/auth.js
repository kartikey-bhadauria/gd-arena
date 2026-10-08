// Authentication and user profile state management

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      localStorage.setItem('gd_user', JSON.stringify({ email, name: email.split('@')[0], loggedIn: true }));
      window.location.href = '/pages/mode-select.html';
    });
  }

  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      localStorage.setItem('gd_user', JSON.stringify({ name, email, loggedIn: true }));
      window.location.href = '/pages/onboarding.html';
    });
  }
});

window.mockOAuth = function(provider) {
  const mockUser = {
    name: "Candidate",
    email: `candidate@${provider.toLowerCase().replace(' ', '')}.com`,
    provider,
    loggedIn: true
  };
  localStorage.setItem('gd_user', JSON.stringify(mockUser));
  window.location.href = '/pages/onboarding.html';
};
