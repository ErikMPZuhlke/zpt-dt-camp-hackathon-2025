"""
StartServicesState - Fifth validation step.

This state starts Docker services for the application.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class StartServicesState(ValidationState):
    """State for starting Docker services."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .wait_for_services_state import WaitForServicesState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name, context.verbose)
        
        try:
            success, message = context.docker_manager.start_services()
            context.add_result(step_num, name, success, message)
            return WaitForServicesState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return WaitForServicesState()
    
    def get_step_name(self) -> str:
        return "Start Services"