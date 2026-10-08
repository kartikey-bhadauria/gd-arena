import os

BASE_DIR = r"C:\Users\Kartikey\gd-arena"

# 1. public/pages/mode-select.html
mode_select_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Choose Practice Mode — GD Arena</title>
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
      <div class="flex items-center gap-4 text-xs">
        <a href="/pages/history.html" class="text-stone-600 hover:text-stone-900 font-medium flex items-center gap-1.5">
          <i data-lucide="history" class="w-3.5 h-3.5"></i>
          <span>Past Sessions</span>
        </a>
        <div class="w-px h-4 bg-stone-200"></div>
        <span id="userChip" class="px-2.5 py-1 rounded-full bg-stone-100 text-stone-700 font-semibold text-[11px]">Candidate</span>
      </div>
    </div>
  </header>

  <!-- Main Grid -->
  <main class="max-w-5xl mx-auto px-4 py-10 w-full flex-1">
    
    <div class="text-center max-w-xl mx-auto mb-10 space-y-2">
      <h1 class="text-3xl font-extrabold tracking-tight text-[#1a1814]">Choose your practice mode</h1>
      <p class="text-xs text-stone-500">Practice full group discussion dynamics or undergo an intense 1-on-1 technical placement interrogation.</p>
    </div>

    <!-- Recommended Banner -->
    <div class="p-3.5 mb-8 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-between text-xs max-w-4xl mx-auto">
      <div class="flex items-center gap-2">
        <i data-lucide="sparkles" class="w-4 h-4 text-emerald-600"></i>
        <span class="text-emerald-900"><strong>Recommended for you:</strong> 4-Person Campus GD round with live speech barge-in.</span>
      </div>
      <a href="/pages/resume-upload.html" class="text-emerald-700 font-semibold underline text-[11px]">Update Resume Profile</a>
    </div>

    <!-- Mode Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
      
      <!-- Card 1: 1-on-1 Interview -->
      <div class="card bg-white !p-7 flex flex-col justify-between space-y-6 border border-[rgba(38,57,90,0.16)] hover:border-[#f99d72]">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center text-stone-800">
              <i data-lucide="user" class="w-6 h-6"></i>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-stone-100 text-stone-600">Medium</span>
              <span class="text-[10px] font-mono text-stone-400">~15 Min</span>
            </div>
          </div>

          <div>
            <h3 class="text-xl font-bold text-[#1a1814]">Live 1-on-1 Interview</h3>
            <p class="text-xs text-stone-500 mt-1 leading-relaxed">
              Practice HR, technical, or case interviews with Ms. Kapoor who adapts questions directly to your uploaded resume.
            </p>
          </div>

          <div class="p-3 rounded-lg bg-stone-50 border border-stone-100 space-y-1.5 text-xs">
            <span class="text-[10px] uppercase font-bold text-stone-400">Sample Scenarios:</span>
            <ul class="text-[11px] text-stone-600 space-y-1 list-disc list-inside">
              <li>High-Concurrency Backend Scalability & Latency</li>
              <li>Distributed Database Sharding & Caching Failures</li>
              <li>Behavioral Conflict & Team Deadlocks</li>
            </ul>
          </div>
        </div>

        <button onclick="startMode('interview')" class="btn-primary w-full !py-3 !text-xs !justify-center">
          <span>Start 1-on-1 Interview</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </button>
      </div>

      <!-- Card 2: Group Discussion -->
      <div class="card bg-white !p-7 flex flex-col justify-between space-y-6 border border-[rgba(38,57,90,0.16)] hover:border-[#f99d72] relative overflow-hidden">
        <div class="absolute top-0 right-0 bg-[#f99d72] text-[#1a1814] text-[9px] font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">
          Most Popular
        </div>

        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="w-12 h-12 rounded-xl bg-stone-900 flex items-center justify-center text-white">
              <i data-lucide="users" class="w-6 h-6"></i>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-red-50 text-red-600">Hard</span>
              <span class="text-[10px] font-mono text-stone-400">8 Min</span>
            </div>
          </div>

          <div>
            <h3 class="text-xl font-bold text-[#1a1814]">Group Discussion (Panel)</h3>
            <p class="text-xs text-stone-500 mt-1 leading-relaxed">
              Sit in a real GD with 4 distinct AI participants (Aarav, Priya, Rohan, Neha) + 1 moderator (Mr. Verma).
            </p>
          </div>

          <div class="p-3 rounded-lg bg-stone-50 border border-stone-100 space-y-1.5 text-xs">
            <span class="text-[10px] uppercase font-bold text-stone-400">Select Topic:</span>
            <select id="gdTopicSelect" class="w-full p-2 bg-white rounded border border-stone-200 text-xs font-medium text-stone-800">
              <option value="Should AI Replace Software Engineers in Campus Hiring?">Should AI Replace Software Engineers in Campus Hiring?</option>
              <option value="Is Remote Work Hurting Engineering Culture and Innovation?">Is Remote Work Hurting Engineering Culture & Innovation?</option>
              <option value="Monolith vs Microservices for Early Stage Startups">Monolith vs Microservices for Early Stage Startups</option>
              <option value="Should Engineering Colleges Eliminate CGPA Filters?">Should Engineering Colleges Eliminate CGPA Filters?</option>
            </select>
          </div>
        </div>

        <button onclick="startMode('gd')" class="btn-primary w-full !py-3 !text-xs !justify-center">
          <span>Start GD Simulation Room</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </button>
      </div>

    </div>

    <!-- History Link Footer -->
    <div class="text-center mt-12">
      <a href="/pages/history.html" class="text-xs text-stone-500 hover:text-stone-900 font-medium underline">
        View your past placement performance reports & trends →
      </a>
    </div>

  </main>

  <footer class="py-4 text-center text-[11px] text-stone-400">
    GD Arena · All AI voices and behaviors simulate real campus placement interviewers.
  </footer>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) window.lucide.createIcons();
      const user = JSON.parse(localStorage.getItem('gd_user') || '{}');
      if (user.name) {
        document.getElementById('userChip').textContent = user.name;
      }
    });

    function startMode(mode) {
      if (mode === 'interview') {
        window.location.href = '/pages/interview-room.html';
      } else {
        const topic = document.getElementById('gdTopicSelect').value;
        localStorage.setItem('gd_selected_topic', topic);
        window.location.href = '/pages/gd-room.html';
      }
    }
  </script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "mode-select.html"), "w", encoding="utf-8") as f:
    f.write(mode_select_html)

# 2. public/js/stt.js
stt_js = """// Web Speech API STT Wrapper

export class STT {
  constructor({ onInterim, onFinal, onError }) {
    this.onInterim = onInterim || (() => {});
    this.onFinal = onFinal || (() => {});
    this.onError = onError || (() => {});
    this.recognition = null;
    this.active = false;
    this.init();
  }

  isSupported() {
    return ('webkitSpeechRecognition' in window) || ('SpeechRecognition' in window);
  }

  init() {
    const SpeechClass = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechClass) return;

    this.recognition = new SpeechClass();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-IN';

    this.recognition.onresult = (event) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          this.onFinal(transcript.trim());
        } else {
          interim += transcript;
        }
      }
      if (interim) {
        this.onInterim(interim.trim());
      }
    };

    this.recognition.onerror = (event) => {
      console.warn('STT Error:', event.error);
      if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
        this.onError('mic_denied');
      } else {
        this.onError(event.error);
      }
    };

    this.recognition.onend = () => {
      if (this.active) {
        try {
          this.recognition.start();
        } catch (e) {
          // Restart gracefully
        }
      }
    };
  }

  start() {
    if (!this.recognition) return;
    this.active = true;
    try {
      this.recognition.start();
    } catch (e) {
      console.log('STT already started');
    }
  }

  stop() {
    this.active = false;
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "stt.js"), "w", encoding="utf-8") as f:
    f.write(stt_js)

# 3. public/js/tts.js
tts_js = """// Neural TTS Player & Instant Barge-In Handler

import { getTTS } from './api.js';

export class TTS {
  constructor({ onStart, onEnd } = {}) {
    this.onStart = onStart || (() => {});
    this.onEnd = onEnd || (() => {});
    this.currentAudio = null;
    this.playing = false;
  }

  isPlaying() {
    return this.playing;
  }

  stop() {
    if (this.currentAudio) {
      try {
        this.currentAudio.pause();
        this.currentAudio.currentTime = 0;
      } catch (e) {}
      this.currentAudio = null;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (this.playing) {
      this.playing = false;
      this.onEnd();
    }
  }

  async speak(text, voice = 'en-IN-PrabhatNeural', rate = '+0%', pitch = '+0Hz', speaker = 'aarav') {
    this.stop(); // Stop any previous audio immediately
    this.playing = true;
    this.onStart(speaker);

    try {
      const blob = await getTTS(text, voice, rate, pitch, speaker);
      if (blob && blob.size > 100) {
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        this.currentAudio = audio;

        audio.onended = () => {
          this.playing = false;
          this.currentAudio = null;
          this.onEnd(speaker);
        };

        audio.onerror = () => {
          this.fallbackSpeechSynthesis(text);
        };

        await audio.play();
        return;
      }
    } catch (err) {
      console.warn('TTS streaming failed, falling back to Web Speech Synthesis:', err);
    }

    this.fallbackSpeechSynthesis(text);
  }

  fallbackSpeechSynthesis(text) {
    if (!('speechSynthesis' in window)) {
      this.playing = false;
      this.onEnd();
      return;
    }

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-IN';
    utter.rate = 1.05;
    utter.onend = () => {
      this.playing = false;
      this.onEnd();
    };
    utter.onerror = () => {
      this.playing = false;
      this.onEnd();
    };
    window.speechSynthesis.speak(utter);
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "tts.js"), "w", encoding="utf-8") as f:
    f.write(tts_js)

# 4. public/js/vu-meter.js
vu_meter_js = """// Web Audio API VU Energy Meter and Instant Voice Barge-In Detector

export class VUMeter {
  constructor(stream, { onLevel, onSilence, onSpeech }) {
    this.stream = stream;
    this.onLevel = onLevel || (() => {});
    this.onSilence = onSilence || (() => {});
    this.onSpeech = onSpeech || (() => {});

    this.audioCtx = null;
    this.analyser = null;
    this.source = null;
    this.animFrame = null;
    this.silenceTimer = null;
    this.isSpeaking = false;
  }

  start() {
    try {
      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 256;
      this.source = this.audioCtx.createMediaStreamSource(this.stream);
      this.source.connect(this.analyser);

      const bufferLength = this.analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const checkVolume = () => {
        this.analyser.getByteFrequencyData(dataArray);
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const avg = sum / bufferLength;
        const level = Math.min(100, Math.round((avg / 128) * 100));

        this.onLevel(level);

        // Speech Energy Threshold for Barge-In
        if (level > 25) {
          if (!this.isSpeaking) {
            this.isSpeaking = true;
            this.onSpeech();
          }
          if (this.silenceTimer) {
            clearTimeout(this.silenceTimer);
            this.silenceTimer = null;
          }
        } else if (this.isSpeaking) {
          if (!this.silenceTimer) {
            this.silenceTimer = setTimeout(() => {
              this.isSpeaking = false;
              this.onSilence();
              this.silenceTimer = null;
            }, 900); // 900ms silence threshold
          }
        }

        this.animFrame = requestAnimationFrame(checkVolume);
      };

      checkVolume();
    } catch (e) {
      console.warn('VUMeter initialization error:', e);
    }
  }

  stop() {
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
    if (this.silenceTimer) clearTimeout(this.silenceTimer);
    if (this.audioCtx) {
      try { this.audioCtx.close(); } catch(e) {}
    }
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "vu-meter.js"), "w", encoding="utf-8") as f:
    f.write(vu_meter_js)

# 5. public/js/turn-manager.js
turn_manager_js = """// Client-Side Turn Management state mirror

export class TurnManager {
  constructor() {
    this.aiTurnsInARow = 0;
    this.lastSpeaker = null;
    this.turnCount = 0;
  }

  noteStudentSpoke() {
    this.aiTurnsInARow = 0;
    this.lastSpeaker = "student";
  }

  noteAISpoke(speakerKey) {
    this.aiTurnsInARow++;
    this.turnCount++;
    this.lastSpeaker = speakerKey;
  }

  shouldInviteStudent() {
    return this.aiTurnsInARow >= 2;
  }

  reset() {
    this.aiTurnsInARow = 0;
    this.lastSpeaker = null;
    this.turnCount = 0;
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "turn-manager.js"), "w", encoding="utf-8") as f:
    f.write(turn_manager_js)

# 6. public/js/room.js
room_js = """// GD Arena & Interview Room Live Voice Orchestration Engine

import { PERSONAS, SESSION } from './config.js';
import { startSession, sendChat, getReport } from './api.js';
import { STT } from './stt.js';
import { TTS } from './tts.js';
import { VUMeter } from './vu-meter.js';
import { TurnManager } from './turn-manager.js';

export class RoomController {
  constructor(mode = 'gd') {
    this.mode = mode;
    this.sessionId = null;
    this.topic = localStorage.getItem('gd_selected_topic') || 'Should AI Replace Entry-Level Software Engineers?';
    this.transcript = [];
    this.secondsElapsed = 0;
    this.totalSeconds = mode === 'interview' ? 15 * 60 : 8 * 60;
    this.timerInterval = null;

    this.turnManager = new TurnManager();
    this.tts = new TTS({
      onStart: (spk) => this.setActiveSpeaker(spk),
      onEnd: () => this.clearActiveSpeaker()
    });
    this.stt = null;
    this.vuMeter = null;
    this.micStream = null;
    this.isMicActive = false;
    this.lastStudentSpeechTs = 0;
  }

  async init() {
    this.setupUI();
    this.startTimer();

    // Start session on backend
    const res = await startSession(this.mode, this.topic, 4);
    if (res) {
      this.sessionId = res.session_id;
      this.addCaption(res.speaker, PERSONAS[res.speaker].name, res.opening, "00:05");
      
      // Auto-play opening speech
      setTimeout(() => {
        this.tts.speak(res.opening, res.moderator_voice, "+0%", "+0Hz", res.speaker);
      }, 600);
    }

    // Initialize Speech Recognition & Audio
    this.initSpeech();
  }

  setupUI() {
    const topicEl = document.getElementById('roomTopic');
    if (topicEl) topicEl.textContent = this.topic;

    // Mic button
    const micBtn = document.getElementById('micToggleBtn');
    if (micBtn) {
      micBtn.addEventListener('click', () => this.toggleMic());
    }

    // Interrupt button
    const intBtn = document.getElementById('interruptBtn');
    if (intBtn) {
      intBtn.addEventListener('click', () => this.handleStudentBargeIn(true));
    }

    // End session button
    const endBtn = document.getElementById('endSessionBtn');
    if (endBtn) {
      endBtn.addEventListener('click', () => this.endSession());
    }

    // Text input fallback form
    const textForm = document.getElementById('textInputForm');
    if (textForm) {
      textForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = document.getElementById('chatInput');
        if (input && input.value.trim()) {
          this.handleFinalSpeech(input.value.trim());
          input.value = '';
        }
      });
    }
  }

  async initSpeech() {
    this.stt = new STT({
      onInterim: (text) => {
        this.showInterimCaption(text);
      },
      onFinal: (text) => {
        this.handleFinalSpeech(text);
      },
      onError: (err) => {
        if (err === 'mic_denied') {
          this.showNotice('Microphone access denied. Text fallback enabled.');
          document.getElementById('textFallbackBar')?.classList.remove('hidden');
        }
      }
    });

    try {
      this.micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.vuMeter = new VUMeter(this.micStream, {
        onLevel: (lvl) => this.updateVULevel(lvl),
        onSpeech: () => {
          // Instant barge-in if AI is currently speaking
          if (this.tts.isPlaying()) {
            this.handleStudentBargeIn(false);
          }
        },
        onSilence: () => {
          // AI turn check after student finishes
        }
      });
      this.vuMeter.start();
    } catch (e) {
      console.warn('Microphone permission not granted:', e);
      document.getElementById('textFallbackBar')?.classList.remove('hidden');
    }
  }

  toggleMic() {
    const btn = document.getElementById('micToggleBtn');
    if (!this.isMicActive) {
      this.stt.start();
      this.isMicActive = true;
      btn?.classList.add('ring-4', 'ring-[#f99d72]', 'bg-emerald-600');
    } else {
      this.stt.stop();
      this.isMicActive = false;
      btn?.classList.remove('ring-4', 'ring-[#f99d72]', 'bg-emerald-600');
    }
  }

  handleStudentBargeIn(isManualButton = false) {
    if (this.tts.isPlaying()) {
      this.tts.stop();
      this.showNudge("You interrupted firmly. Maintain constructive composure.");
      this.turnManager.noteStudentSpoke();
    }
    if (isManualButton && !this.isMicActive) {
      this.toggleMic();
    }
  }

  async handleFinalSpeech(text) {
    if (!text) return;
    this.lastStudentSpeechTs = this.secondsElapsed;
    this.turnManager.noteStudentSpoke();

    const ts = this.formatTime(this.secondsElapsed);
    this.addCaption('student', 'You', text, ts);
    this.removeInterimCaption();

    // Show thinking indicator on next speaker card 800ms early
    this.showThinkingState();

    // Natural 1350ms cognitive delay before AI replies
    setTimeout(async () => {
      const res = await sendChat(this.sessionId, text, false, ts);
      if (res) {
        this.hideThinkingState();
        this.addCaption(res.speaker, res.persona, res.text, this.formatTime(this.secondsElapsed));
        this.tts.speak(res.text, res.voice, res.rate, res.pitch, res.speaker);
        this.turnManager.noteAISpoke(res.speaker);
      }
    }, SESSION.reactionDelay);
  }

  showThinkingState() {
    document.querySelectorAll('.thinking-badge').forEach(b => b.classList.remove('hidden'));
  }

  hideThinkingState() {
    document.querySelectorAll('.thinking-badge').forEach(b => b.classList.add('hidden'));
  }

  setActiveSpeaker(speakerKey) {
    document.querySelectorAll('.participant-card').forEach(c => c.classList.remove('active-speaker'));
    const card = document.getElementById(`card-${speakerKey}`);
    if (card) {
      card.classList.add('active-speaker');
    }
  }

  clearActiveSpeaker() {
    document.querySelectorAll('.participant-card').forEach(c => c.classList.remove('active-speaker'));
  }

  updateVULevel(level) {
    const fill = document.getElementById('userVUFill');
    if (fill) {
      fill.style.width = `${level}%`;
    }
  }

  addCaption(speakerKey, name, text, ts) {
    const feed = document.getElementById('captionFeed');
    if (!feed) return;

    const persona = PERSONAS[speakerKey] || { color: '#1a1814' };
    const div = document.createElement('div');
    div.className = "p-2 rounded bg-stone-50 border border-stone-100 text-xs leading-relaxed";
    div.innerHTML = `
      <div class="flex items-center gap-2 mb-0.5">
        <span class="font-mono text-[10px] text-stone-400">[${ts}]</span>
        <span class="font-bold text-[11px]" style="color: ${persona.color}">${name}:</span>
      </div>
      <p class="text-stone-800">${text}</p>
    `;
    feed.appendChild(div);
    feed.scrollTop = feed.scrollHeight;

    this.transcript.push({ speaker: speakerKey, name, text, timestamp: ts });
  }

  showInterimCaption(text) {
    let interimEl = document.getElementById('interimCaption');
    if (!interimEl) {
      interimEl = document.createElement('div');
      interimEl.id = 'interimCaption';
      interimEl.className = "p-2 rounded bg-stone-100 text-xs italic text-stone-500 border border-dashed border-stone-200";
      document.getElementById('captionFeed')?.appendChild(interimEl);
    }
    interimEl.textContent = `You: ${text}...`;
  }

  removeInterimCaption() {
    document.getElementById('interimCaption')?.remove();
  }

  showNudge(msg) {
    const box = document.getElementById('nudgeBox');
    if (box) {
      box.textContent = msg;
      box.classList.remove('hidden');
      setTimeout(() => box.classList.add('hidden'), 5000);
    }
  }

  showNotice(msg) {
    this.showNudge(msg);
  }

  startTimer() {
    this.timerInterval = setInterval(() => {
      this.secondsElapsed++;
      const timerEl = document.getElementById('roomTimer');
      if (timerEl) {
        timerEl.textContent = `${this.formatTime(this.secondsElapsed)} / ${this.formatTime(this.totalSeconds)}`;
      }

      // Check phase
      const phaseEl = document.getElementById('roomPhase');
      if (phaseEl) {
        if (this.secondsElapsed < 60) phaseEl.textContent = "Opening";
        else if (this.secondsElapsed < this.totalSeconds - 90) phaseEl.textContent = "Discussion";
        else phaseEl.textContent = "Closing";
      }

      // Silent Nudge check: 150s of silence from student
      if (this.secondsElapsed - this.lastStudentSpeechTs > 150 && this.lastStudentSpeechTs > 0) {
        this.showNudge("You haven't spoken in 2:30 — Aarav is dominating the floor.");
      }

      // Auto-end session when time expires
      if (this.secondsElapsed >= this.totalSeconds) {
        this.endSession();
      }
    }, 1000);
  }

  formatTime(secs) {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  async endSession() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.tts.stop();
    this.stt?.stop();
    this.vuMeter?.stop();

    // Fetch report from server
    const report = await getReport(this.sessionId, this.transcript);
    if (report) {
      sessionStorage.setItem('current_report', JSON.stringify(report));
    }
    window.location.href = `/pages/report.html?id=${this.sessionId || 'demo'}`;
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "room.js"), "w", encoding="utf-8") as f:
    f.write(room_js)

# 7. public/pages/interview-room.html
interview_room_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>1-on-1 Placement Interview — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-[#fafaf9] min-h-screen text-[#1a1814] flex flex-col justify-between">

  <!-- Top Navigation Bar -->
  <header class="bg-white border-b border-[rgba(38,57,90,0.1)] py-3 sticky top-0 z-20">
    <div class="max-w-7xl mx-auto px-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/pages/mode-select.html" class="text-stone-400 hover:text-stone-700">
          <i data-lucide="arrow-left" class="w-4 h-4"></i>
        </a>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
          <span class="font-bold text-xs uppercase tracking-wider text-stone-700">1-on-1 Interview</span>
        </div>
        <div class="w-px h-4 bg-stone-200"></div>
        <span id="roomPhase" class="px-2 py-0.5 rounded-full bg-stone-100 text-stone-600 font-mono text-[10px]">Technical Round</span>
      </div>

      <!-- Center Timer -->
      <div class="flex items-center gap-2 font-mono text-xs text-stone-600 bg-stone-50 px-3 py-1 rounded-full border border-stone-200">
        <i data-lucide="clock" class="w-3.5 h-3.5 text-[#f99d72]"></i>
        <span id="roomTimer">00:00 / 15:00</span>
      </div>

      <!-- End Session -->
      <button id="endSessionBtn" class="btn-secondary !py-1.5 !px-3.5 !text-xs !bg-red-50 !text-red-700 !border-red-200 hover:!bg-red-100">
        <i data-lucide="phone-off" class="w-3.5 h-3.5"></i>
        <span>End Interview</span>
      </button>
    </div>
  </header>

  <!-- Main Room Layout -->
  <main class="max-w-7xl mx-auto px-4 py-6 w-full flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    
    <!-- Left Column: Interviewer Panel (30%) -->
    <div class="lg:col-span-4 space-y-4">
      <div id="card-interviewer" class="participant-card card bg-white !p-6 space-y-4 border border-[rgba(38,57,90,0.16)]">
        <div class="flex items-center gap-3">
          <div class="w-14 h-14 rounded-full bg-stone-900 text-white font-black flex items-center justify-center text-lg">
            MK
          </div>
          <div>
            <h3 class="font-bold text-base text-[#1a1814]">Ms. Kapoor</h3>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-stone-100 text-stone-700 font-semibold">Lead Technical Evaluator</span>
          </div>
        </div>

        <div class="p-3 rounded bg-stone-50 border border-stone-100 text-xs text-stone-600 space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-semibold text-stone-800">Interviewer Status:</span>
            <span class="thinking-badge hidden">Evaluating logic...</span>
          </div>
          <p class="text-[11px] text-stone-500">Adapts technical depth to your stated resume projects.</p>
        </div>

        <div class="text-xs text-stone-500">
          <span class="font-semibold text-stone-700">Question Progression:</span>
          <div class="w-full bg-stone-100 h-1.5 rounded-full overflow-hidden mt-1.5">
            <div class="bg-[#f99d72] h-full" style="width: 35%"></div>
          </div>
        </div>
      </div>

      <!-- Candidate Microphone Meter -->
      <div class="card bg-white !p-4 space-y-2 border border-emerald-500/20">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold text-emerald-900">Your Voice Energy (VU)</span>
          <span class="text-[10px] text-stone-400 font-mono">Real-Time</span>
        </div>
        <div class="w-full h-2 bg-stone-100 rounded-full overflow-hidden">
          <div id="userVUFill" class="h-full bg-emerald-500 transition-all duration-75" style="width: 0%"></div>
        </div>
      </div>
    </div>

    <!-- Center Column: Live Caption Feed (55%) -->
    <div class="lg:col-span-8 space-y-4">
      
      <!-- Silent Nudge Box -->
      <div id="nudgeBox" class="nudge hidden w-full justify-between">
        <span class="flex items-center gap-1.5">
          <i data-lucide="alert-circle" class="w-3.5 h-3.5"></i>
          <span id="nudgeText">Be direct. Avoid filler phrases when explaining system bottlenecks.</span>
        </span>
      </div>

      <!-- Captions Container -->
      <div class="card bg-white !p-4 border border-[rgba(38,57,90,0.16)] flex flex-col h-[480px]">
        <div class="flex items-center justify-between pb-3 border-b border-stone-100 text-xs">
          <div class="flex items-center gap-2">
            <i data-lucide="subtitles" class="w-4 h-4 text-stone-400"></i>
            <span class="font-bold text-stone-800">Live Interview Transcript Feed</span>
          </div>
          <span class="text-[10px] font-mono text-stone-400">Speech-to-Text active</span>
        </div>

        <!-- Scrollable Feed -->
        <div id="captionFeed" class="flex-1 overflow-y-auto space-y-2.5 py-3 pr-1 custom-scrollbar">
          <!-- Live captions injected here -->
        </div>

        <!-- Text Input Fallback Bar -->
        <div id="textFallbackBar" class="pt-3 border-t border-stone-100">
          <form id="textInputForm" class="flex items-center gap-2">
            <input type="text" id="chatInput" placeholder="Type your spoken answer if mic is disabled..." class="flex-1 px-3.5 py-2 rounded-lg border border-stone-200 text-xs focus:ring-2 focus:ring-[#f99d72] focus:outline-none">
            <button type="submit" class="btn-primary !py-2 !px-4 !text-xs">
              <span>Send</span>
              <i data-lucide="send" class="w-3 h-3"></i>
            </button>
          </form>
        </div>
      </div>

    </div>

  </main>

  <!-- Bottom Voice Control Bar -->
  <footer class="bg-white border-t border-[rgba(38,57,90,0.1)] py-4 sticky bottom-0 z-20">
    <div class="max-w-4xl mx-auto px-4 flex items-center justify-between">
      <div class="text-xs text-stone-500">
        <span class="font-semibold text-stone-700">Interview Mode:</span> Voice barge-in active
      </div>

      <!-- Large Center Mic Button -->
      <div class="flex items-center gap-4">
        <button id="micToggleBtn" class="w-14 h-14 rounded-full bg-[#f99d72] text-[#1a1814] flex items-center justify-center shadow-lg hover:scale-105 transition-all">
          <i data-lucide="mic" class="w-6 h-6"></i>
        </button>
      </div>

      <div class="flex items-center gap-2">
        <span class="text-[10px] text-stone-400">Press Mic to Speak / Stop</span>
      </div>
    </div>
  </footer>

  <script type="module">
    import { RoomController } from '/js/room.js';
    document.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) window.lucide.createIcons();
      const controller = new RoomController('interview');
      controller.init();
    });
  </script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "interview-room.html"), "w", encoding="utf-8") as f:
    f.write(interview_room_html)

# 8. public/pages/gd-room.html
gd_room_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Group Discussion Simulation Room — GD Arena</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body class="bg-[#fafaf9] min-h-screen text-[#1a1814] flex flex-col justify-between">

  <!-- Top Navigation Bar -->
  <header class="bg-white border-b border-[rgba(38,57,90,0.1)] py-3 sticky top-0 z-20">
    <div class="max-w-7xl mx-auto px-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/pages/mode-select.html" class="text-stone-400 hover:text-stone-700">
          <i data-lucide="arrow-left" class="w-4 h-4"></i>
        </a>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
          <span class="font-bold text-xs uppercase tracking-wider text-stone-700">GD Arena #47</span>
        </div>
        <div class="w-px h-4 bg-stone-200"></div>
        <span id="roomPhase" class="px-2 py-0.5 rounded-full bg-stone-100 text-stone-600 font-mono text-[10px]">Opening</span>
      </div>

      <!-- Center Timer -->
      <div class="flex items-center gap-2 font-mono text-xs text-stone-600 bg-stone-50 px-3 py-1 rounded-full border border-stone-200">
        <i data-lucide="clock" class="w-3.5 h-3.5 text-[#f99d72]"></i>
        <span id="roomTimer">00:00 / 08:00</span>
      </div>

      <!-- End Session -->
      <button id="endSessionBtn" class="btn-secondary !py-1.5 !px-3.5 !text-xs !bg-red-50 !text-red-700 !border-red-200 hover:!bg-red-100">
        <i data-lucide="phone-off" class="w-3.5 h-3.5"></i>
        <span>End GD</span>
      </button>
    </div>
  </header>

  <!-- Topic Header Strip -->
  <div class="bg-stone-50 border-b border-stone-200 py-2.5 px-4 text-center">
    <div class="max-w-4xl mx-auto flex items-center justify-center gap-2 text-xs">
      <span class="font-bold text-stone-400 uppercase text-[10px]">Topic:</span>
      <span id="roomTopic" class="font-semibold text-stone-900">Should AI Replace Entry-Level Software Engineers in Campus Hiring?</span>
    </div>
  </div>

  <!-- Main Multi-Agent Stage Grid -->
  <main class="max-w-7xl mx-auto px-4 py-6 w-full flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    
    <!-- Left: 6-Participant Grid (60%) -->
    <div class="lg:col-span-7 space-y-4">
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        
        <!-- You (Candidate) -->
        <div id="card-student" class="participant-card card bg-white !p-4 border-2 border-emerald-500/30 flex flex-col justify-between h-36">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-emerald-950">You (Candidate)</span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700">Ready</span>
          </div>
          <div class="space-y-1">
            <div class="w-full bg-stone-100 h-1.5 rounded-full overflow-hidden">
              <div id="userVUFill" class="bg-emerald-500 h-full" style="width: 0%"></div>
            </div>
            <p class="text-[10px] text-stone-400 truncate">Speak to make your point...</p>
          </div>
        </div>

        <!-- Mr. Verma (Moderator) -->
        <div id="card-moderator" class="participant-card card bg-white !p-4 border border-stone-200 flex flex-col justify-between h-36">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-bold text-xs text-stone-900">Mr. Verma</h4>
              <span class="text-[9px] text-stone-500">Moderator</span>
            </div>
            <span class="thinking-badge hidden">Managing</span>
          </div>
          <p class="text-[10px] text-stone-600 line-clamp-2">"Keep turns concise and respectful."</p>
        </div>

        <!-- Aarav (Dominator) -->
        <div id="card-aarav" class="participant-card card bg-white !p-4 border border-red-500/30 flex flex-col justify-between h-36">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-bold text-xs text-red-900">Aarav</h4>
              <span class="text-[9px] text-red-600">The Dominator</span>
            </div>
            <span class="thinking-badge hidden">Countering</span>
          </div>
          <p class="text-[10px] text-stone-600 line-clamp-2">"Production benchmarks prove otherwise."</p>
        </div>

        <!-- Priya (Data-Driven) -->
        <div id="card-priya" class="participant-card card bg-white !p-4 border border-cyan-500/30 flex flex-col justify-between h-36">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-bold text-xs text-cyan-900">Priya</h4>
              <span class="text-[9px] text-cyan-700">Data-Driven</span>
            </div>
            <span class="thinking-badge hidden">Calculating</span>
          </div>
          <p class="text-[10px] text-stone-600 line-clamp-2">"74% of enterprise teams report latency spikes."</p>
        </div>

        <!-- Rohan (Synthesizer) -->
        <div id="card-rohan" class="participant-card card bg-white !p-4 border border-amber-500/30 flex flex-col justify-between h-36">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-bold text-xs text-amber-900">Rohan</h4>
              <span class="text-[9px] text-amber-700">Synthesizer</span>
            </div>
            <span class="thinking-badge hidden">Synthesizing</span>
          </div>
          <p class="text-[10px] text-stone-600 line-clamp-2">"Let's bridge Candidate 4's idea with Priya's data."</p>
        </div>

        <!-- Neha (Quiet Thinker) -->
        <div id="card-neha" class="participant-card card bg-white !p-4 border border-purple-500/30 flex flex-col justify-between h-36">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-bold text-xs text-purple-900">Neha</h4>
              <span class="text-[9px] text-purple-700">Quiet Thinker</span>
            </div>
            <span class="thinking-badge hidden">Analyzing</span>
          </div>
          <p class="text-[10px] text-stone-600 line-clamp-2">"What is the first-principles constraint here?"</p>
        </div>

      </div>

      <!-- Silent In-Session Nudge Bar -->
      <div id="nudgeBox" class="nudge hidden w-full justify-between">
        <span class="flex items-center gap-1.5">
          <i data-lucide="alert-circle" class="w-3.5 h-3.5 text-amber-600"></i>
          <span>You haven't spoken in 2:40 — Aarav is dominating the floor.</span>
        </span>
      </div>
    </div>

    <!-- Right: Captions Feed & Controls (40%) -->
    <div class="lg:col-span-5 space-y-4">
      <div class="card bg-white !p-4 border border-[rgba(38,57,90,0.16)] flex flex-col h-[460px]">
        <div class="flex items-center justify-between pb-3 border-b border-stone-100 text-xs">
          <div class="flex items-center gap-2">
            <i data-lucide="subtitles" class="w-4 h-4 text-stone-400"></i>
            <span class="font-bold text-stone-800">Live GD Dialogue Stream</span>
          </div>
          <span class="text-[10px] font-mono text-stone-400">AI Transcript</span>
        </div>

        <div id="captionFeed" class="flex-1 overflow-y-auto space-y-2 py-3 pr-1 custom-scrollbar">
          <!-- Spoken captions injected here -->
        </div>

        <!-- Text Fallback -->
        <div id="textFallbackBar" class="pt-3 border-t border-stone-100">
          <form id="textInputForm" class="flex items-center gap-2">
            <input type="text" id="chatInput" placeholder="Type text argument if mic is disabled..." class="flex-1 px-3.5 py-2 rounded-lg border border-stone-200 text-xs focus:ring-2 focus:ring-[#f99d72] focus:outline-none">
            <button type="submit" class="btn-primary !py-2 !px-4 !text-xs">
              <span>Send</span>
              <i data-lucide="send" class="w-3 h-3"></i>
            </button>
          </form>
        </div>
      </div>
    </div>

  </main>

  <!-- Bottom Voice Bar -->
  <footer class="bg-white border-t border-[rgba(38,57,90,0.1)] py-4 sticky bottom-0 z-20">
    <div class="max-w-4xl mx-auto px-4 flex items-center justify-between">
      <div class="text-xs text-stone-500">
        <span class="font-semibold text-stone-700">Barge-in:</span> Active (Speak anytime to claim floor)
      </div>

      <!-- Center Controls -->
      <div class="flex items-center gap-4">
        <button id="interruptBtn" class="btn-secondary !text-xs !py-2 !px-4 !bg-amber-50 !text-amber-800 !border-amber-200">
          <i data-lucide="hand" class="w-3.5 h-3.5"></i>
          <span>Interrupt AI</span>
        </button>

        <button id="micToggleBtn" class="w-14 h-14 rounded-full bg-[#f99d72] text-[#1a1814] flex items-center justify-center shadow-lg hover:scale-105 transition-all">
          <i data-lucide="mic" class="w-6 h-6"></i>
        </button>
      </div>

      <div class="text-xs text-stone-400">
        All peers are autonomous AI agents
      </div>
    </div>
  </footer>

  <script type="module">
    import { RoomController } from '/js/room.js';
    document.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) window.lucide.createIcons();
      const controller = new RoomController('gd');
      controller.init();
    });
  </script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR, "public", "pages", "gd-room.html"), "w", encoding="utf-8") as f:
    f.write(gd_room_html)

print("Phase 6 Mode & Room files created successfully!")
