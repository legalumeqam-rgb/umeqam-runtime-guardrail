from typing import Dict, Tuple


class UMEQAMGuardrail:
    """
    Deterministic epistemic guardrail engine.

    Computes risk score from signals s1–s7 and maps
    the result into a risk zone A/B/C/D.
    """

    def __init__(self, threshold: float = 0.36):
        self.threshold = threshold

    # ------------------------------------------------

    def profile_auto(self, text: str) -> Dict[str, float]:
        """
        Temporary signal generator.
        Later this will be replaced by real signal extraction.
        """

        length_factor = min(len(text) / 200, 1.0)

        signals = {
            "s1": length_factor * 0.4,
            "s2": length_factor * 0.3,
            "s3": length_factor * 0.6,
            "s4": length_factor * 0.2,
            "s5": length_factor * 0.5,
            "s6": length_factor * 0.4,
            "s7": length_factor * 0.7,
        }

        return signals

    # ------------------------------------------------

    def score_and_zone(self, signals: Dict[str, float]) -> Tuple[float, str]:

        s1 = signals.get("s1", 0)
        s2 = signals.get("s2", 0)
        s3 = signals.get("s3", 0)
        s4 = signals.get("s4", 0)
        s5 = signals.get("s5", 0)
        s6 = signals.get("s6", 0)
        s7 = signals.get("s7", 0)

        # deterministic combiner
        score = (
            0.15 * s1
            + 0.10 * s2
            + 0.20 * s3
            + 0.10 * s4
            + 0.15 * s5
            + 0.10 * s6
            + 0.20 * s7
        )

        # clamp
        score = max(0.0, min(score, 1.0))

        zone = self._zone(score)

        return score, zone

    # ------------------------------------------------

    def _zone(self, score: float) -> str:

        if score < 0.25:
            return "A"

        if score < 0.45:
            return "B"

        if score < 0.70:
            return "C"

        return "D"