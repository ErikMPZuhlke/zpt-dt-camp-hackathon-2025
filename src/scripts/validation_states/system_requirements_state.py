"""
SystemRequirementsState - First validation step.

This state checks system requirements including Python, Docker, and Docker Compose.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class SystemRequirementsState(ValidationState):
    """State for checking system requirements."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .directory_structure_state import DirectoryStructureState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name)
        
        try:
            success, message = context.system_checker.check_requirements()
            context.add_result(step_num, name, success, message)
            return DirectoryStructureState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return DirectoryStructureState()
    
    def get_step_name(self) -> str:
        return "System Requirements"