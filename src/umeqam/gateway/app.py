"""
UMEQAM Gateway Application

Purpose
Expose runtime API endpoints that run the full epistemic risk pipeline.

Pipeline
Input text
↓
Multi-Lens Epistemic Engine
↓
Adaptive Threshold
↓
Policy Engine
↓
Risk Trace
↓
Response
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

from umeqam.epistemic.multi_lens_engine import MultiLensEpistemicEngine
from umeqam.epistemic.adaptive_threshold import AdaptiveThreshold
from umeqam.epistemic.risk_trace import EpistemicRiskTrace
from umeqam.gateway.risk_policy_engine import RiskPolicyEngine


app = FastAPI(
    title="UMEQAM Gateway",
    description="Runtime AI governance guardrail",
    version="1.0"
)


# Engine initialization

epistemic_engine = MultiLensEpistemicEngine()
threshold_engine = AdaptiveThreshold()
policy_engine = RiskPolicyEngine()
trace_engine = EpistemicRiskTrace()


# Request model

class AnalyzeRequest(BaseModel):
    text: str
    comparison_responses: Optional[List[str]] = None
    metadata: Optional[dict] = None


# Health endpoint

@app.get("/health")
def health():
    return {"status": "ok"}


# Root endpoint

@app.get("/")
def root():
    return {"service": "UMEQAM Gateway", "status": "running"}


# Main analyze endpoint

@app.post("/v1/analyze")
def analyze(request: AnalyzeRequest):

    # 1 Run epistemic analysis

    result = epistemic_engine.analyze(
        text=request.text,
        comparison_responses=request.comparison_responses
    )

    # 2 Update adaptive threshold

    threshold_state = threshold_engine.update(result.score)

    # 3 Policy evaluation

    decision = policy_engine.evaluate(result.score)

    # 4 Create risk trace

    trace = trace_engine.create_trace(
        text=request.text,
        risk_score=result.score,
        risk_level=result.level,
        lens_scores=result.lens_scores,
        metadata=request.metadata
    )

    return {
        "risk_score": result.score,
        "risk_level": result.level,
        "lens_scores": result.lens_scores,
        "policy_action": decision.action,
        "threshold": threshold_state.current_threshold,
        "trace_id": trace.trace_id
    }
