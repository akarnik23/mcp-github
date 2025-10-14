#!/usr/bin/env python3
"""
GitHub MCP Server
A FastMCP server that provides access to GitHub repositories and data.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
import httpx
from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("GitHub MCP Server")

# GitHub API configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "demo")
GITHUB_API_BASE = "https://api.github.com"

# Undecorated functions for HTTP endpoint
def get_repos_http(username: str, limit: int = 10, api_key: str = None) -> str:
    """Get repositories for a GitHub user."""
    try:
        limit = min(max(limit, 1), 30)  # Clamp between 1 and 30
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_repos = [
                {
                    "name": "vscode",
                    "full_name": "microsoft/vscode",
                    "description": "Visual Studio Code",
                    "url": "https://github.com/microsoft/vscode",
                    "stars": 150000,
                    "forks": 26000,
                    "language": "TypeScript",
                    "created_at": "2015-09-03T20:33:27Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "private": False
                },
                {
                    "name": "react",
                    "full_name": "facebook/react",
                    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                    "url": "https://github.com/facebook/react",
                    "stars": 220000,
                    "forks": 45000,
                    "language": "JavaScript",
                    "created_at": "2013-05-24T16:15:54Z",
                    "updated_at": "2024-01-15T12:00:00Z",
                    "private": False
                }
            ]
            return json.dumps(demo_repos, indent=2)
        
        params = {
            "sort": "updated",
            "per_page": limit
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/users/{username}/repos",
            headers=get_headers(api_key),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        repos = response.json()
        
        formatted_repos = []
        for repo in repos:
            formatted_repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo.get("description", ""),
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo.get("language", ""),
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "private": repo["private"]
            })
        
        return json.dumps(formatted_repos, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

def get_issues_http(owner: str, repo: str, state: str = "open", limit: int = 10, api_key: str = None) -> str:
    """Get issues for a GitHub repository."""
    try:
        limit = min(max(limit, 1), 30)  # Clamp between 1 and 30
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_issues = [
                {
                    "number": 12345,
                    "title": "Bug: Component not rendering correctly",
                    "body": "The component is not displaying the expected content...",
                    "state": "open",
                    "url": f"https://github.com/{owner}/{repo}/issues/12345",
                    "user": "developer123",
                    "labels": ["bug", "frontend"],
                    "created_at": "2024-01-10T10:30:00Z",
                    "updated_at": "2024-01-15T14:20:00Z",
                    "comments": 5
                },
                {
                    "number": 12344,
                    "title": "Feature: Add dark mode support",
                    "body": "It would be great to have a dark mode option...",
                    "state": "open",
                    "url": f"https://github.com/{owner}/{repo}/issues/12344",
                    "user": "feature-requestor",
                    "labels": ["enhancement", "ui"],
                    "created_at": "2024-01-08T09:15:00Z",
                    "updated_at": "2024-01-12T16:45:00Z",
                    "comments": 12
                }
            ]
            return json.dumps(demo_issues, indent=2)
        
        params = {
            "state": state,
            "per_page": limit,
            "sort": "updated"
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues",
            headers=get_headers(api_key),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        issues = response.json()
        
        formatted_issues = []
        for issue in issues:
            # Skip pull requests (they appear in issues API)
            if "pull_request" in issue:
                continue
                
            formatted_issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "body": issue.get("body", ""),
                "state": issue["state"],
                "url": issue["html_url"],
                "user": issue["user"]["login"],
                "labels": [label["name"] for label in issue["labels"]],
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "comments": issue["comments"]
            })
        
        return json.dumps(formatted_issues, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

def get_pull_requests_http(owner: str, repo: str, state: str = "open", limit: int = 10, api_key: str = None) -> str:
    """Get pull requests for a GitHub repository."""
    try:
        limit = min(max(limit, 1), 30)  # Clamp between 1 and 30
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_prs = [
                {
                    "number": 6789,
                    "title": "Fix: Resolve memory leak in data processing",
                    "body": "This PR fixes a memory leak that was occurring...",
                    "state": "open",
                    "url": f"https://github.com/{owner}/{repo}/pull/6789",
                    "user": "bug-fixer",
                    "head": "feature/fix-memory-leak",
                    "base": "main",
                    "created_at": "2024-01-12T11:30:00Z",
                    "updated_at": "2024-01-15T09:15:00Z",
                    "draft": False,
                    "mergeable": True
                },
                {
                    "number": 6788,
                    "title": "Add: New authentication system",
                    "body": "Implements OAuth2 authentication flow...",
                    "state": "open",
                    "url": f"https://github.com/{owner}/{repo}/pull/6788",
                    "user": "auth-developer",
                    "head": "feature/oauth2-auth",
                    "base": "main",
                    "created_at": "2024-01-10T14:20:00Z",
                    "updated_at": "2024-01-14T16:30:00Z",
                    "draft": False,
                    "mergeable": None
                }
            ]
            return json.dumps(demo_prs, indent=2)
        
        params = {
            "state": state,
            "per_page": limit,
            "sort": "updated"
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls",
            headers=get_headers(api_key),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        prs = response.json()
        
        formatted_prs = []
        for pr in prs:
            formatted_prs.append({
                "number": pr["number"],
                "title": pr["title"],
                "body": pr.get("body", ""),
                "state": pr["state"],
                "url": pr["html_url"],
                "user": pr["user"]["login"],
                "head": pr["head"]["ref"],
                "base": pr["base"]["ref"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "draft": pr["draft"],
                "mergeable": pr.get("mergeable")
            })
        
        return json.dumps(formatted_prs, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

def search_code_http(query: str, language: str = "", limit: int = 10, api_key: str = None) -> str:
    """Search for code on GitHub."""
    try:
        limit = min(max(limit, 1), 20)  # Clamp between 1 and 20
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_results = [
                {
                    "name": "app.js",
                    "path": "src/app.js",
                    "repository": "microsoft/vscode",
                    "url": "https://github.com/microsoft/vscode/blob/main/src/app.js",
                    "language": "JavaScript",
                    "size": 1024,
                    "score": 95.5
                },
                {
                    "name": "component.tsx",
                    "path": "components/Button.tsx",
                    "repository": "facebook/react",
                    "url": "https://github.com/facebook/react/blob/main/components/Button.tsx",
                    "language": "TypeScript",
                    "size": 2048,
                    "score": 88.2
                }
            ]
            return json.dumps({"total_count": 2, "results": demo_results}, indent=2)
        
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        params = {
            "q": search_query,
            "per_page": limit,
            "sort": "indexed"
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/search/code",
            headers=get_headers(api_key),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            results.append({
                "name": item["name"],
                "path": item["path"],
                "repository": item["repository"]["full_name"],
                "url": item["html_url"],
                "language": item.get("language", ""),
                "size": item["size"],
                "score": item["score"]
            })
        
        search_results = {
            "total_count": data["total_count"],
            "results": results
        }
        
        return json.dumps(search_results, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

def get_headers(api_key=None):
    """Get headers for GitHub API requests."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-MCP-Server"
    }
    # Use provided API key or fallback to environment variable
    token = api_key or GITHUB_TOKEN
    if token and token != "demo":
        headers["Authorization"] = f"token {token}"
    return headers

@mcp.tool()
def get_repos(username: str, limit: int = 10, api_key: str = None) -> str:
    """Get repositories for a GitHub user.
    
    Args:
        username: GitHub username
        limit: Number of repositories to return (default: 10, max: 30)
    
    Returns:
        JSON string with repository data
    """
    try:
        limit = min(max(limit, 1), 30)  # Clamp between 1 and 30
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_repos = [
                {
                    "name": "vscode",
                    "full_name": "microsoft/vscode",
                    "description": "Visual Studio Code",
                    "url": "https://github.com/microsoft/vscode",
                    "stars": 150000,
                    "forks": 26000,
                    "language": "TypeScript",
                    "created_at": "2015-09-03T20:33:27Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "private": False
                },
                {
                    "name": "react",
                    "full_name": "facebook/react",
                    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                    "url": "https://github.com/facebook/react",
                    "stars": 220000,
                    "forks": 45000,
                    "language": "JavaScript",
                    "created_at": "2013-05-24T16:15:54Z",
                    "updated_at": "2024-01-15T12:00:00Z",
                    "private": False
                }
            ]
            return json.dumps(demo_repos, indent=2)
        
        params = {
            "sort": "updated",
            "per_page": limit
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/users/{username}/repos",
            headers=get_headers(api_key),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        repos = response.json()
        
        formatted_repos = []
        for repo in repos:
            formatted_repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo.get("description", ""),
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo.get("language", ""),
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "private": repo["private"]
            })
        
        return json.dumps(formatted_repos, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

@mcp.tool()
def get_issues(owner: str, repo: str, state: str = "open", limit: int = 10) -> str:
    """Get issues for a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state: open, closed, or all (default: open)
        limit: Number of issues to return (default: 10, max: 30)
    
    Returns:
        JSON string with issues data
    """
    try:
        limit = min(max(limit, 1), 30)  # Clamp between 1 and 30
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_repos = [
                {
                    "name": "vscode",
                    "full_name": "microsoft/vscode",
                    "description": "Visual Studio Code",
                    "url": "https://github.com/microsoft/vscode",
                    "stars": 150000,
                    "forks": 26000,
                    "language": "TypeScript",
                    "created_at": "2015-09-03T20:33:27Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "private": False
                },
                {
                    "name": "react",
                    "full_name": "facebook/react",
                    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                    "url": "https://github.com/facebook/react",
                    "stars": 220000,
                    "forks": 45000,
                    "language": "JavaScript",
                    "created_at": "2013-05-24T16:15:54Z",
                    "updated_at": "2024-01-15T12:00:00Z",
                    "private": False
                }
            ]
            return json.dumps(demo_repos, indent=2)
        
        params = {
            "state": state,
            "per_page": limit,
            "sort": "updated"
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues",
            headers=get_headers(),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        issues = response.json()
        
        formatted_issues = []
        for issue in issues:
            # Skip pull requests (they appear in issues API)
            if "pull_request" in issue:
                continue
                
            formatted_issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "body": issue.get("body", ""),
                "state": issue["state"],
                "url": issue["html_url"],
                "user": issue["user"]["login"],
                "labels": [label["name"] for label in issue["labels"]],
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "comments": issue["comments"]
            })
        
        return json.dumps(formatted_issues, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

@mcp.tool()
def get_pull_requests(owner: str, repo: str, state: str = "open", limit: int = 10) -> str:
    """Get pull requests for a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: PR state: open, closed, or all (default: open)
        limit: Number of PRs to return (default: 10, max: 30)
    
    Returns:
        JSON string with pull requests data
    """
    try:
        limit = min(max(limit, 1), 30)  # Clamp between 1 and 30
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_repos = [
                {
                    "name": "vscode",
                    "full_name": "microsoft/vscode",
                    "description": "Visual Studio Code",
                    "url": "https://github.com/microsoft/vscode",
                    "stars": 150000,
                    "forks": 26000,
                    "language": "TypeScript",
                    "created_at": "2015-09-03T20:33:27Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "private": False
                },
                {
                    "name": "react",
                    "full_name": "facebook/react",
                    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                    "url": "https://github.com/facebook/react",
                    "stars": 220000,
                    "forks": 45000,
                    "language": "JavaScript",
                    "created_at": "2013-05-24T16:15:54Z",
                    "updated_at": "2024-01-15T12:00:00Z",
                    "private": False
                }
            ]
            return json.dumps(demo_repos, indent=2)
        
        params = {
            "state": state,
            "per_page": limit,
            "sort": "updated"
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls",
            headers=get_headers(),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        prs = response.json()
        
        formatted_prs = []
        for pr in prs:
            formatted_prs.append({
                "number": pr["number"],
                "title": pr["title"],
                "body": pr.get("body", ""),
                "state": pr["state"],
                "url": pr["html_url"],
                "user": pr["user"]["login"],
                "head": pr["head"]["ref"],
                "base": pr["base"]["ref"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "draft": pr["draft"],
                "mergeable": pr.get("mergeable")
            })
        
        return json.dumps(formatted_prs, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

@mcp.tool()
def search_code(query: str, language: str = "", limit: int = 10) -> str:
    """Search for code on GitHub.
    
    Args:
        query: Search query
        language: Programming language filter (optional)
        limit: Number of results to return (default: 10, max: 20)
    
    Returns:
        JSON string with search results
    """
    try:
        limit = min(max(limit, 1), 20)  # Clamp between 1 and 20
        
        if (api_key or GITHUB_TOKEN) == "demo":
            # Return demo data
            demo_repos = [
                {
                    "name": "vscode",
                    "full_name": "microsoft/vscode",
                    "description": "Visual Studio Code",
                    "url": "https://github.com/microsoft/vscode",
                    "stars": 150000,
                    "forks": 26000,
                    "language": "TypeScript",
                    "created_at": "2015-09-03T20:33:27Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "private": False
                },
                {
                    "name": "react",
                    "full_name": "facebook/react",
                    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                    "url": "https://github.com/facebook/react",
                    "stars": 220000,
                    "forks": 45000,
                    "language": "JavaScript",
                    "created_at": "2013-05-24T16:15:54Z",
                    "updated_at": "2024-01-15T12:00:00Z",
                    "private": False
                }
            ]
            return json.dumps(demo_repos, indent=2)
        
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        params = {
            "q": search_query,
            "per_page": limit,
            "sort": "indexed"
        }
        
        response = httpx.get(
            f"{GITHUB_API_BASE}/search/code",
            headers=get_headers(),
            params=params,
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            results.append({
                "name": item["name"],
                "path": item["path"],
                "repository": item["repository"]["full_name"],
                "url": item["html_url"],
                "language": item.get("language", ""),
                "size": item["size"],
                "score": item["score"]
            })
        
        search_results = {
            "total_count": data["total_count"],
            "results": results
        }
        
        return json.dumps(search_results, indent=2)
        
    except httpx.RequestError as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)

if __name__ == "__main__":
    # Run in HTTP mode for testing
    import uvicorn
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    import json
    
    # Create FastAPI app
    app = FastAPI()
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def health_check():
        return {"status": "ok", "server": "GitHub MCP Server"}
    
    @app.post("/")
    @app.post("/mcp")
    async def mcp_endpoint(request: dict):
        """Handle MCP requests via HTTP POST"""
        try:
            print(f"Received request: {request}")
            
            if request.get("method") == "initialize":
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "GitHub MCP Server", "version": "1.0.0"}
                    }
                })
            elif request.get("method") == "tools/list":
                tools = [
                    {
                        "name": "get_repos", 
                        "description": "Get repositories for a GitHub user", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "description": "GitHub username"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of repositories to return (1-30)",
                                    "minimum": 1,
                                    "maximum": 30,
                                    "default": 10
                                },
                                "api_key": {
                                    "type": "string",
                                    "description": "GitHub personal access token (optional)"
                                }
                            },
                            "required": ["username"]
                        }
                    },
                    {
                        "name": "get_issues", 
                        "description": "Get issues for a GitHub repository", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "owner": {
                                    "type": "string",
                                    "description": "Repository owner"
                                },
                                "repo": {
                                    "type": "string",
                                    "description": "Repository name"
                                },
                                "state": {
                                    "type": "string",
                                    "description": "Issue state",
                                    "enum": ["open", "closed", "all"],
                                    "default": "open"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of issues to return (1-30)",
                                    "minimum": 1,
                                    "maximum": 30,
                                    "default": 10
                                },
                                "api_key": {
                                    "type": "string",
                                    "description": "GitHub personal access token (optional)"
                                }
                            },
                            "required": ["owner", "repo"]
                        }
                    },
                    {
                        "name": "get_pull_requests", 
                        "description": "Get pull requests for a GitHub repository", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "owner": {
                                    "type": "string",
                                    "description": "Repository owner"
                                },
                                "repo": {
                                    "type": "string",
                                    "description": "Repository name"
                                },
                                "state": {
                                    "type": "string",
                                    "description": "PR state",
                                    "enum": ["open", "closed", "all"],
                                    "default": "open"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of PRs to return (1-30)",
                                    "minimum": 1,
                                    "maximum": 30,
                                    "default": 10
                                },
                                "api_key": {
                                    "type": "string",
                                    "description": "GitHub personal access token (optional)"
                                }
                            },
                            "required": ["owner", "repo"]
                        }
                    },
                    {
                        "name": "search_code", 
                        "description": "Search for code on GitHub", 
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query"
                                },
                                "language": {
                                    "type": "string",
                                    "description": "Programming language filter (optional)"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of results to return (1-20)",
                                    "minimum": 1,
                                    "maximum": 20,
                                    "default": 10
                                },
                                "api_key": {
                                    "type": "string",
                                    "description": "GitHub personal access token (optional)"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                ]
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": tools}
                })
            elif request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                tool_args = request.get("params", {}).get("arguments", {})
                
                if tool_name == "get_repos":
                    result = get_repos_http(**tool_args)
                elif tool_name == "get_issues":
                    result = get_issues_http(**tool_args)
                elif tool_name == "get_pull_requests":
                    result = get_pull_requests_http(**tool_args)
                elif tool_name == "search_code":
                    result = search_code_http(**tool_args)
                else:
                    return JSONResponse(content={
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                    })
                
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"content": [{"type": "text", "text": result}]}
                })
            else:
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": f"Method '{request.get('method')}' not found"}
                })
                
        except Exception as e:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }, 
                status_code=500
            )
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
