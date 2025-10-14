# GitHub MCP Server

A FastMCP server that provides access to GitHub repositories and data for Poke integration.

## 🚀 Features

- **get_repos**: Get repositories for a GitHub user
- **get_issues**: Get issues for a repository
- **get_pull_requests**: Get pull requests for a repository
- **search_code**: Search for code on GitHub

## 🔑 GitHub Token Setup

This server requires a GitHub personal access token for API access:

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Generate a new token with `repo` and `public_repo` scopes
3. Set the environment variable: `export GITHUB_TOKEN=your_token_here`

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token
export GITHUB_TOKEN=your_token_here

# Run the server
python src/server.py
```

## 🚢 Deployment

### Option 1: One-Click Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deployment

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your forked repository
5. Set environment variable `GITHUB_TOKEN`
6. Deploy!

Your server will be available at `https://github-mcp.onrender.com/mcp`

## 🎯 Poke Integration

1. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
2. Add the MCP URL: `https://github-mcp.onrender.com/mcp`
3. Give it a name like "GitHub"
4. Test with: "Tell the subagent to use the GitHub integration's get_repos tool"

## 🔧 Available Tools

- `get_repos(username, limit=10)`: Get repositories for a user
- `get_issues(owner, repo, state="open", limit=10)`: Get issues for a repository
- `get_pull_requests(owner, repo, state="open", limit=10)`: Get PRs for a repository
- `search_code(query, language="", limit=10)`: Search for code

## 📝 Example Usage

```python
# Get user's repositories
get_repos(username="octocat", limit=5)

# Get open issues
get_issues(owner="microsoft", repo="vscode", state="open", limit=10)

# Get pull requests
get_pull_requests(owner="facebook", repo="react", state="open", limit=5)

# Search for Python code
search_code(query="machine learning", language="python", limit=10)
```

## ⚠️ Rate Limits

GitHub API has rate limits:
- **With token**: 5,000 requests per hour
- **Without token**: 60 requests per hour

The server will return an error if rate limits are exceeded.
