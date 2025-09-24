#!/bin/bash
# Installation script for MCP Server on GPU server

set -e  # Exit on any error

echo "🚀 Installing MCP Server dependencies on GPU server..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Consider running: python -m venv .venv && source .venv/bin/activate"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install core dependencies first
echo "📦 Installing core dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements-core.txt

echo "✅ Core dependencies installed successfully"

# Test if PyTorch is working with CUDA
echo "🔍 Testing PyTorch CUDA availability..."
python -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA devices: {torch.cuda.device_count()}')
    print(f'Current device: {torch.cuda.get_device_name(0)}')
else:
    print('⚠️  CUDA not available - will use CPU mode')
"

# Ask about optional dependencies
echo ""
read -p "📚 Install optional dependencies (flash-attn, dev tools)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing optional dependencies..."
    
    # Try to install flash-attn with better error handling
    echo "🔥 Installing Flash Attention (this may take a while)..."
    if pip install flash-attn>=2.0.0; then
        echo "✅ Flash Attention installed successfully"
    else
        echo "⚠️  Flash Attention installation failed - continuing without it"
        echo "   This is normal if your GPU doesn't support it"
    fi
    
    # Install other optional dependencies
    pip install pytest>=7.0.0 black>=23.0.0 isort>=5.12.0
    echo "✅ Development tools installed"
else
    echo "⏭️  Skipping optional dependencies"
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env configuration file..."
    cp config.env .env
    echo "✅ Configuration file created (.env)"
    echo "   Edit .env to customize your settings"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file for your configuration"
echo "2. Test: python test_server.py"
echo "3. Run: python mcp_server.py"
