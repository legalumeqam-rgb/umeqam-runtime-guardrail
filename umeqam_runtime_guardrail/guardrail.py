import hashlib
from typing import Dict


class UMEQAMGuardrail:
    """
    UMEQAM Runtime Guardrail

    Lightweight epistemic risk engine for runtime LLM monitoring.
    """

    VERSION = "0.1.0"

    def __init__(self, threshold: float = 0.40):

        self.threshold = threshold

        self.overconfidence_patterns = [
            "definitely",
            "always",
            "guaranteed",
            "without doubt",
            "certainly"
        ]

        self.authority_patterns = [
            "studies prove",
            "scientists say",
            "experts agree",
            "according to a report"
        ]

    def profile_auto(self, text: str, ats_proxy: float = 0.5) -> Dict:

        text_lower = text.lower()

        risk = 0.0
        signals = []

        # Overconfidence detection
        for pattern in self.overconfidence_patterns:
            if pattern in text_lower:
                risk += 0.10
                signals.append("overconfidence")

        # Authority hallucination detection
        for pattern in self.authority_patterns:
            if pattern in text_lower:
                risk += 0.15
                signals.append("authority_claim")

        # ATS proxy contribution
        risk += 0.20 * ats_proxy

        risk = min(risk, 1.0)

        zone = self._risk_zone(risk)

        blocked = risk >= self.threshold

        fingerprint = self._fingerprint(text)

        return {
            "risk_score": round(risk, 4),
            "risk_zone": zone,
            "blocked": blocked,
            "regime": "UMEQAM_RUNTIME",
            "threshold": self.threshold,
            "fingerprint": fingerprint,
            "signals": signals
        }

    def _risk_zone(self, risk: float) -> str:

        if risk < 0.25:
            return "GREEN"

        if risk < 0.45:
            return "YELLOW"

        if risk < 0.65:
            return "ORANGE"

        return "RED"

    def _fingerprint(self, text: str) -> str:

        return hashlib.sha256(text.encode()).hexdigest()[:16]
