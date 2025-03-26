"""
Core configuration management for the RAG Chatbot project.
"""
import os
from pathlib import Path
from typing import Optional

class Config:
    """Application configuration."""
    
    # Paths - configurable via environment variables
    PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", "/app"))
    DATA_DIR = PROJECT_ROOT / "data"
    CODEBASE_DIR = DATA_DIR / os.getenv("CODEBASE_SUBDIR", "codebase/functional-csharp-code")
    VECTOR_DB_DIR = DATA_DIR / os.getenv("VECTOR_DB_SUBDIR", "vector_db")
    
    # AI Models
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
    
    # UI Configuration
    UI_HOST = os.getenv("UI_HOST", "0.0.0.0")
    UI_PORT = int(os.getenv("UI_PORT", "8501"))
    
    # Vector Database Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    SEARCH_K = int(os.getenv("SEARCH_K", "5"))
    
    @classmethod
    def get_codebase_path(cls) -> str:
        """Get the path to the LaYumba codebase."""
        return str(cls.CODEBASE_DIR)
    
    @classmethod
    def get_vector_db_path(cls) -> str:
        """Get the path to the vector database."""
        return str(cls.VECTOR_DB_DIR)
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.VECTOR_DB_DIR.mkdir(exist_ok=True)