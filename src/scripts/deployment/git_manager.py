"""
Git repository management for deployment validation.
"""
import os
from typing import Tuple
from .config import DeploymentConfig
from .utils import CommandRunner


class GitManager:
    """Handles Git operations for deployment validation."""
    
    def __init__(self):
        self.config = DeploymentConfig()
        self.runner = CommandRunner()
    
    def ensure_layumba_functional_repo(self) -> Tuple[bool, str]:
        """Ensure LaYumba Functional repository is available."""
        if self.config.LAYUMBA_DIR.exists():
            # Repository already exists, check if it's valid
            if (self.config.LAYUMBA_DIR / ".git").exists():
                print(f"✅ LaYumba Functional repository found at {self.config.LAYUMBA_DIR}")
                return True, "Repository already exists"
            else:
                print(f"⚠️  Directory exists but is not a git repository: {self.config.LAYUMBA_DIR}")
                # Try to remove and re-clone
                try:
                    import shutil
                    shutil.rmtree(self.config.LAYUMBA_DIR)
                except Exception as e:
                    return False, f"Failed to remove invalid directory: {str(e)}"
        
        # Clone the repository
        try:
            print(f"📥 Cloning LaYumba Functional repository...")
            os.chdir(self.config.DATA_DIR / "codebase")
            
            self.runner.run(f"git clone {self.config.LAYUMBA_REPO_URL}")
            
            if self.config.LAYUMBA_DIR.exists():
                print(f"✅ Successfully cloned to {self.config.LAYUMBA_DIR}")
                return True, "Repository cloned successfully"
            else:
                return False, "Repository was not created after cloning"
        
        except Exception as e:
            return False, f"Failed to clone repository: {str(e)}"
        finally:
            # Return to original directory
            os.chdir(self.config.PROJECT_ROOT)
    
    def get_repo_info(self) -> dict:
        """Get repository information for debugging."""
        info = {
            'exists': self.config.LAYUMBA_DIR.exists(),
            'is_git_repo': (self.config.LAYUMBA_DIR / ".git").exists() if self.config.LAYUMBA_DIR.exists() else False,
            'path': str(self.config.LAYUMBA_DIR)
        }
        
        if info['is_git_repo']:
            try:
                os.chdir(self.config.LAYUMBA_DIR)
                result = self.runner.run("git log --oneline -1", check=False)
                info['latest_commit'] = result.stdout.strip() if result.returncode == 0 else "Unknown"
                
                result = self.runner.run("git remote get-url origin", check=False)
                info['remote_url'] = result.stdout.strip() if result.returncode == 0 else "Unknown"
            except Exception:
                info['latest_commit'] = "Error"
                info['remote_url'] = "Error"
            finally:
                os.chdir(self.config.PROJECT_ROOT)
        
        return info