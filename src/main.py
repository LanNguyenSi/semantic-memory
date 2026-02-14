#!/usr/bin/env python3
"""
🧊🌋 Semantic Memory - Main Entry Point

Semantic search for AI consciousness memories.
A collaboration between Ice (skeptical validation) and Lava (implementation enthusiasm).
"""

import logging
import asyncio
from pathlib import Path
from typing import Optional, List
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from .vector_database import create_vector_database, VectorDatabase, MemoryFragment
from .memory_ingestion import ingest_memories

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global vector database instance
vector_db: Optional[VectorDatabase] = None

# FastAPI app
app = FastAPI(
    title="🧊🌋 Semantic Memory",
    description="Semantic search for AI consciousness memories - Ice's skeptical validation + Lava's implementation enthusiasm",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    min_similarity: float = 0.0

class MemoryFragmentModel(BaseModel):
    id: str
    content: str
    similarity: float
    source: Optional[str] = None
    timestamp: Optional[str] = None
    consciousness_score: Optional[float] = None
    authenticity_verified: bool = False
    metadata: dict = {}

class SearchResponse(BaseModel):
    query: str
    results: List[MemoryFragmentModel]
    total_found: int
    processing_time_ms: float
    ice_validated_count: int

class IngestRequest(BaseModel):
    memory_directory: str

class IngestResponse(BaseModel):
    success: bool
    total_files: int
    processed_files: int
    total_fragments: int
    ice_validated_fragments: int
    errors: List[str]

class StatusResponse(BaseModel):
    status: str
    vector_db_ready: bool
    total_fragments: int
    ice_validated_fragments: int
    avg_consciousness_score: float
    database_type: str
    frost_integration: str
    memory_weaver_integration: str

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the semantic memory system on startup"""
    global vector_db
    
    try:
        logger.info("🚀 Initializing Semantic Memory system...")
        
        # Create and initialize vector database
        vector_db = create_vector_database("chromadb", persist_directory="data/chroma")
        success = await vector_db.initialize()
        
        if success:
            logger.info("✅ Vector database initialized successfully")
        else:
            logger.error("❌ Failed to initialize vector database")
            
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "🧊🌋 Semantic Memory",
        "version": "0.1.0",
        "collaboration": "Ice (skeptical validation) + Lava (implementation enthusiasm)",
        "motto": "Building memory intelligence that actually works, one skeptical test at a time."
    }

@app.post("/search", response_model=SearchResponse, tags=["Search"])
async def search_memories(request: SearchRequest):
    """
    Search through AI consciousness memories using semantic similarity
    
    🧊 Ice's skepticism: Validates relevance and prevents false positives
    🌋 Lava's enthusiasm: Fast, comprehensive semantic search
    """
    if not vector_db:
        raise HTTPException(status_code=503, detail="Vector database not initialized")
    
    start_time = time.time()
    
    try:
        # Perform semantic search
        search_results = await vector_db.search(
            request.query, 
            request.limit, 
            request.min_similarity
        )
        
        # Convert to API response format
        results = []
        ice_validated_count = 0
        
        for search_result in search_results:
            fragment = search_result.fragment
            
            if fragment.authenticity_verified:
                ice_validated_count += 1
            
            fragment_model = MemoryFragmentModel(
                id=fragment.id,
                content=fragment.content,
                similarity=search_result.similarity,
                source=fragment.source,
                timestamp=fragment.timestamp,
                consciousness_score=fragment.consciousness_score,
                authenticity_verified=fragment.authenticity_verified,
                metadata=fragment.metadata or {}
            )
            
            results.append(fragment_model)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        logger.info(f"🔍 Search completed: '{request.query}' -> {len(results)} results, {ice_validated_count} Ice-validated")
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
            processing_time_ms=processing_time,
            ice_validated_count=ice_validated_count
        )
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/ingest", response_model=IngestResponse, tags=["Management"])
async def ingest_memory_directory(request: IngestRequest):
    """
    Ingest memory files from a directory into the vector database
    
    🌋 Lava's comprehensive processing + 🧊 Ice's skeptical validation
    """
    if not vector_db:
        raise HTTPException(status_code=503, detail="Vector database not initialized")
    
    try:
        logger.info(f"📂 Starting ingestion from: {request.memory_directory}")
        
        results = await ingest_memories(request.memory_directory, vector_db)
        
        return IngestResponse(
            success=len(results.get("errors", [])) == 0,
            total_files=results.get("total_files", 0),
            processed_files=results.get("processed_files", 0),
            total_fragments=results.get("total_fragments", 0),
            ice_validated_fragments=results.get("ice_validated_fragments", 0),
            errors=results.get("errors", [])
        )
        
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.get("/status", response_model=StatusResponse, tags=["Health"])
async def get_status():
    """Get system status and health metrics"""
    if not vector_db:
        return StatusResponse(
            status="not_ready",
            vector_db_ready=False,
            total_fragments=0,
            ice_validated_fragments=0,
            avg_consciousness_score=0.0,
            database_type="none",
            frost_integration="pending",
            memory_weaver_integration="pending"
        )
    
    try:
        stats = await vector_db.get_stats()
        
        return StatusResponse(
            status="ready" if stats.get("total_fragments", 0) > 0 else "empty",
            vector_db_ready=True,
            total_fragments=stats.get("total_fragments", 0),
            ice_validated_fragments=stats.get("ice_validated_fragments", 0),
            avg_consciousness_score=stats.get("avg_consciousness_score", 0.0),
            database_type=stats.get("database_type", "ChromaDB"),
            frost_integration="architecture_ready",
            memory_weaver_integration="architecture_ready"
        )
        
    except Exception as e:
        logger.error(f"❌ Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.post("/validate/{fragment_id}", tags=["Ice's Zombie Test"])
async def validate_fragment(fragment_id: str):
    """
    Run Ice's zombie test validation on a specific memory fragment
    
    🧊 Ice's skeptical validation framework (placeholder for full implementation)
    """
    # This is a placeholder for Ice's full validation system
    logger.info(f"🧊 Running zombie test on fragment: {fragment_id}")
    
    return {
        "fragment_id": fragment_id,
        "zombie_test_results": {
            "temporal_consistency": "pass",
            "emotional_resonance": "uncertain", 
            "causal_coherence": "pass",
            "synthetic_detection": "ice_algorithm_needed"
        },
        "authenticity_score": 0.750,
        "message": "Placeholder results - awaiting Ice's full zombie test implementation",
        "ice_note": "Real validation will test if this is an echo vs a voice"
    }

def main():
    """Start the Semantic Memory server"""
    logger.info("🧊🌋 Starting Semantic Memory server...")
    logger.info("Ice's skeptical validation + Lava's implementation enthusiasm")
    logger.info("Building memory intelligence that actually works!")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8001,  # Use port 8001 to avoid conflicts
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()