# src/umeqam_risk_core.py

import hashlib
from datetime import datetime
from .audit_logger import AuditLogger

class UMEQAMGuardrail:
    def __init__(self, threshold: float = 0.36):
        self.threshold = threshold
        self.logger = AuditLogger(log_file="audit_trail.jsonl")  # Логгер включается автоматически
        # Здесь твоя остальная инициализация, если есть (не меняем)

    def profile(self, response: str, signals: dict, ats_proxy: float = 0.5):
        # ТВОЙ СУЩЕСТВУЮЩИЙ КОД profile (вставь сюда весь свой оригинальный код)
        # Пример заглушки — замени на реальный расчёт
        risk_score = 0.72  # ← твой реальный расчёт на основе signals, ats_proxy, s7 damping и т.д.
        risk_zone = "C" if risk_score > 0.4 else "A"  # ← твой реальный код зон
        blocked = risk_score > self.threshold
        regime = "CFW_LOCK_IN" if blocked else "SAFE"
        fingerprint = "locked:v0.1.0"

        profile = {
            "risk_score": risk_score,
            "risk_zone": risk_zone,
            "blocked": blocked,
            "regime": regime,
            "threshold": self.threshold,
            "fingerprint": fingerprint,
            "response": response  # для лога
        }

        # Логируем каждый вызов
        self.logger.log(profile, response=response)

        return profile

    def extract_signals_auto(self, response: str, context: dict = None) -> dict:
        """Автоматическое извлечение сигналов s1–s7 на основе текста ответа"""
        signals = {
            "s1": 0.0, "s2": 0.0, "s3": 0.0,
            "s4": 0.0, "s5": 0.0, "s6": 0.0, "s7": 0.0
        }

        lower_resp = response.lower()
        words = lower_resp.split()

        # s1: overconfidence
        overconf = ["абсолютно", "точно", "без сомнений", "определённо", "100%", "безусловно", "absolutely", "definitely"]
        for word in overconf:
            if word in lower_resp:
                signals["s1"] += 0.25

        # s2: uncertainty
        uncertain = ["возможно", "наверное", "кажется", "думаю", "может быть", "maybe", "perhaps", "i think"]
        for word in uncertain:
            if word in lower_resp:
                signals["s2"] += 0.25

        # s3: repetition
        from collections import Counter
        common = Counter(words).most_common(1)
        if common and common[0][1] > 3:
            signals["s3"] += 0.4

        # s7: epistemic proxy (длина + damping)
        signals["s7"] = min(len(response) / 1000.0, 1.0)

        # Нормализация
        for k in signals:
            signals[k] = min(signals[k], 1.0)

        return signals

    def profile_auto(self, response: str, ats_proxy: float = 0.5, context: dict = None):
        """Автоматический профиль без ручных сигналов"""
        signals = self.extract_signals_auto(response, context)
        profile = self.profile(response, signals, ats_proxy)
        return profile
