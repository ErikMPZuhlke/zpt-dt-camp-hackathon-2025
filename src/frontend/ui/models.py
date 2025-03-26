"""
Frontend models - simplified version of backend models.
"""
from enum import Enum

class PersonaMode(str, Enum):
    """AI persona modes for different analysis perspectives."""
    DOMAIN_EXPERT = "domain_expert"
    SOFTWARE_ARCHITECT = "software_architect"