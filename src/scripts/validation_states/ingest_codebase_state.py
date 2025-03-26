"""
IngestCodebaseState - Ninth validation step.

This state ingests the C# codebase into the vector database.
"""

from typing import Tuple
from .base import ValidationState  
from .context import ValidationContext
from scripts.deployment.utils import StepPrinter
class IngestCodebaseState(ValidationState):
    """State for ingesting codebase into vector database."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        from .validation_complete_state import ValidationCompleteState
        
        step_num, name = context.get_current_step_and_increment(self.get_step_name())
        StepPrinter.print_step(step_num, name)
        try:
            success, message = context.service_validator.ingest_codebase()
            context.add_result(step_num, name, success, message)
            return ValidationCompleteState()
        except Exception as e:
            context.add_result(step_num, name, False, f"Error: {str(e)}")
            return ValidationCompleteState()
    
    def get_step_name(self) -> str:
        return "Ingest Codebase"