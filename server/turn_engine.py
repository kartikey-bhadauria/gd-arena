# Turn management logic for Multi-Agent GD & 1-on-1 Interviews
import random
import time

class TurnEngine:
    def __init__(self, personas=None):
        self.personas = personas or ["aarav", "priya", "rohan", "neha", "moderator"]
        self.ai_turns_in_a_row = 0
        self.last_speaker = None
        self.last_two_speakers = []
        self.turn_count = 0
        self.last_student_ts = time.time()
        self.interruption_count = 0

    def note_student_spoke(self, interrupted=False):
        self.ai_turns_in_a_row = 0
        self.last_speaker = "student"
        self.last_two_speakers.append("student")
        if len(self.last_two_speakers) > 2:
            self.last_two_speakers.pop(0)
        self.last_student_ts = time.time()
        if interrupted:
            self.interruption_count += 1

    def note_ai_spoke(self, persona_key):
        self.ai_turns_in_a_row += 1
        self.turn_count += 1
        self.last_speaker = persona_key
        self.last_two_speakers.append(persona_key)
        if len(self.last_two_speakers) > 2:
            self.last_two_speakers.pop(0)

    def should_invite_student(self):
        return self.ai_turns_in_a_row >= 2

    def next_speaker(self, mode="gd", panel_keys=None):
        if mode == "interview":
            return "interviewer"

        if self.should_invite_student():
            return "moderator"

        active_panel = panel_keys or self.personas
        available = [k for k in active_panel if k != "moderator"]
        
        weights = {"aarav": 4, "priya": 3, "rohan": 3, "neha": 1}
        filtered_pool = [k for k in available if k not in self.last_two_speakers]
        if not filtered_pool:
            filtered_pool = available
        
        pool_weights = [weights.get(k, 2) for k in filtered_pool]
        chosen = random.choices(filtered_pool, weights=pool_weights, k=1)[0]
        return chosen
