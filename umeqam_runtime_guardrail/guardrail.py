from typing import Dict


class UMEQAMGuardrail:
    """
    UMEQAM Runtime Guardrail

    Lightweight runtime risk detector used by the gateway.
    Provides quick epistemic risk scoring before deeper analysis.
    """

    VERSION = "1.0"

    def __init__(self):
        self.base_threshold = 0.40

    def analyze(self, text: str) -> Dict:
        """
        Main risk analysis method.
        Returns risk score and signals.
        """

        text_lower = text.lower()

        risk = 0.0
        signals = []

        # Overconfidence patterns
        if "definitely" in text_lower:
            risk += 0.10
            signals.append("overconfidence")

        if "always" in text_lower:
            risk += 0.10
            signals.append("absolute_claim")

        if "guaranteed" in text_lower:
            risk += 0.15
            signals.append("false_certainty")

        # Authority hallucination patterns
        if "studies prove" in text_lower:
            risk += 0.20
            signals.append("fake_authority")

        if "scientists say" in text_lower:
            risk += 0.15
            signals.append("authority_claim")

        # Fabrication indicators
        if "according to a report" in text_lower:
            risk += 0.15
            signals.append("fabricated_source")

        if "experts agree" in text_lower:
            risk += 0.15
            signals.append("fake_consensus")

        # Clamp risk
        risk = min(risk, 1.0)

        decision = self._decision(risk)

        return {
            "version": self.VERSION,
            "risk_score": round(risk, 3),
            "signals": signals,
            "decision": decision
        }

    def check(self, text: str) -> Dict:
        """
        Legacy endpoint compatibility.
        """

        result = self.analyze(text)

        return {
            "risk": result["risk_score"],
            "status": result["decision"],
            "signals": result["signals"]
        }

    def _decision(self, risk: float) -> str:

        if risk < 0.25:
            return "allow"

        if risk < 0.45:
            return "monitor"

        if risk < 0.65:
            return "warn"

        return "block"
