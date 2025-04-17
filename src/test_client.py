"""Test client for the GitHub Repository Analyzer MCP server.

This script demonstrates how to use the GitHub API client directly to test
the functionality without running the MCP server.
"""

import json
import logging
from github_tools import GitHubAPIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Run a test of the GitHub API client functionality."""
    # Initialize the GitHub API client
    client = GitHubAPIClient()
    
    # Test repository to analyze
    repo_name = "modelcontextprotocol/python-sdk"
    
    logger.info(f"Testing GitHub Repository Analyzer with repository: {repo_name}")
    
    # Test repository information
    logger.info("\n1. Testing repository information...")
    repo_info = client.get_repository_info(repo_name)
    print(json.dumps(repo_info, indent=2))
    
    # Test repository issues
    logger.info("\n2. Testing repository issues...")
    issues = client.get_repository_issues(repo_name, state="open", max_issues=5)
    print(json.dumps(issues, indent=2))
    
    # Test README content
    logger.info("\n3. Testing README content...")
    readme = client.get_readme_content(repo_name)
    print(f"README path: {readme['path']}")
    print(f"README size: {readme['size']} bytes")
    print(f"README content (first 500 chars): {readme['content'][:500]}...")
    
    # Test commit history
    logger.info("\n4. Testing commit history...")
    commits = client.get_commit_history(repo_name, days=7, max_commits=5)
    print(json.dumps(commits, indent=2))
    
    # Test activity metrics
    logger.info("\n5. Testing activity metrics...")
    metrics = client.get_activity_metrics(repo_name, days=30)
    print(json.dumps(metrics, indent=2))
    
    # Test activity chart
    logger.info("\n6. Testing activity chart...")
    chart_data = client.generate_activity_chart(repo_name, days=30)
    print(f"Generated chart of size: {len(chart_data)} bytes")
    
    # Save the chart to a file
    with open("activity_chart.png", "wb") as f:
        f.write(chart_data)
    logger.info("Saved activity chart to activity_chart.png")
    
    logger.info("\nAll tests completed successfully!")


if __name__ == "__main__":
    main()
