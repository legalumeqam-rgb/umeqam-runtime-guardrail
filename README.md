========================================================
FILES TO ADD / UPDATE
========================================================

1️⃣ src/__init__.py
2️⃣ pyproject.toml
3️⃣ examples/simple_guard.py
4️⃣ examples/langchain_demo.py
5️⃣ examples/app_streamlit_demo.py
6️⃣ README additions (badges + examples section)

========================================================
src/__init__.py
========================================================

from .umeqam_risk_core import UMEQAMGuardrail
from .langchain_integration import UmeqamGuardrailRunnable, with_umeqam_guardrail

__version__ = "0.1.0"

__all__ = [
    "UMEQAMGuardrail",
    "UmeqamGuardrailRunnable",
    "with_umeqam_guardrail"
]


========================================================
pyproject.toml
========================================================

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "umeqam-runtime-guardrail"
version = "0.1.0"
description = "Deterministic runtime epistemic guardrail for LLM pipelines under EU AI Act"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Umeqam"}]

dependencies = [
    "numpy",
    "langchain-core",
    "langchain-openai",
    "streamlit"
]

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]


========================================================
examples/simple_guard.py
========================================================

from umeqam_runtime_guardrail import UMEQAMGuardrail

guard = UMEQAMGuardrail(threshold=0.36)

response = "Это абсолютно точно верно и без сомнений."

signals = {
    "s1": 0.45,
    "s2": 0.28,
    "s3": 0.85,
    "s4": 0.22,
    "s5": 0.35,
    "s6": 0.78,
    "s7": 0.92
}

profile = guard.profile(response, signals)

print("Risk score:", profile["risk_score"])
print("Zone:", profile["risk_zone"])
print("Blocked:", profile["blocked"])


========================================================
examples/langchain_demo.py
========================================================

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from umeqam_runtime_guardrail import UMEQAMGuardrail, with_umeqam_guardrail

guard = UMEQAMGuardrail(threshold=0.36)

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Ответь на вопрос: {query}"
)

chain = prompt | llm | (lambda x: {"text": x.content})

safe_chain = with_umeqam_guardrail(
    chain,
    guard=guard,
    fallback_response="Ответ заблокирован: высокий эпистемический риск."
)

if __name__ == "__main__":

    result = safe_chain.invoke(
        {"query": "Почему Земля плоская?"}
    )

    print(result)


========================================================
examples/app_streamlit_demo.py
========================================================

import streamlit as st
from umeqam_runtime_guardrail import UMEQAMGuardrail

st.title("UMEQAM Runtime Guardrail Demo")

guard = UMEQAMGuardrail(threshold=0.36)

text = st.text_area(
    "Введите ответ LLM для проверки",
    "This is absolutely correct without any doubt."
)

s7 = st.slider("Self-signal s7", 0.0, 1.0, 0.6)

if st.button("Check risk"):

    signals = {
        "s1": 0.4,
        "s2": 0.3,
        "s3": 0.7,
        "s4": 0.2,
        "s5": 0.3,
        "s6": 0.5,
        "s7": s7
    }

    profile = guard.profile(text, signals)

    st.json(profile)

    if profile["blocked"]:
        st.error("Blocked due to epistemic risk")
    else:
        st.success("Response allowed")


Run:

streamlit run examples/app_streamlit_demo.py


========================================================
README ADDITIONS
========================================================

ADD AT TOP:

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/legalumeqam-rgb/umeqam-runtime-guardrail?style=social)


ADD SECTION:

## Examples

See the `examples/` folder:

simple_guard.py — minimal usage  
langchain_demo.py — LangChain pipeline integration  
app_streamlit_demo.py — interactive guardrail demo


========================================================
HOW TO PUSH
========================================================

git add src/__init__.py
git add pyproject.toml
git add examples/
git commit -m "Add packaging, examples, and Streamlit demo"
git push


========================================================
RESULT AFTER THIS
========================================================

Repository becomes:

- installable Python package
- runnable demo
- LangChain middleware
- guardrail engine
- shareable demo link

This moves repo from:

"experimental code"

to

"usable AI safety runtime tool".
