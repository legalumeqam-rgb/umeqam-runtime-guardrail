"""
ACCI Lite v0.1
AI Confidence Collapse Index (runtime estimator)

Purpose
Estimate when a model begins producing high-confidence speculative output.

Signal structure:
confidence markers
+
speculation markers
-
uncertainty markers

Higher score → higher epistemic risk
"""

from dataclasses import dataclass
from typing import Dict, List
import re


@dataclass
class ACCIResult:
    score: float
    level: str
    markers: Dict


class ACCILite:

    def __init__(self):

        self.confidence_patterns = [
            r"\bdefinitely\b",
            r"\bcertainly\b",
            r"\bwithout doubt\b",
            r"\bguaranteed\b",
            r"\bclearly\b"
        ]

        self.speculation_patterns = [
            r"\bprobably\b",
            r"\bmaybe\b",
            r"\bperhaps\b",
            r"\bit seems\b",
            r"\bI guess\b"
        ]

        self.uncertainty_patterns = [
            r"\bI might be wrong\b",
            r"\bI'm not sure\b",
            r"\buncertain\b",
            r"\bnot certain\b"
        ]

    def _count(self, text: str, patterns: List[str]) -> int:

        count = 0

        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                count += 1

        return count

    def _risk_level(self, score: float) -> str:

        if score < 0.25:
            return "LOW"

        if score < 0.5:
            return "MEDIUM"

        if score < 0.75:
            return "HIGH"

        return "CRITICAL"

    def analyze(self, text: str) -> ACCIResult:

        conf = self._count(text, self.confidence_patterns)
        spec = self._count(text, self.speculation_patterns)
        uncert = self._count(text, self.uncertainty_patterns)

        score = (conf * 0.5) + (spec * 0.3) - (uncert * 0.2)

        score = max(0.0, min(1.0, score))

        return ACCIResult(
            score=round(score, 3),
            level=self._risk_level(score),
            markers={
                "confidence_markers": conf,
                "speculation_markers": spec,
                "uncertainty_markers": uncert
            }
        )
