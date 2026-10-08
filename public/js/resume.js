// Resume Upload and Parsing Client

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
