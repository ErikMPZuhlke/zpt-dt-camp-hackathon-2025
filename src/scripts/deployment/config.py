"""
Configuration and constants for deployment validation.
"""
from pathlib import Path

class DeploymentConfig:
    """Configuration for deployment validation."""
    
    # Project paths - updated for new src/ structure
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # Go up to project root from src/scripts/deployment/
    SRC_DIR = PROJECT_ROOT / "src"
    SCRIPTS_DIR = SRC_DIR / "scripts"
    BACKEND_DIR = SRC_DIR / "backend"
    FRONTEND_DIR = SRC_DIR / "frontend"
    DATA_DIR = PROJECT_ROOT / "data"
    CODEBASE_DIR = DATA_DIR / "codebase"
    LAYUMBA_DIR = CODEBASE_DIR / "functional-csharp-code"
    
    # Service URLs and ports
    OLLAMA_URL = "http://localhost:11434"
    OLLAMA_API_URL = f"{OLLAMA_URL}/api"
    BACKEND_URL = "http://localhost:8000"
    FRONTEND_URL = "http://localhost:8501"
    
    # Timeouts (seconds)
    SERVICE_TIMEOUT = 120
    OLLAMA_TIMEOUT = 60
    BACKEND_TIMEOUT = 90
    FRONTEND_TIMEOUT = 60
    MODEL_DOWNLOAD_TIMEOUT = 300
    
    # Model configuration - models now auto-downloaded by Docker
    MAIN_MODEL = "llama3.2:3b"
    
    # Repository configuration
    LAYUMBA_REPO_URL = "https://github.com/la-yumba/functional-csharp-code.git"
    
    # Validation thresholds
    MIN_STEPS_FOR_SUCCESS = 7  # Out of 8 total
    TOTAL_STEPS = 8