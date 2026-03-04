import yaml
from pathlib import Path


class PolicyEngine:

    def __init__(self, config_path="config/policy.yaml"):

        path = Path(config_path)

        if not path.exists():
            raise RuntimeError(f"Policy config not found: {config_path}")

        with open(path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.zones = self.config["zones"]
        self.thresholds = self.config["thresholds"]

    def evaluate(self, zone: str, score: float):

        zone_cfg = self.zones.get(zone)

        if zone_cfg is None:
            return {
                "action": "allow",
                "message": "",
                "zone": zone,
                "score": score
            }

        return {
            "action": zone_cfg.get("action", "allow"),
            "message": zone_cfg.get("message", ""),
            "zone": zone,
            "score": score
        }
