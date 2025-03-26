#!/usr/bin/env python3
"""
🚀 Docker Deployment Validation Script
Ensures Docker-based RAG Chatbot deployment is working correctly!

This script validates that the RAG Chatbot Docker deployment is functioning
properly by running a 9-step validation process:

1. Check system requirements (Python, Docker, Docker Compose)
2. Verify directory structure (updated for src/ organization)
3. Clean up previous deployments
4. Build Docker containers (production configuration)
5. Start Docker services (models auto-downloaded by Docker)
6. Wait for services to be ready
7. Test backend API functionality 
8. Test frontend accessibility
9. Ingest C# codebase into vector database

The modular design allows for easy testing and maintenance of individual components.
Models (llama3.2:3b) are automatically downloaded during Docker startup, and 
the C# codebase is automatically ingested into the vector database as the final step.
This script uses the standard docker-compose.yml for production deployment.

For debugging with VS Code, use docker-compose.debug.yml separately.

Usage:
    python setup_environment.py [--verbose]
    
Options:
    --verbose    Show detailed command output during Docker operations
"""

import sys
import argparse
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent  # Go up to project root from src/scripts/
sys.path.insert(0, str(project_root / "src"))

from scripts.deployment import (
    SystemChecker,
    DockerManager,
    ServiceValidator,
    GitManager
)
from scripts.validation_states import (
    ValidationContext,
    ValidationStateMachine
)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Docker Deployment Validation for RAG Chatbot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python setup_environment.py           # Run with minimal output
    python setup_environment.py --verbose # Run with detailed command output
        """
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Show detailed command output during Docker operations'
    )
    
    return parser.parse_args()


def main():
    """Main validation process - now using State pattern."""
    args = parse_arguments()
    
    print("🚀 RAG Chatbot Docker Deployment Validation")
    print("=" * 60)
    
    if args.verbose:
        print("📝 Verbose mode enabled - showing detailed command output")
        print("-" * 60)
    
    # Create validation context with all components
    context = ValidationContext(
        system_checker=SystemChecker(),
        docker_manager=DockerManager(verbose=args.verbose),
        service_validator=ServiceValidator(),
        git_manager=GitManager(),
        verbose=args.verbose
    )
    
    # Create and run the state machine
    state_machine = ValidationStateMachine(context)
    return state_machine.run_validation()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)