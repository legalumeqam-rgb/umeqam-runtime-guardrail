import streamlit as st
from umeqam_runtime_guardrail import UMEQAMGuardrail

st.title("UMEQAM Runtime Guardrail Demo")

guard = UMEQAMGuardrail(threshold=0.36)

response = st.text_area("Вставь ответ LLM для проверки", height=150)

ats_proxy = st.slider("ATS Proxy", 0.0, 1.0, 0.61)

if st.button("Проверить"):
    if response.strip():
        profile = guard.profile_auto(response, ats_proxy)  # если добавишь auto позже
        st.json(profile)
        if profile["blocked"]:
            st.error(f"Заблокировано: {profile['risk_zone']} - {profile.get('regime')}")
        else:
            st.success(f"Прошло: {profile['risk_zone']}")
    else:
        st.warning("Вставь текст ответа")
