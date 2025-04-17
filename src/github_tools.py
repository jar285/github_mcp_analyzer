"""GitHub API client for the GitHub Repository Analyzer MCP server.

This module provides a class for interacting with the GitHub API to retrieve
repository information, issues, commits, and other data.
"""

import os
import io
import base64
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from github import Github, GithubException, RateLimitExceededException
from github.Repository import Repository
from github.Issue import Issue
from github.ContentFile import ContentFile
from github.Commit import Commit

# Load environment variables
load_dotenv()


class GitHubAPIClient:
    """Client for interacting with the GitHub API.

    This class provides methods for retrieving repository information,
    issues, commits, and other data from GitHub repositories.
    """

    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHub API client.

        Args:
            token: GitHub API token. If not provided, it will be loaded from
                  the GITHUB_TOKEN environment variable.
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError(
                "GitHub API token not provided. Set the GITHUB_TOKEN environment variable."
            )
        self.github = Github(self.token)

    def get_repository(self, repo_name: str) -> Repository:
        """Get a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".

        Returns:
            Repository object.

        Raises:
            ValueError: If the repository name is invalid or the repository doesn't exist.
            RateLimitExceededException: If the GitHub API rate limit is exceeded.
        """
        try:
            if "/" not in repo_name:
                raise ValueError(
                    f"Invalid repository name: {repo_name}. Format should be 'username/repository'."
                )
            return self.github.get_repo(repo_name)
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"Repository not found: {repo_name}")
            if e.status == 403 and "rate limit" in str(e).lower():
                raise RateLimitExceededException(
                    f"GitHub API rate limit exceeded. Please try again later."
                )
            raise

    def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
        """Get information about a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".

        Returns:
            Dictionary containing repository information.
        """
        repo = self.get_repository(repo_name)
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "owner": {
                "login": repo.owner.login,
                "avatar_url": repo.owner.avatar_url,
                "html_url": repo.owner.html_url,
            },
            "html_url": repo.html_url,
            "api_url": repo.url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "open_issues": repo.open_issues_count,
            "language": repo.language,
            "license": repo.license.name if repo.license else None,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
            "visibility": "public" if repo.visibility == "public" else "private",
            "default_branch": repo.default_branch,
            "topics": repo.get_topics(),
        }

    def get_repository_issues(
        self, repo_name: str, state: str = "open", max_issues: int = 30
    ) -> List[Dict[str, Any]]:
        """Get issues from a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".
            state: Issue state ("open", "closed", or "all").
            max_issues: Maximum number of issues to return.

        Returns:
            List of dictionaries containing issue information.
        """
        repo = self.get_repository(repo_name)
        issues = []

        try:
            for issue in repo.get_issues(state=state)[:max_issues]:
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    "author": issue.user.login if issue.user else None,
                    "labels": [label.name for label in issue.labels],
                    "comments": issue.comments,
                    "html_url": issue.html_url,
                    "body": issue.body[:500] + "..." if issue.body and len(issue.body) > 500 else issue.body,
                })
        except GithubException as e:
            if e.status == 403 and "rate limit" in str(e).lower():
                raise RateLimitExceededException(
                    f"GitHub API rate limit exceeded. Please try again later."
                )
            raise

        return issues

    def get_readme_content(self, repo_name: str) -> Dict[str, Any]:
        """Get the README content from a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".

        Returns:
            Dictionary containing README content and metadata.

        Raises:
            ValueError: If the repository doesn't have a README file.
        """
        repo = self.get_repository(repo_name)

        try:
            readme = repo.get_readme()
            content = base64.b64decode(readme.content).decode("utf-8")
            return {
                "content": content,
                "path": readme.path,
                "url": readme.download_url,
                "size": readme.size,
                "name": readme.name,
            }
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"README not found in repository: {repo_name}")
            if e.status == 403 and "rate limit" in str(e).lower():
                raise RateLimitExceededException(
                    f"GitHub API rate limit exceeded. Please try again later."
                )
            raise

    def get_commit_history(
        self, repo_name: str, days: int = 30, max_commits: int = 50
    ) -> List[Dict[str, Any]]:
        """Get commit history from a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".
            days: Number of days to look back.
            max_commits: Maximum number of commits to return.

        Returns:
            List of dictionaries containing commit information.
        """
        repo = self.get_repository(repo_name)
        commits = []
        since_date = datetime.datetime.now() - datetime.timedelta(days=days)

        try:
            for commit in repo.get_commits(since=since_date)[:max_commits]:
                stats = commit.stats
                commits.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "author_login": commit.author.login if commit.author else None,
                    "date": commit.commit.author.date.isoformat(),
                    "html_url": commit.html_url,
                    "stats": {
                        "additions": stats.additions,
                        "deletions": stats.deletions,
                        "total": stats.total,
                    },
                })
        except GithubException as e:
            if e.status == 403 and "rate limit" in str(e).lower():
                raise RateLimitExceededException(
                    f"GitHub API rate limit exceeded. Please try again later."
                )
            raise

        return commits

    def get_activity_metrics(
        self, repo_name: str, days: int = 30
    ) -> Dict[str, Any]:
        """Get activity metrics for a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".
            days: Number of days to look back.

        Returns:
            Dictionary containing activity metrics.
        """
        repo = self.get_repository(repo_name)
        since_date = datetime.datetime.now() - datetime.timedelta(days=days)

        # Get commits
        commits = list(repo.get_commits(since=since_date))
        commit_count = len(commits)

        # Get issues
        open_issues = list(repo.get_issues(state="open", since=since_date))
        open_issues_count = len(open_issues)

        # Get closed issues
        closed_issues = list(repo.get_issues(state="closed", since=since_date))
        closed_issues_count = len(closed_issues)

        # Get pull requests
        open_prs = list(repo.get_pulls(state="open"))
        open_prs_count = len(open_prs)

        # Get merged pull requests
        merged_prs = list(repo.get_pulls(state="closed"))
        merged_prs_count = sum(1 for pr in merged_prs if pr.merged)

        # Get contributors
        contributors = list(repo.get_contributors())
        contributor_count = len(contributors)

        # Get contributor names
        contributor_names = [contributor.login for contributor in contributors[:10]]

        return {
            "commit_count": commit_count,
            "open_issues_count": open_issues_count,
            "closed_issues_count": closed_issues_count,
            "open_prs_count": open_prs_count,
            "merged_prs_count": merged_prs_count,
            "contributor_count": contributor_count,
            "top_contributors": contributor_names,
            "time_period_days": days,
        }

    def generate_activity_chart(
        self, repo_name: str, days: int = 30
    ) -> bytes:
        """Generate an activity chart for a GitHub repository.

        Args:
            repo_name: Repository name in the format "username/repository".
            days: Number of days to look back.

        Returns:
            PNG image as bytes.
        """
        repo = self.get_repository(repo_name)
        since_date = datetime.datetime.now() - datetime.timedelta(days=days)

        # Get commits by date
        commits = repo.get_commits(since=since_date)
        commit_dates = []

        for commit in commits:
            date = commit.commit.author.date.date()
            commit_dates.append(date)

        # Count commits by date
        date_counts = {}
        for date in commit_dates:
            date_str = date.isoformat()
            date_counts[date_str] = date_counts.get(date_str, 0) + 1

        # Create a date range for the chart
        date_range = []
        current_date = since_date.date()
        end_date = datetime.datetime.now().date()

        while current_date <= end_date:
            date_range.append(current_date)
            current_date += datetime.timedelta(days=1)

        # Create data for the chart
        dates = [date.isoformat() for date in date_range]
        counts = [date_counts.get(date, 0) for date in dates]

        # Create the chart
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(dates)), counts, color="#0366d6")
        plt.title(f"Commit Activity for {repo_name} (Last {days} Days)")
        plt.xlabel("Date")
        plt.ylabel("Number of Commits")

        # Format x-axis labels
        if len(dates) > 14:
            # Show every nth label to avoid crowding
            n = len(dates) // 14 + 1
            plt.xticks(
                range(0, len(dates), n),
                [dates[i] for i in range(0, len(dates), n)],
                rotation=45,
                ha="right",
            )
        else:
            plt.xticks(range(len(dates)), dates, rotation=45, ha="right")

        plt.tight_layout()

        # Save the chart to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        return buf.getvalue()
