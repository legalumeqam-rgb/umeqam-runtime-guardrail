# UMEQAM Runtime Guardrail

**Runtime epistemic risk mitigation for LLM pipelines under EU AI Act.**

### Key features
- 7-axis nonlinear risk combiner + s7 self-signal damping  
- Deterministic scoring with fingerprint lock  
- ONNX export for production inference  
- LangChain callback for real-time blocking  
- Joint risk + ATS regime classification  

### Quick start
```python
from umeqam_guardrail import UMEQAMGuardrail

guard = UMEQAMGuardrail()
profile = guard.profile(response="...", signals={...})
if profile["risk_zone"] in ["C", "D"]:
    raise ValueError("High epistemic risk")
