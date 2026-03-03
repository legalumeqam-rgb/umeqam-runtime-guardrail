# UMEQAM Guardrail

Runtime защита от ошибок с высокой уверенностью в LLM (EU AI Act)

Ключевые возможности:
- 7 сигналов + s7 демпфирование
- Детерминированный расчёт риска
- ONNX + LangChain
- Блокировка/эскалация в реальном времени

Быстрый запуск:
```python
from umeqam_guardrail import UMEQAMGuardrail

guard = UMEQAMGuardrail()
profile = guard.profile(response="...", signals={...})
if profile["risk_zone"] in ["C", "D"]:
    raise ValueError("Высокий риск")
