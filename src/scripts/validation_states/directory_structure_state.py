"""
DirectoryStructureState - Second validation step.

This state checks that all required directories exist in the project structure.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class DirectoryStructureState(ValidationState):
    """State for checking directory structure."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .cleanup_state import CleanupState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name)
        
        try:
            success, message = context.system_checker.check_directory_structure()
            context.add_result(step_num, name, success, message)
            return CleanupState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return CleanupState()
    
    def get_step_name(self) -> str:
        return "Directory Structure"