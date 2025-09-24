#!/bin/bash
# Setup script for Cursor IDE integration

echo "🎯 Setting up Cursor IDE integration with MCP Server"
echo "=" * 60

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "🖥️  Detected OS: ${MACHINE}"

# Set Cursor config path based on OS
case "${MACHINE}" in
    Mac)
        CURSOR_CONFIG_DIR="$HOME/Library/Application Support/Cursor/User"
        ;;
    Linux)
        CURSOR_CONFIG_DIR="$HOME/.config/Cursor/User"
        ;;
    Cygwin|MinGw)
        CURSOR_CONFIG_DIR="$APPDATA/Cursor/User"
        ;;
    *)
        echo "❌ Unsupported OS: ${MACHINE}"
        exit 1
        ;;
esac

echo "📁 Cursor config directory: ${CURSOR_CONFIG_DIR}"

# Check if Cursor is installed
if [ ! -d "${CURSOR_CONFIG_DIR}" ]; then
    echo "⚠️  Cursor config directory not found. Is Cursor installed?"
    echo "   Expected: ${CURSOR_CONFIG_DIR}"
    read -p "Create directory anyway? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p "${CURSOR_CONFIG_DIR}"
    else
        exit 1
    fi
fi

# Ask for integration method
echo ""
echo "🔧 Choose integration method:"
echo "1) SSH Tunnel (Recommended - connects directly to GPU server)"
echo "2) HTTP Bridge (Alternative - local bridge to GPU server)"
echo "3) Show configuration only (manual setup)"
echo ""
read -p "Select option (1-3): " -n 1 -r
echo

case $REPLY in
    1)
        echo "🚇 Setting up SSH tunnel integration..."
        
        # Get GPU server details
        read -p "GPU server IP/hostname: " GPU_SERVER
        read -p "GPU server username [sazzad]: " GPU_USER
        GPU_USER=${GPU_USER:-sazzad}
        read -p "Path to mcp-server on GPU server [/home/sazzad/mcp-server]: " MCP_PATH
        MCP_PATH=${MCP_PATH:-/home/sazzad/mcp-server}
        
        # Create SSH config
        cat > cursor-ssh-config.json << EOF
{
  "mcp.servers": {
    "gpu-llm": {
      "command": "ssh",
      "args": [
        "-t",
        "${GPU_USER}@${GPU_SERVER}",
        "cd ${MCP_PATH} && source .venv/bin/activate && python mcp_server.py"
      ],
      "env": {
        "MODEL_NAME": "Qwen/Qwen3-8B",
        "MAX_NEW_TOKENS": "512",
        "TEMPERATURE": "0.7"
      }
    }
  }
}
EOF
        
        echo "✅ Created cursor-ssh-config.json"
        echo ""
        echo "📋 Next steps:"
        echo "1. Test SSH access: ssh ${GPU_USER}@${GPU_SERVER}"
        echo "2. Add the JSON content to ${CURSOR_CONFIG_DIR}/settings.json"
        echo "3. Restart Cursor"
        ;;
        
    2)
        echo "🌉 Setting up HTTP bridge integration..."
        
        # Install bridge dependencies
        echo "📦 Installing bridge dependencies..."
        pip install aiohttp aiohttp-cors requests
        
        read -p "GPU server URL [http://localhost:8080]: " GPU_URL
        GPU_URL=${GPU_URL:-http://localhost:8080}
        
        # Create HTTP bridge config
        cat > cursor-http-config.json << EOF
{
  "mcp.servers": {
    "gpu-llm": {
      "command": "python",
      "args": ["$(pwd)/cursor-integration/mcp-http-bridge.py"],
      "env": {
        "GPU_SERVER_URL": "${GPU_URL}"
      }
    }
  }
}
EOF
        
        echo "✅ Created cursor-http-config.json"
        echo "✅ HTTP bridge script ready at cursor-integration/mcp-http-bridge.py"
        echo ""
        echo "📋 Next steps:"
        echo "1. Ensure GPU server is running with HTTP endpoint"
        echo "2. Add the JSON content to ${CURSOR_CONFIG_DIR}/settings.json"
        echo "3. Restart Cursor"
        ;;
        
    3)
        echo "📖 Configuration information:"
        echo ""
        echo "Cursor settings location: ${CURSOR_CONFIG_DIR}/settings.json"
        echo ""
        echo "Example configurations are available in:"
        echo "- cursor-ssh-config.json (SSH tunnel method)"
        echo "- cursor-integration/cursor-ssh-config.json"
        echo ""
        echo "Add the configuration to your Cursor settings.json file."
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo ""
echo "💡 Troubleshooting:"
echo "- Check Cursor logs if integration doesn't work"
echo "- Ensure GPU server is running and accessible"
echo "- Test SSH connection manually first"
echo "- Restart Cursor after configuration changes"
