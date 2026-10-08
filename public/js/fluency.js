// Real-time Speech Pace, WPM and Filler Word Tracker

export class SpeechAnalytics {
  constructor({ onUpdate } = {}) {
    this.onUpdate = onUpdate || (() => {});
    this.fillerWords = ["um", "uh", "like", "actually", "basically", "you know", "sort of", "i mean", "right"];
    this.fillerCount = 0;
    this.totalWords = 0;
    this.startTime = null;
    this.wpm = 0;
    this.status = "Ready";
  }

  start() {
    this.startTime = Date.now();
  }

  processText(text) {
    if (!text || !text.trim()) return;
    if (!this.startTime) this.startTime = Date.now();

    const words = text.toLowerCase().match(/\b[\w']+\b/g) || [];
    this.totalWords += words.length;

    // Detect fillers
    for (const w of words) {
      if (this.fillerWords.includes(w)) {
        this.fillerCount++;
      }
    }

    // Calculate WPM
    const elapsedMinutes = (Date.now() - this.startTime) / 60000;
    if (elapsedMinutes > 0.05) {
      this.wpm = Math.round(this.totalWords / elapsedMinutes);
    } else {
      this.wpm = Math.round(words.length * 15);
    }

    // Determine Pace Status
    if (this.wpm < 100) {
      this.status = "Slow / Hesitant";
    } else if (this.wpm <= 165) {
      this.status = "Optimal Pace";
    } else {
      this.status = "Fast / Rushed";
    }

    this.onUpdate({
      wpm: this.wpm,
      status: this.status,
      fillerCount: this.fillerCount,
      totalWords: this.totalWords
    });
  }

  reset() {
    this.fillerCount = 0;
    this.totalWords = 0;
    this.startTime = null;
    this.wpm = 0;
    this.status = "Ready";
  }
}
