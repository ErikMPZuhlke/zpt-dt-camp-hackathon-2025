"""
Vector database operations and management - simplified approach like original commit.
"""
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain.docstore.document import Document
from typing import List, Dict, Any
import os

from core.config import Config
from .embeddings import EmbeddingManager
from .csharp_processor import CSharpProcessor

class VectorDatabase:
    """Manages vector database operations - simplified like original ingest.py."""
    
    def __init__(self, persist_directory: str = None):
        """Initialize vector database."""
        self.persist_directory = persist_directory or Config.get_vector_db_path()
        self.embedding_manager = EmbeddingManager()
        # Simple text splitter like original commit
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE, 
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self._vector_db = None
    
    @property
    def vector_db(self):
        """Lazy load vector database."""
        if self._vector_db is None:
            Config.ensure_directories()
            self._vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_manager.embedding_model
            )
        return self._vector_db
    
    def ingest_codebase(self, codebase_path: str = None) -> Dict[str, Any]:
        """Ingest the entire codebase - simplified but enhanced with CSharpProcessor."""
        codebase_path = codebase_path or Config.get_codebase_path()
        
        print(f"Loading C# files from {codebase_path}...")
        
        # Simple directory loader like original
        loader = DirectoryLoader(codebase_path, glob="**/*.cs", show_progress=True)
        documents = loader.load()
        
        if not documents:
            print(f"No C# files found in {codebase_path}")
            # Create empty database
            vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_manager.embedding_model
            )
            return {"total_files": 0, "total_chunks": 0, "patterns_found": {}}
        
        print(f"Found {len(documents)} C# files")
        
        # Process and enhance documents with CSharpProcessor
        enhanced_documents = []
        for doc in documents:
            # Filter files using CSharpProcessor
            if not CSharpProcessor.should_include_file(doc.metadata["source"]):
                continue
            
            # Extract metadata using CSharpProcessor
            code_metadata = CSharpProcessor.extract_metadata(
                doc.page_content, 
                doc.metadata["source"]
            )
            
            # Create enhanced content for better semantic search
            enhanced_content = CSharpProcessor.create_enhanced_content(
                doc.page_content, 
                code_metadata
            )
            
            # Update document with enhanced content and metadata
            doc.page_content = enhanced_content
            doc.metadata.update({
                "namespace": code_metadata.namespace,
                "file_name": code_metadata.file_name,
                "category": getattr(code_metadata, 'category', 'unknown')
            })
            
            enhanced_documents.append(doc)
        
        print(f"Processed {len(enhanced_documents)} files with CSharpProcessor")
        
        # Simple text splitting by function/class like original
        docs = self.text_splitter.split_documents(enhanced_documents)
        print(f"Created {len(docs)} chunks")
        
        # Simple ChromaDB store like original commit
        vector_db = Chroma.from_documents(
            docs, 
            self.embedding_manager.embedding_model, 
            persist_directory=self.persist_directory
        )
        print(f"Ingested {len(docs)} chunks into ChromaDB.")
        
        return {
            "total_files": len(enhanced_documents),
            "total_chunks": len(docs),
            "patterns_found": {}
        }
    
    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """Search for similar documents."""
        k = k or Config.SEARCH_K
        return self.vector_db.similarity_search(query, k=k)
    
    def is_empty(self) -> bool:
        """Check if the vector database is empty."""
        try:
            # Try a simple search to see if there are any documents
            results = self.vector_db.similarity_search("test", k=1)
            return len(results) == 0
        except:
            return True