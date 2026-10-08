// Strict Single-Speaker Lock & Neural TTS Player
// VOICE RULE: Only one voice plays at a time. Student always wins. Never talk over student.

import { getTTS } from './api.js';

export const speakerLock = {
  active: false,
  currentSpeaker: null,
  isStudent: false,
  queue: []
};

export class TTS {
  constructor({ onStart, onEnd } = {}) {
    this.onStart = onStart || (() => {});
    this.onEnd = onEnd || (() => {});
    this.currentAudio = null;
    this.playing = false;
  }

  isPlaying() {
    return this.playing || speakerLock.active;
  }

  // Student speech or barge-in always wins: immediately pause & clear audio & queue
  stop(byStudent = false) {
    if (this.currentAudio) {
      try {
        this.currentAudio.pause();
        this.currentAudio.currentTime = 0;
      } catch (e) {}
      this.currentAudio = null;
    }
    if (window.speechSynthesis) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }

    this.playing = false;

    if (byStudent) {
      speakerLock.active = true;
      speakerLock.currentSpeaker = 'student';
      speakerLock.isStudent = true;
      speakerLock.queue = []; // Clear pending AI turns
    } else if (!speakerLock.isStudent) {
      speakerLock.active = false;
      speakerLock.currentSpeaker = null;
    }

    this.onEnd();
  }

  // Unlock when student finishes speaking
  releaseStudentLock() {
    if (speakerLock.isStudent) {
      speakerLock.active = false;
      speakerLock.currentSpeaker = null;
      speakerLock.isStudent = false;
      this.drainQueue();
    }
  }

  async speak(text, voice = 'en-IN-PrabhatNeural', rate = '+0%', pitch = '+0Hz', speaker = 'aarav') {
    if (!text || !text.trim()) return;

    // RULE: If student is actively speaking, NEVER play AI and NEVER talk over student
    if (speakerLock.isStudent) {
      console.log(`[VoiceRule] AI ${speaker} suppressed: Student is currently speaking.`);
      return;
    }

    // RULE: Moderator can interrupt other AI, but never the student
    if (speakerLock.active && speakerLock.currentSpeaker !== 'student') {
      if (speaker === 'moderator' || speaker === 'interviewer') {
        console.log(`[VoiceRule] Moderator/Interviewer preempting AI ${speakerLock.currentSpeaker}`);
        this.stop(false);
      } else {
        console.log(`[VoiceRule] Lock busy with ${speakerLock.currentSpeaker}. Queuing ${speaker}.`);
        speakerLock.queue.push({ text, voice, rate, pitch, speaker });
        return;
      }
    } else if (speakerLock.active && speakerLock.isStudent) {
      console.log(`[VoiceRule] Lock held by Student. Dropping AI turn.`);
      return;
    }

    // Acquire lock
    speakerLock.active = true;
    speakerLock.currentSpeaker = speaker;
    speakerLock.isStudent = false;
    this.playing = true;
    this.onStart(speaker);

    const engine = localStorage.getItem('gd_tts_engine') || 'edge';
    const voiceChoice = localStorage.getItem('gd_voice_choice') || 'voice1';

    try {
      const blob = await getTTS(text, voice, rate, pitch, speaker, engine, voiceChoice);
      
      // Double check lock before playback starts in case student started speaking during fetch
      if (speakerLock.isStudent) {
        console.log(`[VoiceRule] Student began speaking during TTS fetch. Aborting ${speaker} playback.`);
        this.stop(true);
        return;
      }

      if (blob && blob.size > 100) {
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        this.currentAudio = audio;

        audio.onended = () => {
          this.handlePlaybackComplete(speaker);
        };

        audio.onerror = () => {
          this.handlePlaybackComplete(speaker);
        };

        await audio.play();
        return;
      }
    } catch (err) {
      console.warn('TTS streaming failed, falling back to Web Speech Synthesis:', err);
    }

    // Fallback to browser SpeechSynthesis
    this.fallbackSpeechSynthesis(text, speaker);
  }

  handlePlaybackComplete(speaker) {
    this.playing = false;
    this.currentAudio = null;
    speakerLock.active = false;
    speakerLock.currentSpeaker = null;
    this.onEnd(speaker);
    this.drainQueue();
  }

  drainQueue() {
    if (speakerLock.queue.length > 0 && !speakerLock.active && !speakerLock.isStudent) {
      const next = speakerLock.queue.shift();
      if (next) {
        this.speak(next.text, next.voice, next.rate, next.pitch, next.speaker);
      }
    }
  }

  fallbackSpeechSynthesis(text, speaker) {
    if (speakerLock.isStudent) return;

    if (!('speechSynthesis' in window)) {
      this.handlePlaybackComplete(speaker);
      return;
    }

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-IN';
    utter.rate = 1.05;
    utter.onend = () => {
      this.handlePlaybackComplete(speaker);
    };
    utter.onerror = () => {
      this.handlePlaybackComplete(speaker);
    };
    window.speechSynthesis.speak(utter);
  }
}
