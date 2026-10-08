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
    // Generate sample authentic report data if opened directly
    report = {
      overall_score: 7.6,
      tier: "Strong",
      pass: true,
      stats: {
        total_words: 340,
        talk_time_pct: { student: 28.5, aarav: 32.0, priya: 24.5, rohan: 15.0 },
        student_words: 97,
        interruptions: 1
      },
      dimensions: {
        opening: { score: 8.0, quote: "[00:45] \"I believe AI will augment engineer productivity rather than replace junior roles completely.\"", comment: "Strong structured assertion; grounded debate early." },
        idea_quality: { score: 7.5, quote: "[01:30] \"Junior devs handle glue code and edge case verification that models struggle with.\"", comment: "Solid domain logic; effectively countered Aarav." },
        building_on_others: { score: 7.0, quote: "[03:15] \"Building on Priya's metric regarding latency overhead...\"", comment: "Good explicit reference to peer arguments." },
        listening: { score: 8.5, quote: "[02:10] Listened attentively during Aarav's counter.", comment: "Maintained poise under aggressive interruption." },
        handling_interruptions: { score: 7.5, quote: "[03:40] Recovered floor calmly.", comment: "Assertive voice modulation without aggression." },
        closing: { score: 7.0, quote: "[04:20] \"To summarize, AI accelerates coding velocity while humans preserve architectural integrity.\"", comment: "Clear consensus synthesis." }
      },
      strengths: [
        "Composed demeanor when challenged directly by Aarav on production latency.",
        "Structured reasoning using concrete industry examples instead of generic buzzwords."
      ],
      weaknesses: [
        "Could cite more exact quantitative benchmarks (e.g. error rate deltas) to solidify claims.",
        "Slight delay (2.5s) before jumping into the opening round."
      ],
      missed_openings: [
        { ts: "02:15", what_happened: "Priya presented a flawed scalability assumption regarding serverless cold starts.", what_you_could_have_said: "Priya makes a valid point on compute cost, but cold start latencies remain the primary blocker." }
      ],
      drills: [
        "Drill 1: STAR method rapid response to high-concurrency architecture challenges.",
        "Drill 2: 15-second opening assertion structuring drill.",
        "Drill 3: Counter-argument synthesis under aggressive peer interruption."
      ]
    };
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
