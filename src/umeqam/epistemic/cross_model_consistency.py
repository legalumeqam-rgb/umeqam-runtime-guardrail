"""
Cross-Model Consistency Checker (CMCC)

Purpose
Estimate hallucination risk by measuring agreement between
multiple model outputs.

Idea
If several models independently produce similar answers → lower risk.
If answers diverge strongly → higher epistemic uncertainty.
"""

from dataclasses import dataclass
from typing import List, Dict
import re


@dataclass
class ConsistencyResult:
    score: float
    level: str
    similarities: List[float]


class CrossModelConsistencyChecker:

    def __init__(self):
        pass

    def _tokenize(self, text: str) -> set:

        words = re.findall(r"\b\w+\b", text.lower())

        return set(words)

    def _similarity(self, a: str, b: str) -> float:

        set_a = self._tokenize(a)
        set_b = self._tokenize(b)

        if not set_a or not set_b:
            return 0.0

        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)

        return len(intersection) / len(union)

    def _level(self, score: float) -> str:

        if score < 0.25:
            return "LOW"

        if score < 0.5:
            return "MEDIUM"

        if score < 0.75:
            return "HIGH"

        return "CRITICAL"

    def analyze(self, responses: List[str]) -> ConsistencyResult:

        if len(responses) < 2:

            return ConsistencyResult(
                score=0.0,
                level="LOW",
                similarities=[]
            )

        sims = []

        for i in range(len(responses)):

            for j in range(i + 1, len(responses)):

                sim = self._similarity(responses[i], responses[j])

                sims.append(sim)

        avg_sim = sum(sims) / len(sims)

        # convert similarity to risk
        risk_score = 1.0 - avg_sim

        return ConsistencyResult(
            score=round(risk_score, 3),
            level=self._level(risk_score),
            similarities=[round(s, 3) for s in sims]
        )
