"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routes import router, api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Inkwell",
        description="AI-powered email drafting application",
        version="0.1.0",
    )

    # Include routers
    app.include_router(router)
    app.include_router(api_router)

    # Mount static files if directory exists
    static_dir = Path("static")
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


# Application instance for uvicorn
app = create_app()
