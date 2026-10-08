// Resume Upload and Target Mode Forwarding Client

import { parseResume } from './api.js';

let targetMode = 'interview';

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Parse URL parameters for target next room
  const params = new URLSearchParams(window.location.search);
  const next = params.get('next');
  if (next === 'gd' || next === 'interview') {
    targetMode = next;
  }

  const badge = document.getElementById('targetModeBadge');
  const heading = document.getElementById('resumeHeading');
  const btnText = document.getElementById('proceedBtnText');

  if (targetMode === 'interview') {
    if (badge) badge.textContent = "Placement Preparation: 1-on-1 Interview";
    if (heading) heading.textContent = "Submit Resume for 1-on-1 Interview";
    if (btnText) btnText.textContent = "Attach Resume & Enter Interview Room →";
  } else if (targetMode === 'gd') {
    const topic = localStorage.getItem('gd_selected_topic') || 'Should AI Replace Software Engineers?';
    if (badge) badge.textContent = `Campus GD Preparation: ${topic.slice(0, 32)}...`;
    if (heading) heading.textContent = "Submit Resume / Profile for Group Discussion";
    if (btnText) btnText.textContent = "Attach Profile & Enter GD Room →";
  }

  // Check if resume is already in local storage or prepopulate sample
  const existing = localStorage.getItem('gd_resume');
  const resumeInput = document.getElementById('resumeText');
  if (existing && resumeInput) {
    try {
      const parsed = JSON.parse(existing);
      if (parsed.raw_text) {
        resumeInput.value = parsed.raw_text;
      }
    } catch(e) {}
  }

  if (resumeInput && !resumeInput.value) {
    loadSampleResume();
  }
});

window.loadSampleResume = function() {
  const sample = `Kartikey Bhadauria\nB.Tech Computer Science & Engineering (2026) | CGPA: 8.4\nSkills: Python, JavaScript, React, FastAPI, Node.js, Docker, SQL, Redis, REST APIs, Git, Machine Learning\n\nExperience:\n- SDE Intern at AI Startup: Built low-latency multi-agent voice orchestration pipelines with sub-50ms streaming.\n\nProjects:\n- GD Arena: Voice-first AI group discussion simulator with speech barge-in and quote-verified scoring.\n- Distributed Microservices Engine: High-throughput background worker pipeline with Redis and PostgreSQL sharding.`;

  const resumeInput = document.getElementById('resumeText');
  if (resumeInput) {
    resumeInput.value = sample;
  }
};

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

window.handleParseAndProceed = async function() {
  const text = document.getElementById('resumeText').value.trim();
  const jdText = document.getElementById('jdText')?.value.trim() || '';

  if (text) {
    const btn = document.getElementById('proceedBtnText');
    if (btn) btn.textContent = "Parsing & Grounding Profile...";
    
    try {
      const res = await parseResume(text, jdText);
      if (res) {
        res.raw_text = text;
        localStorage.setItem('gd_resume', JSON.stringify(res));
      }
    } catch(e) {
      localStorage.setItem('gd_resume', JSON.stringify({ raw_text: text, skills: ['Python', 'Problem Solving'] }));
    }
  }

  // Navigate straight to the selected room
  navigateToTargetRoom();
};

window.skipAndProceed = function() {
  navigateToTargetRoom();
};

function navigateToTargetRoom() {
  if (targetMode === 'gd') {
    window.location.href = '/pages/gd-room.html';
  } else {
    window.location.href = '/pages/interview-room.html';
  }
}
