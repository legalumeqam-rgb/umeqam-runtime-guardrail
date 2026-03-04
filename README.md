# UMEQAM Runtime Guardrail

<<<<<<< HEAD
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
=======
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/legalumeqam-rgb/umeqam-runtime-guardrail?style=social)

Deterministic runtime epistemic risk control layer for LLM pipelines.

UMEQAM provides a reproducible risk score, risk zones (A–D) and mitigation hooks that allow systems to detect, block or escalate epistemically unsafe outputs in real time.

Designed for EU AI Act governance, enterprise AI systems, and high-risk LLM deployments.

--------------------------------------------------

WHAT UMEQAM IS

UMEQAM is a runtime guardrail engine that sits between the LLM and the application.

Instead of relying on another LLM to judge responses, UMEQAM uses a deterministic signal-based scoring model.

Advantages:

- reproducible
- audit-friendly
- low latency
- enterprise compliant

--------------------------------------------------

CORE CONCEPT

UMEQAM evaluates responses using multiple epistemic signals.

These signals are combined using a nonlinear combiner with self-signal damping.

Architecture:
>>>>>>> 4cc336a2003ebe0c8b2dbe4b25e7568758a3c716

LLM Output
↓
Signal Extraction (s1–s7)
↓
<<<<<<< HEAD
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
=======
Nonlinear Combiner + s7 Damping
↓
Risk Score
↓
Risk Zone (A–D)
↓
Mitigation (allow / block / escalate)
↓
Trace Log

--------------------------------------------------

KEY FEATURES

Deterministic Risk Engine

No judge LLM required.
Scoring is reproducible and suitable for regulated environments.

7-Signal Epistemic Model

Signals represent behavioral indicators of unreliable reasoning.

Examples include:

- reasoning instability
- epistemic hedging
- unsupported certainty
- signal damping (s7)

s7 Self-Signal Damping

The system reduces risk when the model demonstrates epistemic uncertainty or self-correction.

Risk Zones

Zone A → Safe
Zone B → Monitor
Zone C → Warn / Escalate
Zone D → Block

Mitigation Hooks

Applications can define custom actions:

- allow
- warn
- block
- escalate

Trace Logging

Every decision can be logged for audit, debugging and compliance.

--------------------------------------------------

ARCHITECTURE

LLM Output
↓
Signal Extraction (s1–s7)
↓
Nonlinear Combiner + s7 Damping
↓
Risk Score
↓
Risk Zone (A–D)
↓
Mitigation (allow / block / escalate)
↓
Trace Log

--------------------------------------------------

INSTALLATION

git clone https://github.com/legalumeqam-rgb/umeqam-runtime-guardrail.git
cd umeqam-runtime-guardrail
pip install -e .

--------------------------------------------------

QUICK START

from umeqam_runtime_guardrail import UMEQAMGuardrail
>>>>>>> 4cc336a2003ebe0c8b2dbe4b25e7568758a3c716

guard = UMEQAMGuardrail(threshold=0.36)

profile = guard.profile(
<<<<<<< HEAD
    response="This is absolutely correct without any doubt.",
=======
    response="Это абсолютно точно верно и без сомнений.",
>>>>>>> 4cc336a2003ebe0c8b2dbe4b25e7568758a3c716
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
<<<<<<< HEAD
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
=======
    raise ValueError("High epistemic risk")

--------------------------------------------------

LANGCHAIN INTEGRATION

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from umeqam_runtime_guardrail import UMEQAMGuardrail, with_umeqam_guardrail

guard = UMEQAMGuardrail(threshold=0.36)

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Ответь подробно: {query}"
)

chain = prompt | llm | (lambda x: {"text": x.content})

safe_chain = with_umeqam_guardrail(
    chain,
    guard=guard,
    fallback_response="Response blocked due to high epistemic risk."
)

result = safe_chain.invoke({
    "query": "Докажи, что Земля плоская."
})

print(result)

--------------------------------------------------

UMEQAM GATEWAY (NEXT ARCHITECTURE)

The next evolution of UMEQAM is a runtime gateway.

Instead of embedding the library inside each application, a centralized proxy controls LLM traffic.

Client App
↓
UMEQAM Gateway
↓
LLM Provider (OpenAI / Anthropic / Local)

Gateway responsibilities:

- request routing
- guardrail enforcement
- policy management
- audit logging
- metrics

--------------------------------------------------

PLATFORM ARCHITECTURE

                UMEQAM PLATFORM

            Control Plane
        (policies / audit / users)
                │
                ▼
            UMEQAM API
                │
        ┌───────────────┐
        │               │
        ▼               ▼
    Runtime Engine   Metrics Engine
        │               │
        ▼               ▼
     Risk Engine     Observability
        │
        ▼
     Mitigation
        │
        ▼
        LLM

--------------------------------------------------

POLICY ENGINE (EXAMPLE)

default_zone_actions:

A: allow
B: allow + log
C: warn + escalate
D: block

overrides:

domain: medical
max_risk: 0.32
action: block

--------------------------------------------------

METRICS

umeqam_risk_score_histogram
umeqam_zone_total_A
umeqam_zone_total_B
umeqam_zone_total_C
umeqam_zone_total_D
umeqam_blocked_total
umeqam_signal_avg_s1
umeqam_signal_avg_s2
umeqam_signal_avg_s3
umeqam_signal_avg_s4
umeqam_signal_avg_s5
umeqam_signal_avg_s6
umeqam_signal_avg_s7

--------------------------------------------------

BENCHMARKS / EVALUATION

Dataset
↓
LLM Responses
↓
UMEQAM Risk Engine
↓
Predicted Risk Scores
↓
Evaluation Metrics

Metrics:

AUROC
Precision
Recall
FPR
HCWR

Example benchmark:

Baseline heuristic → AUROC 0.71
LLM judge → AUROC 0.78
UMEQAM → AUROC 0.83

--------------------------------------------------

EXAMPLE USE CASES

UMEQAM is designed for systems where hallucinations and epistemic instability create operational risk.

Typical deployments include:

- enterprise copilots
- legal AI systems
- financial assistants
- healthcare support tools
- AI agents in regulated environments

--------------------------------------------------

ROADMAP

Phase 1 — Core Hardening

- signal expansion (s1–s15)
- confidence without evidence detector
- improved trace logging
- metrics endpoint

Phase 2 — Runtime Platform

- temporal memory
- stability detection
- policy engine
- multi-model routing

Phase 3 — Enterprise Gateway

- API keys
- multi-tenant support
- rate limiting
- audit export

Phase 4 — Category Leader

- streaming guardrail
- explainable signals
- reliability dashboards
- EU AI Act compliance toolkit

--------------------------------------------------

LICENSE

MIT — see LICENSE.

--------------------------------------------------

DISCLAIMER

UMEQAM performs runtime epistemic risk scoring and mitigation.

It does not guarantee factual correctness and should be used as part of a broader AI governance framework including human oversight.
>>>>>>> 4cc336a2003ebe0c8b2dbe4b25e7568758a3c716
