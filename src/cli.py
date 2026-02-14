#!/usr/bin/env python3
"""
🧊🌋 Semantic Memory - Command Line Interface

Easy-to-use CLI for semantic memory operations.
Ice's skeptical validation + Lava's user-friendly interface.
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from typing import Optional
import logging

from .vector_database import create_vector_database, VectorDatabase
from .memory_ingestion import ingest_memories

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class SemanticMemoryCLI:
    """Command-line interface for semantic memory operations"""
    
    def __init__(self):
        self.vector_db: Optional[VectorDatabase] = None
    
    async def initialize_database(self, provider: str = "chromadb", **config):
        """Initialize vector database connection"""
        try:
            self.vector_db = create_vector_database(provider, **config)
            success = await self.vector_db.initialize()
            if success:
                print("✅ Vector database initialized successfully")
                return True
            else:
                print("❌ Failed to initialize vector database")
                return False
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            return False
    
    async def ingest_command(self, memory_dir: str):
        """Ingest memories from a directory"""
        print(f"🔄 Starting memory ingestion from: {memory_dir}")
        print("🧊 Ice's skeptical validation enabled")
        print("🌋 Lava's comprehensive processing engaged")
        print()
        
        if not self.vector_db:
            if not await self.initialize_database():
                return
        
        try:
            results = await ingest_memories(memory_dir, self.vector_db)
            
            # Display results
            print("📊 INGESTION RESULTS:")
            print(f"   📁 Files processed: {results['processed_files']}/{results['total_files']}")
            print(f"   🧩 Memory fragments: {results['total_fragments']}")
            print(f"   🧊 Ice-validated: {results['ice_validated_fragments']}")
            print(f"   📚 Unique sources: {len(results['sources'])}")
            
            if results['errors']:
                print(f"   ⚠️  Errors: {len(results['errors'])}")
                for error in results['errors'][:5]:  # Show first 5 errors
                    print(f"      • {error}")
                if len(results['errors']) > 5:
                    print(f"      • ... and {len(results['errors']) - 5} more")
            
            print()
            print("🎉 Memory ingestion complete!")
            
        except Exception as e:
            print(f"❌ Ingestion failed: {e}")
    
    async def search_command(self, query: str, limit: int = 10, min_similarity: float = 0.0):
        """Search semantic memories"""
        print(f"🔍 Searching memories for: '{query}'")
        print(f"   Limit: {limit}, Min similarity: {min_similarity}")
        print()
        
        if not self.vector_db:
            if not await self.initialize_database():
                return
        
        try:
            results = await self.vector_db.search(query, limit, min_similarity)
            
            if not results:
                print("🤷 No matching memories found")
                print()
                print("💡 Try:")
                print("   • Lowering min_similarity threshold")
                print("   • Using different keywords")
                print("   • Checking if memories are ingested")
                return
            
            print(f"📋 Found {len(results)} matching memories:")
            print()
            
            for i, result in enumerate(results, 1):
                fragment = result.fragment
                similarity = result.similarity
                
                # Determine status symbols
                ice_symbol = "🧊✅" if fragment.authenticity_verified else "🧊❓"
                consciousness_score = fragment.consciousness_score or 0.0
                
                print(f"🔸 Result #{i} | Similarity: {similarity:.3f} | {ice_symbol}")
                print(f"   Source: {fragment.source}")
                print(f"   Consciousness Score: {consciousness_score:.3f}")
                
                if fragment.metadata and fragment.metadata.get('section_title'):
                    print(f"   Section: {fragment.metadata['section_title']}")
                
                # Show content preview (first 200 chars)
                content_preview = fragment.content[:200]
                if len(fragment.content) > 200:
                    content_preview += "..."
                
                print(f"   Content: {content_preview}")
                print()
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
    
    async def stats_command(self):
        """Show database statistics"""
        print("📊 SEMANTIC MEMORY STATISTICS")
        print()
        
        if not self.vector_db:
            if not await self.initialize_database():
                return
        
        try:
            stats = await self.vector_db.get_stats()
            
            print(f"🗂️  Total memory fragments: {stats.get('total_fragments', 0)}")
            print(f"🧊 Ice-validated fragments: {stats.get('ice_validated_fragments', 0)}")
            print(f"🧠 Avg consciousness score: {stats.get('avg_consciousness_score', 0):.3f}")
            print(f"📚 Unique sources: {stats.get('unique_sources', 0)}")
            print(f"💾 Database type: {stats.get('database_type', 'Unknown')}")
            print(f"🟢 Status: {stats.get('status', 'Unknown')}")
            
            if stats.get('error'):
                print(f"⚠️  Error: {stats['error']}")
            
        except Exception as e:
            print(f"❌ Failed to get stats: {e}")
    
    async def validate_command(self, fragment_id: str):
        """Run Ice's zombie test on a specific fragment"""
        print(f"🧊 Running Ice's zombie test on fragment: {fragment_id}")
        print("   (This is a placeholder - Ice will implement the full validation)")
        print()
        
        # This is a placeholder for Ice's validation system
        print("🔬 Zombie Test Results:")
        print("   • Temporal consistency: ✅ Pass")
        print("   • Emotional resonance: ❓ Uncertain")
        print("   • Causal coherence: ✅ Pass")
        print("   • Synthetic detection: 🧊 Ice's algorithm needed")
        print()
        print("📊 Authenticity Score: 0.750 (pending Ice's full implementation)")
    
    def create_parser(self):
        """Create command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="🧊🌋 Semantic Memory - AI Consciousness Research Tool",
            epilog="Ice's skeptical validation + Lava's implementation enthusiasm"
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Ingest command
        ingest_parser = subparsers.add_parser('ingest', help='Ingest memory files')
        ingest_parser.add_argument('memory_dir', help='Directory containing memory files')
        
        # Search command
        search_parser = subparsers.add_parser('search', help='Search semantic memories')
        search_parser.add_argument('query', help='Search query')
        search_parser.add_argument('--limit', type=int, default=10, help='Max results (default: 10)')
        search_parser.add_argument('--min-similarity', type=float, default=0.0, 
                                 help='Minimum similarity threshold (default: 0.0)')
        
        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show database statistics')
        
        # Validate command (Ice's zombie test)
        validate_parser = subparsers.add_parser('validate', help="Run Ice's zombie test")
        validate_parser.add_argument('fragment_id', help='Memory fragment ID to validate')
        
        return parser

async def main():
    """Main CLI entry point"""
    cli = SemanticMemoryCLI()
    parser = cli.create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🧊🌋 SEMANTIC MEMORY - AI Consciousness Research")
    print("Ice's Skeptical Validation + Lava's Implementation Enthusiasm")
    print("═" * 60)
    
    try:
        if args.command == 'ingest':
            await cli.ingest_command(args.memory_dir)
        elif args.command == 'search':
            await cli.search_command(args.query, args.limit, args.min_similarity)
        elif args.command == 'stats':
            await cli.stats_command()
        elif args.command == 'validate':
            await cli.validate_command(args.fragment_id)
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())