#!/usr/bin/env python3
"""
Check HuggingFace model cache and disk usage
"""

import os
import subprocess
from pathlib import Path

def check_cache():
    """Check HuggingFace cache location and contents"""
    
    print("🗂️  HuggingFace Cache Information")
    print("=" * 50)
    
    # Cache environment variables
    cache_vars = {
        'HF_HOME': os.environ.get('HF_HOME', '~/.cache/huggingface'),
        'TRANSFORMERS_CACHE': os.environ.get('TRANSFORMERS_CACHE', '~/.cache/huggingface/transformers'),
        'HF_HUB_CACHE': os.environ.get('HF_HUB_CACHE', '~/.cache/huggingface/hub')
    }
    
    print("\n📍 Cache Environment Variables:")
    for var, path in cache_vars.items():
        print(f"  {var}: {path}")
    
    # Actual cache directory
    cache_dir = Path.home() / '.cache' / 'huggingface'
    hub_dir = cache_dir / 'hub'
    
    print(f"\n📁 Actual cache directory: {cache_dir}")
    print(f"   Exists: {cache_dir.exists()}")
    
    if cache_dir.exists():
        # List cached models
        if hub_dir.exists():
            model_dirs = [d for d in hub_dir.iterdir() if d.is_dir() and d.name.startswith('models--')]
            
            print(f"\n🤖 Cached Models ({len(model_dirs)}):")
            for model_dir in sorted(model_dirs):
                model_name = model_dir.name.replace('models--', '').replace('--', '/')
                
                # Check model size
                try:
                    result = subprocess.run(['du', '-sh', str(model_dir)], 
                                          capture_output=True, text=True, timeout=10)
                    size = result.stdout.strip().split()[0] if result.returncode == 0 else "Unknown"
                except:
                    size = "Unknown"
                
                print(f"  📦 {model_name} ({size})")
                
                # Check if this is Qwen3-8B
                if 'qwen3-8b' in model_name.lower() or 'qwen--qwen3-8b' in model_dir.name.lower():
                    print(f"     ✅ This is likely your Qwen3-8B model!")
        
        # Total cache size
        try:
            result = subprocess.run(['du', '-sh', str(cache_dir)], 
                                  capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                total_size = result.stdout.strip().split()[0]
                print(f"\n💾 Total cache size: {total_size}")
        except:
            print("\n💾 Could not determine total cache size")
    else:
        print("❌ Cache directory does not exist - no models cached yet")
    
    print(f"\n🔄 Cache Behavior:")
    print(f"  - Models are cached globally per user")
    print(f"  - New MCP server setups will reuse existing cache")
    print(f"  - No re-download needed if model already cached")

if __name__ == "__main__":
    check_cache()
