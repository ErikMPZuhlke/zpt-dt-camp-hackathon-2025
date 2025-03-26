"""
Embedding and vector database operations.
"""
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import Config

class EmbeddingManager:
    """Manages embedding models and operations - simplified approach."""
    
    def __init__(self, model_name: str = None):
        """Initialize embedding manager."""
        self.model_name = model_name or Config.EMBEDDING_MODEL
        self._embedding_model = None
    
    @property
    def embedding_model(self):
        """Lazy load embedding model."""
        if self._embedding_model is None:
            # Simple direct instantiation like the original commit
            self._embedding_model = HuggingFaceEmbeddings(
                model_name=self.model_name
            )
        return self._embedding_model
    
    def embed_documents(self, texts: list) -> list:
        """Embed a list of documents."""
        return self.embedding_model.embed_documents(texts)
    
    def embed_query(self, text: str) -> list:
        """Embed a single query."""
        return self.embedding_model.embed_query(text)