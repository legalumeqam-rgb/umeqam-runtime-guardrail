# UMEQAM Runtime Guardrail

Experimental runtime guardrail for LLM pipelines.

The guardrail sits between the language model and the application layer and evaluates generated outputs for structural risk signals.

It produces a deterministic risk classification before the response reaches the application.

Pipeline:

LLM Output  
↓  
UMEQAM Runtime Guardrail  
↓  
risk_score  
risk_zone (A–D)  
↓  
allow / block / escalate


---

# Installation

Clone the repository and install locally:

```bash
git clone https://github.com/<your-username>/umeqam-runtime-guardrail.git
cd umeqam-runtime-guardrail
pip install .
