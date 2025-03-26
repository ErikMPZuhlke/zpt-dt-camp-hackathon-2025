"""
Frontend configuration management for the RAG Chatbot project.
"""
import os
from typing import Optional

class Config:
    """Frontend application configuration."""
    
    # API Configuration
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "120"))  # 2 minutes for health checks
    
    # UI Configuration
    UI_HOST = os.getenv("UI_HOST", "0.0.0.0")
    UI_PORT = int(os.getenv("UI_PORT", "8501"))
    
    # Streamlit Configuration
    STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "light")
    STREAMLIT_DEBUG = os.getenv("STREAMLIT_DEBUG", "false").lower() == "true"
    
    @classmethod
    def get_api_url(cls) -> str:
        """Get the API base URL."""
        return cls.API_URL
    
    @classmethod
    def get_health_url(cls) -> str:
        """Get the health check URL."""
        return f"{cls.API_URL}/health/"
    
    @classmethod
    def is_debug_mode(cls) -> bool:
        """Check if debug mode is enabled."""
        return cls.STREAMLIT_DEBUG or os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> dict:
        """Validate the configuration and return status."""
        status = {
            "api_url": cls.API_URL,
            "ui_host": cls.UI_HOST,
            "ui_port": cls.UI_PORT,
            "debug_mode": cls.is_debug_mode(),
            "valid": True,
            "errors": []
        }
        
        # Validate API URL format
        if not cls.API_URL.startswith(('http://', 'https://')):
            status["errors"].append("API_URL must start with http:// or https://")
            status["valid"] = False
        
        return status