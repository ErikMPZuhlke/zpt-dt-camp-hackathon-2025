"""
TestBackendState - Seventh validation step.

This state tests backend API functionality to ensure it's working correctly.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class TestBackendState(ValidationState):
    """State for testing backend API functionality."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .test_frontend_state import TestFrontendState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name)
        
        try:
            success, message = context.service_validator.test_backend_api()
            context.add_result(step_num, name, success, message)
            return TestFrontendState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return TestFrontendState()
    
    def get_step_name(self) -> str:
        return "Test Backend API"