// Web Speech API STT Wrapper

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
