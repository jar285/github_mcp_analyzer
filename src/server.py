"""GitHub Repository Analyzer MCP Server.

This module implements an MCP server that provides tools for analyzing GitHub repositories,
including repository information, issues, commits, and activity metrics.
"""

import os
import logging
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.fastmcp.resources.types import BinaryResource, TextResource

from github_tools import GitHubAPIClient, RateLimitExceededException

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize the GitHub API client
github_client = GitHubAPIClient()

# Create the MCP server
server = FastMCP(
    name="GitHub Repository Analyzer",
    instructions="""This MCP server provides tools for analyzing GitHub repositories.
    You can retrieve repository information, issues, commits, and activity metrics.
    All repository names should be in the format 'username/repository'.
    """
)


@server.tool(
    name="get_repository_info",
    description="Retrieve basic metadata about a GitHub repository."
)
async def get_repository_info(repo_name: str, context: Context) -> Dict[str, Any]:
    """Retrieve basic metadata about a GitHub repository.
    
    Args:
        repo_name: Repository name in the format "username/repository".
        
    Returns:
        Dictionary containing repository information including name, description,
        star count, fork count, and other metadata.
    """
    try:
        await context.info(f"Retrieving repository information for {repo_name}")
        return github_client.get_repository_info(repo_name)
    except ValueError as e:
        await context.error(f"Error: {str(e)}")
        raise
    except RateLimitExceededException as e:
        await context.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        await context.error(f"Unexpected error: {str(e)}")
        raise


@server.tool(
    name="get_repository_issues",
    description="List and categorize repository issues."
)
async def get_repository_issues(
    repo_name: str,
    context: Context,
    state: str = "open",
    max_issues: int = 30
) -> List[Dict[str, Any]]:
    """List and categorize repository issues.
    
    Args:
        repo_name: Repository name in the format "username/repository".
        state: Issue state ("open", "closed", or "all").
        max_issues: Maximum number of issues to return.
        
    Returns:
        List of dictionaries containing issue information.
    """
    try:
        await context.info(f"Retrieving {state} issues for {repo_name} (max: {max_issues})")
        return github_client.get_repository_issues(repo_name, state, max_issues)
    except ValueError as e:
        await context.error(f"Error: {str(e)}")
        raise
    except RateLimitExceededException as e:
        await context.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        await context.error(f"Unexpected error: {str(e)}")
        raise


@server.resource("readme://{repo_name}")
async def get_readme(repo_name: str) -> str:
    """Get the README content from a GitHub repository.
    
    Args:
        repo_name: Repository name in the format "username/repository".
        
    Returns:
        README content as text.
    """
    try:
        readme_data = github_client.get_readme_content(repo_name)
        return readme_data["content"]
    except ValueError as e:
        raise ValueError(f"Error accessing README: {str(e)}")
    except RateLimitExceededException as e:
        raise ValueError(f"GitHub API rate limit exceeded: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")


@server.tool(
    name="get_commit_history",
    description="Analyze recent code changes in a repository."
)
async def get_commit_history(
    repo_name: str,
    context: Context,
    days: int = 30,
    max_commits: int = 50
) -> List[Dict[str, Any]]:
    """Analyze recent code changes in a repository.
    
    Args:
        repo_name: Repository name in the format "username/repository".
        days: Number of days to look back.
        max_commits: Maximum number of commits to return.
        
    Returns:
        List of dictionaries containing commit information.
    """
    try:
        await context.info(f"Retrieving commit history for {repo_name} (last {days} days, max: {max_commits})")
        return github_client.get_commit_history(repo_name, days, max_commits)
    except ValueError as e:
        await context.error(f"Error: {str(e)}")
        raise
    except RateLimitExceededException as e:
        await context.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        await context.error(f"Unexpected error: {str(e)}")
        raise


@server.tool(
    name="get_activity_metrics",
    description="Calculate repository activity metrics."
)
async def get_activity_metrics(
    repo_name: str,
    context: Context,
    days: int = 30
) -> Dict[str, Any]:
    """Calculate repository activity metrics.
    
    Args:
        repo_name: Repository name in the format "username/repository".
        days: Number of days to look back.
        
    Returns:
        Dictionary containing activity metrics.
    """
    try:
        await context.info(f"Calculating activity metrics for {repo_name} (last {days} days)")
        return github_client.get_activity_metrics(repo_name, days)
    except ValueError as e:
        await context.error(f"Error: {str(e)}")
        raise
    except RateLimitExceededException as e:
        await context.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        await context.error(f"Unexpected error: {str(e)}")
        raise


@server.tool(
    name="generate_activity_chart",
    description="Create a visual chart of repository commit activity."
)
async def generate_activity_chart(
    repo_name: str,
    context: Context,
    days: int = 30
) -> BinaryResource:
    """Create a visual chart of repository commit activity.
    
    Args:
        repo_name: Repository name in the format "username/repository".
        days: Number of days to look back.
        
    Returns:
        PNG image showing commit activity over time.
    """
    try:
        await context.info(f"Generating activity chart for {repo_name} (last {days} days)")
        image_data = github_client.generate_activity_chart(repo_name, days)
        
        # Create a binary resource with the image data
        return BinaryResource(
            uri=f"chart://{repo_name}/activity",
            data=image_data,
            mime_type="image/png",
            description=f"Commit activity chart for {repo_name} (last {days} days)"
        )
    except ValueError as e:
        await context.error(f"Error: {str(e)}")
        raise
    except RateLimitExceededException as e:
        await context.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        await context.error(f"Unexpected error: {str(e)}")
        raise


if __name__ == "__main__":
    import argparse
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from starlette.responses import HTMLResponse
    
    parser = argparse.ArgumentParser(description="GitHub Repository Analyzer MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        print(f"Starting GitHub Repository Analyzer MCP Server on http://{args.host}:{args.port}")
    
    # Create a landing page for web browsers
    async def landing_page(request):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GitHub Repository Analyzer MCP Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #333; }}
                h2 {{ color: #444; }}
                pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .tool {{ margin-bottom: 20px; border-left: 4px solid #0366d6; padding-left: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>GitHub Repository Analyzer MCP Server</h1>
                <p>This server implements the Model Context Protocol (MCP) for analyzing GitHub repositories.</p>
                <p>Server is running at: <code>http://{args.host}:{args.port}</code></p>
                
                <h2>Available Tools</h2>
                <div class="tool">
                    <h3>get_repository_info</h3>
                    <p>Retrieve basic metadata about a GitHub repository.</p>
                </div>
                <div class="tool">
                    <h3>get_repository_issues</h3>
                    <p>List and categorize repository issues.</p>
                </div>
                <div class="tool">
                    <h3>get_commit_history</h3>
                    <p>Analyze recent code changes in a repository.</p>
                </div>
                <div class="tool">
                    <h3>get_activity_metrics</h3>
                    <p>Calculate repository activity metrics.</p>
                </div>
                <div class="tool">
                    <h3>generate_activity_chart</h3>
                    <p>Create a visual chart of repository commit activity.</p>
                </div>
                
                <h2>Available Resources</h2>
                <div class="tool">
                    <h3>readme://{{{{repo_name}}}}</h3>
                    <p>Get the README content from a GitHub repository.</p>
                </div>
                
                <h2>Note</h2>
                <p>This server is designed to be used with MCP clients. Direct browser access to MCP endpoints may not work as expected.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(html_content)
    
    # Create a Starlette app and mount the MCP server
    app = Starlette(
        routes=[
            Route('/', endpoint=landing_page),
            Mount('/mcp', app=server.sse_app()),
        ]
    )
    
    # Run the server with uvicorn
    uvicorn.run(app, host=args.host, port=args.port)
