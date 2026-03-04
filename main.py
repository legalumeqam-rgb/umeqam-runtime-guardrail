# main.py - FastAPI wrapper for UMEQAM Runtime Guardrail + Epistemic Engine

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Existing guardrail engine
from umeqam_runtime_guardrail import UMEQAMGuardrail

# New epistemic engine
from umeqam.epistemic.multi_lens_engine import MultiLensEpistemicEngine


app = FastAPI(
    title="UMEQAM Runtime Guardrail API",
    description="Runtime epistemic guardrail for LLM outputs under EU AI Act",
    version="0.2.0"
)

# Existing runtime guardrail
guard = UMEQAMGuardrail(threshold=0.36)

# New epistemic engine
epistemic_engine = MultiLensEpistemicEngine()


# ===============================
# Request Models
# ===============================

class CheckRequest(BaseModel):
    response: str
    ats_proxy: float = 0.5
    use_auto_signals: bool = True


class CheckResponse(BaseModel):
    risk_score: float
    risk_zone: str
    blocked: bool
    regime: str
    threshold: float
    fingerprint: str


class EpistemicRequest(BaseModel):
    text: str
    comparison_responses: Optional[List[str]] = None


# ===============================
# Health Endpoint
# ===============================

@app.get("/health")
def health():
    return {"status": "ok", "engine": "UMEQAM"}


# ===============================
# Existing Guardrail Endpoint
# ===============================

@app.post("/check", response_model=CheckResponse)
async def check(request: CheckRequest):

    try:

        if request.use_auto_signals:
            profile = guard.profile_auto(
                request.response,
                ats_proxy=request.ats_proxy
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Manual signals required when use_auto_signals=false"
            )

        return CheckResponse(
            risk_score=profile["risk_score"],
            risk_zone=profile["risk_zone"],
            blocked=profile["blocked"],
            regime=profile.get("regime", "UNKNOWN"),
            threshold=profile["threshold"],
            fingerprint=profile.get("fingerprint", "v0.1.0")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# New Epistemic Engine Endpoint
# ===============================

@app.post("/v1/analyze")
async def analyze_epistemic(request: EpistemicRequest):

    try:

        result = epistemic_engine.analyze(
            text=request.text,
            comparison_responses=request.comparison_responses
        )

        return {
            "risk_score": result.score,
            "risk_level": result.level,
            "lens_scores": result.lens_scores
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# Root Endpoint
# ===============================

@app.get("/")
def root():
    return {
        "service": "UMEQAM Runtime Guardrail",
        "version": "0.2.0",
        "engines": [
            "UMEQAMGuardrail",
            "EpistemicEngine"
        ]
    }


# ===============================
# Run server
# ===============================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
