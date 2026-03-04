"""
Epistemic Risk Trace (ERT)

Purpose
Persist a complete trace of epistemic risk analysis for each model response.

Trace includes:
- input text (or hash)
- final risk score
- lens contributions
- timestamp
- deterministic fingerprint

Designed for audit logging and reproducibility.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
import hashlib
import json
import time
import uuid


@dataclass
class RiskTraceRecord:
    trace_id: str
    timestamp: float
    fingerprint: str
    risk_score: float
    risk_level: str
    lens_scores: Dict
    metadata: Optional[Dict]


class EpistemicRiskTrace:

    def __init__(self):
        pass

    def _fingerprint(self, text: str) -> str:

        normalized = text.strip().encode("utf-8")

        return hashlib.sha256(normalized).hexdigest()

    def create_trace(
        self,
        text: str,
        risk_score: float,
        risk_level: str,
        lens_scores: Dict,
        metadata: Optional[Dict] = None
    ) -> RiskTraceRecord:

        fingerprint = self._fingerprint(text)

        record = RiskTraceRecord(
            trace_id=str(uuid.uuid4()),
            timestamp=time.time(),
            fingerprint=fingerprint,
            risk_score=risk_score,
            risk_level=risk_level,
            lens_scores=lens_scores,
            metadata=metadata or {}
        )

        return record

    def to_json(self, trace: RiskTraceRecord) -> str:

        return json.dumps(asdict(trace), indent=2)
