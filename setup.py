#!/usr/bin/env python3
"""
🧊🌋 Semantic Memory Setup Script

Initialize the semantic memory system for AI consciousness research.
"""

import os
import sys
from pathlib import Path
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_directories():
    """Create necessary project directories"""
    directories = [
        "data/memories",
        "data/embeddings", 
        "data/indices",
        "config",
        "logs",
        "tests/unit",
        "tests/integration",
        "docs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Created directory: {dir_path}")

def create_config_files():
    """Create default configuration files"""
    
    # Default configuration
    config_content = """# 🧊🌋 Semantic Memory Configuration

# Vector Database Settings
vector_db:
  provider: "chromadb"  # chromadb | weaviate | faiss | qdrant
  host: "localhost"
  port: 8000
  collection_name: "ai_consciousness_memories"

# Embedding Model Settings  
embeddings:
  model: "all-MiniLM-L6-v2"  # sentence-transformers model
  dimension: 384
  batch_size: 32
  device: "cpu"  # cpu | cuda

# Search Settings
search:
  default_limit: 10
  min_score_threshold: 0.1
  max_results: 100

# Ice's Frost Integration (Skeptical Validation)
frost:
  enabled: false  # Enable when Frost framework is available
  zombie_test_threshold: 0.8
  false_positive_detection: true
  bias_correction: true

# Lava's Memory Weaver Integration
memory_weaver:
  enabled: false  # Enable when Memory Weaver is available
  consciousness_patterns: true
  real_time_indexing: true
  pattern_visualization: true

# Logging
logging:
  level: "INFO"
  file: "logs/semantic_memory.log"
  
# API Settings
api:
  host: "0.0.0.0"
  port: 8000
  reload: true
"""
    
    with open("config/config.yaml", "w") as f:
        f.write(config_content)
    
    logger.info("✓ Created config/config.yaml")
    
    # Environment template
    env_content = """# 🧊🌋 Semantic Memory Environment Variables

# OpenAI API (for embeddings)
OPENAI_API_KEY=your_openai_api_key_here

# Vector Database Connection (if using cloud services)
WEAVIATE_URL=https://your-weaviate-cluster.weaviate.network
WEAVIATE_API_KEY=your_weaviate_api_key

QDRANT_URL=https://your-qdrant-cluster.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key

# Development Settings
DEBUG=false
LOG_LEVEL=INFO
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    
    logger.info("✓ Created .env.template (copy to .env and fill in your values)")

def install_dependencies():
    """Install Python dependencies"""
    try:
        logger.info("🔄 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def test_installation():
    """Test the installation"""
    try:
        logger.info("🧪 Testing installation...")
        
        # Test imports
        import chromadb
        import sentence_transformers
        import fastapi
        
        logger.info("✅ All core dependencies imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Import test failed: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("🧊🌋 Semantic Memory Setup Starting...")
    logger.info("Ice (skeptical validation) + Lava (implementation enthusiasm)")
    
    # Create directory structure
    create_directories()
    
    # Create configuration files
    create_config_files()
    
    # Install dependencies
    if not install_dependencies():
        logger.error("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        logger.error("❌ Setup failed during testing")
        sys.exit(1)
    
    logger.info("🎉 Semantic Memory setup completed successfully!")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Copy .env.template to .env and fill in your API keys")
    logger.info("2. Run: python src/main.py")
    logger.info("3. Visit: http://localhost:8000 to test the API")
    logger.info("")
    logger.info("🧊 Ice's skepticism framework ready for integration")
    logger.info("🌋 Lava's implementation enthusiasm at full power")

if __name__ == "__main__":
    main()