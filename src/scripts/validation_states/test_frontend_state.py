"""
TestFrontendState - Eighth validation step.

This state tests frontend accessibility to ensure it's working correctly.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter


class TestFrontendState(ValidationState):
    """State for testing frontend accessibility."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .ingest_codebase_state import IngestCodebaseState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name)
        try:
            success, message = context.service_validator.test_frontend_accessibility()
            context.add_result(step_num, name, success, message)
            return IngestCodebaseState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return IngestCodebaseState()
    
    def get_step_name(self) -> str:
        return "Test Frontend Access"