import os

BASE_DIR = r"C:\Users\Kartikey\gd-arena"

# 1. public/css/style.css
css_code = """/* ======================================================================
   GD Arena — Primefold-Inspired Clean Light B2B Design System
   ====================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Fragment+Mono:ital@0;1&family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --ink: #1a1814;
  --muted: #848481;
  --apricot: #f99d72;
  --apricot-soft: #ffd4be;
  --bg: #ffffff;
  --surface: #fafaf9;
  --ring: rgba(38, 57, 90, 0.16);

  /* Strict Scoring Colors */
  --tier-weak: #dc2626;
  --tier-average: #d97706;
  --tier-strong: #059669;
  --tier-elite: #7c3aed;

  /* Fonts */
  --font-heading: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'Fragment Mono', monospace;
}

* {
  box-sizing: border-box;
}

body {
  background-color: var(--bg);
  color: var(--ink);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.5;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  color: var(--ink);
  letter-spacing: -0.025em;
}

.font-mono {
  font-family: var(--font-mono);
}

/* Card Styles */
.card {
  background-color: #ffffff;
  border-radius: 8px;
  border: 1px solid var(--ring);
  padding: 24px;
  transition: transform 300ms ease, box-shadow 300ms ease, border-color 300ms ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px -4px rgba(0, 0, 0, 0.08);
}

.card-surface {
  background-color: var(--surface);
  border-radius: 8px;
  border: 1px solid var(--ring);
  padding: 20px;
}

/* Buttons & Pills */
.pill {
  border-radius: 9999px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 200ms ease;
}

.btn-primary {
  background-color: var(--apricot);
  color: var(--ink);
  border-radius: 9999px;
  padding: 10px 22px;
  font-weight: 600;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 200ms ease;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: var(--apricot-soft);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px -2px rgba(249, 157, 114, 0.35);
}

.btn-secondary {
  background-color: #ffffff;
  color: var(--ink);
  border: 1px solid var(--ring);
  border-radius: 9999px;
  padding: 10px 22px;
  font-weight: 600;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 200ms ease;
  cursor: pointer;
}

.btn-secondary:hover {
  background-color: var(--surface);
  border-color: rgba(38, 57, 90, 0.3);
  transform: translateY(-1px);
}

/* Glass Header */
.glass {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--ring);
}

/* Speaker States */
.active-speaker {
  border-color: var(--apricot) !important;
  box-shadow: 0 0 0 2px var(--apricot), 0 4px 16px -2px rgba(249, 157, 114, 0.25) !important;
}

.thinking-badge {
  background-color: rgba(249, 157, 114, 0.15);
  color: #c25e2e;
  border: 1px solid rgba(249, 157, 114, 0.3);
  border-radius: 9999px;
  padding: 2px 8px;
  font-size: 10px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.nudge {
  background-color: rgba(217, 119, 6, 0.1);
  color: #b45309;
  border: 1px solid rgba(217, 119, 6, 0.25);
  border-radius: 9999px;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* Equalizer VU Meter */
.eq-container {
  display: inline-flex;
  align-items: flex-end;
  gap: 2px;
  height: 14px;
}

.eq-bar {
  width: 2px;
  background-color: var(--apricot);
  border-radius: 2px;
  animation: eq-bounce 0.8s ease-in-out infinite alternate;
}
.eq-bar:nth-child(1) { height: 40%; animation-delay: 0.1s; }
.eq-bar:nth-child(2) { height: 90%; animation-delay: 0.3s; }
.eq-bar:nth-child(3) { height: 60%; animation-delay: 0.2s; }
.eq-bar:nth-child(4) { height: 100%; animation-delay: 0.4s; }
.eq-bar:nth-child(5) { height: 50%; animation-delay: 0.15s; }

@keyframes eq-bounce {
  0% { transform: scaleY(0.3); }
  100% { transform: scaleY(1.0); }
}

/* Score Tier Helpers */
.tier-weak { color: var(--tier-weak); }
.bg-tier-weak { background-color: rgba(220, 38, 38, 0.1); border-color: rgba(220, 38, 38, 0.3); }
.tier-average { color: var(--tier-average); }
.bg-tier-average { background-color: rgba(217, 119, 6, 0.1); border-color: rgba(217, 119, 6, 0.3); }
.tier-strong { color: var(--tier-strong); }
.bg-tier-strong { background-color: rgba(5, 150, 105, 0.1); border-color: rgba(5, 150, 105, 0.3); }
.tier-elite { color: var(--tier-elite); }
.bg-tier-elite { background-color: rgba(124, 58, 237, 0.1); border-color: rgba(124, 58, 237, 0.3); }

/* Scroll-triggered fade-in */
.scroll-fade {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 500ms ease-out, transform 500ms ease-out;
}
.scroll-fade.in {
  opacity: 1;
  transform: translateY(0);
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: var(--surface);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(38, 57, 90, 0.2);
  border-radius: 4px;
}

/* Infinite Marquee */
.marquee-track {
  display: flex;
  width: max-content;
  animation: marquee 25s linear infinite;
}
.marquee-track:hover {
  animation-play-state: paused;
}
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
"""
with open(os.path.join(BASE_DIR, "public", "css", "style.css"), "w", encoding="utf-8") as f:
    f.write(css_code)

# 2. public/js/config.js
config_js = """// GD Arena Global Configuration & Persona Definitions

export const API_BASE = ""; // Same-origin

export const PERSONAS = {
  moderator: {
    name: "Mr. Verma",
    role: "Moderator",
    color: "#1a1814",
    voice: "en-IN-PrabhatNeural",
    avatar: "MV"
  },
  aarav: {
    name: "Aarav",
    role: "The Dominator",
    color: "#dc2626",
    voice: "en-IN-PrabhatNeural",
    avatar: "AR"
  },
  priya: {
    name: "Priya",
    role: "Data-Driven",
    color: "#0891b2",
    voice: "en-IN-NeerjaNeural",
    avatar: "PR"
  },
  rohan: {
    name: "Rohan",
    role: "The Synthesizer",
    color: "#d97706",
    voice: "en-US-GuyNeural",
    avatar: "RO"
  },
  neha: {
    name: "Neha",
    role: "The Quiet Thinker",
    color: "#7c3aed",
    voice: "en-IN-NeerjaNeural",
    avatar: "NE"
  },
  interviewer: {
    name: "Ms. Kapoor",
    role: "Lead Interviewer",
    color: "#1a1814",
    voice: "en-IN-NeerjaNeural",
    avatar: "MK"
  }
};

export const SESSION = {
  durations: [5, 8, 15], // minutes
  phases: ["Opening", "Discussion", "Closing"],
  reactionDelay: 1350, // ms natural pause before AI speaks
  silenceThreshold: 900, // ms of silence before AI considers taking turn
  maxAITurnsInARow: 2
};

export const TIERS = {
  weak: { label: "Weak", min: 0, max: 4, color: "#dc2626", meaning: "You'd get cut in Round 1" },
  average: { label: "Average", min: 4, max: 6, color: "#d97706", meaning: "You'd survive, not stand out" },
  strong: { label: "Strong", min: 6, max: 8, color: "#059669", meaning: "You'd get shortlisted" },
  elite: { label: "Elite", min: 8, max: 10, color: "#7c3aed", meaning: "You'd lead the room" }
};
"""
with open(os.path.join(BASE_DIR, "public", "js", "config.js"), "w", encoding="utf-8") as f:
    f.write(config_js)

# 3. public/js/api.js
api_js = """// API Client wrapper for GD Arena Backend

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

export async function startSession(mode = 'gd', topic = '', panelSize = 4) {
  try {
    const res = await fetch(`${API_BASE}/api/session/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode, topic, panel_size: panelSize })
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

export async function getTTS(text, voice = 'en-IN-PrabhatNeural', rate = '+0%', pitch = '+0Hz', speaker = 'aarav') {
  try {
    const res = await fetch(`${API_BASE}/api/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, voice, rate, pitch, speaker })
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
"""
with open(os.path.join(BASE_DIR, "public", "js", "api.js"), "w", encoding="utf-8") as f:
    f.write(api_js)

print("Phase 3 Design System created successfully!")
