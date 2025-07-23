# Template Agent

A web search assistant that uses AI agents to perform intelligent web searches and provide helpful responses.

## Features

- **Intelligent Web Search**: Uses AI agents to perform targeted web searches
- **Translation Support**: Automatically translates non-English queries to English
- **Conversation History**: Maintains session history for contextual responses
- **Simple CLI Interface**: Clean command-line interface for easy interaction
- **Error Handling**: Graceful handling of API errors and network issues

## Quick Start

### Prerequisites

- Python 3.9-3.12
- OpenAI API key (or compatible API endpoint)
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lchen4-godaddy/agent-template-openai-agents-sdk.git
   cd agent-template-openai-agents-sdk
   ```

2. **Set up virtual environment and install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API key and configuration
   ```

4. **Run the web search assistant**
   ```bash
   # Option 1: Direct Python command
   python -m src.main
   
   # Option 2: Using the shell script (recommended)
   ./run.sh
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GOCODE_API_TOKEN='your-api-key'
OPENAI_BASE_URL=https://caas-gocode-prod.caas-prod.prod.onkatana.net
OPENAI_API_KEY=${GOCODE_API_TOKEN}
OPENAI_AGENTS_DISABLE_TRACING=1
OPENAI_LOGGING_LEVEL=ERROR
AGENTS_LOGGING_LEVEL=ERROR
```

### API Key Security

- The `.env` file is automatically ignored by git
- Never commit your actual API keys
- Use environment variables for sensitive data

## Project Structure

```
src/
├── agents/                    # Agent definitions
│   └── web_search_agent.py   # Web search agent with translation
├── main.py                   # Entry point
└── manager.py                # Session management and CLI interface
```

## Usage

1. **Start the assistant**: Run `python -m src.main`
2. **Ask questions**: Type your search queries in natural language
3. **Get responses**: The agent will search the web and provide helpful answers
4. **Exit**: Type "exit" to quit the assistant

## Dependencies

- **openai-agents**: OpenAI Agents SDK for AI-powered web search
- **openai**: OpenAI client for advanced agent building
- **python-dotenv**: Environment variable management

## Development

This project uses a minimal configuration focused on runtime dependencies. For development, you can add linting and testing tools as needed.

## License

MIT License