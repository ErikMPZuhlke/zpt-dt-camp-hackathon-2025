"""
WaitForServicesState - Sixth validation step.

This state waits for Docker services to be ready and available.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class WaitForServicesState(ValidationState):
    """State for waiting for services to be ready."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .test_backend_state import TestBackendState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name, context.verbose)
        
        try:
            success, message = context.docker_manager.wait_for_services()
            context.add_result(step_num, name, success, message)
            return TestBackendState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return TestBackendState()
    
    def get_step_name(self) -> str:
        return "Wait for Services"