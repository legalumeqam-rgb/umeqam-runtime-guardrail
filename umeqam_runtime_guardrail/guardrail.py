class UMEQAMGuardrail:

    def __init__(self, threshold=0.36):
        self.threshold = threshold

    def profile_auto(self, text, ats_proxy=0.5):

        risk_score = ats_proxy
        blocked = risk_score >= self.threshold

        return {
            "risk_score": risk_score,
            "risk_zone": "HIGH" if blocked else "LOW",
            "blocked": blocked,
            "regime": "runtime",
            "threshold": self.threshold
        }
