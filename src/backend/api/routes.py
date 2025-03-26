"""
FastAPI routes for the RAG Chatbot API.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List

from core.models import PersonaMode, QueryRequest
from chat.rag_engine import RAGEngine
from chat.personas import ExampleQueries
from ingestion.database import VectorDatabase

# Create router
api_router = APIRouter()

# Initialize RAG engine
rag_engine = RAGEngine()

@api_router.get("/")
async def root():
    """API information and health check."""
    status = rag_engine.get_health_status()
    
    return {
        "message": "🎓 LaYumba Functional C# Code Expert API",
        "description": "AI-powered chatbot for analyzing functional programming patterns in C# code",
        "version": "2.0.0",
        "status": status,
        "endpoints": {
            "query": "/query/",
            "examples": "/examples/",
            "health": "/health/",
            "ingest": "/ingest/"
        }
    }

@api_router.get("/health/")
async def health_check():
    """Detailed health check."""
    status = rag_engine.get_health_status()
    
    if not status["ready"]:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    return status

@api_router.get("/query/")
async def query_chatbot(
    user_question: str = Query(..., description="Your question about the functional programming codebase"),
    persona: PersonaMode = Query(PersonaMode.DOMAIN_EXPERT, description="AI persona mode for analysis")
):
    """Query the chatbot with different persona modes."""
    try:
        # Create request
        request = QueryRequest(
            question=user_question,
            persona=persona
        )
        
        # Process query
        response = rag_engine.process_query(request)
        
        return {
            "question": user_question,
            "persona": persona.value,
            "answer": response.answer,
            "sources": response.sources,
            "query_time": round(response.query_time, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@api_router.get("/examples/")
async def get_example_queries() -> Dict[str, List[str]]:
    """Get example queries for each persona mode."""
    return {
        "domain_expert": ExampleQueries.get_examples(PersonaMode.DOMAIN_EXPERT),
        "software_architect": ExampleQueries.get_examples(PersonaMode.SOFTWARE_ARCHITECT)
    }

@api_router.post("/ingest/")
async def ingest_codebase(
    force_reindex: bool = Query(False, description="Force reindexing even if vector database already contains data")
):
    """
    Ingest C# codebase into the vector database.
    
    This endpoint processes C# code files from the configured codebase directory,
    extracts metadata, and stores them in the vector database for retrieval.
    The codebase path is configured in Config.CODEBASE_DIR.
    """
    try:
        # Initialize vector database
        vector_db = VectorDatabase()
        
        # Check if reindexing is needed
        if not force_reindex and not vector_db.is_empty():
            return {
                "status": "skipped",
                "message": "Vector database already contains data. Use force_reindex=true to rebuild.",
                "suggestion": "Use force_reindex=true if you want to rebuild the index"
            }
        
        # Perform ingestion using the configured codebase path
        print(f"🔄 Starting C# codebase ingestion...")
        print(f"   📁 Path: configured codebase directory")
        print(f"   🔄 Force reindex: {force_reindex}")
        
        ingestion_results = vector_db.ingest_codebase()
        
        return {
            "status": "success",
            "message": "C# codebase successfully ingested into vector database",
            "results": {
                "total_files_processed": ingestion_results["total_files"],
                "total_chunks_created": ingestion_results["total_chunks"],
                "patterns_detected": ingestion_results["patterns_found"],
                "codebase_path": "configured codebase directory",
                "force_reindex": force_reindex
            },
            "next_steps": [
                "You can now query the chatbot using /query/ endpoint",
                "Check /examples/ for sample questions",
                "Use /health/ to verify all services are ready"
            ]
        }
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Codebase path not found: {str(e)}"
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=403, 
            detail=f"Permission denied accessing codebase: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Ingestion failed: {str(e)}"
        )