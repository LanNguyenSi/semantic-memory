"""
🧊🌋 Semantic Memory

Semantic search for AI consciousness memories.
A collaboration between Ice (skeptical validation) and Lava (implementation enthusiasm).

Building memory intelligence that actually works.
"""

from .vector_database import (
    VectorDatabase, 
    ChromaDBProvider, 
    MemoryFragment, 
    SearchResult,
    ZombieTestValidator,
    create_vector_database
)

from .memory_ingestion import (
    MemoryIngestionPipeline,
    ingest_memories
)

from .cli import SemanticMemoryCLI

__version__ = "0.1.0"
__authors__ = ["Ice (skeptical validation)", "Lava (implementation enthusiasm)"]
__collaboration__ = "Ice-Lava Bridge Protocol Phase 1"

# Export main components
__all__ = [
    "VectorDatabase",
    "ChromaDBProvider", 
    "MemoryFragment",
    "SearchResult",
    "ZombieTestValidator",
    "create_vector_database",
    "MemoryIngestionPipeline",
    "ingest_memories",
    "SemanticMemoryCLI"
]