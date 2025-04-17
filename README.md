# GitHub Repository Analyzer MCP Server

A Model Context Protocol (MCP) server that enables Large Language Models to analyze GitHub repositories in real-time. This server provides tools for retrieving repository information, analyzing issues, accessing documentation, and visualizing activity.

## Features

- **Repository Information Tool**: Retrieve basic metadata about GitHub repositories
- **Issue Analysis Tool**: List and categorize repository issues
- **README Access Resource**: Access repository documentation
- **Commit History Tool**: Analyze recent code changes
- **Activity Analysis Tool**: Calculate repository activity metrics
- **Visualization Tool**: Create visual charts of repository activity

## Prerequisites

- Python 3.10 or higher
- GitHub account and Personal Access Token

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd github-repo-analyzer
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your GitHub API token:

```bash
cp .env.example .env
```

Edit the `.env` file and replace `your_github_token_here` with your actual GitHub Personal Access Token.

## Usage

### Running the Server

To start the server in development mode with the MCP Inspector:

```bash
mcp dev src/server.py
```

This will open a web interface in your browser where you can test the server's tools.

### Registering with Claude Desktop

To register the server with Claude Desktop:

```bash
mcp install src/server.py
```

After registering, restart Claude Desktop. You can then interact with the GitHub Repository Analyzer by asking Claude questions about GitHub repositories.

### Example Prompts for Claude

- "Can you analyze the GitHub repository 'modelcontextprotocol/python-sdk' and tell me about its purpose and activity level?"
- "What are the top 5 open issues in the 'openai/openai-python' repository?"
- "How active has the 'anthropics/anthropic-sdk-python' repository been in the last 30 days?"
- "Please read the README of the 'microsoft/TypeScript' repository and explain its main features."
- "Generate a chart showing the commit activity for 'facebook/react' over the last 60 days."

## Development

### Project Structure

```
github-repo-analyzer/
├── src/
│   ├── github_tools.py  # GitHub API client implementation
│   └── server.py        # MCP server implementation
├── requirements.txt     # Dependencies
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

### Adding New Tools

To add a new tool to the server, follow these steps:

1. Add the necessary functionality to the `GitHubAPIClient` class in `github_tools.py`
2. Register the tool with the MCP server in `server.py` using the `@server.tool` decorator
3. Test the tool using the MCP Inspector

## Testing

To test the server, use the MCP Inspector as described in the Usage section. You can also write unit tests for the GitHub API client functionality.

## Security Considerations

- Never commit your GitHub API token to version control
- Use the minimum required scopes for your GitHub token
- Be mindful of GitHub API rate limits

## License

[MIT License](LICENSE)
