// Neural TTS Player & Instant Barge-In Handler with Engine & Voice Selection

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

    // Read configured engine and voice option
    const engine = localStorage.getItem('gd_tts_engine') || 'edge'; // 'edge' or 'groq'
    const voiceChoice = localStorage.getItem('gd_voice_choice') || 'voice1'; // 'voice1' or 'voice2'

    try {
      const blob = await getTTS(text, voice, rate, pitch, speaker, engine, voiceChoice);
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
