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

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Steps:**
1. **Click the "Deploy to Render" button above** or go to [render.com](https://render.com)
2. **Connect your GitHub account to Render** (if you haven't already)
3. **Create a new Web Service:**
   - Connect this repository
   - **Name**: `github-mcp`
   - **Environment**: `Python 3`
   - **Plan**: `Free`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/server.py`
4. **Set environment variable:**
   - Go to your Render service dashboard
   - Click on "Environment" tab
   - Add environment variable: `GITHUB_TOKEN` = `your_github_token_here`
   - Click "Save Changes"
5. **Deploy!**

> Note: On Render's free tier, services go idle after ~15 minutes of inactivity and may require a manual "Deploy" to wake or to pick up the latest commit. Unlike Vercel, pushes do not auto-deploy by default.

Your server will be available at `https://github-mcp.onrender.com/mcp`

## 🎯 Poke Integration

1. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
2. Add the MCP URL: `https://github-mcp.onrender.com/mcp`
3. Give it a name like "GitHub"
4. Try: "Can you use the GitHub MCP to list my repos?"

## 🧩 Architecture Note (FastAPI + FastMCP Hybrid)

Note: FastMCP 2.x responses didn’t work well with Poke’s client in my testing due to response format differences. The client expects simpler JSON but errors on FastMCP’s structured content with "Cannot read properties of undefined (reading 'status')". This was reproducible with Interaction’s basic FastMCP template as well.

So for now, this server uses a hybrid architecture where:
- FastAPI endpoints deliver Poke‑compatible JSON
- `@mcp.tool()` functions exist as future‑ready wrappers
- Shared logic lives in `_http` functions to avoid duplication

To try pure FastMCP later:
1) replace the entire FastAPI main block with `mcp.run()`,
2) optionally move each `_http` function’s logic into the corresponding `@mcp.tool()` (or keep wrappers calling `_http`), and
3) remove FastAPI routes if no longer needed.

This works with Poke today while keeping a clean migration path to pure FastMCP.

## References

- Based on the Interaction MCP server template: [MCP Server Template](https://github.com/InteractionCo/mcp-server-template/tree/main)
- Discovered via Interaction’s HackMIT challenge: [Interaction HackMIT Challenge](https://interaction.co/HackMIT)

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
