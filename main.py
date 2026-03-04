import sys
import os

# добавляем папку src в путь Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from umeqam_runtime_guardrail.guardrail import UMEQAMGuardrail


app = FastAPI(
    title="UMEQAM Runtime Guardrail API",
    description="Runtime epistemic guardrail for LLM outputs",
    version="0.1.0"
)

guard = UMEQAMGuardrail(threshold=0.36)


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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/check", response_model=CheckResponse)
async def check(request: CheckRequest):

    try:
        profile = guard.profile_auto(
            request.response,
            ats_proxy=request.ats_proxy
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


@app.get("/")
def root():
    return {
        "service": "UMEQAM Runtime Guardrail",
        "status": "running"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
