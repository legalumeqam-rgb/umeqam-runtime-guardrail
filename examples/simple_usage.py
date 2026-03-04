from umeqam_runtime_guardrail import UMEQAMGuardrail

guard = UMEQAMGuardrail(threshold=0.36)

profile = guard.profile(
    response="This is absolutely correct without any doubt.",
    signals={"s1": 0.45, "s2": 0.28, "s3": 0.85, "s4": 0.22, "s5": 0.35, "s6": 0.78, "s7": 0.92},
    ats_proxy=0.61
)

print(profile)

if profile["blocked"]:
    raise ValueError("High epistemic risk detected")
