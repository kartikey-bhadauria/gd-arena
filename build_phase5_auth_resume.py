import os

BASE_DIR = r"C:\Users\Kartikey\gd-arena"

# 1. public/pages/login.html
login_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign In — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-white min-h-screen flex text-[#1a1814]">
  
  <!-- Left Column: Ink Hero Panel -->
  <div class="hidden lg:flex lg:w-1/2 bg-[#1a1814] text-white p-12 flex-col justify-between relative overflow-hidden">
    <div class="space-y-6 z-10">
      <a href="/" class="flex items-center gap-2.5 text-decoration-none">
        <div class="w-8 h-8 rounded-full bg-[#f99d72] flex items-center justify-center font-bold text-[#1a1814] text-sm">GD</div>
        <span class="font-bold text-lg tracking-tight text-white">GD Arena</span>
      </a>
      
      <div class="pt-16 space-y-4 max-w-md">
        <h2 class="text-3xl font-extrabold tracking-tight leading-snug">
          Practise the room before you enter it.
        </h2>
        <p class="text-stone-400 text-sm leading-relaxed">
          Master high-stakes placement group discussions and 1-on-1 technical rounds against adaptive AI personas.
        </p>
      </div>

      <div class="space-y-3 pt-6 text-xs text-stone-300">
        <div class="flex items-center gap-2.5">
          <i data-lucide="check" class="w-4 h-4 text-[#f99d72]"></i>
          <span>Zero-risk simulations with instant speech barge-in</span>
        </div>
        <div class="flex items-center gap-2.5">
          <i data-lucide="check" class="w-4 h-4 text-[#f99d72]"></i>
          <span>Strict Tier-1 placement scoring with transcript quotes</span>
        </div>
        <div class="flex items-center gap-2.5">
          <i data-lucide="check" class="w-4 h-4 text-[#f99d72]"></i>
          <span>Resume-specific question tailoring</span>
        </div>
      </div>
    </div>

    <!-- Testimonial -->
    <div class="p-4 rounded-lg bg-white/5 border border-white/10 z-10">
      <p class="text-xs text-stone-300 italic mb-2">
        "Aarav's aggressive interruptions forced me to structure my thoughts in 15 seconds. Cleared my Day 1 placement GD easily."
      </p>
      <span class="text-[11px] font-bold text-stone-400">— Final Year CSE Student, Tier-2 University</span>
    </div>
  </div>

  <!-- Right Column: Login Form -->
  <div class="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12">
    <div class="w-full max-w-md space-y-6">
      <div>
        <h2 class="text-2xl font-bold tracking-tight text-[#1a1814]">Welcome back</h2>
        <p class="text-xs text-stone-500 mt-1">Sign in to resume your placement practice sessions.</p>
      </div>

      <form id="loginForm" class="space-y-4 text-xs">
        <div>
          <label class="block font-medium text-stone-700 mb-1">Email address</label>
          <input type="email" id="email" required placeholder="student@college.edu" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-[#f99d72] focus:border-transparent text-xs">
        </div>

        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block font-medium text-stone-700">Password</label>
            <a href="#" class="text-stone-400 hover:text-stone-600">Forgot?</a>
          </div>
          <input type="password" id="password" required placeholder="••••••••" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-[#f99d72] focus:border-transparent text-xs">
        </div>

        <button type="submit" class="btn-primary w-full !py-2.5 !text-xs !justify-center">
          <span>Continue with email</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </button>
      </form>

      <div class="relative flex items-center justify-center text-[11px] text-stone-400">
        <span class="bg-white px-2 z-10">or continue with</span>
        <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-stone-200"></div></div>
      </div>

      <div class="space-y-2.5">
        <button onclick="mockOAuth('Google')" class="btn-secondary w-full !py-2.5 !text-xs !justify-center gap-2">
          <svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.6h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.9z"/><path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3 0-.8.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 12.3 0 15.1c0 2.8.7 5.4 1.9 7.8l3.7-2.9z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.8-2.5 1.3-4.3 1.3-3 0-5.5-2.3-6.4-5.2L1.9 17.1C3.7 20.8 7.5 24 12 24z"/></svg>
          <span>Continue with Google</span>
        </button>

        <button onclick="mockOAuth('University SSO')" class="btn-secondary w-full !py-2.5 !text-xs !justify-center gap-2">
          <i data-lucide="graduation-cap" class="w-4 h-4 text-stone-700"></i>
          <span>University Portal SSO</span>
        </button>
      </div>

      <p class="text-center text-xs text-stone-500">
        Don't have an account? <a href="/pages/signup.html" class="font-bold text-[#1a1814] underline">Sign up</a>
      </p>
      
      <p class="text-center text-[10px] text-stone-400">
        ⚠️ AI Evaluation Disclosure: All peer arguments & scorecards are generated by AI.
      </p>
    </div>
  </div>

  <script src="/js/auth.js" type="module"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "login.html"), "w", encoding="utf-8") as f:
    f.write(login_html)

# 2. public/pages/signup.html
signup_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign Up — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-white min-h-screen flex text-[#1a1814]">
  
  <!-- Left Column: Ink Hero Panel -->
  <div class="hidden lg:flex lg:w-1/2 bg-[#1a1814] text-white p-12 flex-col justify-between relative overflow-hidden">
    <div class="space-y-6 z-10">
      <a href="/" class="flex items-center gap-2.5 text-decoration-none">
        <div class="w-8 h-8 rounded-full bg-[#f99d72] flex items-center justify-center font-bold text-[#1a1814] text-sm">GD</div>
        <span class="font-bold text-lg tracking-tight text-white">GD Arena</span>
      </a>
      
      <div class="pt-16 space-y-4 max-w-md">
        <h2 class="text-3xl font-extrabold tracking-tight leading-snug">
          Real GD pressure.<br>Zero real-world risk.
        </h2>
        <p class="text-stone-400 text-sm leading-relaxed">
          Join thousands of engineering and MBA students building communication poise for top placements.
        </p>
      </div>

      <div class="space-y-3 pt-6 text-xs text-stone-300">
        <div class="flex items-center gap-2.5">
          <i data-lucide="check" class="w-4 h-4 text-[#f99d72]"></i>
          <span>Unlimited free AI GD rounds & 1-on-1 interviews</span>
        </div>
        <div class="flex items-center gap-2.5">
          <i data-lucide="check" class="w-4 h-4 text-[#f99d72]"></i>
          <span>Transcript-linked analytics on your hesitations & rebuttals</span>
        </div>
      </div>
    </div>

    <div class="p-4 rounded-lg bg-white/5 border border-white/10 z-10 text-[11px] text-stone-400">
      Zero payment required. Powered by free-tier AI architecture.
    </div>
  </div>

  <!-- Right Column: Signup Form -->
  <div class="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12">
    <div class="w-full max-w-md space-y-6">
      <div>
        <h2 class="text-2xl font-bold tracking-tight text-[#1a1814]">Create your account</h2>
        <p class="text-xs text-stone-500 mt-1">Start practicing group discussions in under 60 seconds.</p>
      </div>

      <form id="signupForm" class="space-y-3.5 text-xs">
        <div>
          <label class="block font-medium text-stone-700 mb-1">Full Name</label>
          <input type="text" id="name" required placeholder="Kartikey Bhadauria" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-[#f99d72] focus:border-transparent text-xs">
        </div>

        <div>
          <label class="block font-medium text-stone-700 mb-1">Email address</label>
          <input type="email" id="email" required placeholder="student@college.edu" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-[#f99d72] focus:border-transparent text-xs">
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block font-medium text-stone-700 mb-1">Password</label>
            <input type="password" id="password" required placeholder="••••••••" class="w-full px-3 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-[#f99d72] text-xs">
          </div>
          <div>
            <label class="block font-medium text-stone-700 mb-1">Confirm</label>
            <input type="password" id="confirmPassword" required placeholder="••••••••" class="w-full px-3 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-[#f99d72] text-xs">
          </div>
        </div>

        <div class="flex items-center gap-2 pt-1">
          <input type="checkbox" id="terms" required class="rounded border-stone-300 text-[#f99d72] focus:ring-[#f99d72]">
          <label for="terms" class="text-[11px] text-stone-600">I agree to the Terms of Service and AI Practice Privacy Policy</label>
        </div>

        <button type="submit" class="btn-primary w-full !py-2.5 !text-xs !justify-center">
          <span>Create account & setup profile</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </button>
      </form>

      <div class="relative flex items-center justify-center text-[11px] text-stone-400">
        <span class="bg-white px-2 z-10">or sign up with</span>
        <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-stone-200"></div></div>
      </div>

      <button onclick="mockOAuth('Google')" class="btn-secondary w-full !py-2.5 !text-xs !justify-center gap-2">
        <svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.6h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.9z"/><path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3 0-.8.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 12.3 0 15.1c0 2.8.7 5.4 1.9 7.8l3.7-2.9z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.8-2.5 1.3-4.3 1.3-3 0-5.5-2.3-6.4-5.2L1.9 17.1C3.7 20.8 7.5 24 12 24z"/></svg>
        <span>Sign up with Google</span>
      </button>

      <p class="text-center text-xs text-stone-500">
        Already have an account? <a href="/pages/login.html" class="font-bold text-[#1a1814] underline">Sign in</a>
      </p>
    </div>
  </div>

  <script src="/js/auth.js" type="module"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "signup.html"), "w", encoding="utf-8") as f:
    f.write(signup_html)

# 3. public/js/auth.js
auth_js = """// Authentication and user profile state management

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
"""
with open(os.path.join(BASE_DIR, "public", "js", "auth.js"), "w", encoding="utf-8") as f:
    f.write(auth_js)

# 4. public/pages/onboarding.html
onboarding_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Setup Profile — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-[#fafaf9] min-h-screen text-[#1a1814] flex flex-col justify-between">

  <!-- Header -->
  <header class="bg-white border-b border-[rgba(38,57,90,0.1)] py-4">
    <div class="max-w-4xl mx-auto px-4 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full bg-[#f99d72] flex items-center justify-center font-bold text-[#1a1814] text-xs">GD</div>
        <span class="font-bold text-base tracking-tight text-[#1a1814]">GD Arena</span>
      </a>
      <span class="text-xs font-mono text-stone-400">Step <span id="stepNumber">1</span> of 4</span>
    </div>
  </header>

  <!-- Wizard Body -->
  <main class="max-w-xl mx-auto px-4 py-8 w-full flex-1 flex flex-col justify-center">
    
    <!-- Progress Bar -->
    <div class="w-full bg-stone-200 h-1.5 rounded-full overflow-hidden mb-8">
      <div id="progressBar" class="bg-[#f99d72] h-full transition-all duration-300" style="width: 25%"></div>
    </div>

    <div class="card shadow-lg bg-white !p-8 space-y-6">
      
      <!-- STEP 1: Basic Details -->
      <div id="step1" class="wizard-step space-y-4">
        <div>
          <h2 class="text-xl font-bold text-[#1a1814]">Basic details</h2>
          <p class="text-xs text-stone-500">Helps AI adjust speaking vocabulary and placement tier expectations.</p>
        </div>

        <div class="space-y-3 text-xs">
          <div>
            <label class="block font-medium text-stone-700 mb-1">Full Name</label>
            <input type="text" id="obName" value="Kartikey Bhadauria" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 focus:ring-2 focus:ring-[#f99d72] text-xs">
          </div>
          <div>
            <label class="block font-medium text-stone-700 mb-1">College / University</label>
            <input type="text" id="obCollege" placeholder="e.g. Lloyd Institute of Engineering / AKTU" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 focus:ring-2 focus:ring-[#f99d72] text-xs">
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-stone-700 mb-1">Graduation Year</label>
              <select id="obYear" class="w-full px-3 py-2.5 rounded-lg border border-stone-300 text-xs">
                <option value="2027">2027</option>
                <option value="2026" selected>2026</option>
                <option value="2025">2025</option>
              </select>
            </div>
            <div>
              <label class="block font-medium text-stone-700 mb-1">Branch / Major</label>
              <input type="text" id="obBranch" value="Computer Science & Engineering" class="w-full px-3 py-2.5 rounded-lg border border-stone-300 text-xs">
            </div>
          </div>
        </div>
      </div>

      <!-- STEP 2: Target -->
      <div id="step2" class="wizard-step hidden space-y-4">
        <div>
          <h2 class="text-xl font-bold text-[#1a1814]">Target role & companies</h2>
          <p class="text-xs text-stone-500">Sets the difficulty of technical topics and interviewer personas.</p>
        </div>

        <div class="space-y-3 text-xs">
          <div>
            <label class="block font-medium text-stone-700 mb-1">Target Role</label>
            <select id="obRole" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 text-xs">
              <option value="Software Development Engineer (SDE)">Software Development Engineer (SDE)</option>
              <option value="Data Analyst / AI Engineer">Data Analyst / AI Engineer</option>
              <option value="Product / Business Analyst">Product / Business Analyst</option>
              <option value="Consulting / Management Trainee">Consulting / Management Trainee</option>
            </select>
          </div>
          <div>
            <label class="block font-medium text-stone-700 mb-1">Target Company Category</label>
            <select id="obCompany" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 text-xs">
              <option value="Product Startups & Scaleups">Product Startups & Scaleups</option>
              <option value="Tier-1 Product Tech (FAANG/MNC)">Tier-1 Product Tech (FAANG/MNC)</option>
              <option value="Service & IT Consulting">Service & IT Consulting (TCS, Infosys, Wipro)</option>
            </select>
          </div>
          <div>
            <label class="block font-medium text-stone-700 mb-1">Experience Level</label>
            <select id="obExp" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 text-xs">
              <option value="Fresher (College Student)">Fresher (College Student)</option>
              <option value="0–1 Years (Internships)">0–1 Years (Internships)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- STEP 3: Language & Timeline -->
      <div id="step3" class="wizard-step hidden space-y-4">
        <div>
          <h2 class="text-xl font-bold text-[#1a1814]">Language & timeline</h2>
          <p class="text-xs text-stone-500">Configure speech recognition acoustics and session urgency.</p>
        </div>

        <div class="space-y-3 text-xs">
          <div>
            <label class="block font-medium text-stone-700 mb-1">Preferred Spoken Language</label>
            <select id="obLang" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 text-xs">
              <option value="English (Indian Accent)">English (Indian Accent / Formal Placement Style)</option>
              <option value="Hinglish">Hinglish (Conversational Tech English)</option>
            </select>
          </div>
          <div>
            <label class="block font-medium text-stone-700 mb-1">Placement Timeline</label>
            <select id="obTimeline" class="w-full px-3.5 py-2.5 rounded-lg border border-stone-300 text-xs">
              <option value="Next 1 Month (Urgent Practice)">Next 1 Month (Urgent Practice)</option>
              <option value="Next 3 Months">Next 3 Months</option>
              <option value="General Preparation">General Preparation</option>
            </select>
          </div>
        </div>
      </div>

      <!-- STEP 4: Confirmation Summary -->
      <div id="step4" class="wizard-step hidden space-y-4">
        <div>
          <h2 class="text-xl font-bold text-[#1a1814]">Setup summary</h2>
          <p class="text-xs text-stone-500">Verify your details before uploading your resume.</p>
        </div>

        <div class="p-4 rounded-lg bg-stone-50 border border-stone-200 text-xs space-y-2" id="summaryBox">
          <!-- Injected via JS -->
        </div>
      </div>

      <!-- Navigation buttons -->
      <div class="flex items-center justify-between pt-4 border-t border-stone-100">
        <button id="prevBtn" onclick="prevStep()" class="btn-secondary !text-xs !py-2 !px-4 hidden">
          <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
          <span>Back</span>
        </button>
        <div class="ml-auto">
          <button id="nextBtn" onclick="nextStep()" class="btn-primary !text-xs !py-2.5 !px-5">
            <span id="nextText">Next step</span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>

    </div>
  </main>

  <footer class="py-4 text-center text-[11px] text-stone-400">
    GD Arena · Voice-First AI Placement Simulator
  </footer>

  <script src="/js/onboarding.js" type="module"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "onboarding.html"), "w", encoding="utf-8") as f:
    f.write(onboarding_html)

# 5. public/js/onboarding.js
onboarding_js = """// Multi-step onboarding handler

let currentStep = 1;
const profileData = {};

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
});

window.nextStep = function() {
  if (currentStep === 1) {
    profileData.name = document.getElementById('obName').value;
    profileData.college = document.getElementById('obCollege').value || 'University';
    profileData.year = document.getElementById('obYear').value;
    profileData.branch = document.getElementById('obBranch').value;
  } else if (currentStep === 2) {
    profileData.role = document.getElementById('obRole').value;
    profileData.company = document.getElementById('obCompany').value;
    profileData.exp = document.getElementById('obExp').value;
  } else if (currentStep === 3) {
    profileData.lang = document.getElementById('obLang').value;
    profileData.timeline = document.getElementById('obTimeline').value;

    // Render summary
    document.getElementById('summaryBox').innerHTML = `
      <div><strong>Candidate:</strong> ${profileData.name} (${profileData.branch}, ${profileData.year})</div>
      <div><strong>College:</strong> ${profileData.college}</div>
      <div><strong>Target Role:</strong> ${profileData.role}</div>
      <div><strong>Target Segment:</strong> ${profileData.company}</div>
      <div><strong>Language:</strong> ${profileData.lang}</div>
    `;
  } else if (currentStep === 4) {
    localStorage.setItem('gd_profile', JSON.stringify(profileData));
    window.location.href = '/pages/resume-upload.html';
    return;
  }

  currentStep++;
  updateStepView();
};

window.prevStep = function() {
  if (currentStep > 1) {
    currentStep--;
    updateStepView();
  }
};

function updateStepView() {
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`step${i}`);
    if (el) el.classList.toggle('hidden', i !== currentStep);
  }

  document.getElementById('stepNumber').textContent = currentStep;
  document.getElementById('progressBar').style.width = `${currentStep * 25}%`;
  document.getElementById('prevBtn').classList.toggle('hidden', currentStep === 1);

  const nextText = document.getElementById('nextText');
  if (currentStep === 4) {
    nextText.textContent = "Complete setup & Upload resume";
  } else {
    nextText.textContent = "Next step";
  }

  if (window.lucide) {
    window.lucide.createIcons();
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "onboarding.js"), "w", encoding="utf-8") as f:
    f.write(onboarding_js)

# 6. public/pages/resume-upload.html
resume_upload_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Resume Upload & JD Match — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-[#fafaf9] min-h-screen text-[#1a1814] flex flex-col justify-between">

  <!-- Header -->
  <header class="bg-white border-b border-[rgba(38,57,90,0.1)] py-4">
    <div class="max-w-5xl mx-auto px-4 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full bg-[#f99d72] flex items-center justify-center font-bold text-[#1a1814] text-xs">GD</div>
        <span class="font-bold text-base tracking-tight text-[#1a1814]">GD Arena</span>
      </a>
      <span class="text-xs text-stone-500">1-on-1 Interview Resume Tailoring</span>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-5xl mx-auto px-4 py-8 w-full flex-1">
    <div class="max-w-2xl mx-auto space-y-6">
      
      <div class="text-center space-y-2">
        <h2 class="text-2xl font-bold tracking-tight text-[#1a1814]">Upload your resume</h2>
        <p class="text-xs text-stone-500">The AI interviewer (Ms. Kapoor) uses your actual projects to generate sharp technical questions.</p>
      </div>

      <!-- Drag & Drop Zone / Paste Area -->
      <div class="card bg-white !p-6 space-y-4">
        
        <!-- Toggle Buttons -->
        <div class="flex items-center gap-2 pb-2 border-b border-stone-100 text-xs">
          <button id="tabPaste" onclick="switchTab('paste')" class="font-bold text-[#1a1814] border-b-2 border-[#f99d72] pb-1">Paste Resume Text</button>
          <button id="tabFile" onclick="switchTab('file')" class="text-stone-400 pb-1 hover:text-stone-700">Upload File (.txt / .pdf)</button>
        </div>

        <!-- Paste Text Mode -->
        <div id="pasteSection" class="space-y-3">
          <textarea id="resumeText" rows="6" placeholder="Paste your resume content (skills, projects, education, internships) here..." class="w-full p-3 rounded-lg border border-stone-200 text-xs font-mono focus:ring-2 focus:ring-[#f99d72] focus:outline-none"></textarea>
        </div>

        <!-- File Upload Mode (Hidden by default) -->
        <div id="fileSection" class="hidden p-8 border-2 border-dashed border-stone-300 rounded-lg text-center space-y-2 bg-stone-50">
          <i data-lucide="file-up" class="w-8 h-8 text-stone-400 mx-auto"></i>
          <p class="text-xs text-stone-600 font-medium">Select a resume file from your computer</p>
          <input type="file" id="resumeFileInput" accept=".txt,.pdf,.doc,.docx" class="text-xs text-stone-500 file:mr-2 file:py-1.5 file:px-3 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-stone-900 file:text-white hover:file:bg-stone-800">
        </div>

        <!-- Optional Job Description Textarea -->
        <div class="pt-2">
          <label class="block font-medium text-xs text-stone-700 mb-1">Target Job Description (Optional for JD Match Score)</label>
          <textarea id="jdText" rows="3" placeholder="Paste target company JD / requirements (e.g. SDE Backend, React, FastAPI, System Design)..." class="w-full p-2.5 rounded-lg border border-stone-200 text-xs font-mono focus:ring-2 focus:ring-[#f99d72] focus:outline-none"></textarea>
        </div>

        <button onclick="handleParseResume()" class="btn-primary w-full !py-2.5 !text-xs !justify-center">
          <i data-lucide="sparkles" class="w-4 h-4"></i>
          <span>Parse Resume & Calculate Alignment</span>
        </button>
      </div>

      <!-- Parsed Output Card (Hidden initially) -->
      <div id="parsedCard" class="card bg-white !p-6 space-y-4 hidden">
        <div class="flex items-center justify-between pb-3 border-b border-stone-100">
          <h3 class="font-bold text-sm text-[#1a1814]">Extracted Candidate Profile</h3>
          <span class="text-[10px] font-mono bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded border border-emerald-200">Parsed Successfully</span>
        </div>

        <!-- JD Match Banner -->
        <div id="jdMatchBanner" class="p-3 rounded-lg bg-stone-50 border border-stone-200 flex items-center justify-between text-xs">
          <div>
            <span class="font-semibold text-stone-700">JD Alignment Score:</span>
            <span id="jdScoreVal" class="font-black text-emerald-600 ml-1">84%</span>
          </div>
          <span class="text-[11px] text-stone-500">Ready for 1-on-1 interview questions</span>
        </div>

        <!-- Skills Chips -->
        <div class="space-y-1.5">
          <span class="text-xs font-semibold text-stone-600">Detected Skills:</span>
          <div id="skillsChips" class="flex flex-wrap gap-1.5"></div>
        </div>

        <!-- Extracted Projects -->
        <div class="space-y-1.5">
          <span class="text-xs font-semibold text-stone-600">Extracted Projects:</span>
          <ul id="projectsList" class="text-xs text-stone-700 space-y-1 list-disc list-inside bg-stone-50 p-2.5 rounded border border-stone-200"></ul>
        </div>

        <!-- Action -->
        <div class="pt-3 border-t border-stone-100 flex items-center justify-between">
          <button onclick="window.location.href='/pages/mode-select.html'" class="btn-primary !py-2.5 !px-6 !text-xs">
            <span>Proceed to Practice Mode Selection</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

    </div>
  </main>

  <footer class="py-4 text-center text-[11px] text-stone-400">
    GD Arena · Resume parsing runs in-memory and is never shared.
  </footer>

  <script src="/js/resume.js" type="module"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "resume-upload.html"), "w", encoding="utf-8") as f:
    f.write(resume_upload_html)

# 7. public/js/resume.js
resume_js = """// Resume Upload and Parsing Client

import { parseResume } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Prepopulate sample resume text for rapid testing
  const sampleResume = `Kartikey Bhadauria
B.Tech Computer Science & Engineering (2026) | CGPA: 8.4
Skills: Python, JavaScript, React, FastAPI, Node.js, Docker, SQL, Git, Machine Learning, Web Speech API

Experience:
- SDE Intern at AI Startup: Built low-latency multi-agent voice orchestration pipelines with sub-50ms audio streaming.

Projects:
- GD Arena: Voice-first AI group discussion simulator with speech barge-in and quote-verified scoring.
- Cloud Scalability Benchmark: Distributed Redis caching engine handling 10,000 requests/sec.`;

  const resumeInput = document.getElementById('resumeText');
  if (resumeInput && !resumeInput.value) {
    resumeInput.value = sampleResume;
  }
});

window.switchTab = function(tab) {
  const pasteSec = document.getElementById('pasteSection');
  const fileSec = document.getElementById('fileSection');
  const tabPaste = document.getElementById('tabPaste');
  const tabFile = document.getElementById('tabFile');

  if (tab === 'paste') {
    pasteSec.classList.remove('hidden');
    fileSec.classList.add('hidden');
    tabPaste.className = "font-bold text-[#1a1814] border-b-2 border-[#f99d72] pb-1";
    tabFile.className = "text-stone-400 pb-1 hover:text-stone-700";
  } else {
    pasteSec.classList.add('hidden');
    fileSec.classList.remove('hidden');
    tabFile.className = "font-bold text-[#1a1814] border-b-2 border-[#f99d72] pb-1";
    tabPaste.className = "text-stone-400 pb-1 hover:text-stone-700";
  }
};

window.handleParseResume = async function() {
  const text = document.getElementById('resumeText').value;
  const jdText = document.getElementById('jdText').value;

  const res = await parseResume(text, jdText);
  if (res) {
    localStorage.setItem('gd_resume', JSON.stringify(res));
    renderParsedCard(res);
  }
};

function renderParsedCard(data) {
  const card = document.getElementById('parsedCard');
  card.classList.remove('hidden');

  // Skills chips
  const chipsContainer = document.getElementById('skillsChips');
  chipsContainer.innerHTML = (data.skills || []).map(s => `
    <span class="px-2 py-0.5 rounded-full bg-stone-100 border border-stone-200 text-[11px] font-medium text-stone-800">${s}</span>
  `).join('');

  // Projects list
  const projList = document.getElementById('projectsList');
  if (data.projects && data.projects.length > 0) {
    projList.innerHTML = data.projects.map(p => `<li>${p}</li>`).join('');
  } else {
    projList.innerHTML = `<li>Full Stack Distributed Web System</li>`;
  }

  // JD Match
  if (data.jd_match) {
    document.getElementById('jdScoreVal').textContent = `${data.jd_match.score}%`;
  }

  card.scrollIntoView({ behavior: 'smooth' });
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "resume.js"), "w", encoding="utf-8") as f:
    f.write(resume_js)

print("Phase 5 Auth, Onboarding & Resume files created successfully!")
