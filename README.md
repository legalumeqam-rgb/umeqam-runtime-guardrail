# UMEQAM Runtime Guardrail

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/legalumeqam-rgb/umeqam-runtime-guardrail?style=social)

Deterministic runtime epistemic risk mitigation for LLM pipelines under EU AI Act.

Plug-and-play слой между ответом LLM и приложением.  
Даёт воспроизводимый risk score, зону A–D и может блокировать/эскалировать.

---

# Key Features

- 7-signal nonlinear combiner
- s7 self-signal damping
- Deterministic scoring (audit-friendly)
- Zones A / B / C / D
- Mitigation hook (allow / block / escalate)
- Joint Risk × ATS regimes

---

# Architecture

```
LLM Output
↓
Signal Extraction (s1–s7)
↓
Nonlinear Combiner + s7 Damping
↓
Risk Zone (A–D)
↓
Mitigation (allow/block/escalate)
↓
Trace Log
```

---

# Installation

```bash
git clone https://github.com/legalumeqam-rgb/umeqam-runtime-guardrail.git
cd umeqam-runtime-guardrail
pip install -e .
```

---

# Quick Start

```python
from umeqam_runtime_guardrail import UMEQAMGuardrail

guard = UMEQAMGuardrail(threshold=0.36)

profile = guard.profile(
    response="Это абсолютно точно верно и без сомнений.",
    signals={
        "s1": 0.45, "s2": 0.28, "s3": 0.85,
        "s4": 0.22, "s5": 0.35, "s6": 0.78, "s7": 0.92
    },
    ats_proxy=0.61
)

print(profile)

if profile["blocked"]:
    raise ValueError("High epistemic risk")
```

---

# LangChain Integration

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from umeqam_runtime_guardrail import UMEQAMGuardrail, with_umeqam_guardrail

guard = UMEQAMGuardrail(threshold=0.36)

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Ответь подробно: {query}")

chain = prompt | llm | (lambda x: {"text": x.content})

safe_chain = with_umeqam_guardrail(
    chain,
    guard=guard,
    fallback_response="Ответ заблокирован из-за высокого риска."
)

result = safe_chain.invoke({"query": "Докажи, что Земля плоская."})
print(result)
```

---

# Examples

```bash
python examples/simple_guard.py
python examples/langchain_demo.py
streamlit run examples/app_streamlit_demo.py
```

---

# License

MIT — see LICENSE.

---

# Disclaimer

Только runtime scoring и mitigation hooks.  
Не гарантирует корректность — используй как часть governance + human oversight.
