# Deployment Guide

This directory contains deployment configurations and guides for running the MCP server on a remote GPU server.

## Files

- `gpu-server-setup.md` - Complete setup guide for GPU server deployment
- `gpu-client-config.json` - Claude Desktop configuration for remote GPU server
- `local-setup.sh` - Local setup script for development

## Quick Start

1. **Push to Git:**
   ```bash
   git add .
   git commit -m "Initial MCP server implementation"
   git push origin main
   ```

2. **Clone on GPU Server:**
   ```bash
   git clone https://github.com/yourusername/mcp-server.git
   cd mcp-server
   ```

3. **Follow Setup Guide:**
   See `gpu-server-setup.md` for detailed instructions.

## Architecture Options

### Option 1: SSH Tunnel (Recommended)
- MCP server runs on GPU server
- Claude Desktop connects via SSH
- Most secure and performant

### Option 2: HTTP Bridge
- MCP server runs on GPU server with HTTP wrapper
- Claude Desktop uses HTTP client bridge
- More complex but flexible

Choose Option 1 for simplicity and security.
