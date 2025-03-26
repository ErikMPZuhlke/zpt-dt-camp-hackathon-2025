"""
CleanupState - Third validation step.

This state cleans up any previous Docker deployment.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class CleanupState(ValidationState):
    """State for cleaning up previous deployment."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .build_containers_state import BuildContainersState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name, context.verbose)
        
        try:
            success, message = context.docker_manager.cleanup_previous_deployment()
            context.add_result(step_num, name, success, message)
            return BuildContainersState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return BuildContainersState()
    
    def get_step_name(self) -> str:
        return "Cleanup Previous Deployment"