"""
UMEQAM Risk Policy Engine

Purpose
Translate epistemic risk scores into enforcement decisions.

Policy levels
LOW        → allow
MEDIUM     → allow + log
HIGH       → warn
CRITICAL   → block
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class PolicyDecision:
    action: str
    risk_score: float
    risk_level: str
    reason: str


class RiskPolicyEngine:

    def __init__(
        self,
        warn_threshold: float = 0.6,
        block_threshold: float = 0.8
    ):

        self.warn_threshold = warn_threshold
        self.block_threshold = block_threshold

    def _risk_level(self, score: float) -> str:

        if score < 0.25:
            return "LOW"

        if score < 0.5:
            return "MEDIUM"

        if score < 0.75:
            return "HIGH"

        return "CRITICAL"

    def evaluate(self, risk_score: float) -> PolicyDecision:

        level = self._risk_level(risk_score)

        if risk_score >= self.block_threshold:

            return PolicyDecision(
                action="block",
                risk_score=risk_score,
                risk_level=level,
                reason="risk_above_block_threshold"
            )

        if risk_score >= self.warn_threshold:

            return PolicyDecision(
                action="warn",
                risk_score=risk_score,
                risk_level=level,
                reason="risk_above_warning_threshold"
            )

        if risk_score >= 0.25:

            return PolicyDecision(
                action="log",
                risk_score=risk_score,
                risk_level=level,
                reason="moderate_risk_detected"
            )

        return PolicyDecision(
            action="allow",
            risk_score=risk_score,
            risk_level=level,
            reason="risk_within_safe_limits"
        )
