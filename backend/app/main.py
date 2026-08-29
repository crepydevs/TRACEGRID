from fastapi import FastAPI
from app.api import routes_actors, routes_search, routes_scan, routes_export
app = FastAPI(title="Dark Web Threat Actor Intelligence API")
app.include_router(routes_actors.router, prefix="/api/actors", tags=["actors"])
app.include_router(routes_search.router, prefix="/api/search", tags=["search"])
app.include_router(routes_scan.router, prefix="/api/scan", tags=["scan"])
app.include_router(routes_export.router, prefix="/api/export", tags=["export"])

@app.get("/health")
def health_check():
return {"status": "ok"}