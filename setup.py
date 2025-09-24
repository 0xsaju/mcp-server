#!/usr/bin/env python3
"""
Setup script for MCP Local LLM Server
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def check_gpu():
    """Check GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU detected: {gpu_name} ({gpu_count} device(s))")
            return True
        else:
            print("⚠️  No GPU detected - will use CPU (slower)")
            return False
    except ImportError:
        print("ℹ️  PyTorch not installed yet - GPU check will happen after installation")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    config_file = Path("config.env")
    
    if not env_file.exists() and config_file.exists():
        shutil.copy(config_file, env_file)
        print("✅ Created .env file from template")
    elif env_file.exists():
        print("ℹ️  .env file already exists")
    else:
        print("⚠️  No config template found")


def check_model_cache():
    """Check if model is already cached"""
    from transformers import AutoTokenizer
    
    model_name = os.getenv("MODEL_NAME", "Qwen/Qwen3-8B")
    
    try:
        # This will download the model if not cached
        print(f"\n🔄 Checking model cache for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        print(f"✅ Model {model_name} is available")
    except Exception as e:
        print(f"⚠️  Model download may be needed: {e}")


def main():
    """Main setup function"""
    print("🚀 MCP Local LLM Server Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check GPU
    has_gpu = check_gpu()
    
    # Install dependencies
    install_dependencies()
    
    # Create environment file
    create_env_file()
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Check model availability
    try:
        check_model_cache()
    except Exception as e:
        print(f"⚠️  Could not check model cache: {e}")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Configure your .env file if needed")
    print("2. Test the server: python test_server.py")
    print("3. Run the server: python mcp_server.py")
    print("4. Integrate with Claude Desktop using claude_desktop_config.json")
    
    if not has_gpu:
        print("\n💡 Note: Consider using a smaller model or enabling GPU acceleration for better performance")


if __name__ == "__main__":
    main()
