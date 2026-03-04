import hashlib


class UMEQAMGuardrail:

    def __init__(self, threshold: float = 0.4):
        self.threshold = threshold

    def profile_auto(self, text: str, ats_proxy: float = 0.5):

        text = text.lower()

        risk = 0.0
        signals = []

        if "definitely" in text:
            risk += 0.1
            signals.append("overconfidence")

        if "always" in text:
            risk += 0.1
            signals.append("absolute_claim")

        if "scientists say" in text:
            risk += 0.2
            signals.append("authority_claim")

        risk += 0.2 * ats_proxy

        risk = min(risk, 1.0)

        if risk < 0.25:
            zone = "GREEN"
        elif risk < 0.45:
            zone = "YELLOW"
        elif risk < 0.65:
            zone = "ORANGE"
        else:
            zone = "RED"

        blocked = risk >= self.threshold

        fingerprint = hashlib.sha256(text.encode()).hexdigest()[:16]

        return {
            "risk_score": round(risk, 4),
            "risk_zone": zone,
            "blocked": blocked,
            "regime": "UMEQAM_RUNTIME",
            "threshold": self.threshold,
            "fingerprint": fingerprint,
            "signals": signals
        }
