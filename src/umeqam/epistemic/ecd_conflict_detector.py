import re
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ConflictResult:
    conflicts: List[Tuple[str, str]]
    score: float


class EpistemicConflictDetector:

    def __init__(self):
        self.negation = r"\b(not|never|no|cannot|can't)\b"

    def split_sentences(self, text: str) -> List[str]:
        return re.split(r"[.!?]", text)

    def extract_claims(self, sentences: List[str]) -> List[str]:
        claims = []
        for s in sentences:
            s = s.strip()
            if len(s) > 0:
                claims.append(s.lower())
        return claims

    def detect(self, text: str) -> ConflictResult:

        sentences = self.split_sentences(text)
        claims = self.extract_claims(sentences)

        conflicts = []

        for i in range(len(claims)):
            for j in range(i + 1, len(claims)):

                a = claims[i]
                b = claims[j]

                if a == b:
                    continue

                # very simple contradiction heuristic
                if re.search(self.negation, a) and not re.search(self.negation, b):
                    if any(word in b for word in a.split()):
                        conflicts.append((a, b))

                if re.search(self.negation, b) and not re.search(self.negation, a):
                    if any(word in a for word in b.split()):
                        conflicts.append((a, b))

        score = min(1.0, len(conflicts) * 0.4)

        return ConflictResult(conflicts=conflicts, score=round(score, 3))
