"""
Base ValidationState abstract class.

This module defines the abstract base class for all validation states
in the State pattern implementation.
"""

from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .context import ValidationContext


class ValidationState(ABC):
    """Abstract base class for validation states."""
    
    @abstractmethod
    def execute(self, context: 'ValidationContext') -> 'ValidationState':
        """Execute this state and return the next state."""
        pass
    
    @abstractmethod
    def get_step_name(self) -> str:
        """Return the step name for this state."""
        pass