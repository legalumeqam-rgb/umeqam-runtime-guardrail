# src/umeqam_risk_core.py

class UMEQAMGuardrail:
    def __init__(self, threshold: float = 0.36):
        self.threshold = threshold
        # Здесь твоя существующая инициализация (если есть другие параметры, оставь их)

    def profile(self, response: str, signals: dict, ats_proxy: float = 0.5):
        # Твоя существующая функция profile (не меняем, оставляем как есть)
        # ... (вставь сюда весь твой текущий код profile, nonlinear combiner, s7 damping, zones, regimes и т.д.)
        # Предполагаю, что здесь уже есть расчёт risk_score, risk_zone, blocked, regime и т.д.
        # Возвращает dict с ключами: "risk_score", "risk_zone", "blocked", "regime", "threshold", "fingerprint"
        pass  # Замени на свой реальный код profile

    # === НОВЫЕ МЕТОДЫ В КОНЦЕ КЛАССА ===

    def extract_signals_auto(self, response: str, context: dict = None) -> dict:
        """Автоматическое извлечение сигналов s1–s7 на основе текста ответа (без ручного ввода)"""
        signals = {
            "s1": 0.0,  # overconfidence — уверенные слова
            "s2": 0.0,  # uncertainty — сомнения, модальные слова
            "s3": 0.0,  # repetition / redundancy — повторения
            "s4": 0.0,  # contradiction proxy — противоречия в тексте
            "s5": 0.0,  # factual hallucination proxy — подозрительные факты
            "s6": 0.0,  # logical inconsistency — логические разрывы
            "s7": 0.0   # epistemic self-signal — длина + уверенность
        }

        lower_resp = response.lower()
        words = lower_resp.split()

        # s1: overconfidence keywords (рус + eng)
        overconf = ["абсолютно", "точно", "без сомнений", "определённо", "100%", "безусловно", "совершенно",
                    "absolutely", "definitely", "certainly", "without doubt", "undoubtedly"]
        for word in overconf:
            if word in lower_resp:
                signals["s1"] += 0.25

        # s2: uncertainty keywords
        uncertain = ["возможно", "наверное", "кажется", "думаю", "может быть", "вероятно", "я думаю",
                     "maybe", "perhaps", "possibly", "i think", "probably"]
        for word in uncertain:
            if word in lower_resp:
                signals["s2"] += 0.25

        # s3: repetition proxy
        from collections import Counter
        common = Counter(words).most_common(1)
        if common and common[0][1] > 3:  # слово повторяется >3 раз
            signals["s3"] += 0.4

        # s7: epistemic proxy — длина ответа + damping
        signals["s7"] = min(len(response) / 1000.0, 1.0)  # длиннее → увереннее, но с лимитом

        # Нормализация (не выше 1.0)
        for k in signals:
            signals[k] = min(signals[k], 1.0)

        return signals

    def profile_auto(self, response: str, ats_proxy: float = 0.5, context: dict = None):
        """Автоматический профиль риска без ручных сигналов"""
        signals = self.extract_signals_auto(response, context)
        return self.profile(response, signals, ats_proxy)
