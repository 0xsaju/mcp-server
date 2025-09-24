# MCP Server with Local LLM

A Model Context Protocol (MCP) server that integrates with your local Large Language Model, providing tools and resources that can be used by MCP-compatible clients like Claude Desktop, IDEs, and other AI assistants.

## Features

- **Local LLM Integration**: Uses your local language model (default: Qwen3-8B) for all operations
- **MCP-Compatible**: Implements the Model Context Protocol specification
- **Multiple Tools**: Provides various tools for different use cases
- **Resource Access**: Exposes model information and conversation history
- **Memory Efficient**: Uses 4-bit quantization for optimal performance

## Available Tools

### 1. `chat_with_llm`
Basic chat interface with the local LLM.

**Parameters:**
- `message` (required): The message to send to the LLM
- `system_prompt` (optional): System prompt to guide behavior
- `temperature` (optional): Temperature for generation (0-1, default: 0.7)
- `max_tokens` (optional): Maximum tokens to generate (default: 512)

### 2. `analyze_code`
Analyze and review code using the local LLM.

**Parameters:**
- `code` (required): The code to analyze
- `language` (optional): Programming language
- `analysis_type` (optional): Type of analysis (review, explain, optimize, debug)

### 3. `generate_text`
Generate text content in various styles and lengths.

**Parameters:**
- `prompt` (required): The prompt for text generation
- `style` (optional): Writing style (formal, casual, technical, creative)
- `length` (optional): Desired length (short, medium, long)

### 4. `translate_text`
Translate text between languages.

**Parameters:**
- `text` (required): Text to translate
- `target_language` (required): Target language
- `source_language` (optional): Source language (auto-detect if not provided)

### 5. `summarize_content`
Summarize content in different formats.

**Parameters:**
- `content` (required): Content to summarize
- `summary_type` (optional): Type of summary (brief, detailed, bullet_points)
- `max_length` (optional): Maximum length in words (default: 150)

## Available Resources

### 1. `llm://model/info`
Information about the loaded local LLM model.

### 2. `llm://conversations/history`
History of conversations with the LLM.

### 3. `llm://system/status`
Current system status and resource usage.

## Installation

1. **Clone or download** this repository to your local machine.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (create a `.env` file):
   ```bash
   MODEL_NAME=Qwen/Qwen3-8B
   MAX_NEW_TOKENS=512
   TEMPERATURE=0.7
   ```

4. **Ensure you have sufficient hardware:**
   - GPU with at least 8GB VRAM (recommended)
   - 16GB+ system RAM
   - CUDA-compatible GPU (for optimal performance)

## Usage

### Running the Server

1. **Start the MCP server:**
   ```bash
   python mcp_server.py
   ```

2. **The server will:**
   - Load the specified model (Qwen3-8B by default)
   - Initialize the MCP server
   - Wait for JSON-RPC requests via stdin/stdout

### Integrating with Claude Desktop

To use this server with Claude Desktop, add it to your MCP configuration:

1. **Create or edit** your Claude Desktop MCP configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the server configuration:**
   ```json
   {
     "mcpServers": {
       "local-llm": {
         "command": "python",
         "args": ["/Users/sazzad/Documents/mcp-server/mcp_server.py"],
         "env": {
           "MODEL_NAME": "Qwen/Qwen3-8B"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to load the new server.

### Example Usage in Claude Desktop

Once configured, you can use the tools in Claude Desktop:

```
Please use the local LLM to analyze this Python code:
```

Claude will then use the `analyze_code` tool to get analysis from your local LLM.

## Configuration

### Environment Variables

- `MODEL_NAME`: HuggingFace model name (default: "Qwen/Qwen3-8B")
- `MAX_NEW_TOKENS`: Maximum tokens to generate (default: 512)
- `TEMPERATURE`: Default temperature for generation (default: 0.7)

### Supported Models

This server works with most HuggingFace transformers models that support:
- Chat templates
- 4-bit quantization via BitsAndBytesConfig
- Causal language modeling

Popular choices:
- `Qwen/Qwen3-8B` (default)
- `microsoft/DialoGPT-medium`
- `meta-llama/Llama-2-7b-chat-hf`
- `mistralai/Mistral-7B-Instruct-v0.1`

## Hardware Requirements

### Minimum Requirements
- 8GB RAM
- 4GB GPU VRAM (with 4-bit quantization)
- 10GB disk space (for model storage)

### Recommended Requirements
- 16GB+ RAM
- 8GB+ GPU VRAM
- CUDA-compatible GPU
- SSD storage for faster model loading

## Troubleshooting

### Common Issues

1. **Out of Memory Error:**
   - Reduce `MAX_NEW_TOKENS`
   - Use a smaller model
   - Ensure 4-bit quantization is working

2. **Model Loading Fails:**
   - Check internet connection for initial download
   - Verify model name is correct
   - Ensure sufficient disk space

3. **CUDA Errors:**
   - Update CUDA drivers
   - Check GPU compatibility
   - Fall back to CPU if needed

### Performance Optimization

1. **Use GPU acceleration:**
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Enable Flash Attention** (if compatible):
   ```bash
   pip install flash-attn
   ```

3. **Adjust batch size and sequence length** based on your hardware.

## Development

### Project Structure
```
mcp-server/
├── mcp_server.py          # Main MCP server implementation
├── mcp-server.py          # Legacy FastAPI server (keep for reference)
├── requirements.txt       # Python dependencies
├── mcp/                   # MCP protocol implementation
│   ├── __init__.py
│   ├── server.py         # MCP server base
│   └── types.py          # MCP protocol types
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration
3. Open an issue on GitHub
