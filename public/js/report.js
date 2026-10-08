// Placement Report Rendering Logic

import { PERSONAS } from './config.js';

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  let report = null;
  try {
    const raw = sessionStorage.getItem('current_report');
    if (raw) report = JSON.parse(raw);
  } catch (e) {}

  if (!report) {
    // No active session report found — guide user to start a real session
    const mainEl = document.querySelector('main') || document.body;
    mainEl.innerHTML = `
      <div class="max-w-2xl mx-auto py-20 px-6 text-center">
        <div class="w-16 h-16 bg-amber-50 text-amber-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm border border-amber-200">
          <i data-lucide="alert-circle" class="w-8 h-8"></i>
        </div>
        <h1 class="text-2xl font-bold text-stone-900 mb-2">No Active Session Report Found</h1>
        <p class="text-stone-600 mb-8 text-sm">Please complete a live Group Discussion or 1-on-1 Technical Interview session to generate your authentic API-evaluated scorecard.</p>
        <div class="flex items-center justify-center gap-4">
          <a href="/pages/mode-select.html" class="btn-primary text-sm py-2.5 px-6">Start New Practice Session</a>
          <a href="/pages/history.html" class="btn-secondary text-sm py-2.5 px-6">View Past History</a>
        </div>
      </div>
    `;
    if (window.lucide) window.lucide.createIcons();
    return;
  }

  // Save to history storage
  saveToHistory(report);

  renderReport(report);
});

function renderReport(data) {
  document.getElementById('overallScore').innerHTML = `${data.overall_score}<span class="text-xs text-stone-400 font-normal">/10</span>`;

  const tierBadge = document.getElementById('tierBadge');
  tierBadge.textContent = `Tier: ${data.tier} (${data.pass ? 'Passed Bar' : 'Did Not Pass'})`;
  if (data.tier === 'Weak') {
    tierBadge.className = "mt-1 text-[11px] font-bold px-3 py-0.5 rounded-full inline-block uppercase bg-red-50 text-red-700 border border-red-200";
  } else if (data.tier === 'Average') {
    tierBadge.className = "mt-1 text-[11px] font-bold px-3 py-0.5 rounded-full inline-block uppercase bg-amber-50 text-amber-700 border border-amber-200";
  } else if (data.tier === 'Disqualified') {
    tierBadge.className = "mt-1 text-[11px] font-bold px-3 py-0.5 rounded-full inline-block uppercase bg-red-900 text-white border border-red-700";
    document.getElementById('overallScore').innerHTML = `<span class="text-red-600">REJECTED</span>`;
  } else if (data.tier === 'Elite') {
    tierBadge.className = "mt-1 text-[11px] font-bold px-3 py-0.5 rounded-full inline-block uppercase bg-purple-50 text-purple-700 border border-purple-200";
  }

  // Talk time bar
  const pcts = data.stats?.talk_time_pct || { student: 25, aarav: 35, priya: 25, rohan: 15 };
  const barContainer = document.getElementById('talkTimeBarContainer');
  barContainer.innerHTML = `
    <div class="h-full bg-emerald-500" style="width: ${pcts.student || 25}%" title="You: ${pcts.student || 25}%"></div>
    <div class="h-full bg-red-500" style="width: ${pcts.aarav || 30}%" title="Aarav: ${pcts.aarav || 30}%"></div>
    <div class="h-full bg-cyan-500" style="width: ${pcts.priya || 25}%" title="Priya: ${pcts.priya || 25}%"></div>
    <div class="h-full bg-amber-500" style="width: ${pcts.rohan || 20}%" title="Rohan: ${pcts.rohan || 20}%"></div>
  `;
  document.getElementById('studentAirtimeText').textContent = `You: ${pcts.student || 25}% of spoken discussion words`;

  // 6 Dimension cards
  const grid = document.getElementById('dimensionsGrid');
  const dimLabels = {
    opening: "Opening Statement & Initiation",
    idea_quality: "Idea Quality & Logical Reasoning",
    building_on_others: "Building on Others & Synthesis",
    listening: "Active Listening & Composure",
    handling_interruptions: "Handling Interruptions & Rebuttals",
    closing: "Closing Synthesis & Conclusion"
  };

  grid.innerHTML = Object.entries(data.dimensions || {}).map(([key, item]) => `
    <div class="card bg-white !p-4 border border-[rgba(38,57,90,0.16)] space-y-2">
      <div class="flex items-center justify-between">
        <span class="font-bold text-xs text-[#1a1814]">${dimLabels[key] || key}</span>
        <span class="font-mono text-xs font-bold ${item.score >= 7 ? 'text-emerald-600' : item.score >= 5 ? 'text-amber-600' : 'text-red-600'}">${item.score}/10</span>
      </div>
      <div class="p-2.5 rounded bg-stone-50 border-l-2 border-[#f99d72] text-[11px] text-stone-700 italic">
        ${item.quote}
      </div>
      <p class="text-[11px] text-stone-500">${item.comment}</p>
    </div>
  `).join('');

  // Strengths & Weaknesses
  document.getElementById('strengthsList').innerHTML = (data.strengths || []).map(s => `
    <li class="flex items-start gap-2">
      <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5"></i>
      <span>${s}</span>
    </li>
  `).join('');

  document.getElementById('weaknessesList').innerHTML = (data.weaknesses || []).map(w => `
    <li class="flex items-start gap-2">
      <i data-lucide="x" class="w-3.5 h-3.5 text-red-600 shrink-0 mt-0.5"></i>
      <span>${w}</span>
    </li>
  `).join('');

  // Missed openings
  document.getElementById('missedOpeningsList').innerHTML = (data.missed_openings || []).map(m => `
    <div class="p-3 rounded-lg bg-stone-50 border border-stone-200 space-y-1">
      <div class="flex items-center justify-between text-[10px] font-mono text-stone-500">
        <span class="font-bold text-amber-700">[${m.ts}] Opportunity Detected</span>
      </div>
      <p class="text-stone-700"><strong>What happened:</strong> ${m.what_happened}</p>
      <p class="text-emerald-700"><strong>What you could have said:</strong> "${m.what_you_could_have_said}"</p>
    </div>
  `).join('');

  // Drills
  document.getElementById('drillsList').innerHTML = (data.drills || []).map((d, i) => `
    <div class="flex items-center gap-2 p-2 rounded bg-white/5 border border-white/10">
      <span class="w-5 h-5 rounded-full bg-[#f99d72] text-stone-900 font-bold flex items-center justify-center text-[10px]">${i+1}</span>
      <span>${d}</span>
    </div>
  `).join('');

  // Evaluator Review Statement
  const reviewEl = document.getElementById('evaluatorReviewStatement');
  if (reviewEl) {
    reviewEl.textContent = data.review_statement || "Candidate evaluated according to official placement assessment rubric across domain competence, logical synthesis, and verbal fluency.";
  }

  // Full Quoted Transcript Log
  const transcript = data.transcript || [];
  const turnCountEl = document.getElementById('transcriptTurnCount');
  if (turnCountEl) turnCountEl.textContent = transcript.length;

  const feed = document.getElementById('fullTranscriptFeed');
  if (feed && transcript.length > 0) {
    feed.innerHTML = transcript.map(t => {
      const isStudent = t.speaker === 'student' || t.speaker === 'user';
      const color = isStudent ? '#059669' : (PERSONAS[t.speaker]?.color || '#1a1814');
      return `
        <div class="p-2 rounded ${isStudent ? 'bg-emerald-50/50 border border-emerald-100' : 'bg-stone-50 border border-stone-100'}">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-stone-400 font-mono text-[10px]">[${t.timestamp || '00:00'}]</span>
            <span class="font-bold text-[11px]" style="color: ${color}">${t.name || t.speaker}:</span>
          </div>
          <p class="text-stone-800 text-xs">${t.text}</p>
        </div>
      `;
    }).join('');
  }

  if (window.lucide) window.lucide.createIcons();
}

function saveToHistory(report) {
  let history = [];
  try {
    history = JSON.parse(localStorage.getItem('gd_history') || '[]');
  } catch(e) {}
  history.unshift({
    id: Date.now().toString(),
    date: new Date().toLocaleDateString(),
    topic: localStorage.getItem('gd_selected_topic') || 'Should AI Replace Entry-Level Software Engineers?',
    score: report.overall_score,
    tier: report.tier,
    mode: 'gd'
  });
  localStorage.setItem('gd_history', JSON.stringify(history.slice(0, 10)));
}

window.toggleTranscript = function() {
  const feed = document.getElementById('fullTranscriptFeed');
  const chevron = document.getElementById('transcriptChevron');
  feed.classList.toggle('hidden');
  chevron.classList.toggle('rotate-180');
};
