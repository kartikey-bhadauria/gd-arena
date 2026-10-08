// API Client wrapper for GD Arena Backend

import { API_BASE } from './config.js';

export async function getHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    return await res.json();
  } catch (err) {
    console.error('getHealth error:', err);
    return null;
  }
}

export async function startSession(mode = 'gd', topic = '', panelSize = 4, resume = null) {
  try {
    const resumeData = resume || JSON.parse(localStorage.getItem('gd_resume') || '{}');
    const res = await fetch(`${API_BASE}/api/session/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode, topic, panel_size: panelSize, resume: resumeData })
    });
    return await res.json();
  } catch (err) {
    console.error('startSession error:', err);
    return null;
  }
}

export async function sendChat(sessionId, text, interrupted = false, timestamp = '01:00') {
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, text, interrupted, timestamp })
    });
    return await res.json();
  } catch (err) {
    console.error('sendChat error:', err);
    return null;
  }
}

export async function getTTS(text, voice = 'en-IN-PrabhatNeural', rate = '+0%', pitch = '+0Hz', speaker = 'aarav', engine = 'edge', voiceChoice = 'voice1') {
  try {
    const res = await fetch(`${API_BASE}/api/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, voice, rate, pitch, speaker, engine, voice_choice: voiceChoice })
    });
    if (res.ok) {
      return await res.blob();
    }
    return null;
  } catch (err) {
    console.error('getTTS error:', err);
    return null;
  }
}

export async function getReport(sessionId, transcript = []) {
  try {
    const res = await fetch(`${API_BASE}/api/report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, transcript })
    });
    return await res.json();
  } catch (err) {
    console.error('getReport error:', err);
    return null;
  }
}

export async function parseResume(text, jdText = '') {
  try {
    const res = await fetch(`${API_BASE}/api/parse-resume`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, jd_text: jdText })
    });
    return await res.json();
  } catch (err) {
    console.error('parseResume error:', err);
    return null;
  }
}

export async function getSession(sessionId) {
  try {
    const res = await fetch(`${API_BASE}/api/session/${sessionId}`);
    return await res.json();
  } catch (err) {
    console.error('getSession error:', err);
    return null;
  }
}

export async function generateTopics(category = 'Technology & Architecture') {
  try {
    const res = await fetch(`${API_BASE}/api/generate-topics`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category })
    });
    return await res.json();
  } catch (err) {
    console.error('generateTopics error:', err);
    return { topics: [] };
  }
}
