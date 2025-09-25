#!/bin/bash
# Setup script for n8n integration with DeenMate MCP Server

echo "🚀 Setting up n8n integration with DeenMate MCP Server"
echo "=" * 60

# Check if n8n is installed
if ! command -v n8n &> /dev/null; then
    echo "📦 Installing n8n..."
    npm install -g n8n
else
    echo "✅ n8n is already installed"
fi

# Check if FastAPI dependencies are installed
echo "📦 Installing HTTP bridge dependencies..."
pip install fastapi uvicorn

# Create environment file for n8n
echo "📝 Creating environment configuration..."
cat > .env.n8n << EOF
# n8n Configuration
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_ENCRYPTION_KEY=your-encryption-key-here
WEBHOOK_URL=http://localhost:5678

# DeenMate MCP Server
MCP_SERVER_URL=http://localhost:8080
MCP_HTTP_BRIDGE_URL=http://localhost:8080

# DeenMate Backend
DEENMATE_BACKEND_URL=http://localhost:3000
DEENMATE_API_TOKEN=your-api-token-here

# Notification Services
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHANNEL_ID=your-channel-id
SLACK_WEBHOOK=your-slack-webhook-url
FCM_SERVER_KEY=your-fcm-server-key

# GitHub Integration
GITHUB_TOKEN=your-github-token
GITHUB_REPO=yourusername/deenmate-app

# Database (if needed)
DATABASE_URL=postgresql://user:password@localhost:5432/deenmate_n8n
EOF

echo "✅ Environment file created: .env.n8n"

# Create n8n startup script
cat > start-n8n.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting n8n with DeenMate configuration..."

# Load environment variables
source .env.n8n

# Export environment variables for n8n
export N8N_HOST
export N8N_PORT
export N8N_PROTOCOL
export N8N_ENCRYPTION_KEY
export WEBHOOK_URL
export MCP_SERVER_URL
export DEENMATE_BACKEND_URL
export DEENMATE_API_TOKEN
export TELEGRAM_BOT_TOKEN
export TELEGRAM_CHANNEL_ID
export SLACK_WEBHOOK
export FCM_SERVER_KEY
export GITHUB_TOKEN
export GITHUB_REPO
export DATABASE_URL

# Start n8n
echo "📡 Starting n8n on http://${N8N_HOST}:${N8N_PORT}"
n8n start
EOF

chmod +x start-n8n.sh

# Create HTTP bridge startup script
cat > start-bridge.sh << 'EOF'
#!/bin/bash
echo "🌉 Starting MCP HTTP Bridge..."

# Load environment variables
source .env.n8n

# Start the HTTP bridge
echo "📡 Starting HTTP bridge on http://localhost:8080"
python mcp_http_bridge.py --host 0.0.0.0 --port 8080
EOF

chmod +x start-bridge.sh

# Create docker-compose file for complete setup
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/workflows
    depends_on:
      - postgres
    networks:
      - deenmate_network

  mcp-bridge:
    build:
      context: .
      dockerfile: Dockerfile.bridge
    ports:
      - "8080:8080"
    environment:
      - MCP_SERVER_URL=http://localhost:8080
    volumes:
      - ../deenmate-integration:/app/deenmate-integration
    networks:
      - deenmate_network

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: deenmate_n8n
      POSTGRES_USER: n8n_user
      POSTGRES_PASSWORD: n8n_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - deenmate_network

volumes:
  n8n_data:
  postgres_data:

networks:
  deenmate_network:
    driver: bridge
EOF

# Create Dockerfile for HTTP bridge
cat > Dockerfile.bridge << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-n8n.txt .
RUN pip install -r requirements-n8n.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run the bridge
CMD ["python", "mcp_http_bridge.py", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Create requirements file for n8n integration
cat > requirements-n8n.txt << 'EOF'
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
aiofiles>=23.2.1
EOF

echo ""
echo "🎉 n8n integration setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env.n8n with your actual tokens and URLs"
echo "2. Start the MCP HTTP bridge: ./start-bridge.sh"
echo "3. Start n8n: ./start-n8n.sh"
echo "4. Import workflows from the workflows/ directory"
echo "5. Configure your DeenMate backend endpoints"
echo ""
echo "🌐 Access URLs:"
echo "- n8n Web UI: http://localhost:5678"
echo "- MCP HTTP Bridge: http://localhost:8080"
echo "- API Documentation: http://localhost:8080/docs"
echo ""
echo "📚 Example workflows available:"
echo "- Daily Islamic content generation"
echo "- Prayer time notifications"
echo "- Automated code generation"
echo ""
echo "💡 Use Docker Compose for complete setup:"
echo "   docker-compose up -d"
