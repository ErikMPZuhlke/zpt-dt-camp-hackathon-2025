"""
C# code processing and metadata extraction - simplified approach.
"""
import re
import os
from typing import Dict, List, Any
from pathlib import Path

from core.models import CodeMetadata

class CSharpProcessor:
    """Processes C# code files - simplified for dumber approach."""
    
    @staticmethod
    def extract_metadata(content: str, file_path: str) -> CodeMetadata:
        """Extract basic C# code metadata - simplified."""
        metadata = CodeMetadata(
            file_path=file_path,
            file_name=os.path.basename(file_path)
        )
        
        # Keep minimal metadata extraction for compatibility
        # But don't overcomplicate like the original simple approach
        namespace_match = re.search(r'namespace\s+([^\s{]+)', content)
        if namespace_match:
            metadata.namespace = namespace_match.group(1)
        
        return metadata
    
    @staticmethod
    def create_enhanced_content(content: str, metadata: CodeMetadata) -> str:
        """Create simple enhanced content - minimal approach."""
        # Just return original content for simplicity
        return content
    
    @staticmethod
    def should_include_file(file_path: str) -> bool:
        """Simple file inclusion check."""
        # Simple check - just ensure it's a C# file
        return file_path.endswith('.cs')