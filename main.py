from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError
from pydantic import ValidationError
from pathlib import Path
from core.config import get_settings
from routers import auth as auth_router
from routers import measurements as measurements_router
from routers import admin as admin_router


from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi


# NEW imports for Swagger JWT support
from fastapi.openapi.models import APIKey
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Create HTTP Bearer scheme for Swagger
bearer_scheme = HTTPBearer()

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    origins = [o.strip() for o in settings.cors_origins.split(",")] if settings.cors_origins else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    app.include_router(auth_router.router)
    app.include_router(measurements_router.router)
    app.include_router(admin_router.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description="API documentation",
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        # Apply globally
        for path in openapi_schema["paths"].values():
            for op in path.values():
                op.setdefault("security", [{"BearerAuth": []}])
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    # Mount Vue frontend AFTER API routes
    frontend_dist = Path(__file__).parent / "frontend" / "dist"
    if frontend_dist.exists():
        app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

        # Catch-all: send index.html for Vue Router routes
        @app.get("/{full_path:path}")
        async def serve_vue_app(full_path: str):
            return FileResponse(frontend_dist / "index.html")

    return app


app = create_app()


