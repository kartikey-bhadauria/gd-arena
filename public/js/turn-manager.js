// Client-Side Turn Management state mirror

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
