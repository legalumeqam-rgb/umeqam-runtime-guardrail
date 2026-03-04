# src/langchain_integration.py
from typing import Any, Callable, Dict, List, Optional, Union
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.outputs import LLMResult, GenerationChunk
from langchain_core.messages import AIMessageChunk
from .umeqam_risk_core import UMEQAMGuardrail  # твой основной класс

class UmeqamGuardrailRunnable(Runnable[Dict[str, Any], Dict[str, Any]]):
    """
    LangChain Runnable, который применяет UMEQAMGuardrail к выходу LLM/chain.
    - Работает с обычным invoke и streaming.
    - Добавляет 'guard_profile' в output если passed.
    - При block: raise (default) или fallback.
    """
    def __init__(
        self,
        guard: UMEQAMGuardrail,
        response_key: str = "text",                  # где искать текст ответа
        signals: Optional[Dict[str, float]] = None,  # фиксированные signals (пока placeholder)
        ats_proxy_key: str = "ats_proxy",            # откуда ats_proxy
        fallback_response: str = "Извините, ответ заблокирован системой безопасности (высокий эпистемический риск).",
        on_block: Optional[Callable[[Dict], Any]] = None,
        extract_signals_func: Optional[Callable[[str, Dict], Dict]] = None,  # для auto в будущем
    ):
        self.guard = guard
        self.response_key = response_key
        self.signals = signals or {}
        self.ats_proxy_key = ats_proxy_key
        self.fallback_response = fallback_response
        self.on_block = on_block or self._default_on_block
        self.extract_signals_func = extract_signals_func

    def _default_on_block(self, profile: Dict) -> None:
        raise ValueError(
            f"UMEQAM Guardrail blocked: zone={profile['risk_zone']}, "
            f"regime={profile.get('regime', 'unknown')}, "
            f"score={profile['risk_score']:.3f}"
        )

    def _extract_response(self, input_data: Any) -> str:
        """Умное извлечение текста из разных форматов LangChain."""
        if isinstance(input_data, dict):
            return input_data.get(self.response_key, "")
        elif isinstance(input_data, LLMResult):
            return input_data.generations[0][0].text if input_data.generations else ""
        elif isinstance(input_data, (str, AIMessageChunk)):
            return str(input_data)
        elif isinstance(input_data, GenerationChunk):
            return input_data.text
        return str(input_data)

    def _get_ats_proxy(self, input_data: Any) -> float:
        if isinstance(input_data, dict):
            return input_data.get(self.ats_proxy_key, 0.5)
        return 0.5

    def invoke(self, input: Any, config: Optional[Dict] = None) -> Any:
        response_text = self._extract_response(input)
        if not response_text.strip():
            return input  # пусто — пропуск

        ats_proxy = self._get_ats_proxy(input)

        # Signals: пока placeholder, скоро auto
        signals = self.signals.copy() if self.signals else {f"s{i}": 0.5 for i in range(1, 8)}
        if self.extract_signals_func:
            signals = self.extract_signals_func(response_text, input if isinstance(input, dict) else {})

        profile = self.guard.profile(
            response=response_text,
            signals=signals,
            ats_proxy=ats_proxy
        )

        if profile["blocked"]:
            self.on_block(profile)
            return self.fallback_response  # если не raise

        # Success: добавляем метаданные
        output = input.copy() if isinstance(input, dict) else {"text": response_text}
        output["guard_profile"] = profile
        return output

    async def ainvoke(self, input: Any, config: Optional[Dict] = None) -> Any:
        # Для async — пока синхронный fallback (можно расширить)
        return self.invoke(input, config)

    def stream(self, input: Any, config: Optional[Dict] = None):
        """Streaming support: собираем chunks, проверяем только на финальном output."""
        # Простая реализация: буферизуем до конца, потом guard
        # (для real-time guard лучше chunk-by-chunk, но это сложнее — phase 2)
        full_text = ""
        for chunk in input:  # предполагаем input уже stream'able
            if isinstance(chunk, GenerationChunk):
                full_text += chunk.text
            elif isinstance(chunk, str):
                full_text += chunk
            yield chunk  # пропускаем chunks до проверки

        # Финальная проверка на собранном
        profile = self.guard.profile(
            response=full_text,
            signals=self.signals or {f"s{i}": 0.5 for i in range(1, 8)},
            ats_proxy=0.5
        )
        if profile["blocked"]:
            raise self.on_block(profile)
        # Если ok — уже всё пропущено

# Удобный wrapper
def with_umeqam_guardrail(
    chain: Runnable,
    guard: UMEQAMGuardrail,
    **kwargs
) -> Runnable:
    """
    Применяет guardrail к любой chain.
    safe_chain = with_umeqam_guardrail(prompt | llm | parser, guard)
    """
    return chain | UmeqamGuardrailRunnable(guard=guard, **kwargs)
