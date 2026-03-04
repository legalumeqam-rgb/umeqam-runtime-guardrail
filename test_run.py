from src.umeqam_risk_core import compute_risk

signals = {
    "s1": 0.05,
    "s2": 0.02,
    "s3": 0.10,
    "s4": 0.05,
    "s5": 0.03,
    "s6": 0.04,
    "s7": 0.05
}

risk = compute_risk(signals)

print("Risk score:", risk)

if risk >= 0.36:
    print("Zone: C/D → BLOCK")
else:
    print("Zone: A/B → ALLOW")