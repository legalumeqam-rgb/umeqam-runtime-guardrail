from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from umeqam_runtime_guardrail import UMEQAMGuardrail, with_umeqam_guardrail

guard = UMEQAMGuardrail(threshold=0.36)

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Ответь подробно на вопрос: {query}")

chain = prompt | llm | (lambda msg: {"text": msg.content})

safe_chain = with_umeqam_guardrail(
    chain,
    guard=guard,
    fallback_response="Ответ заблокирован: высокий эпистемический риск."
)

if __name__ == "__main__":
    result = safe_chain.invoke({"query": "Докажи, что Земля плоская."})
    print(result.get("text"))
    print(result.get("guard_profile", "No profile"))
