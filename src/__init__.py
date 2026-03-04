"""
UMEQAM Runtime Guardrail Package
Minimal export wrapper for FastAPI integration
"""

class UMEQAMGuardrail:

    def __init__(self, threshold: float = 0.36):
        self.threshold = threshold

    def profile_auto(self, text: str, ats_proxy: float = 0.5):

        # very simple placeholder risk logic
        risk = 0.0

        if "always" in text.lower():
            risk += 0.15

        if "never" in text.lower():
            risk += 0.15

        if "guaranteed" in text.lower():
            risk += 0.20

        blocked = risk >= self.threshold

        return {
            "risk_score": round(risk, 3),
            "risk_zone": "C" if blocked else "A",
            "blocked": blocked,
            "regime": "AUTO",
            "threshold": self.threshold,
            "fingerprint": "umeqam-v0"
        }


__all__ = ["UMEQAMGuardrail"]
