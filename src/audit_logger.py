# src/audit_logger.py
import json
import hashlib
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file: str = "audit_trail.jsonl"):
        self.log_file = log_file

    def log(self, profile: dict, response: str = "", extra: dict = None):
        """Логирует каждый вызов guardrail в JSONL (для аудита и EU AI Act)"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "response_hash": hashlib.sha256(response.encode('utf-8')).hexdigest() if response else "",
            "risk_score": profile.get("risk_score"),
            "risk_zone": profile.get("risk_zone"),
            "blocked": profile.get("blocked"),
            "regime": profile.get("regime"),
            "threshold": profile.get("threshold"),
            "fingerprint": profile.get("fingerprint"),
            "extra": extra or {}
        }

        # Tamper-proof hash всей записи (чтобы нельзя было подделать)
        entry_str = json.dumps(entry, sort_keys=True, ensure_ascii=False)
        entry["audit_hash"] = hashlib.sha256(entry_str.encode('utf-8')).hexdigest()

        # Запись в конец файла (append mode)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
