// Web Audio API VU Energy Meter and Instant Voice Barge-In Detector

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
