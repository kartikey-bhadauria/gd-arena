import { SpeechAnalytics } from './fluency.js';
// GD Arena & Interview Room Live Voice Orchestration Engine
// STRICT VOICE RULE: Only one voice at a time. Student speech always wins.

import { PERSONAS, SESSION } from './config.js';
import { startSession, sendChat, getReport } from './api.js';
import { STT } from './stt.js';
import { TTS, speakerLock } from './tts.js';
import { VUMeter } from './vu-meter.js';
import { TurnManager } from './turn-manager.js';

export class RoomController {
  constructor(mode = 'gd') {
    this.mode = mode;
    this.sessionId = null;
    this.topic = localStorage.getItem('gd_selected_topic') || 'Should AI Replace Entry-Level Software Engineers?';
    this.transcript = [];
    this.secondsElapsed = 0;
    this.totalSeconds = 10 * 60; // Exact 10 mins timer
    this.warningCount = 0;
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
    this.analytics = new SpeechAnalytics({
      onUpdate: (stats) => this.updateFluencyUI(stats)
    });
    this.pendingThinkingTimeout = null;
  }

  async init() {
    this.setupUI();
    this.startTimer();

    // Start session on backend
    const res = await startSession(this.mode, this.topic, 4);
    if (res) {
      this.sessionId = res.session_id;
      this.addCaption(res.speaker, PERSONAS[res.speaker].name, res.opening, "00:05");
      
      // Auto-play opening speech (Moderator)
      setTimeout(() => {
        if (!speakerLock.isStudent) {
          this.tts.speak(res.opening, res.moderator_voice, "+0%", "+0Hz", res.speaker);
        }
      }, 600);
    }

    // Initialize Speech Recognition & Audio
    this.initSpeech();
  }

  setupUI() {
    const topicEl = document.getElementById('roomTopic');
    if (topicEl) topicEl.textContent = this.topic;

    // Mic toggle button
    const micBtn = document.getElementById('micToggleBtn');
    if (micBtn) {
      micBtn.addEventListener('click', () => this.toggleMic());
    }

    // Interrupt button (Student force claim)
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
        // As soon as student starts speaking, seize speakerLock and stop any AI audio instantly
        this.handleStudentBargeIn(false);
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
          // Instant barge-in: Student voice energy detected
          this.handleStudentBargeIn(false);
        },
        onSilence: () => {
          // Release student lock when student is finished speaking
          this.tts.releaseStudentLock();
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
      this.tts.releaseStudentLock();
      btn?.classList.remove('ring-4', 'ring-[#f99d72]', 'bg-emerald-600');
    }
  }

  // RULE: Student speech always wins — instantly pause and clear current audio on barge-in
  handleStudentBargeIn(isManualButton = false) {
    this.tts.stop(true); // byStudent = true
    this.hideThinkingState();
    this.clearActiveSpeaker();
    this.turnManager.noteStudentSpoke();
    this.analytics.processText(text);

    if (isManualButton) {
      this.showNudge("You claimed the floor. Speak now.");
      if (!this.isMicActive) this.toggleMic();
    }
  }

  async handleFinalSpeech(text) {
    if (!text || !text.trim()) return;
    this.lastStudentSpeechTs = this.secondsElapsed;
    this.turnManager.noteStudentSpoke();
    this.analytics.processText(text);

    const ts = this.formatTime(this.secondsElapsed);
    this.addCaption('student', 'You', text, ts);
    this.removeInterimCaption();

    // Release student lock so AI reply can queue/prepare
    this.tts.releaseStudentLock();

    // RULE: Thinking badge shows 800ms before TTS, but only if lock is free
    if (this.pendingThinkingTimeout) clearTimeout(this.pendingThinkingTimeout);
    
    this.pendingThinkingTimeout = setTimeout(() => {
      if (!speakerLock.isStudent) {
        this.showThinkingState();
      }
    }, Math.max(0, SESSION.reactionDelay - 800));

    // Natural cognitive pause before AI reply
    setTimeout(async () => {
      // Do not generate or play if student started talking again
      if (speakerLock.isStudent) {
        this.hideThinkingState();
        return;
      }

      const res = await sendChat(this.sessionId, text, false, ts);
      if (res) {
        this.hideThinkingState();

        // Check lock again before speaking
        if (!speakerLock.isStudent) {
          this.addCaption(res.speaker, res.persona, res.text, this.formatTime(this.secondsElapsed));
          this.tts.speak(res.text, res.voice, res.rate, res.pitch, res.speaker);
          this.turnManager.noteAISpoke(res.speaker);
          
          if (res.warnings) {
            this.warningCount = res.warnings;
            this.showNotice(res.warning_msg || `Conduct Warning ${this.warningCount}/5 issued.`);
          }

          if (res.rejected) {
            this.showNotice("Session Terminated: Exceeded 5 Conduct/Relevance Warnings.");
            this.stt.stop();
            const micBtn = document.getElementById('micToggleBtn');
            if (micBtn) micBtn.disabled = true;
            // Wait for rejection audio to finish then end
            setTimeout(() => this.endSession(), 4500);
          }
        }
      }
    }, SESSION.reactionDelay);
  }


  updateFluencyUI(stats) {
    const paceEl = document.getElementById('livePaceBadge');
    if (paceEl) {
      paceEl.textContent = `${stats.wpm} WPM (${stats.status}) · ${stats.fillerCount} Fillers`;
      if (stats.status === "Optimal Pace") {
        paceEl.className = "text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200";
      } else {
        paceEl.className = "text-[10px] font-mono px-2 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200";
      }
    }
  }

  showThinkingState() {
    if (!speakerLock.isStudent) {
      document.querySelectorAll('.thinking-badge').forEach(b => b.classList.remove('hidden'));
    }
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
    if (this.pendingThinkingTimeout) clearTimeout(this.pendingThinkingTimeout);
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
