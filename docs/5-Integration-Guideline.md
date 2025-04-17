Integration Guidelines: GitHub Repository Analyzer MCP Server
=============================================================

This document provides guidelines for integrating the GitHub Repository Analyzer MCP server with LLM clients, particularly Claude Desktop. It covers registration procedures, example prompts, and expected input/output patterns.

Registering with Claude Desktop
-------------------------------

### Installation Prerequisites

Before registering the server with Claude Desktop, ensure:

1.  Claude Desktop is installed on your computer
2.  The MCP Python SDK is installed: `pip install mcp-python-sdk`
3.  Your GitHub Repository Analyzer server is fully implemented and working

### Registration Steps

1.  Open a terminal or command prompt
2.  Navigate to your project directory
3.  Run the following command:

    ```
    mcp install server.py
    ```

4.  You should see a confirmation message that the server was registered
5.  Restart Claude Desktop if it was already running

### Verifying Registration

1.  Open Claude Desktop
2.  Type "What tools do you have access to?"
3.  Claude should list the GitHub Repository Analyzer among available tools

Example Prompts
---------------

Here are example prompts to interact with the GitHub Repository Analyzer through Claude Desktop:

### Basic Repository Information

```
Can you analyze the GitHub repository "modelcontextprotocol/python-sdk" and tell me about its purpose, activity level, and main features?
```

Expected behavior: Claude should use the repository information tool to fetch basic data about the repository and provide a summary.

### Issue Analysis

```
What are the top 5 open issues in the "openai/openai-python" repository? Summarize the main problems being addressed.
```

Expected behavior: Claude should use the issue analysis tool to list current open issues and provide a brief analysis of common themes or priorities.

### Repository Activity

```
How active has the "anthropics/anthropic-sdk-python" repository been in the last 30 days? Who are the main contributors?
```

Expected behavior: Claude should use the activity analysis tool to gather statistics about recent activity and identify key contributors.

### Documentation Review

```
Please read the README of the "microsoft/TypeScript" repository and explain its main features and how to get started with it.
```

Expected behavior: Claude should access the README content and provide a summary of the key points.

### Visualization Request

```
Generate a chart showing the commit activity for "facebook/react" over the last 60 days and explain what patterns you observe.
```

Expected behavior: Claude should generate and display an activity chart, then analyze visible patterns.

### Comprehensive Analysis

```
I'm considering contributing to "langchain-ai/langchain". Can you analyze this repository and tell me about its:
1. Overall activity and health
2. Current open issues I might help with
3. Recent development focus based on commits
4. How to get started based on the README
```

Expected behavior: Claude should use multiple tools to provide a comprehensive analysis of the repository.

Input and Output Patterns
-------------------------

### Repository Information Tool

**Input:**

-   Repository name in the format "owner/repo"

**Expected Output:**

-   JSON-formatted repository metadata

### Issue Analysis Tool

**Input:**

-   Repository name in the format "owner/repo"
-   Optional state filter (open, closed, all)
-   Optional maximum number of issues

**Expected Output:**

-   JSON list of issues with metadata

### README Access Resource

**Input:**

-   Repository name in the format "owner/repo"

**Expected Output:**

-   The raw content of the README file

### Commit History Tool

**Input:**

-   Repository name in the format "owner/repo"
-   Optional number of days to look back
-   Optional maximum number of commits

**Expected Output:**

-   JSON list of commits with metadata

### Activity Analysis Tool

**Input:**

-   Repository name in the format "owner/repo"
-   Optional time period in days

**Expected Output:**

-   JSON object with activity metrics

### Visualization Tool

**Input:**

-   Repository name in the format "owner/repo"
-   Optional time period in days

**Expected Output:**

-   Image object showing the activity chart

Error Handling Expectations
---------------------------

When errors occur, Claude should:

1.  Clearly communicate that there was an issue
2.  Explain the nature of the problem (if known)
3.  Suggest alternative approaches when appropriate

Example error scenarios:

-   Repository doesn't exist
-   Rate limiting by GitHub API
-   Authentication issues
-   Timeout due to large repositories

Checkpoint List
---------------

-   [ ]  Understand the process for registering the MCP server with Claude Desktop
-   [ ]  Review example prompts for interacting with the GitHub Repository Analyzer
-   [ ]  Understand the expected input patterns for each tool
-   [ ]  Understand the expected output patterns from each tool
-   [ ]  Know how Claude should handle and communicate errors
-   [ ]  Prepare to test integration with sample prompts