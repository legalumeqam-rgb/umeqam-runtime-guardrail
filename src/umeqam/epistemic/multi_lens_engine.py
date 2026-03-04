"""
Multi-Lens Epistemic Analysis Engine (MLEA)

Purpose
Run multiple epistemic detectors and combine their signals into
a single risk evaluation.

Lenses
- ECD  : Epistemic Conflict Detector
- FWD  : False World Detector
- ACCI : Confidence Collapse Estimator
- CMCC : Cross-Model Consistency Checker

Design
Deterministic, lightweight, runtime-safe.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from umeqam.epistemic.ecd_conflict_detector import EpistemicConflictDetector
from umeqam.epistemic.false_world_detector import FalseWorldDetector
from umeqam.epistemic.acci_lite import ACCILite
from umeqam.epistemic.cross_model_consistency import CrossModelConsistencyChecker


@dataclass
class MultiLensResult:
    score: float
    level: str
    lens_scores: Dict


class MultiLensEpistemicEngine:

    def __init__(self):

        self.ecd = EpistemicConflictDetector()
        self.fwd = FalseWorldDetector()
        self.acci = ACCILite()
        self.cmcc = CrossModelConsistencyChecker()

    def _level(self, score: float) -> str:

        if score < 0.25:
            return "LOW"

        if score < 0.5:
            return "MEDIUM"

        if score < 0.75:
            return "HIGH"

        return "CRITICAL"

    def analyze(
        self,
        text: str,
        comparison_responses: Optional[List[str]] = None
    ) -> MultiLensResult:

        # run single-response lenses
        ecd_result = self.ecd.detect(text)
        fwd_result = self.fwd.analyze(text)
        acci_result = self.acci.analyze(text)

        cmcc_score = 0.0
        cmcc_sims = []

        # run cross-model lens if provided
        if comparison_responses and len(comparison_responses) > 1:

            cmcc_result = self.cmcc.analyze(comparison_responses)

            cmcc_score = cmcc_result.score
            cmcc_sims = cmcc_result.similarities

        # weighted aggregation
        score = (
            ecd_result.score * 0.30 +
            fwd_result.score * 0.30 +
            acci_result.score * 0.25 +
            cmcc_score * 0.15
        )

        score = max(0.0, min(1.0, score))

        return MultiLensResult(
            score=round(score, 3),
            level=self._level(score),
            lens_scores={
                "ecd": ecd_result.score,
                "false_world": fwd_result.score,
                "acci": acci_result.score,
                "cmcc": cmcc_score,
                "cmcc_similarities": cmcc_sims
            }
        )
