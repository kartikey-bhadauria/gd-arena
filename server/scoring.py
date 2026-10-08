# Scoring weights, dimension thresholds and strict rubric
import json
import os

RUBRIC_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "rubric.json")

def load_rubric():
    if os.path.exists(RUBRIC_FILE):
        try:
            with open(RUBRIC_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "dimensions": {
            "opening": { "weight": 1.5, "min_pass": 5 },
            "idea_quality": { "weight": 2.0, "min_pass": 5 },
            "building_on_others": { "weight": 1.5, "min_pass": 4 },
            "listening": { "weight": 1.5, "min_pass": 5 },
            "handling_interruptions": { "weight": 1.0, "min_pass": 4 },
            "closing": { "weight": 1.5, "min_pass": 5 }
        },
        "tiers": {
            "weak": { "range": [0, 4], "label": "Weak" },
            "average": { "range": [4, 6], "label": "Average" },
            "strong": { "range": [6, 8], "label": "Strong" },
            "elite": { "range": [8, 10], "label": "Elite" }
        }
    }

def calculate_tier(overall_score):
    if overall_score >= 8.0:
        return "Elite"
    elif overall_score >= 6.0:
        return "Strong"
    elif overall_score >= 4.0:
        return "Average"
    else:
        return "Weak"
