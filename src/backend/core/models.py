"""
Data models and types for the RAG Chatbot project.
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

class PersonaMode(str, Enum):
    """AI persona modes for different analysis perspectives."""
    DOMAIN_EXPERT = "domain_expert"
    SOFTWARE_ARCHITECT = "software_architect"

@dataclass
class CodeMetadata:
    """Metadata extracted from C# code files."""
    file_path: str
    file_name: str
    language: str = "csharp"
    namespace: Optional[str] = None
    classes: List[str] = None
    interfaces: List[str] = None
    functional_patterns: List[str] = None
    category: Optional[str] = None
    
    def __post_init__(self):
        if self.classes is None:
            self.classes = []
        if self.interfaces is None:
            self.interfaces = []
        if self.functional_patterns is None:
            self.functional_patterns = []

@dataclass
class QueryRequest:
    """Request for RAG query."""
    question: str
    persona: PersonaMode
    context_k: int = 5

@dataclass
class QueryResponse:
    """Response from RAG query."""
    answer: str
    sources: List[str]
    persona: PersonaMode
    query_time: float