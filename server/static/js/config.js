// GD Arena Global Configuration & Persona Definitions

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
