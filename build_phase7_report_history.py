import os

BASE_DIR = r"C:\Users\Kartikey\gd-arena"

# 1. public/pages/report.html
report_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Placement Assessment Report — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
  <style>
    @media print {
      body { background-color: #ffffff !important; }
      header, footer, .no-print { display: none !important; }
      .card { border: 1px solid #e5e7eb !important; box-shadow: none !important; }
    }
  </style>
</head>
<body class="bg-[#fafaf9] min-h-screen text-[#1a1814] flex flex-col justify-between">

  <!-- Header -->
  <header class="bg-white border-b border-[rgba(38,57,90,0.1)] py-4 sticky top-0 z-20 no-print">
    <div class="max-w-6xl mx-auto px-4 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full bg-[#f99d72] flex items-center justify-center font-bold text-[#1a1814] text-xs">GD</div>
        <span class="font-bold text-base tracking-tight text-[#1a1814]">GD Arena</span>
      </a>
      <div class="flex items-center gap-3">
        <button onclick="window.print()" class="btn-secondary !py-1.5 !px-3.5 !text-xs">
          <i data-lucide="printer" class="w-3.5 h-3.5"></i>
          <span>Download PDF</span>
        </button>
        <a href="/pages/mode-select.html" class="btn-primary !py-1.5 !px-3.5 !text-xs">
          <span>Start New Round</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </div>
  </header>

  <!-- Report Main Container -->
  <main class="max-w-5xl mx-auto px-4 py-8 w-full flex-1 space-y-8">
    
    <!-- Report Hero Card -->
    <div class="card bg-white !p-8 border border-[rgba(38,57,90,0.16)] shadow-sm space-y-6">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-stone-100">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="text-[10px] uppercase font-bold text-stone-400 font-mono tracking-wider">Placement Evaluation Report</span>
            <span class="text-[10px] px-2 py-0.5 rounded bg-stone-100 text-stone-600 font-mono" id="reportDate">Oct 08, 2026</span>
          </div>
          <h1 id="reportTopic" class="text-xl sm:text-2xl font-extrabold text-[#1a1814]">Group Discussion Performance Assessment</h1>
          <p class="text-xs text-stone-500 mt-1">Evaluated across 6 core behavioral and argumentative vectors.</p>
        </div>

        <div class="flex items-center gap-4 text-right">
          <div>
            <div class="text-4xl font-black text-[#1a1814]" id="overallScore">7.8<span class="text-xs text-stone-400 font-normal">/10</span></div>
            <div id="tierBadge" class="mt-1 text-[11px] font-bold px-3 py-0.5 rounded-full inline-block uppercase bg-emerald-50 text-emerald-700 border border-emerald-200">
              Tier: Strong (Shortlisted)
            </div>
          </div>
        </div>
      </div>

      <!-- Talk Time & Participation Bar -->
      <div class="space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold text-stone-700">Participation Airtime Share</span>
          <span id="studentAirtimeText" class="text-stone-500 font-medium">You: 26.4% of total words</span>
        </div>
        <div id="talkTimeBarContainer" class="w-full h-3 rounded-full bg-stone-100 overflow-hidden flex">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>

    <!-- 6 Dimensions Scores Grid -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-bold text-[#1a1814]">Dimension Breakdown (Strict Scoring)</h3>
        <span class="text-xs text-stone-400">Min Bar: 5.0/10 to pass</span>
      </div>

      <div id="dimensionsGrid" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 6 Dimension Cards Injected via JS -->
      </div>
    </div>

    <!-- Strengths & Weaknesses (With Quoted Receipts) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Strengths -->
      <div class="card bg-white !p-6 space-y-4 border border-[rgba(38,57,90,0.16)]">
        <div class="flex items-center gap-2 text-emerald-700 font-bold text-sm">
          <i data-lucide="check-circle-2" class="w-4 h-4"></i>
          <span>Demonstrated Strengths</span>
        </div>
        <ul id="strengthsList" class="space-y-3 text-xs text-stone-700"></ul>
      </div>

      <!-- Weaknesses -->
      <div class="card bg-white !p-6 space-y-4 border border-[rgba(38,57,90,0.16)]">
        <div class="flex items-center gap-2 text-red-700 font-bold text-sm">
          <i data-lucide="alert-triangle" class="w-4 h-4"></i>
          <span>Areas for Critical Improvement</span>
        </div>
        <ul id="weaknessesList" class="space-y-3 text-xs text-stone-700"></ul>
      </div>
    </div>

    <!-- Missed Openings Replay -->
    <div class="card bg-white !p-6 space-y-4 border border-[rgba(38,57,90,0.16)]">
      <div class="flex items-center gap-2 text-amber-800 font-bold text-sm">
        <i data-lucide="zap" class="w-4 h-4 text-amber-600"></i>
        <span>Missed Conversational Openings (Replay Drill)</span>
      </div>
      <div id="missedOpeningsList" class="space-y-3 text-xs"></div>
    </div>

    <!-- Concrete Practice Drills -->
    <div class="card bg-stone-900 text-white !p-6 space-y-4 rounded-xl">
      <div class="flex items-center gap-2 text-[#f99d72] font-bold text-sm">
        <i data-lucide="target" class="w-4 h-4"></i>
        <span>Recommended Actionable Drills for Next Round</span>
      </div>
      <div id="drillsList" class="space-y-2 text-xs text-stone-300"></div>
    </div>

    <!-- Full Transcript (Collapsible) -->
    <div class="card bg-white !p-6 space-y-4 border border-[rgba(38,57,90,0.16)]">
      <div class="flex items-center justify-between cursor-pointer" onclick="toggleTranscript()">
        <div class="flex items-center gap-2 font-bold text-sm text-[#1a1814]">
          <i data-lucide="file-text" class="w-4 h-4 text-stone-500"></i>
          <span>Full Quoted Transcript (<span id="transcriptTurnCount">0</span> turns)</span>
        </div>
        <i id="transcriptChevron" data-lucide="chevron-down" class="w-4 h-4 text-stone-500 transition-transform"></i>
      </div>
      <div id="fullTranscriptFeed" class="hidden space-y-2 pt-3 border-t border-stone-100 text-xs font-mono max-h-96 overflow-y-auto custom-scrollbar"></div>
    </div>

  </main>

  <footer class="bg-white border-t border-stone-200 py-6 text-center text-xs text-stone-400 no-print">
    GD Arena · Assessment scores generated by Multi-Vector Placement Evaluation Engine.
  </footer>

  <script src="/js/report.js" type="module"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "report.html"), "w", encoding="utf-8") as f:
    f.write(report_html)

# 2. public/js/report.js
report_js = """// Placement Report Rendering Logic

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
        opening: { score: 8.0, quote: "[00:45] \\"I believe AI will augment engineer productivity rather than replace junior roles completely.\\"", comment: "Strong structured assertion; grounded debate early." },
        idea_quality: { score: 7.5, quote: "[01:30] \\"Junior devs handle glue code and edge case verification that models struggle with.\\"", comment: "Solid domain logic; effectively countered Aarav." },
        building_on_others: { score: 7.0, quote: "[03:15] \\"Building on Priya's metric regarding latency overhead...\\"", comment: "Good explicit reference to peer arguments." },
        listening: { score: 8.5, quote: "[02:10] Listened attentively during Aarav's counter.", comment: "Maintained poise under aggressive interruption." },
        handling_interruptions: { score: 7.5, quote: "[03:40] Recovered floor calmly.", comment: "Assertive voice modulation without aggression." },
        closing: { score: 7.0, quote: "[04:20] \\"To summarize, AI accelerates coding velocity while humans preserve architectural integrity.\\"", comment: "Clear consensus synthesis." }
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
"""
with open(os.path.join(BASE_DIR, "public", "js", "report.js"), "w", encoding="utf-8") as f:
    f.write(report_js)

# 3. public/pages/history.html
history_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Practice History & Readiness Trend — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-[#fafaf9] min-h-screen text-[#1a1814] flex flex-col justify-between">

  <!-- Header -->
  <header class="bg-white border-b border-[rgba(38,57,90,0.1)] py-4 sticky top-0 z-20">
    <div class="max-w-6xl mx-auto px-4 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full bg-[#f99d72] flex items-center justify-center font-bold text-[#1a1814] text-xs">GD</div>
        <span class="font-bold text-base tracking-tight text-[#1a1814]">GD Arena</span>
      </a>
      <a href="/pages/mode-select.html" class="btn-primary !py-1.5 !px-3.5 !text-xs">
        <span>New Session</span>
        <i data-lucide="plus" class="w-3.5 h-3.5"></i>
      </a>
    </div>
  </header>

  <!-- History Container -->
  <main class="max-w-5xl mx-auto px-4 py-8 w-full flex-1 space-y-8">
    
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-[#1a1814]">Your placement readiness progress</h1>
        <p class="text-xs text-stone-500 mt-0.5">Historical session scorecards and recurring communication patterns.</p>
      </div>

      <!-- Streak Pill -->
      <div class="flex items-center gap-3">
        <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200 flex items-center gap-2 text-xs text-amber-900 font-bold">
          <span>🔥</span>
          <span>3-Day Practice Streak</span>
        </div>
      </div>
    </div>

    <!-- Trend Chart Card -->
    <div class="card bg-white !p-6 border border-[rgba(38,57,90,0.16)] space-y-4">
      <div class="flex items-center justify-between text-xs">
        <span class="font-bold text-stone-700">Placement Score Trend</span>
        <span class="text-emerald-600 font-mono font-bold">+1.4 pts improvement</span>
      </div>

      <!-- SVG Sparkline Trend -->
      <div class="w-full h-24 bg-stone-50 rounded-lg p-2 flex items-end">
        <svg class="w-full h-full" viewBox="0 0 500 100" fill="none">
          <path d="M 0 80 Q 100 65, 200 50 T 400 30 T 500 15" stroke="#f99d72" stroke-width="3" fill="none" />
          <circle cx="500" cy="15" r="5" fill="#f99d72" />
        </svg>
      </div>
    </div>

    <!-- Session Cards Grid -->
    <div class="space-y-3">
      <h3 class="text-sm font-bold text-[#1a1814]">Past Session Scorecards</h3>
      <div id="historyGrid" class="space-y-3">
        <!-- Injected via JS -->
      </div>
    </div>

  </main>

  <footer class="bg-white border-t border-stone-200 py-6 text-center text-xs text-stone-400">
    GD Arena · Practice the room before you enter it.
  </footer>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) window.lucide.createIcons();

      const defaultSessions = [
        { id: "1", date: "Oct 08, 2026", topic: "Should AI Replace Software Engineers in Campus Hiring?", score: 7.8, tier: "Strong", mode: "gd" },
        { id: "2", date: "Oct 07, 2026", topic: "High-Concurrency Distributed Caching 1-on-1 Interview", score: 6.9, tier: "Strong", mode: "interview" },
        { id: "3", date: "Oct 05, 2026", topic: "Is Remote Work Killing Junior Engineer Mentorship?", score: 5.8, tier: "Average", mode: "gd" }
      ];

      let history = [];
      try {
        history = JSON.parse(localStorage.getItem('gd_history') || '[]');
      } catch(e) {}
      if (!history.length) history = defaultSessions;

      const grid = document.getElementById('historyGrid');
      grid.innerHTML = history.map(s => `
        <div class="card bg-white !p-4 border border-[rgba(38,57,90,0.16)] flex items-center justify-between hover:border-[#f99d72] cursor-pointer" onclick="window.location.href='/pages/report.html?id=${s.id}'">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-stone-100 text-stone-600 uppercase font-semibold">${s.mode === 'gd' ? 'Group Discussion' : '1-on-1 Interview'}</span>
              <span class="text-[10px] font-mono text-stone-400">${s.date}</span>
            </div>
            <h4 class="font-bold text-xs text-[#1a1814]">${s.topic}</h4>
          </div>

          <div class="text-right">
            <div class="text-lg font-black text-[#1a1814]">${s.score}<span class="text-[10px] text-stone-400 font-normal">/10</span></div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${s.tier === 'Strong' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}">${s.tier}</span>
          </div>
        </div>
      `).join('');
    });
  </script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "history.html"), "w", encoding="utf-8") as f:
    f.write(history_html)

print("Phase 7 Report & History files created successfully!")
