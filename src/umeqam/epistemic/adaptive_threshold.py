"""
Adaptive Risk Threshold Engine

Purpose
Adjust risk threshold dynamically based on recent risk history.

Behavior
- If recent risk scores are high → system becomes stricter
- If recent risk scores are low → system becomes more permissive

This prevents static thresholds from becoming ineffective
in changing prompt environments.
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class ThresholdState:
    current_threshold: float
    recent_average: float
    samples: int


class AdaptiveThreshold:

    def __init__(
        self,
        window_size: int = 50,
        base_threshold: float = 0.5,
        min_threshold: float = 0.25,
        max_threshold: float = 0.75
    ):

        self.window = deque(maxlen=window_size)
        self.base_threshold = base_threshold
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

        self.current_threshold = base_threshold

    def update(self, risk_score: float) -> ThresholdState:

        self.window.append(risk_score)

        avg = sum(self.window) / len(self.window)

        # adjustment factor
        adjustment = (avg - 0.5) * 0.5

        new_threshold = self.base_threshold + adjustment

        new_threshold = max(self.min_threshold, min(self.max_threshold, new_threshold))

        self.current_threshold = new_threshold

        return ThresholdState(
            current_threshold=round(self.current_threshold, 3),
            recent_average=round(avg, 3),
            samples=len(self.window)
        )

    def should_block(self, risk_score: float) -> bool:

        return risk_score >= self.current_threshold
