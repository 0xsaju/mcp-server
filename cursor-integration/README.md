# Cursor IDE Integration with MCP Server

This guide helps you integrate your local LLM MCP server with Cursor IDE.

## 🎯 Integration Options

### Option 1: SSH Tunnel Integration (Recommended)
Connect Cursor to your GPU server via SSH tunnel.

### Option 2: HTTP Bridge Integration  
Run an HTTP-to-MCP bridge locally.

### Option 3: Local Installation
Install the MCP server locally (CPU-only mode).

## 🔧 Setup Instructions

### Option 1: SSH Tunnel Integration

**Step 1: Configure SSH Tunnel**

```bash
# On your local machine (where Cursor runs)
ssh -L 8080:localhost:8080 -N sazzad@your-gpu-server-ip &

# Or use the tunnel script
./deploy/ssh-tunnel-setup.sh setup
```

**Step 2: Create Cursor MCP Configuration**

Cursor uses similar configuration to Claude Desktop. Create a configuration file:

**macOS:** `~/Library/Application Support/Cursor/User/settings.json`
**Windows:** `%APPDATA%\Cursor\User\settings.json`
**Linux:** `~/.config/Cursor/User/settings.json`

Add this to your Cursor settings:

```json
{
  "mcp.servers": {
    "local-llm": {
      "command": "ssh",
      "args": [
        "-t",
        "sazzad@your-gpu-server-ip", 
        "cd /home/sazzad/mcp-server && source .venv/bin/activate && python mcp_server.py"
      ],
      "env": {
        "MODEL_NAME": "Qwen/Qwen3-8B"
      }
    }
  }
}
```

### Option 2: HTTP Bridge Integration

**Step 1: Create HTTP Bridge**

This runs locally and forwards requests to your GPU server via HTTP.

**Step 2: Install Bridge Dependencies**

```bash
pip install aiohttp aiohttp-cors requests
```

**Step 3: Configure Cursor**

```json
{
  "mcp.servers": {
    "local-llm": {
      "command": "python",
      "args": ["/path/to/mcp-http-bridge.py"],
      "env": {
        "GPU_SERVER_URL": "http://your-gpu-server-ip:8080"
      }
    }
  }
}
```

### Option 3: Local CPU Installation

For testing or if you want CPU-only mode:

```json
{
  "mcp.servers": {
    "local-llm": {
      "command": "python",
      "args": ["/Users/your-username/mcp-server/mcp_server.py"],
      "env": {
        "MODEL_NAME": "microsoft/DialoGPT-small"
      }
    }
  }
}
```

## 🧪 Testing Integration

1. **Restart Cursor** after adding configuration
2. **Open Command Palette** (Cmd/Ctrl + Shift + P)
3. **Look for MCP commands** or check if tools appear
4. **Test with a simple query**

## 🔍 Troubleshooting

### Common Issues

1. **SSH Connection Issues**
   - Test SSH access: `ssh sazzad@your-gpu-server-ip`
   - Check SSH key authentication
   - Verify server is reachable

2. **Configuration Not Loading**
   - Check JSON syntax in settings.json
   - Restart Cursor completely
   - Check Cursor logs for errors

3. **MCP Server Not Responding**
   - Ensure server is running on GPU machine
   - Check if model is loaded successfully
   - Verify network connectivity

### Debug Commands

```bash
# Test SSH connection
ssh -v sazzad@your-gpu-server-ip

# Test MCP server directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | ssh sazzad@your-gpu-server-ip "cd mcp-server && source .venv/bin/activate && python mcp_server.py"

# Check Cursor logs (location varies by OS)
# macOS: ~/Library/Logs/Cursor/
# Windows: %APPDATA%\Cursor\logs\
# Linux: ~/.config/Cursor/logs/
```

## 🎯 Expected Behavior

Once configured correctly, you should be able to:

- ✅ Access your local LLM through Cursor's chat interface
- ✅ Use code analysis tools powered by your GPU server
- ✅ Generate text and translations
- ✅ Summarize content using your Qwen3-8B model

## 🔧 Performance Notes

- **SSH Tunnel**: Adds ~1-5ms latency per request
- **HTTP Bridge**: Slightly higher latency but more robust
- **Local CPU**: No network latency but much slower inference

Choose the option that best fits your workflow and performance needs!
