from fastapi import APIRouter
from pydantic import BaseModel

from src.umeqam_risk_core import UMEQAMGuardrail
from src.umeqam.gateway.policy import PolicyEngine

router = APIRouter()

guard = UMEQAMGuardrail(threshold=0.36)
policy = PolicyEngine("config/policy.yaml")


class ChatRequest(BaseModel):
    message: str


def _severity(action: str) -> int:
    order = {"allow": 0, "warn": 1, "restrict": 2, "block": 3}
    return order.get(action or "allow", 0)


def _threshold_action(score: float, thresholds: dict) -> str:
    # thresholds: warn/restrict/block
    warn_t = float(thresholds.get("warn", 1.0))
    restrict_t = float(thresholds.get("restrict", 1.0))
    block_t = float(thresholds.get("block", 1.0))

    if score >= block_t:
        return "block"
    if score >= restrict_t:
        return "restrict"
    if score >= warn_t:
        return "warn"
    return "allow"


@router.post("/v1/chat/completions")
def chat(req: ChatRequest):
    # 1) LLM stub (пока echo; позже заменим на real provider proxy)
    llm_response = f"Echo: {req.message}"

    # 2) Guardrail scoring
    profile = guard.profile_auto(llm_response)
    score, zone = guard.score_and_zone(profile)

    # 3) Policy decision by zone + thresholds
    zone_decision = policy.evaluate(zone, score)  # action/message from zone map
    thr_action = _threshold_action(score, policy.thresholds)

    # take stricter action
    final_action = zone_decision["action"]
    if _severity(thr_action) > _severity(final_action):
        final_action = thr_action

    message = zone_decision.get("message", "")

    # 4) Enforce
    if final_action == "block":
        return {
            "blocked": True,
            "reason": message or "Blocked by policy.",
            "risk_score": score,
            "zone": zone,
            "policy": final_action,
            "profile": profile,
        }

    if final_action == "restrict":
        # Restrict = возвращаем, но помечаем как ограниченный ответ
        return {
            "restricted": True,
            "notice": message or "Restricted by policy.",
            "response": llm_response,
            "risk_score": score,
            "zone": zone,
            "policy": final_action,
            "profile": profile,
        }

    if final_action == "warn":
        return {
            "warning": True,
            "notice": message or "Warning by policy.",
            "response": llm_response,
            "risk_score": score,
            "zone": zone,
            "policy": final_action,
            "profile": profile,
        }

    # allow
    return {
        "response": llm_response,
        "risk_score": score,
        "zone": zone,
        "policy": "allow",
        "profile": profile,
    }
