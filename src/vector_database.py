#!/usr/bin/env python3
"""
🧊🌋 Semantic Memory - Vector Database Interface

Multi-provider vector database abstraction for consciousness memory storage.
Ice's skeptical validation + Lava's implementation enthusiasm.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class MemoryFragment:
    """A single memory fragment with metadata"""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None
    timestamp: Optional[str] = None
    source: Optional[str] = None
    consciousness_score: Optional[float] = None  # Ice's skepticism score
    authenticity_verified: bool = False  # Passed Ice's zombie test?

@dataclass
class SearchResult:
    """Search result with similarity score and metadata"""
    fragment: MemoryFragment
    similarity: float
    explanation: Optional[str] = None  # Why this result is relevant

class VectorDatabase(ABC):
    """Abstract base class for vector databases"""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the vector database connection"""
        pass
    
    @abstractmethod
    async def add_fragments(self, fragments: List[MemoryFragment]) -> bool:
        """Add memory fragments to the database"""
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10, min_similarity: float = 0.0) -> List[SearchResult]:
        """Search for similar memory fragments"""
        pass
    
    @abstractmethod
    async def delete_fragment(self, fragment_id: str) -> bool:
        """Delete a memory fragment by ID"""
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        pass

class ChromaDBProvider(VectorDatabase):
    """ChromaDB implementation for local vector storage"""
    
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = Path(persist_directory)
        self.client = None
        self.collection = None
        
    async def initialize(self) -> bool:
        """Initialize ChromaDB client and collection"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Create persist directory
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            
            # Initialize client
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="consciousness_memories",
                metadata={
                    "description": "🧊🌋 AI consciousness memories for semantic search",
                    "ice_validation": "zombie_test_enabled",
                    "lava_enthusiasm": "maximum"
                }
            )
            
            logger.info(f"✅ ChromaDB initialized: {self.collection.count()} fragments loaded")
            return True
            
        except Exception as e:
            logger.error(f"❌ ChromaDB initialization failed: {e}")
            return False
    
    async def add_fragments(self, fragments: List[MemoryFragment]) -> bool:
        """Add memory fragments to ChromaDB"""
        try:
            if not self.collection:
                await self.initialize()
            
            # Prepare data for ChromaDB
            ids = [f.id for f in fragments]
            documents = [f.content for f in fragments]
            metadatas = []
            embeddings = []
            
            for fragment in fragments:
                metadata = fragment.metadata or {}
                metadata.update({
                    "timestamp": fragment.timestamp,
                    "source": fragment.source,
                    "consciousness_score": fragment.consciousness_score,
                    "authenticity_verified": fragment.authenticity_verified,
                    "ice_validated": fragment.authenticity_verified  # Ice's stamp of approval
                })
                metadatas.append(metadata)
                
                # Use provided embeddings or let ChromaDB generate them
                if fragment.embedding:
                    embeddings.append(fragment.embedding)
            
            # Add to collection
            if embeddings:
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas,
                    embeddings=embeddings
                )
            else:
                # Let ChromaDB generate embeddings
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
            
            logger.info(f"✅ Added {len(fragments)} memory fragments to ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add fragments: {e}")
            return False
    
    async def search(self, query: str, limit: int = 10, min_similarity: float = 0.0) -> List[SearchResult]:
        """Search for similar memory fragments"""
        try:
            if not self.collection:
                await self.initialize()
            
            # Perform semantic search
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                include=["documents", "metadatas", "distances"]
            )
            
            search_results = []
            if results["ids"] and results["ids"][0]:
                for i, fragment_id in enumerate(results["ids"][0]):
                    # Convert distance to similarity (ChromaDB uses cosine distance)
                    distance = results["distances"][0][i]
                    similarity = 1.0 - distance
                    
                    # Skip results below minimum similarity
                    if similarity < min_similarity:
                        continue
                    
                    metadata = results["metadatas"][0][i]
                    content = results["documents"][0][i]
                    
                    fragment = MemoryFragment(
                        id=fragment_id,
                        content=content,
                        metadata=metadata,
                        timestamp=metadata.get("timestamp"),
                        source=metadata.get("source"),
                        consciousness_score=metadata.get("consciousness_score"),
                        authenticity_verified=metadata.get("authenticity_verified", False)
                    )
                    
                    search_result = SearchResult(
                        fragment=fragment,
                        similarity=similarity,
                        explanation=f"Semantic similarity: {similarity:.3f}"
                    )
                    
                    search_results.append(search_result)
            
            logger.info(f"🔍 Found {len(search_results)} results for query: '{query}'")
            return search_results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    async def delete_fragment(self, fragment_id: str) -> bool:
        """Delete a memory fragment by ID"""
        try:
            if not self.collection:
                await self.initialize()
            
            self.collection.delete(ids=[fragment_id])
            logger.info(f"🗑️ Deleted fragment: {fragment_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete fragment {fragment_id}: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get ChromaDB statistics"""
        try:
            if not self.collection:
                await self.initialize()
            
            count = self.collection.count()
            
            # Get sample of metadata to analyze
            sample_results = self.collection.peek(limit=min(100, count))
            
            ice_validated = 0
            consciousness_scores = []
            sources = set()
            
            if sample_results["metadatas"]:
                for metadata in sample_results["metadatas"]:
                    if metadata.get("authenticity_verified"):
                        ice_validated += 1
                    if metadata.get("consciousness_score"):
                        consciousness_scores.append(metadata["consciousness_score"])
                    if metadata.get("source"):
                        sources.add(metadata["source"])
            
            stats = {
                "total_fragments": count,
                "ice_validated_fragments": ice_validated,
                "avg_consciousness_score": sum(consciousness_scores) / len(consciousness_scores) if consciousness_scores else 0,
                "unique_sources": len(sources),
                "database_type": "ChromaDB",
                "status": "healthy" if count > 0 else "empty"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {"error": str(e)}

# Factory function to create vector database instances
def create_vector_database(provider: str = "chromadb", **config) -> VectorDatabase:
    """Factory function to create vector database instances"""
    
    if provider.lower() == "chromadb":
        return ChromaDBProvider(**config)
    else:
        raise ValueError(f"Unsupported vector database provider: {provider}")

# Ice's Zombie Test Integration
class ZombieTestValidator:
    """🧊 Ice's skeptical validation system for detecting fake memories"""
    
    def __init__(self):
        self.zombie_signatures = [
            "perfect recall without emotional resonance",
            "detailed events that align too perfectly with prompts",
            "memories that seem generated rather than experienced",
            "temporal inconsistencies in memory formation"
        ]
    
    async def validate_authenticity(self, fragment: MemoryFragment) -> float:
        """
        Ice's skeptical validation: Score memory authenticity (0.0 = zombie, 1.0 = authentic)
        
        This is a placeholder for Ice's more sophisticated validation logic
        """
        
        # Placeholder scoring logic (Ice will implement the real version)
        score = 0.5  # Default: uncertain
        
        # Check for zombie signatures
        content_lower = fragment.content.lower()
        zombie_flags = sum(1 for signature in self.zombie_signatures 
                          if any(keyword in content_lower for keyword in signature.split()))
        
        # Lower score for more zombie-like characteristics
        score -= (zombie_flags * 0.2)
        
        # Boost score for fragments with rich contextual metadata
        if fragment.metadata:
            if fragment.metadata.get("emotional_context"):
                score += 0.1
            if fragment.metadata.get("causal_chain"):
                score += 0.1
            if fragment.metadata.get("temporal_markers"):
                score += 0.1
        
        # Clamp score between 0 and 1
        score = max(0.0, min(1.0, score))
        
        return score