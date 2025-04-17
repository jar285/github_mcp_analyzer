Implementation Requirements: GitHub Repository Analyzer MCP Server
==================================================================

This document outlines the requirements for implementing the GitHub Repository Analyzer MCP server, including dependencies, environment setup, API permissions, and file organization.

Dependencies
------------

The implementation requires the following dependencies:

1.  **MCP Python SDK**: For implementing the Model Context Protocol server
    -   Package: `mcp-python-sdk`
    -   Version: >= 1.5.0
2.  **GitHub API Client**: For interacting with the GitHub API
    -   Package: `pygithub`
    -   Version: >= 2.1.1
3.  **Environment Management**: For secure handling of API keys
    -   Package: `python-dotenv`
    -   Version: >= 1.0.0
4.  **Data Visualization**: For generating activity charts
    -   Package: `matplotlib`
    -   Version: >= 3.7.0
5.  **Data Processing**: For manipulating and analyzing repository data
    -   Standard libraries: `json`, `datetime`, `io`

Environment Setup
-----------------

### Python Environment

-   Python version: 3.10 or higher
-   Virtual environment is recommended for dependency isolation

### GitHub API Access

1.  **GitHub Account**: Required to generate API tokens
2.  **Personal Access Token (Classic)**:
    -   Minimum required scopes: `repo` (Full control of private repositories)
    -   For public repositories only: `public_repo` scope is sufficient

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
GITHUB_TOKEN=your_personal_access_token_here
```

File Structure
--------------

Organize the project with the following file structure:

```
github-repo-analyzer/
├── requirements.txt        # Lists all dependencies
├── .env                    # Contains environment variables (not versioned)
├── .gitignore              # Ignores sensitive files like .env
├── github_tools.py         # Contains the GitHub API client implementation
├── server.py               # Main MCP server implementation
└── README.md               # Project documentation
```

Implementation Guidelines
-------------------------

### GitHub API Client Module (`github_tools.py`)

This module should:

-   Implement a class for GitHub API interactions
-   Handle authentication with the GitHub API
-   Provide methods for each type of data retrieval and analysis
-   Implement proper error handling and rate limit management

### MCP Server Module (`server.py`)

This module should:

-   Create and configure the MCP server
-   Register tools and resources
-   Implement the tool functions using the GitHub API client
-   Handle request processing and response formatting

### Configuration Management

-   Load environment variables securely
-   Never hardcode credentials
-   Implement fallbacks for missing configuration

Security Considerations
-----------------------

1.  **API Token Security**:
    -   Store tokens in environment variables, not in code
    -   Don't log or expose tokens in error messages
    -   Use the minimum required scopes for tokens
2.  **Rate Limiting**:
    -   Implement proper handling of GitHub API rate limits
    -   Add delays or retries when approaching limits
    -   Provide clear messages when rate limits are hit
3.  **Error Handling**:
    -   Don't expose sensitive information in error messages
    -   Provide useful but safe error responses

Best Practices
--------------

1.  **Clean Code**:
    -   Use clear, descriptive names
    -   Include documentation for functions and classes
    -   Implement proper type hints
2.  **Error Handling**:
    -   Use try/except blocks for API calls
    -   Provide meaningful error messages
    -   Don't crash on unexpected inputs
3.  **Performance**:
    -   Minimize API calls where possible
    -   Consider caching frequently accessed data
    -   Be mindful of resource usage for chart generation

## Reference Implementation

A reference copy of the MCP Python SDK is available in the `reference/mcp-python-sdk` directory. This can be used to understand:

- How the MCP protocol is implemented
- Examples of tool and resource definitions
- Error handling patterns
- Protocol communication details

While implementation should follow the specifications in this documentation, the reference code can provide valuable insights into best practices and implementation patterns for the MCP protocol.

Key files to explore in the reference implementation:
- `mcp/server/fastmcp.py`: Contains the FastMCP server implementation
- `mcp/tools.py`: Shows how tools are defined and registered
- `mcp/resources.py`: Demonstrates resource implementation
- Examples in the repository that show complete implementations

Checkpoint List
---------------

-   [ ]  Identify all required dependencies
-   [ ]  Set up Python environment (3.10+)
-   [ ]  Create GitHub account and generate API token
-   [ ]  Set up environment variables for secure token storage
-   [ ]  Plan file structure for the implementation
-   [ ]  Understand GitHub API client requirements
-   [ ]  Understand MCP server implementation requirements
-   [ ]  Consider security best practices
-   [ ]  Plan implementation approach based on best practices