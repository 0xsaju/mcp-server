# GPU Server Deployment Guide

This guide helps you deploy the MCP server on your GPU server after cloning from Git.

## Prerequisites on GPU Server

- Python 3.8+
- CUDA-compatible GPU with drivers installed
- Git
- Network access to download models

## Deployment Steps

### 1. Clone the Repository

```bash
# Clone your repository (replace with your actual repo URL)
git clone https://github.com/yourusername/mcp-server.git
cd mcp-server
```

### 2. Set Up Python Environment

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy configuration template
cp config.env .env

# Edit configuration for GPU server
nano .env
```

**GPU Server `.env` configuration:**
```bash
# Model Configuration
MODEL_NAME=Qwen/Qwen3-8B
MAX_NEW_TOKENS=512
TEMPERATURE=0.7

# GPU Configuration (adjust as needed)
CUDA_VISIBLE_DEVICES=0
```

### 4. Test the Installation

```bash
# Test server functionality (without loading model)
python test_server.py

# If tests pass, run the full server
python mcp_server.py
```

### 5. Network Access Setup

#### Option A: SSH Tunneling (Recommended for security)

**On your local machine:**
```bash
# Create SSH tunnel to forward MCP server
ssh -L 8080:localhost:8080 username@gpu-server-ip

# Or for stdio-based MCP (more complex)
ssh -t username@gpu-server-ip "cd /path/to/mcp-server && python mcp_server.py"
```

#### Option B: Direct Network Access

**On GPU server, modify `mcp_server.py` for network access:**

Add this network-enabled version to your deployment:

```python
# Add to mcp_server.py after line 544
async def run_network(self, host: str = "0.0.0.0", port: int = 8080):
    """Run MCP server over HTTP for remote access"""
    from aiohttp import web, web_runner
    import aiohttp_cors
    
    async def handle_mcp_request(request):
        data = await request.json()
        response = await self.server.handle_request(data)
        return web.json_response(response)
    
    app = web.Application()
    app.router.add_post('/mcp', handle_mcp_request)
    
    # Enable CORS for cross-origin requests
    cors = aiohttp_cors.setup(app)
    cors.add(app.router.add_resource("/mcp").add_route("POST", handle_mcp_request))
    
    runner = web_runner.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    logger.info(f"🌐 MCP Server running on http://{host}:{port}/mcp")
    
    # Keep server running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        await runner.cleanup()
```

### 6. Firewall Configuration

```bash
# Allow MCP server port (if using network access)
sudo ufw allow 8080
# Or for specific IP only:
# sudo ufw allow from YOUR_LOCAL_IP to any port 8080
```

## Client Configuration

### For Claude Desktop (Local Machine)

**Option A: SSH Tunnel + Local Config**
```json
{
  "mcpServers": {
    "local-llm": {
      "command": "ssh",
      "args": [
        "-t", 
        "username@gpu-server-ip", 
        "cd /path/to/mcp-server && python mcp_server.py"
      ]
    }
  }
}
```

**Option B: HTTP Client (if using network mode)**
Create a local HTTP-to-stdio bridge script.

### For Direct SSH Access

```bash
# Connect to GPU server and run MCP server
ssh username@gpu-server-ip
cd mcp-server
python mcp_server.py
```

## Monitoring and Maintenance

### Check GPU Usage
```bash
# Monitor GPU usage
nvidia-smi -l 1

# Check memory usage
htop
```

### Update Deployment
```bash
# Pull latest changes
git pull origin main

# Restart server
pkill -f mcp_server.py
python mcp_server.py
```

### Logs and Debugging
```bash
# Run with verbose logging
python mcp_server.py 2>&1 | tee mcp-server.log

# Check system resources
df -h  # Disk space
free -h  # Memory
```

## Security Considerations

1. **Use SSH tunneling** instead of direct network access when possible
2. **Configure firewall** to restrict access to MCP server port
3. **Use strong authentication** for SSH access
4. **Keep dependencies updated** regularly
5. **Monitor resource usage** to prevent abuse

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory:**
   - Reduce model size or use smaller model
   - Check `CUDA_VISIBLE_DEVICES` setting
   - Monitor with `nvidia-smi`

2. **Network Connection Issues:**
   - Check firewall settings
   - Verify SSH tunnel is active
   - Test with `telnet gpu-server-ip 8080`

3. **Model Download Issues:**
   - Check internet connectivity on GPU server
   - Verify HuggingFace access
   - Check disk space for model storage

4. **Permission Issues:**
   - Ensure proper file permissions: `chmod +x mcp_server.py`
   - Check Python virtual environment activation
   - Verify write permissions for logs and cache

## Performance Optimization

1. **Model Caching:** First run will download model (~8GB for Qwen3-8B)
2. **GPU Memory:** Monitor usage with `nvidia-smi`
3. **CPU Usage:** Use `htop` to monitor system resources
4. **Network Latency:** SSH tunneling adds ~1-5ms latency per request
