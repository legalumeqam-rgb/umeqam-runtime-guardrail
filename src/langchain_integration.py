# src/langchain_integration.py
from typing import Any, Callable, Dict, Optional, Union
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.outputs import LLMResult, Generation
from .umeqam_risk_core import UMEQAMGuardrail  # импорт твоего основного класса

class UmeqamGuardrailRunnable(Runnable[Dict[str, Any], Dict[str, Any]]):
    """
    LangChain Runnable wrapper для UMEQAMGuardrail.
    Применяет guardrail к тексту после LLM или chain.
    Возвращает input + 'guard_profile' если passed, иначе fallback или raise.
    """
    def __init__(
        self,
        guard: UMEQAMGuardrail,
        response_key: str = "text",  # ключ, где лежит строка ответа (обычно "text" или "output")
        signals: Optional[Dict[str, float]] = None,  # если хочешь вручную передать — но лучше extractor
        ats_proxy_key: str = "ats_proxy",  # откуда брать ats_proxy если в input dict
        fallback_response: str = "Извините, но данный ответ не прошёл проверку безопасности.",
        on_block: Optional[Callable[[Dict], Any]] = None,  # callback при block (по умолчанию raise)
    ):
        self.guard = guard
        self.response_key = response_key
        self.signals = signals or {}  # placeholder, потом заменим на extractor
        self.ats_proxy_key = ats_proxy_key
        self.fallback_response = fallback_response
        self.on_block = on_block or (lambda profile: ValueError(
            f"Blocked by UMEQAM Guardrail: zone={profile['risk_zone']}, "
            f"regime={profile.get('regime')}, score={profile['risk_score']:.3f}"
        ))

    def invoke(self, input: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        # Нормализуем input → извлекаем текст ответа
        if isinstance(input, dict):
            response = input.get(self.response_key, "")
            ats_proxy = input.get(self.ats_proxy_key, 0.5)  # default 0.5 если нет
        elif isinstance(input, LLMResult):
            response = input.generations[0][0].text if input.generations else ""
            ats_proxy = 0.5
        elif isinstance(input, str):
            response = input
            ats_proxy = 0.5
        else:
            response = str(input)
            ats_proxy = 0.5

        if not response.strip():
            return input  # пустой → пропускаем

        # Пока signals вручную или placeholder (добавим auto-extractor позже)
        signals = self.signals.copy() if self.signals else {f"s{i}": 0.5 for i in range(1, 8)}

        profile = self.guard.profile(
            response=response,
            signals=signals,
            ats_proxy=ats_proxy
        )

        if profile["blocked"]:
            if self.on_block:
                raise self.on_block(profile)
            return self.fallback_response  # или dict с fallback

        # Успех: возвращаем input + метаданные guard
        output = input.copy() if isinstance(input, dict) else {"text": response}
        output["guard_profile"] = profile
        return output

# Helper для удобства
def with_umeqam_guardrail(
    chain: Runnable,
    guard: UMEQAMGuardrail,
    **runnable_kwargs
) -> Runnable:
    """
    Оборачивает любой chain guardrail'ом в конце.
    Пример: safe_chain = with_umeqam_guardrail(prompt | llm, guard)
    """
    guard_runnable = UmeqamGuardrailRunnable(guard=guard, **runnable_kwargs)
    return chain | guard_runnable
