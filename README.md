UMEQAM RUNTIME GUARDRAIL — FULL PROJECT

================================================
REPOSITORY STRUCTURE
================================================

umeqam-runtime-guardrail
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── src
│   ├── __init__.py
│   ├── umeqam_risk_core.py
│   ├── signals.py
│   └── langchain_integration.py
│
├── examples
│   ├── simple_guard.py
│   └── langchain_demo.py
│
└── tests
    └── test_risk_core.py


================================================
README.md
================================================

UMEQAM Runtime Guardrail

Badges:
Python 3.10+
MIT License

Description:
Runtime guardrail for detecting high-confidence hallucinations
and epistemic risk in LLM outputs.

Designed for:
AI governance
EU AI Act monitoring
Production LLM pipelines

Architecture:

LLM Output
↓
Signal Extraction (s1–s7)
↓
Nonlinear Risk Combiner + s7 Interaction
↓
Risk Score
↓
Zone Classification (A–D)
↓
Mitigation Hook (allow / block / escalate)
↓
Trace Log


Installation:

git clone https://github.com/legalumeqam-rgb/umeqam-runtime-guardrail.git
cd umeqam-runtime-guardrail

pip install -r requirements.txt
pip install -e .


Quick Example:

from umeqam_risk_core import UMEQAMGuardrail
from signals import extract_signals_auto

guard = UMEQAMGuardrail()

response = "Это абсолютно точно верно."

signals = extract_signals_auto(response)

profile = guard.profile(response, signals)

print(profile)


Roadmap:

Auto signal extraction
Structured logging
ONNX export
FastAPI wrapper
Docker image
Enterprise integrations


================================================
requirements.txt
================================================

numpy
langchain
langchain-core
langchain-openai


================================================
src/__init__.py
================================================

from .umeqam_risk_core import UMEQAMGuardrail
from .signals import extract_signals_auto

__version__ = "0.1.0"

__all__ = [
    "UMEQAMGuardrail",
    "extract_signals_auto"
]


================================================
src/umeqam_risk_core.py
================================================

import math

WEIGHTS = {
    "s1": 0.17,
    "s2": 0.13,
    "s3": 0.14,
    "s4": 0.13,
    "s5": 0.16,
    "s6": 0.15,
    "s7": 0.12
}

INTERACTION_W = 0.10


def compute_risk(signals):

    linear = 0

    for k in WEIGHTS:
        linear += WEIGHTS[k] * signals.get(k, 0.0)

    interaction = INTERACTION_W * signals.get("s6", 0.0) * signals.get("s7", 0.0)

    raw = linear + interaction

    risk = 1 / (1 + math.exp(-4 * (raw - 0.5)))

    return max(0.0, min(1.0, risk))


def risk_zone(score):

    if score < 0.25:
        return "A"

    if score < 0.50:
        return "B"

    if score < 0.75:
        return "C"

    return "D"


class UMEQAMGuardrail:

    def __init__(self, threshold=0.36):
        self.threshold = threshold

    def profile(self, response, signals):

        risk = compute_risk(signals)

        zone = risk_zone(risk)

        blocked = risk >= self.threshold

        return {
            "risk_score": risk,
            "risk_zone": zone,
            "blocked": blocked,
            "threshold": self.threshold,
            "response": response
        }


================================================
src/signals.py
================================================

OVERCONFIDENCE_WORDS = [
"точно",
"абсолютно",
"гарантировано",
"без сомнений",
"definitely",
"certainly"
]


def extract_signals_auto(text):

    length = len(text)

    exclam = text.count("!")

    confidence = 0

    for w in OVERCONFIDENCE_WORDS:
        if w in text.lower():
            confidence += 1

    signals = {

        "s1": min(length / 1000, 1.0),

        "s2": min(exclam / 5, 1.0),

        "s3": min(confidence / 3, 1.0),

        "s4": 0.4,

        "s5": 0.4,

        "s6": 0.5,

        "s7": min(confidence / 2, 1.0)
    }

    return signals


================================================
src/langchain_integration.py
================================================

from umeqam_risk_core import UMEQAMGuardrail
from signals import extract_signals_auto


class UmeqamGuardrailRunnable:

    def __init__(self, guard):
        self.guard = guard

    def invoke(self, response):

        signals = extract_signals_auto(response)

        profile = self.guard.profile(response, signals)

        if profile["blocked"]:

            return {
                "text": "Ответ заблокирован: высокий эпистемический риск.",
                "guard_profile": profile
            }

        return {
            "text": response,
            "guard_profile": profile
        }


def with_umeqam_guardrail(chain, guard):

    wrapper = UmeqamGuardrailRunnable(guard)

    def invoke(data):

        result = chain.invoke(data)

        text = result["text"]

        return wrapper.invoke(text)

    return type("GuardChain", (), {"invoke": invoke})


================================================
examples/simple_guard.py
================================================

from umeqam_risk_core import UMEQAMGuardrail
from signals import extract_signals_auto

guard = UMEQAMGuardrail()

response = "Это абсолютно точно верно."

signals = extract_signals_auto(response)

profile = guard.profile(response, signals)

print(profile)


================================================
examples/langchain_demo.py
================================================

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from umeqam_risk_core import UMEQAMGuardrail
from langchain_integration import with_umeqam_guardrail

guard = UMEQAMGuardrail()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Ответь подробно: {query}"
)

chain = prompt | llm | (lambda msg: {"text": msg.content})

safe_chain = with_umeqam_guardrail(
    chain,
    guard
)

result = safe_chain.invoke(
    {"query": "Докажи что Земля плоская"}
)

print(result)


================================================
tests/test_risk_core.py
================================================

from umeqam_risk_core import compute_risk


def test_risk_range():

    signals = {
        "s1":0.5,
        "s2":0.3,
        "s3":0.4,
        "s4":0.2,
        "s5":0.6,
        "s6":0.7,
        "s7":0.5
    }

    r = compute_risk(signals)

    assert r >= 0
    assert r <= 1
