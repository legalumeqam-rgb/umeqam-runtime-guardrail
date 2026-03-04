# UMEQAM Runtime Guardrail

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Deterministic runtime epistemic risk mitigation for LLM pipelines (EU AI Act–oriented).

UMEQAM Runtime Guardrail is a plug-and-play runtime scoring layer that sits between an LLM response and your application output. It produces a reproducible risk score, assigns a risk zone (A–D), and supports blocking or escalation workflows.

---

## Key Features

- 7-signal nonlinear risk combiner
- s7 self-signal damping
- Deterministic scoring (audit-friendly)
- Risk zones A / B / C / D
- Runtime mitigation hook (allow / block / escalate)
- Joint Risk × ATS regime classification

---

## Architecture

LLM Output
↓
Signal Extraction (s1–s7)
↓
Nonlinear Risk Combiner + s7 Damping
↓
Risk Zone Classification (A–D)
↓
Mitigation Hook (allow / block / escalate)
↓
Trace Log

---

## Installation

pip install -r requirements.txt
pip install -e .

---

## Quick Start

from umeqam_guardrail import UMEQAMGuardrail

guard = UMEQAMGuardrail(threshold=0.36)

profile = guard.profile(
    response="This is absolutely correct without any doubt.",
    signals={
        "s1": 0.45,
        "s2": 0.28,
        "s3": 0.85,
        "s4": 0.22,
        "s5": 0.35,
        "s6": 0.78,
        "s7": 0.92
    },
    ats_proxy=0.61
)

print(profile)

if profile["blocked"]:
    raise ValueError("High epistemic risk detected")

---

## Example Output

{
  "risk_score": 0.72,
  "risk_zone": "C",
  "blocked": true,
  "regime": "CFW_LOCK_IN",
  "threshold": 0.36,
  "fingerprint": "locked:v0.1.0"
}

If risk zone is C or D, the system can block the response or escalate to human review.

---

## License

MIT License — see LICENSE.

---

## Disclaimer

This project provides runtime risk scoring and mitigation hooks for LLM outputs.
It does not guarantee correctness and should be used as part of a broader governance and human oversight system.
