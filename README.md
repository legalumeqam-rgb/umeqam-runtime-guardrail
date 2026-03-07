# UMEQAM Runtime Guardrail

Experimental runtime guardrail for LLM pipelines.

The guardrail sits between the language model and the application layer and evaluates generated outputs before they reach the application.

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

## Installation

```bash
git clone https://github.com/<your-username>/umeqam-runtime-guardrail.git
cd umeqam-runtime-guardrail
pip install .
```

Requirements:

- Python 3.10+
- pip


---

## Quick Start

```python
from umeqam_runtime_guardrail import Guardrail

guard = Guardrail()

result = guard.evaluate("Example LLM response")

print("Risk score:", result.risk_score)
print("Risk zone:", result.risk_zone)
```

Example output:

```
Risk score: 0.23
Risk zone: B
```


---

## Running the Example

```bash
python main.py
```

Example output:

```
Input: Example LLM response
Risk score: 0.23
Risk zone: B
Decision: allow
```


---

## Project Structure

```
umeqam-runtime-guardrail/

docs/
examples/
src/
umeqam_runtime_guardrail/

main.py
test_run.py
requirements.txt
pyproject.toml
LICENSE
README.md
```


---

## Status

Experimental runtime guardrail prototype.

Capabilities:

- runtime evaluation
- deterministic risk scoring
- zone classification (A–D)
- allow / block / escalate routing


---

## License

MIT License
