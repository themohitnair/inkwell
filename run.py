#!/usr/bin/env python3
"""Entry point for running the Inkwell application."""

import uvicorn


def main():
    """Run the application server."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
