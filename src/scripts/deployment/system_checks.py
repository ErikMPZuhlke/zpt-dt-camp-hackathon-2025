"""
System requirements checking for deployment validation.
"""
import subprocess
import shutil
from typing import Tuple
from .config import DeploymentConfig
from .utils import CommandRunner


class SystemChecker:
    """Handles system requirements validation."""
    
    def __init__(self):
        self.config = DeploymentConfig()
        self.runner = CommandRunner()
    
    def check_requirements(self) -> Tuple[bool, str]:
        """Check system requirements."""        
        # Check Python version
        try:
            result = self.runner.run("python --version")
            python_version = result.stdout.strip()
            print(f"✅ Python found: {python_version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "Python is not installed or not in PATH"
        
        # Check Docker
        if not shutil.which("docker"):
            return False, "Docker is not installed or not in PATH"
        
        try:
            result = self.runner.run("docker --version")
            docker_version = result.stdout.strip()
            print(f"✅ Docker found: {docker_version}")
        except subprocess.CalledProcessError:
            return False, "Docker is not working properly"
        
        # Check Docker Compose
        try:
            result = self.runner.run("docker compose version")
            compose_version = result.stdout.strip()
            print(f"✅ Docker Compose found: {compose_version}")
        except subprocess.CalledProcessError:
            return False, "Docker Compose is not available"
        
        # Check if Docker daemon is running
        try:
            self.runner.run("docker ps")
            print("✅ Docker daemon is running")
        except subprocess.CalledProcessError:
            return False, "Docker daemon is not running. Please start Docker."
        
        return True, "All system requirements met"
    
    def check_directory_structure(self) -> Tuple[bool, str]:
        """Check directory structure and ensure LaYumba repository exists."""        
        # Basic required paths (excluding LAYUMBA_DIR which we'll handle separately)
        required_paths = [
            self.config.PROJECT_ROOT,
            self.config.SRC_DIR,
            self.config.DATA_DIR,
            self.config.PROJECT_ROOT / "docker-compose.yml",
            self.config.BACKEND_DIR,
            self.config.FRONTEND_DIR,
            self.config.SCRIPTS_DIR
        ]
        
        missing_paths = []
        for path in required_paths:
            if not path.exists():
                missing_paths.append(str(path))
            else:
                print(f"✅ Found: {path.relative_to(self.config.PROJECT_ROOT)}")
        
        if missing_paths:
            return False, f"Missing required paths: {', '.join(missing_paths)}"
        
        # Ensure codebase directory exists
        self.config.CODEBASE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Ensured: {self.config.CODEBASE_DIR.relative_to(self.config.PROJECT_ROOT)}")
        
        # Handle LaYumba repository separately using GitManager
        from .git_manager import GitManager
        git_manager = GitManager()
        repo_success, repo_message = git_manager.ensure_layumba_functional_repo()
        
        if not repo_success:
            return False, f"LaYumba repository issue: {repo_message}"
        
        return True, "Directory structure is valid and LaYumba repository is available"