# GitHub Repository Analyzer Demo Guide

This guide provides step-by-step commands to demonstrate the functionality of the GitHub Repository Analyzer during a show and tell session.

## Setup (Before Demo)

1. Make sure your environment is set up correctly:

```bash
# Navigate to the project directory
cd /Users/your-user-name/github_mcp_analyzer

# Activate the virtual environment
source venv/bin/activate

# Verify your GitHub token is set in .env file
cat .env
# Should show: GITHUB_TOKEN="your_github_token_here"
```

## Demo Flow

### 1. Introduction to the Project

Show the project structure and explain its purpose:

```bash
# Show the project structure
ls -la

# Show the README file
cat README.md | more
```

### 2. Demonstrate the GitHub API Client

Run the test client to show the core functionality:

```bash
# Run the test client with a popular repository
python src/test_client.py

# This will:
# 1. Retrieve repository information
# 2. List issues
# 3. Get README content
# 4. Show commit history
# 5. Calculate activity metrics
# 6. Generate an activity chart
```

### 3. Show the Generated Activity Chart

```bash
# Open the generated activity chart
open activity_chart.png
```

### 4. Customize the Analysis

Modify the test client to analyze a different repository:

```bash
# Edit the test_client.py file
nano src/test_client.py

# Change the repo_name variable to a different repository, for example:
# repo_name = "facebook/react"
# or
# repo_name = "microsoft/vscode"
# or
# repo_name = "tensorflow/tensorflow"

# Run the test client with the new repository
python src/test_client.py
```

### 5. Explore the Implementation

Show the core implementation files:

```bash
# Show the GitHub API client implementation
cat src/github_tools.py | more

# Show the MCP server implementation
cat src/server.py | more
```

### 6. Future Specific Features

#### Repository Information

```bash
# Create a quick Python script to show just the repository information
cat > demo_repo_info.py << 'EOF'
from github_tools import GitHubAPIClient
import json

client = GitHubAPIClient()
repo_name = input("Enter a repository name (format: username/repository): ")
repo_info = client.get_repository_info(repo_name)
print(json.dumps(repo_info, indent=2))
EOF

# Run the script
python demo_repo_info.py
```

#### Issue Analysis

```bash
# Create a quick Python script to show issue analysis
cat > demo_issues.py << 'EOF'
from github_tools import GitHubAPIClient
import json

client = GitHubAPIClient()
repo_name = input("Enter a repository name (format: username/repository): ")
state = input("Enter issue state (open, closed, all): ")
max_issues = int(input("Enter maximum number of issues to return: "))
issues = client.get_repository_issues(repo_name, state, max_issues)
print(json.dumps(issues, indent=2))
EOF

# Run the script
python demo_issues.py
```

#### Activity Visualization

```bash
# Create a quick Python script to show activity visualization
cat > demo_chart.py << 'EOF'
from github_tools import GitHubAPIClient
import matplotlib.pyplot as plt

client = GitHubAPIClient()
repo_name = input("Enter a repository name (format: username/repository): ")
days = int(input("Enter number of days to analyze: "))
image_data = client.generate_activity_chart(repo_name, days)

# Save the chart
with open(f"{repo_name.replace('/', '_')}_activity.png", "wb") as f:
    f.write(image_data)
print(f"Chart saved as {repo_name.replace('/', '_')}_activity.png")

# Display the chart
plt.imshow(plt.imread(f"{repo_name.replace('/', '_')}_activity.png"))
plt.axis('off')
plt.show()
EOF

# Run the script
python demo_chart.py
```

## Advanced Demo (If Time Permits)

### Compare Multiple Repositories

```bash
# Create a script to compare multiple repositories
cat > demo_compare.py << 'EOF'
from github_tools import GitHubAPIClient
import json

client = GitHubAPIClient()
repos = input("Enter repository names separated by commas (e.g., facebook/react,angular/angular): ").split(',')
days = int(input("Enter number of days to analyze: "))

results = {}
for repo in repos:
    repo = repo.strip()
    print(f"Analyzing {repo}...")
    results[repo] = client.get_activity_metrics(repo, days)

print("\nComparison Results:")
for repo, metrics in results.items():
    print(f"\n{repo}:")
    print(f"  Commits: {metrics['commit_count']}")
    print(f"  Open Issues: {metrics['open_issues_count']}")
    print(f"  Closed Issues: {metrics['closed_issues_count']}")
    print(f"  Contributors: {metrics['contributor_count']}")
EOF

# Run the script
python demo_compare.py
```

### Show README Content

```bash
# Create a script to display README content
cat > demo_readme.py << 'EOF'
from github_tools import GitHubAPIClient

client = GitHubAPIClient()
repo_name = input("Enter a repository name (format: username/repository): ")
readme = client.get_readme_content(repo_name)
print(f"README for {repo_name}:\n")
print(readme['content'][:1000] + "..." if len(readme['content']) > 1000 else readme['content'])
EOF

# Run the script
python demo_readme.py
```

## Cleanup (After Demo)

```bash
# Deactivate the virtual environment
deactivate

# Remove any temporary demo files
rm -f demo_*.py
```

## Troubleshooting

If you encounter any issues during the demo:

1. **GitHub API Rate Limit**: If you hit the rate limit, wait a few minutes before trying again or use a different token.

2. **Repository Not Found**: Double-check the repository name format (username/repository).

3. **Token Issues**: Verify your GitHub token is correctly set in the `.env` file.

4. **Chart Generation Errors**: Make sure matplotlib is correctly installed and working.

## Example Repositories for Demo

Here are some interesting repositories to use in your demo:

- `tensorflow/tensorflow` - Large, active machine learning library
- `facebook/react` - Popular frontend framework
- `microsoft/vscode` - Well-maintained IDE
- `kubernetes/kubernetes` - Complex cloud infrastructure project
- `flutter/flutter` - Mobile development framework
- `bitcoin/bitcoin` - Cryptocurrency reference implementation
