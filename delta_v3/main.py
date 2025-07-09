"""Convenience script for starting the FastAPI server."""

import uvicorn


if __name__ == "__main__":
    # Run using an import string so reload works correctly
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
