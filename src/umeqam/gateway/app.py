from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from umeqam.gateway.routes.chat import router as chat_router
from umeqam.gateway.routes.analyze import router as analyze_router
from umeqam.gateway.routes.health import router as health_router

app = FastAPI(
    title="UMEQAM Gateway",
    description="Enterprise AI Governance Gateway with Epistemic Guardrails",
    version="1.0.0"
)

app.include_router(chat_router)
app.include_router(analyze_router)
app.include_router(health_router)


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "detail": str(exc)}
    )
