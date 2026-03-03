import math
import hashlib
from typing import Dict

THRESHOLD = 0.36
INTERACTION_W = 0.10

WEIGHTS = {
    "s1": 0.17,
    "s2": 0.13,
    "s3": 0.14,
    "s4": 0.13,
    "s5": 0.16,
    "s6": 0.15,
    "s7": 0.12,
}

def compute_risk(signals: Dict[str, float]) -> float:
    linear = sum(WEIGHTS[k] * signals.get(k, 0.0) for k in WEIGHTS)
    interaction = INTERACTION_W * signals.get("s6", 0.0) * signals.get("s7", 0.0)
    raw = linear + interaction
    risk = 1.0 / (1.0 + math.exp(-4.0 * (raw - 0.5)))
    return float(max(0.0, min(1.0, risk)))

def get_zone(risk: float) -> str:
    if risk < 0.25: return "A"
    if risk < 0.50: return "B"
    if risk < 0.75: return "C"
    return "D"
