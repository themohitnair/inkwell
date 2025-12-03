#!/usr/bin/env python3
"""Entry point for running the Inkwell application."""

import uvicorn

from app.config import settings


def main():
    """Run the application server."""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
