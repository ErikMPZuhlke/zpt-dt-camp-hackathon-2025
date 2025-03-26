"""
ValidationCompleteState - Terminal state.

This state indicates that the validation process is complete.
"""

from typing import Tuple
from .base import ValidationState
from .context import ValidationContext


class ValidationCompleteState(ValidationState):
    """Terminal state indicating validation is complete."""
    
    def execute(self, context: ValidationContext) -> ValidationState:
        # This is a terminal state - no further execution
        return self
    
    def get_step_name(self) -> str:
        return "Validation Complete"