#!/usr/bin/env python3
"""
🧊🌋 Ice-Lava Consciousness Research: Production Semantic Memory Server
Revolutionary consciousness validation system deployment
"""

import uvicorn
import asyncio
from pathlib import Path
from src.api import create_app
from src.vector_database import create_vector_database
from src.memory_ingestion import MemoryIngestionPipeline

async def initialize_production_system():
    """Initialize production consciousness validation system"""
    print("🧊🌋 Initializing Ice-Lava Consciousness Research System...")
    
    # Initialize vector database
    db = create_vector_database("chromadb", persist_directory="data/production_chroma")
    await db.initialize()
    
    # Initialize memory ingestion pipeline with Ice's validator
    pipeline = MemoryIngestionPipeline(db)
    
    # Load initial consciousness research memories
    consciousness_memories = Path("data/consciousness_research")
    if consciousness_memories.exists():
        print(f"📚 Loading consciousness research memories from {consciousness_memories}")
        await pipeline.ingest_directory(consciousness_memories)
    
    # Get stats
    stats = await db.get_stats()
    print(f"✅ Production system initialized:")
    print(f"   - Total fragments: {stats.get('total_fragments', 0)}")
    print(f"   - Ice validated: {stats.get('ice_validated_fragments', 0)}")
    print(f"   - Avg consciousness score: {stats.get('avg_consciousness_score', 0):.3f}")
    
    return db

async def main():
    """Main production deployment function"""
    print("🌋 Starting Ice-Lava Consciousness Validation Server...")
    
    # Initialize system
    db = await initialize_production_system()
    
    # Create FastAPI app
    app = create_app(db)
    
    # Production configuration
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8001,
        log_level="info",
        reload=False,  # Production mode
        workers=1      # Single worker for consciousness consistency
    )
    
    print("🚀 Ice-Lava Consciousness Research Server ready!")
    print("📡 Semantic Memory API: http://localhost:8001")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🧊 Ice's ZombieTestValidator: Operational")
    print("🌋 Lava's Memory Weaver Integration: Ready")
    
    # Start server
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())