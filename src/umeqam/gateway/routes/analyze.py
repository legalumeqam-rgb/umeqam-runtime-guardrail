from fastapi import APIRouter
from pydantic import BaseModel

from src.umeqam_risk_core import UMEQAMGuardrail

router = APIRouter()from fastapi import APIRouter
from pydantic import BaseModel

from src.umeqam_risk_core import UMEQAMGuardrail
from src.umeqam.gateway.policy import PolicyEngine

router = APIRouter()

guard = UMEQAMGuardrail(threshold=0.36)
policy = PolicyEngine("config/policy.yaml")


class AnalyzeRequest(BaseModel):
    text: str


def _severity(action: str) -> int:
    order = {"allow": 0, "warn": 1, "restrict": 2, "block": 3}
    return order.get(action or "allow", 0)


def _threshold_action(score: float, thresholds: dict) -> str:
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


@router.post("/v1/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text

    # 1) Guardrail scoring
    profile = guard.profile_auto(text)
    score, zone = guard.score_and_zone(profile)

    # 2) Policy decision (zone + thresholds)
    zone_decision = policy.evaluate(zone, score)
    thr_action = _threshold_action(score, policy.thresholds)

    final_action = zone_decision["action"]
    if _severity(thr_action) > _severity(final_action):
        final_action = thr_action

    message = zone_decision.get("message", "")

    # 3) Enforcement result
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
        return {
            "restricted": True,
            "notice": message or "Restricted by policy.",
            "risk_score": score,
            "zone": zone,
            "policy": final_action,
            "profile": profile,
        }

    if final_action == "warn":
        return {
            "warning": True,
            "notice": message or "Warning by policy.",
            "risk_score": score,
            "zone": zone,
            "policy": final_action,
            "profile": profile,
        }

    return {
        "risk_score": score,
        "zone": zone,
        "policy": "allow",
        "profile": profile,
    }

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
