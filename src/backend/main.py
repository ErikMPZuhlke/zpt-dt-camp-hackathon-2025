"""
Backend application entry point.
"""
import uvicorn
from api.main import app
from core.config import Config

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=False  # Disabled in container
    )