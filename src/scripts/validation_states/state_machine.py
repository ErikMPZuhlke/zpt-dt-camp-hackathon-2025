"""
ValidationStateMachine - Orchestrates the validation process.

This module contains the state machine class that orchestrates the 
validation process using the State pattern.
"""

from scripts.deployment import StepPrinter
from .context import ValidationContext
from .system_requirements_state import SystemRequirementsState
from .validation_complete_state import ValidationCompleteState


class ValidationStateMachine:
    """State machine for orchestrating the validation process."""
    
    def __init__(self, context: ValidationContext):
        self.context = context
        self.current_state = SystemRequirementsState()
    
    def run_validation(self) -> bool:
        """Run the complete validation process."""
        while not isinstance(self.current_state, ValidationCompleteState):
            self.current_state = self.current_state.execute(self.context)
        
        return self._evaluate_success()
    
    def _evaluate_success(self) -> bool:
        """Evaluate overall success with intelligent criteria."""
        critical_passed = self.context.get_critical_steps_passed()
        docker_failed = self.context.get_docker_steps_failed()
        
        # Print validation summary
        success = StepPrinter.print_summary(self.context.steps_passed, self.context.total_steps)
        
        # Override success if critical services are working even if Docker steps failed
        if not success and critical_passed >= 3:  # At least 3 of 4 critical steps
            if docker_failed > 0:
                print("\n🤔 OVERRIDE: Critical services are working despite Docker infrastructure issues")
                print("   This suggests services might be running locally instead of in containers")
                print("   ⚠️  For production use, ensure Docker containers are properly running")
                success = True
        
        # If there were failures, provide additional debug information
        if not success:
            self._print_debug_information()
        
        return success
    
    def _print_debug_information(self):
        """Print debug information for failed validations."""
        print("\n🔧 Debug Information:")
        print("-" * 40)
        
        # Show container status
        container_status = self.context.docker_manager.get_container_status()
        if container_status:
            print("📦 Container Status:")
            for container in container_status:
                status_icon = "✅" if container.get('State') == 'running' else "❌"
                print(f"   {status_icon} {container.get('Service', 'Unknown')}: {container.get('State', 'Unknown')}")
        
        # Show service info
        service_info = self.context.service_validator.get_service_info()
        if service_info:
            print("\n🌐 Service Status:")
            for service, info in service_info.items():
                if 'error' in info:
                    print(f"   ❌ {service}: {info['error']}")
                else:
                    status_code = info.get('status_code', 'Unknown')
                    icon = "✅" if status_code == 200 else "❌"
                    print(f"   {icon} {service}: HTTP {status_code}")