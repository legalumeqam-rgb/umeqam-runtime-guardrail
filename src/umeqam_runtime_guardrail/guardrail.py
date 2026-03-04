from __future__ import annotations


def _import_guardrail_class():
    """
    Shim-loader: tries known project locations for UMEQAMGuardrail.
    This makes the import stable even if internal module layout changes.
    """
    # вариант 1: src/umeqam_risk_core.py
    try:
        from umeqam_risk_core import UMEQAMGuardrail  # type: ignore
        return UMEQAMGuardrail
    except Exception:
        pass

    # вариант 2: если класс лежит внутри пакета src/umeqam/...
    try:
        from umeqam.umeqam_risk_core import UMEQAMGuardrail  # type: ignore
        return UMEQAMGuardrail
    except Exception:
        pass

    # если не нашли — даём точную ошибку, без воды
    raise ImportError(
        "UMEQAMGuardrail not found. Expected it in 'src/umeqam_risk_core.py' "
        "or 'src/umeqam/umeqam_risk_core.py'."
    )


UMEQAMGuardrail = _import_guardrail_class()
