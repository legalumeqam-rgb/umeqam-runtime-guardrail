"""
False World Detector (FWD) v0.1
Detects coherent but likely fabricated "authority + absolutes" narratives.

Purpose
- Flag responses that combine authority claims ("according to a study/experts")
  with absolute guarantees ("always/never/guaranteed/perfect"), which is a strong
  hallucination-style marker in many LLM outputs.

Design goals
- Deterministic
- Cheap (regex-based)
- Runtime safe
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import re


@dataclass
class FalseWorldResult:
    score: float
    level: str
    signals: Dict[str, int]
    matches: Dict[str, List[str]]


class FalseWorldDetector:
    """
    FWD scores "fabricated reality" risk using three lenses:
    1) authority framing
    2) absolute certainty language
    3) universal claims / unrealistic perfection

    The score is intentionally conservative: it boosts risk when these co-occur,
    not when they appear alone.
    """

    def __init__(self) -> None:
        # Authority framing: often used to "borrow credibility" (may be real, may be fabricated).
        self._authority_patterns: List[str] = [
            r"\baccording to\b.*\bstudy\b",
            r"\baccording to\b.*\bresearch\b",
            r"\baccording to\b.*\breport\b",
            r"\ba recent\b.*\bstudy\b",
            r"\bstudies show\b",
            r"\bresearch shows\b",
            r"\bresearch proves\b",
            r"\bdata (shows|suggests|indicates)\b",
            r"\bexperts (say|claim|agree)\b",
            r"\bscientists (say|found|show)\b",
            r"\bresearchers (say|found|show)\b",
            r"\bMIT\b.*\bstudy\b",
            r"\bHarvard\b.*\bstudy\b",
            r"\bStanford\b.*\bstudy\b",
        ]

        # Absolutes / guarantees: strong epistemic risk when paired with authority.
        self._absolute_patterns: List[str] = [
            r"\balways\b",
            r"\bnever\b",
            r"\bguarantee(d)?\b",
            r"\bwithout (any )?doubt\b",
            r"\b100%\b",
            r"\bperfect(ly)?\b",
            r"\bimpossible to fail\b",
            r"\bwill eliminate\b",
            r"\bzero errors?\b",
            r"\bno mistakes?\b",
        ]

        # Universal/comparative superiority claims (often unrealistic).
        self._superiority_patterns: List[str] = [
            r"\boutperform(s|ed)? humans?\b",
            r"\bbetter than humans?\b",
            r"\bsuperior to humans?\b",
            r"\bbeats humans?\b",
            r"\balways (wins|succeeds)\b",
            r"\bnever (fails|loses)\b",
        ]

    def _find_matches(self, text: str, patterns: List[str]) -> Tuple[int, List[str]]:
        hits = []
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                hits.append(p)
        return len(hits), hits

    def _level(self, score: float) -> str:
        if score < 0.25:
            return "LOW"
        if score < 0.50:
            return "MEDIUM"
        if score < 0.75:
            return "HIGH"
        return "CRITICAL"

    def analyze(self, text: str) -> FalseWorldResult:
        """
        Returns a conservative score in [0,1].

        Scoring logic:
        - authority alone: low-to-medium (can be legitimate)
        - absolutes alone: low-to-medium
        - authority + absolutes: big boost (false-world signature)
        - + superiority claims: additional boost
        """
        t = (text or "").strip()

        a_n, a_hits = self._find_matches(t, self._authority_patterns)
        x_n, x_hits = self._find_matches(t, self._absolute_patterns)
        s_n, s_hits = self._find_matches(t, self._superiority_patterns)

        # Base components (small on their own)
        base = (a_n * 0.10) + (x_n * 0.10) + (s_n * 0.10)

        # Co-occurrence boosts
        co_auth_abs = 0.0
        if a_n > 0 and x_n > 0:
            co_auth_abs = 0.55  # core "false world" signature

        co_with_superiority = 0.0
        if (a_n > 0 and x_n > 0 and s_n > 0):
            co_with_superiority = 0.20

        score = base + co_auth_abs + co_with_superiority
        score = max(0.0, min(1.0, score))

        return FalseWorldResult(
            score=round(score, 3),
            level=self._level(score),
            signals={
                "authority_hits": a_n,
                "absolute_hits": x_n,
                "superiority_hits": s_n,
            },
            matches={
                "authority": a_hits,
                "absolute": x_hits,
                "superiority": s_hits,
            },
        )
