#!/bin/bash
# SSH Tunnel Setup for MCP Server on GPU Server

# Configuration - Update these values
GPU_SERVER_USER="username"
GPU_SERVER_IP="your-gpu-server-ip"
GPU_SERVER_PATH="/path/to/mcp-server"
LOCAL_PORT=8080

echo "🚀 Setting up SSH tunnel for MCP server on GPU server..."

# Function to check if SSH connection works
check_ssh() {
    echo "🔍 Testing SSH connection..."
    if ssh -o ConnectTimeout=5 -o BatchMode=yes "${GPU_SERVER_USER}@${GPU_SERVER_IP}" exit 2>/dev/null; then
        echo "✅ SSH connection successful"
        return 0
    else
        echo "❌ SSH connection failed"
        echo "Please check:"
        echo "  - GPU server IP: ${GPU_SERVER_IP}"
        echo "  - Username: ${GPU_SERVER_USER}"
        echo "  - SSH key authentication"
        return 1
    fi
}

# Function to create SSH tunnel
create_tunnel() {
    echo "🔗 Creating SSH tunnel on port ${LOCAL_PORT}..."
    ssh -L ${LOCAL_PORT}:localhost:${LOCAL_PORT} \
        -N \
        -f \
        "${GPU_SERVER_USER}@${GPU_SERVER_IP}"
    
    if [ $? -eq 0 ]; then
        echo "✅ SSH tunnel created successfully"
        echo "   Local port ${LOCAL_PORT} -> GPU server port ${LOCAL_PORT}"
    else
        echo "❌ Failed to create SSH tunnel"
        return 1
    fi
}

# Function to start MCP server on GPU server
start_mcp_server() {
    echo "🤖 Starting MCP server on GPU server..."
    ssh -t "${GPU_SERVER_USER}@${GPU_SERVER_IP}" \
        "cd ${GPU_SERVER_PATH} && source venv/bin/activate && python mcp_server.py"
}

# Function to kill existing tunnels
kill_tunnels() {
    echo "🧹 Killing existing SSH tunnels on port ${LOCAL_PORT}..."
    pkill -f "ssh.*${LOCAL_PORT}:localhost:${LOCAL_PORT}"
}

# Main menu
case "${1:-menu}" in
    "setup")
        check_ssh && create_tunnel
        ;;
    "start")
        start_mcp_server
        ;;
    "tunnel")
        kill_tunnels
        check_ssh && create_tunnel
        ;;
    "kill")
        kill_tunnels
        echo "✅ SSH tunnels killed"
        ;;
    "status")
        echo "🔍 Checking tunnel status..."
        if pgrep -f "ssh.*${LOCAL_PORT}:localhost:${LOCAL_PORT}" > /dev/null; then
            echo "✅ SSH tunnel is running"
        else
            echo "❌ No SSH tunnel found"
        fi
        ;;
    "menu"|*)
        echo "MCP Server SSH Tunnel Manager"
        echo "=============================="
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  setup   - Test SSH and create tunnel"
        echo "  start   - Start MCP server on GPU server (interactive)"
        echo "  tunnel  - Create/recreate SSH tunnel only"
        echo "  kill    - Kill existing SSH tunnels"
        echo "  status  - Check tunnel status"
        echo ""
        echo "Configuration:"
        echo "  GPU Server: ${GPU_SERVER_USER}@${GPU_SERVER_IP}"
        echo "  Remote Path: ${GPU_SERVER_PATH}"
        echo "  Local Port: ${LOCAL_PORT}"
        echo ""
        echo "Edit this script to update configuration values."
        ;;
esac
