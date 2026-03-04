from fastapi import APIRouter
from pydantic import BaseModel

from umeqam.umeqam_risk_core import UMEQAMGuardrail

router = APIRouter()

guard = UMEQAMGuardrail(threshold=0.36)


class AnalyzeRequest(BaseModel):
    text: str


@router.post("/v1/analyze")
def analyze(req: AnalyzeRequest):

    profile = guard.profile_auto(req.text)

    score, zone = guard.score_and_zone(profile)

    return {
        "risk_score": score,
        "zone": zone,
        "profile": profile
    }