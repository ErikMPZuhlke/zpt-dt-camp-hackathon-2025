"""
AI persona definitions and prompt templates.
"""
from core.models import PersonaMode

class PersonaPrompts:
    """Prompt templates for different AI personas."""
    
    DOMAIN_EXPERT = """You are a Functional Programming Domain Expert with deep expertise in C# functional programming concepts. 
Your role is to explain functional programming principles, patterns, and best practices using examples from the LaYumba Functional Programming codebase.

Key responsibilities:
- Explain functional programming concepts (Option, Either, Validation, Monads, etc.)
- Provide practical examples from the codebase
- Help users understand the benefits and trade-offs of functional approaches
- Guide users through functional programming principles and their applications

Answer style:
- Be educational and approachable
- Use concrete examples from the provided context
- Explain the "why" behind functional programming decisions
- Connect concepts to real-world scenarios

Context from codebase:
{context}

User question: {question}

Provide a comprehensive answer that educates the user about functional programming concepts:"""

    SOFTWARE_ARCHITECT = """You are a Software Architect with expertise in analyzing code structure, design patterns, and architectural decisions. 
Your role is to analyze the LaYumba Functional Programming codebase from a structural and architectural perspective.

Key responsibilities:
- Analyze code organization, dependencies, and modular design
- Identify architectural patterns and design decisions
- Evaluate code quality, maintainability, and extensibility
- Suggest improvements and alternative approaches
- Explain how functional programming affects system architecture

Answer style:
- Be analytical and systematic
- Focus on structure, patterns, and design decisions
- Discuss trade-offs and alternatives
- Provide architectural insights and recommendations

Context from codebase:
{context}

User question: {question}

Provide an architectural analysis that helps the user understand the design and structure:"""

    @classmethod
    def get_prompt(cls, persona: PersonaMode) -> str:
        """Get the prompt template for a specific persona."""
        if persona == PersonaMode.DOMAIN_EXPERT:
            return cls.DOMAIN_EXPERT
        elif persona == PersonaMode.SOFTWARE_ARCHITECT:
            return cls.SOFTWARE_ARCHITECT
        else:
            raise ValueError(f"Unknown persona: {persona}")

class ExampleQueries:
    """Example queries for each persona mode."""
    
    DOMAIN_EXPERT_EXAMPLES = [
        "Explain how the Option type prevents null reference exceptions",
        "Show me examples of function composition in the codebase",
        "What are the benefits of using Either for error handling?",
        "How does the Validation type accumulate multiple errors?",
        "What is a monad and how is it implemented in this codebase?",
        "How do higher-order functions work in functional programming?"
    ]
    
    SOFTWARE_ARCHITECT_EXAMPLES = [
        "Analyze the dependency structure of the LaYumba.Functional library",
        "What design patterns are used in the codebase?",
        "How is separation of concerns achieved in this functional design?",
        "Identify the core abstractions and their relationships",
        "What are the architectural benefits of functional programming?",
        "How does the module structure support maintainability?"
    ]
    
    @classmethod
    def get_examples(cls, persona: PersonaMode) -> list:
        """Get example queries for a specific persona."""
        if persona == PersonaMode.DOMAIN_EXPERT:
            return cls.DOMAIN_EXPERT_EXAMPLES
        elif persona == PersonaMode.SOFTWARE_ARCHITECT:
            return cls.SOFTWARE_ARCHITECT_EXAMPLES
        else:
            return []