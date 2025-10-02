"""
InstallDependenciesState - Install Python dependencies.

This state checks and installs required Python dependencies for the deployment script.
"""

import subprocess
import sys
from typing import Tuple, List
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class InstallDependenciesState(ValidationState):
    """State for checking and installing Python dependencies."""
    
    # Required dependencies for the deployment script
    REQUIRED_DEPENDENCIES = [
        "requests>=2.28.0",
        "docker>=6.0.0", 
        "GitPython>=3.1.0",
        "psutil>=5.9.0",
        "pyyaml>=6.0",
        "urllib3>=1.26.0"
    ]
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .directory_structure_state import DirectoryStructureState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name)
        
        try:
            # Check which dependencies are missing
            missing_deps = self._check_dependencies()
            
            if not missing_deps:
                context.add_result(step_num, name, True, "All Python dependencies are already installed")
                return DirectoryStructureState()
            
            # Install missing dependencies
            success, message = self._install_dependencies(missing_deps, context.verbose)
            context.add_result(step_num, name, success, message)
            return DirectoryStructureState()
            
        except Exception as e:
            context.add_result(step_num, name, False, f"Error checking/installing dependencies: {str(e)}")
            return DirectoryStructureState()
    
    def _check_dependencies(self) -> List[str]:
        """Check which dependencies are missing."""
        missing = []
        
        for dependency in self.REQUIRED_DEPENDENCIES:
            package_name = dependency.split(">=")[0].split("==")[0]
            
            # Special handling for GitPython (imports as 'git')
            if package_name == "GitPython":
                import_name = "git"
            elif package_name == "pyyaml":
                import_name = "yaml"
            else:
                import_name = package_name
            
            try:
                __import__(import_name)
            except ImportError:
                missing.append(dependency)
        
        return missing
    
    def _install_dependencies(self, dependencies: List[str], verbose: bool) -> Tuple[bool, str]:
        """Install missing dependencies using pip."""
        try:
            if verbose:
                print(f"   Installing dependencies: {', '.join(dependencies)}")
            
            # Build pip install command
            cmd = [sys.executable, "-m", "pip", "install"] + dependencies
            
            # Run pip install
            if verbose:
                result = subprocess.run(cmd, capture_output=False, text=True, check=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return True, f"Successfully installed {len(dependencies)} dependencies"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to install dependencies: {e}"
            if hasattr(e, 'stderr') and e.stderr:
                error_msg += f"\nError details: {e.stderr}"
            return False, error_msg
        except Exception as e:
            return False, f"Unexpected error during installation: {str(e)}"
    
    def get_step_name(self) -> str:
        return "Install Python Dependencies"