from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from src.umeqam.gateway.routes.health import router as health_router
from src.umeqam.gateway.routes.analyze import router as analyze_router
from src.umeqam.gateway.routes.chat import router as chat_router


app = FastAPI(
    title="UMEQAM Runtime Guardrail",
    version="1.0"
)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(chat_router)
