// Multi-step onboarding handler

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
