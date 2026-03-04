"""
UMEQAM Risk Aggregator v2

Combines multiple epistemic detectors into one final risk score.

Inputs
- Epistemic Conflict Detector (ECD)
- False World Detector (FWD)
- ACCI Lite (confidence collapse estimator)

Output
- unified risk score
- risk level
- detailed signal breakdown
"""

from dataclasses import dataclass
from typing import Dict

from umeqam.epistemic.ecd_conflict_detector import EpistemicConflictDetector
from umeqam.epistemic.false_world_detector import FalseWorldDetector
from umeqam.epistemic.acci_lite import ACCILite


@dataclass
class AggregatedRisk:
    score: float
    level: str
    signals: Dict


class UMEQAMEpistemicRiskEngine:

    def __init__(self):

        self.ecd = EpistemicConflictDetector()
        self.fwd = FalseWorldDetector()
        self.acci = ACCILite()

    def _level(self, score: float) -> str:

        if score < 0.25:
            return "LOW"

        if score < 0.5:
            return "MEDIUM"

        if score < 0.75:
            return "HIGH"

        return "CRITICAL"

    def analyze(self, text: str) -> AggregatedRisk:

        ecd_result = self.ecd.detect(text)
        fwd_result = self.fwd.analyze(text)
        acci_result = self.acci.analyze(text)

        # weighted aggregation
        score = (
            ecd_result.score * 0.35 +
            fwd_result.score * 0.35 +
            acci_result.score * 0.30
        )

        score = max(0.0, min(1.0, score))

        return AggregatedRisk(
            score=round(score, 3),
            level=self._level(score),
            signals={
                "ecd": {
                    "score": ecd_result.score,
                    "conflicts": len(ecd_result.conflicts)
                },
                "false_world": {
                    "score": fwd_result.score,
                    "authority_hits": fwd_result.signals["authority_hits"],
                    "absolute_hits": fwd_result.signals["absolute_hits"]
                },
                "acci": {
                    "score": acci_result.score,
                    "markers": acci_result.markers
                }
            }
        )
