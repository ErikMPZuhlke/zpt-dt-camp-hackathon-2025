"""
RAG (Retrieval-Augmented Generation) engine for processing queries.
"""
import time
import ollama
from typing import List

from core.models import PersonaMode, QueryRequest, QueryResponse
from core.config import Config
from ingestion.database import VectorDatabase
from .personas import PersonaPrompts

class RAGEngine:
    """Main RAG processing engine."""
    
    def __init__(self):
        """Initialize RAG engine."""
        self.vector_db = VectorDatabase()
        self.llm_model = Config.LLM_MODEL
        # Configure Ollama client with Docker DNS URL
        self.ollama_client = ollama.Client(host=Config.OLLAMA_URL)
    
    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a query using RAG."""
        start_time = time.time()
        
        # 1. Retrieve relevant context
        context_docs = self.vector_db.similarity_search(
            request.question, 
            k=request.context_k
        )
        
        # 2. Prepare context
        context = self._prepare_context(context_docs)
        sources = [doc.metadata.get("source", "unknown") for doc in context_docs]
        
        # 3. Get persona prompt
        prompt_template = PersonaPrompts.get_prompt(request.persona)
        
        # 4. Format prompt
        formatted_prompt = prompt_template.format(
            context=context,
            question=request.question
        )
        
        # 5. Generate response
        response = self._generate_response(formatted_prompt)
        
        # 6. Create response object
        query_time = time.time() - start_time
        
        return QueryResponse(
            answer=response,
            sources=sources,
            persona=request.persona,
            query_time=query_time
        )
    
    def _prepare_context(self, documents: List) -> str:
        """Prepare context from retrieved documents."""
        if not documents:
            return "No relevant context found in the codebase."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            
            # Create context entry
            context_entry = f"**Context {i}:**\n"
            
            if metadata.get("file_name"):
                context_entry += f"File: {metadata['file_name']}\n"
            
            if metadata.get("namespace"):
                context_entry += f"Namespace: {metadata['namespace']}\n"
            
            if metadata.get("functional_patterns"):
                patterns = ", ".join(metadata['functional_patterns'])
                context_entry += f"Patterns: {patterns}\n"
            
            context_entry += f"Code:\n{doc.page_content}\n"
            context_parts.append(context_entry)
        
        return "\n---\n".join(context_parts)
    
    def _generate_response(self, prompt: str) -> str:
        """Generate response using Ollama."""
        try:
            response = self.ollama_client.chat(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_health_status(self) -> dict:
        """Get health status of the RAG engine."""
        status = {
            "vector_db": "unknown",
            "llm": "unknown",
            "ready": False
        }
        
        try:
            # Check vector database
            if not self.vector_db.is_empty():
                status["vector_db"] = "ready"
            else:
                status["vector_db"] = "empty"
        except Exception:
            status["vector_db"] = "error"
        
        try:
            # Check LLM availability without generating text
            models = self.ollama_client.list()
            model_names = [model.model for model in models.models]
            if self.llm_model in model_names:
                status["llm"] = "ready"
            else:
                status["llm"] = "model_not_found"
        except Exception as e:
            status["llm"] = f"error: {str(e)}"
        
        status["ready"] = (
            status["vector_db"] == "ready" and 
            status["llm"] == "ready"
        )
        
        return status