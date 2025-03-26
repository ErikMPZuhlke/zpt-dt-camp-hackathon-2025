"""
ValidationContext class for maintaining state during validation process.

This module contains the context class that maintains shared state and 
provides access to validation components during the State pattern execution.
"""

from dataclasses import dataclass
from typing import List, Tuple
from scripts.deployment import (
    SystemChecker,
    DockerManager,
    ServiceValidator,
    GitManager
)


@dataclass
class ValidationContext:
    """Context class that maintains state and provides access to validation components."""
    system_checker: SystemChecker
    docker_manager: DockerManager
    service_validator: ServiceValidator
    git_manager: GitManager
    steps_passed: int = 0
    total_steps: int = 9
    current_step: int = 1
    validation_results: List[Tuple[int, str, bool, str]] = None
    verbose: bool = False
    
    def __post_init__(self):
        if self.validation_results is None:
            self.validation_results = []
    
    def add_result(self, step_num: int, name: str, success: bool, message: str):
        """Add a validation result and update counters."""
        self.validation_results.append((step_num, name, success, message))
        if success:
            self.steps_passed += 1
    
    def get_current_step_and_increment(self, step_name: str) -> Tuple[int, str]:
        """Get current step number and name, then increment for next step."""
        current = self.current_step
        self.current_step += 1
        return (current, step_name)
    
    def get_critical_steps_passed(self) -> int:
        """Get count of critical steps that passed."""
        critical_steps = [6, 7, 8, 9]
        return sum(1 for step_num, _, success, _ in self.validation_results 
                  if step_num in critical_steps and success)
    
    def get_docker_steps_failed(self) -> int:
        """Get count of Docker infrastructure steps that failed."""
        docker_steps = [4, 5]
        return sum(1 for step_num, _, success, _ in self.validation_results 
                  if step_num in docker_steps and not success)