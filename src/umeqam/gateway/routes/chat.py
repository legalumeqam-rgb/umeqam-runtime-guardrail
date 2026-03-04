from fastapi import APIRouter
from pydantic import BaseModel

from umeqam.umeqam_risk_core import UMEQAMGuardrail

router = APIRouter()

guard = UMEQAMGuardrail(threshold=0.36)


class ChatRequest(BaseModel):
    message: str


@router.post("/v1/chat/completions")
def chat(req: ChatRequest):

    # временный mock-ответ (LLM proxy добавим позже)
    llm_response = f"Echo: {req.message}"

    profile = guard.profile_auto(llm_response)

    score, zone = guard.score_and_zone(profile)

    return {
        "response": llm_response,
        "risk_score": score,
        "zone": zone
    }