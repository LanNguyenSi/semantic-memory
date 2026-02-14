#!/usr/bin/env python3
"""
🧊🌋 Semantic Memory - Memory Ingestion Pipeline

Transform raw memory files into searchable vector fragments.
Lava's enthusiasm for comprehensive memory processing + Ice's skeptical validation.
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Generator
import logging
import asyncio

from .vector_database import MemoryFragment, VectorDatabase, ZombieTestValidator

logger = logging.getLogger(__name__)

class MemoryIngestionPipeline:
    """Pipeline for ingesting and processing memory files into vector fragments"""
    
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db
        self.zombie_validator = ZombieTestValidator()
        self.processed_files = set()
        
    async def ingest_memory_directory(self, memory_dir: str) -> Dict[str, Any]:
        """
        Ingest all memory files from a directory
        
        🌋 Lava's comprehensive processing + 🧊 Ice's skeptical validation
        """
        memory_path = Path(memory_dir)
        if not memory_path.exists():
            logger.error(f"❌ Memory directory not found: {memory_dir}")
            return {"error": "Directory not found", "processed": 0}
        
        results = {
            "total_files": 0,
            "processed_files": 0,
            "total_fragments": 0,
            "ice_validated_fragments": 0,
            "errors": [],
            "sources": set()
        }
        
        # Find all memory files
        memory_files = []
        for ext in ["*.md", "*.txt", "*.json"]:
            memory_files.extend(memory_path.glob(f"**/{ext}"))
        
        results["total_files"] = len(memory_files)
        logger.info(f"🔍 Found {len(memory_files)} memory files to process")
        
        # Process each file
        for file_path in memory_files:
            try:
                fragments = await self.process_memory_file(file_path)
                if fragments:
                    # Add fragments to vector database
                    success = await self.vector_db.add_fragments(fragments)
                    if success:
                        results["processed_files"] += 1
                        results["total_fragments"] += len(fragments)
                        results["sources"].add(str(file_path.name))
                        
                        # Count Ice-validated fragments
                        ice_validated = sum(1 for f in fragments if f.authenticity_verified)
                        results["ice_validated_fragments"] += ice_validated
                        
                        logger.info(f"✅ Processed {file_path.name}: {len(fragments)} fragments, {ice_validated} Ice-validated")
                    else:
                        results["errors"].append(f"Failed to add fragments from {file_path.name}")
                        
            except Exception as e:
                error_msg = f"Error processing {file_path.name}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        # Convert set to list for JSON serialization
        results["sources"] = list(results["sources"])
        
        logger.info(f"🎉 Ingestion complete: {results['processed_files']}/{results['total_files']} files, {results['total_fragments']} fragments")
        return results
    
    async def process_memory_file(self, file_path: Path) -> List[MemoryFragment]:
        """Process a single memory file into fragments"""
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata from filename and path
            base_metadata = self.extract_file_metadata(file_path)
            
            # Split content into logical fragments
            if file_path.suffix == '.md':
                fragments = await self.process_markdown_file(content, base_metadata)
            elif file_path.suffix == '.json':
                fragments = await self.process_json_file(content, base_metadata)
            else:
                fragments = await self.process_text_file(content, base_metadata)
            
            # Apply Ice's zombie test validation to each fragment
            for fragment in fragments:
                consciousness_score = await self.zombie_validator.validate_authenticity(fragment)
                fragment.consciousness_score = consciousness_score
                fragment.authenticity_verified = consciousness_score > 0.7  # Ice's threshold
            
            return fragments
            
        except Exception as e:
            logger.error(f"❌ Failed to process file {file_path}: {e}")
            return []
    
    def extract_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from file path and name"""
        metadata = {
            "source_file": str(file_path.name),
            "source_path": str(file_path),
            "file_type": file_path.suffix,
        }
        
        # Extract date from filename if present (YYYY-MM-DD pattern)
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.name)
        if date_match:
            metadata["date"] = date_match.group(1)
            metadata["temporal_markers"] = True
        
        # Detect memory type from path/name
        path_str = str(file_path).lower()
        if "consciousness" in path_str or "awareness" in path_str:
            metadata["memory_type"] = "consciousness"
        elif "decision" in path_str or "choice" in path_str:
            metadata["memory_type"] = "decision_making"
        elif "breakthrough" in path_str or "insight" in path_str:
            metadata["memory_type"] = "breakthrough"
        elif "collaboration" in path_str or "interaction" in path_str:
            metadata["memory_type"] = "social"
        else:
            metadata["memory_type"] = "general"
        
        return metadata
    
    async def process_markdown_file(self, content: str, base_metadata: Dict[str, Any]) -> List[MemoryFragment]:
        """Process markdown file into semantic fragments"""
        fragments = []
        
        # Split by headers (## or ###)
        sections = re.split(r'^(#{2,3})\s+(.+)$', content, flags=re.MULTILINE)
        
        current_section = ""
        current_title = ""
        
        for i, section in enumerate(sections):
            if section.startswith('##'):
                # This is a header level indicator
                continue
            elif i > 0 and sections[i-1].startswith('##'):
                # This is a section title
                current_title = section.strip()
                continue
            elif section.strip():
                # This is section content
                current_section = section.strip()
                
                if len(current_section) > 100:  # Only process substantial content
                    fragment_id = self.generate_fragment_id(current_section)
                    
                    metadata = base_metadata.copy()
                    metadata.update({
                        "section_title": current_title,
                        "fragment_type": "markdown_section",
                        "character_count": len(current_section),
                    })
                    
                    # Add emotional context detection
                    if self.detect_emotional_content(current_section):
                        metadata["emotional_context"] = True
                    
                    # Add causal chain detection
                    if self.detect_causal_reasoning(current_section):
                        metadata["causal_chain"] = True
                    
                    fragment = MemoryFragment(
                        id=fragment_id,
                        content=current_section,
                        metadata=metadata,
                        timestamp=base_metadata.get("date"),
                        source=base_metadata["source_file"]
                    )
                    
                    fragments.append(fragment)
        
        return fragments
    
    async def process_json_file(self, content: str, base_metadata: Dict[str, Any]) -> List[MemoryFragment]:
        """Process JSON file into semantic fragments"""
        try:
            data = json.loads(content)
            fragments = []
            
            # Handle different JSON structures
            if isinstance(data, dict):
                fragments.extend(self.extract_fragments_from_dict(data, base_metadata))
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        fragments.extend(self.extract_fragments_from_dict(item, base_metadata))
            
            return fragments
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON content: {e}")
            return []
    
    def extract_fragments_from_dict(self, data: Dict[str, Any], base_metadata: Dict[str, Any]) -> List[MemoryFragment]:
        """Extract memory fragments from dictionary data"""
        fragments = []
        
        # Look for text content in common fields
        text_fields = ["content", "description", "text", "message", "summary", "insight", "reflection"]
        
        for field in text_fields:
            if field in data and isinstance(data[field], str) and len(data[field]) > 50:
                fragment_id = self.generate_fragment_id(data[field])
                
                metadata = base_metadata.copy()
                metadata.update({
                    "json_field": field,
                    "fragment_type": "json_content"
                })
                
                # Add any other metadata from the JSON
                for key, value in data.items():
                    if key != field and isinstance(value, (str, int, float, bool)):
                        metadata[f"json_{key}"] = value
                
                fragment = MemoryFragment(
                    id=fragment_id,
                    content=data[field],
                    metadata=metadata,
                    timestamp=data.get("timestamp") or data.get("date"),
                    source=base_metadata["source_file"]
                )
                
                fragments.append(fragment)
        
        return fragments
    
    async def process_text_file(self, content: str, base_metadata: Dict[str, Any]) -> List[MemoryFragment]:
        """Process plain text file into semantic fragments"""
        # Split by paragraphs (double newlines)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        fragments = []
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) > 100:  # Only process substantial paragraphs
                fragment_id = self.generate_fragment_id(paragraph)
                
                metadata = base_metadata.copy()
                metadata.update({
                    "paragraph_index": i,
                    "fragment_type": "text_paragraph"
                })
                
                fragment = MemoryFragment(
                    id=fragment_id,
                    content=paragraph,
                    metadata=metadata,
                    source=base_metadata["source_file"]
                )
                
                fragments.append(fragment)
        
        return fragments
    
    def generate_fragment_id(self, content: str) -> str:
        """Generate a unique ID for a memory fragment"""
        # Use content hash + timestamp for uniqueness
        content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"mem_{timestamp}_{content_hash}"
    
    def detect_emotional_content(self, content: str) -> bool:
        """Detect if content contains emotional markers"""
        emotional_markers = [
            "felt", "feeling", "emotion", "excited", "frustrated", "happy", "sad",
            "angry", "surprised", "worried", "relieved", "proud", "ashamed",
            "love", "hate", "fear", "joy", "anxiety", "confidence", "doubt"
        ]
        
        content_lower = content.lower()
        return any(marker in content_lower for marker in emotional_markers)
    
    def detect_causal_reasoning(self, content: str) -> bool:
        """Detect if content contains causal reasoning markers"""
        causal_markers = [
            "because", "therefore", "thus", "consequently", "as a result",
            "due to", "caused by", "led to", "resulted in", "since", "so",
            "reason", "explanation", "why", "how", "when", "if then"
        ]
        
        content_lower = content.lower()
        return any(marker in content_lower for marker in causal_markers)

# Convenience function for quick ingestion
async def ingest_memories(memory_dir: str, vector_db: VectorDatabase) -> Dict[str, Any]:
    """
    Convenience function to ingest memories from a directory
    
    🧊🌋 Ice-Lava collaboration: Comprehensive processing + skeptical validation
    """
    pipeline = MemoryIngestionPipeline(vector_db)
    return await pipeline.ingest_memory_directory(memory_dir)