# AI Data Analysis & Visualization Assistant

An intelligent multi-agent system for e-commerce data analysis and QuickSight visualization. This system uses specialized AI agents to process natural language queries, analyze data, and generate interactive dashboards.

## 🚀 Features

- **Multi-Agent Architecture**: Coordinated agents for data insights, visualization planning, and QuickSight integration
- **Natural Language Queries**: Ask questions about your e-commerce data in plain English
- **Intelligent Data Analysis**: Automated query planning and SQL generation
- **QuickSight Integration**: Generate and deploy interactive dashboards to AWS QuickSight
- **Real-time Visualization**: Create charts, graphs, and analytics from your data
- **Web Interface**: User-friendly Streamlit UI with chat interface
- **Memory System**: Maintains context across agent interactions for complex workflows

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Coordinator     │───▶│ Data Insights    │───▶│ Knowledge Base  │
│ Agent           │    │ Agent            │    │ (SQL + Results) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Visual          │───▶│ Visual Planner   │───▶│ QuickSight      │
│ Coordinator     │    │ Agent            │    │ Analysis        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.9-3.12**
- **AWS Account** with QuickSight access
- **OpenAI API Key** (or compatible API endpoint)
- **AWS CLI** configured with appropriate permissions
- **[uv](https://docs.astral.sh/uv/)** package manager

## 🛠️ Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd summer_intern_project
```

### 2. AWS CLI Setup

Install and configure AWS CLI with QuickSight permissions:

```bash
# Install AWS CLI (if not already installed)
# macOS
brew install awscli

# Linux/Windows - see AWS documentation
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and output format
```

**Required AWS Permissions:**
- `quicksight:CreateAnalysis`
- `quicksight:CreateDashboard`
- `quicksight:UpdateAnalysisPermissions`
- `quicksight:UpdateDashboardPermissions`
- `quicksight:ListAnalyses`
- `quicksight:DescribeAnalysis`

### 3. Virtual Environment Setup

```bash
# Create and activate virtual environment using uv
uv sync

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows
```

### 4. Environment Configuration

Create a `.env` file with required environment variables:

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional: custom endpoint

# AWS Configuration (if not using AWS CLI default profile)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-east-1

# Agent Configuration
OPENAI_AGENTS_DISABLE_TRACING=1
OPENAI_LOGGING_LEVEL=ERROR
AGENTS_LOGGING_LEVEL=ERROR
```

### 5. Install Dependencies

```bash
# Install all project dependencies
uv sync

# Verify installation
python -c "import streamlit, agents, boto3; print('✅ All dependencies installed')"
```

## 🚀 Running the Application

### Option 1: Streamlit Web Interface (Recommended)

```bash
# Run the web interface
./run_ui.sh

# OR manually:
streamlit run src/app.py
```

Access the application at `http://localhost:8501`

### Option 2: Command Line Interface

```bash
# Run CLI version
./run.sh

# OR manually:
python -m src.main
```

### Option 3: Direct Python Execution

```bash
# Run specific components
python src/main.py                    # CLI interface
python -m streamlit run src/app.py    # Web interface
```

## 💡 Usage Examples

### Data Analysis Queries

```
"What are the top-selling products this month?"
"Show me revenue by product category"
"Compare sales performance across different channels"
```

### Visualization Requests

```
"Create a bar chart showing revenue by category"
"I want to visualize customer demographics"
"Create an analysis for product performance"
```

### QuickSight Integration

```
"Deploy this visualization to QuickSight"
```

## 📁 Project Structure

```
src/
├── agents/                           # AI Agent definitions
│   ├── coordinator_agent.py         # Main routing agent
│   ├── data_insights_agent.py       # Data analysis agent
│   ├── visual_coordinator_agent.py  # Visualization workflow coordinator
│   └── tools/                       # Agent tools and utilities
│       ├── insights_planner.py      # Query planning
│       ├── visual_planner.py        # Visualization planning
│       ├── visual_creator.py        # JSON definition generation
│       ├── quicksight_agent.py      # QuickSight operations
│       └── sql_analyzer.py          # SQL query analysis
├── memory/                          # Shared memory system
│   └── agent_memory.py             # Context management
├── services/                        # External service integrations
│   └── quicksight_service.py       # AWS QuickSight API
├── app.py                          # Streamlit web interface
├── main.py                         # CLI entry point
└── manager.py                      # Session management
```

## 🔧 Configuration

### Agent Memory System

The system uses a centralized memory store (`AgentMemory`) to maintain context across agent interactions:

- **Data Insights Context**: Query plans, SQL queries, and results
- **Visualization Plans**: Chart configurations and field mappings
- **QuickSight Definitions**: Complete JSON definitions for dashboard creation
- **Analysis Metadata**: QuickSight analysis names, IDs, and permissions

### QuickSight Integration

Configure your AWS QuickSight setup:

1. **Dataset Configuration**: Update dataset identifiers in `src/services/quicksight_service.py`
2. **Permissions**: Modify permission templates in QuickSight service functions
3. **Account ID**: Update AWS account ID in service configurations

## 🐛 Debugging

### Common Issues

**AWS Permissions**: Ensure your AWS credentials have QuickSight access
```bash
aws quicksight describe-user --aws-account-id YOUR-ACCOUNT-ID --namespace default --user-name YOUR-USERNAME
```

**Environment Variables**: Verify all required variables are set
```bash
python -c "import os; print('✅ OpenAI API Key:', bool(os.getenv('OPENAI_API_KEY')))"
```

**Dependencies**: Reinstall if imports fail
```bash
uv sync --reinstall
```

## 🧪 Testing

```bash
# Test QuickSight connectivity
python test_quicksight.py

# Test OpenAI integration
python test_openai.py

# Run specific agent tests
python -c "from src.agents.coordinator_agent import coordinator_agent; print('✅ Agents loaded')"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:

1. Check the terminal output for agent processing logs
2. Verify AWS and OpenAI API configurations  
3. Review the project structure and agent interactions
4. Create an issue with detailed error information

