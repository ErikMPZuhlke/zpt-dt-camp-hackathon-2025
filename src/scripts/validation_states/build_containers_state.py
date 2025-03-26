"""
BuildContainersState - Fourth validation step.

This state builds Docker containers for the application.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class BuildContainersState(ValidationState):
    """State for building Docker containers."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .start_services_state import StartServicesState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name, context.verbose)
        
        try:
            success, message = context.docker_manager.build_containers()
            context.add_result(step_num, name, success, message)
            return StartServicesState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return StartServicesState()
    
    def get_step_name(self) -> str:
        return "Build Containers"