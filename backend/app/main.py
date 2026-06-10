from fastapi import FastAPI

from app.api.imports import router as imports_router
from app.api.normalization import router as normalization_router

app = FastAPI(
    title="WMS-WME Reconciliation API",
    description="Read-only API for reconciling WMS/xTrack and WME/WinMentor events through ERP imports.",
    version="0.1.0",
)

app.include_router(imports_router)
app.include_router(normalization_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "mode": "read-only"}
