import os
import asyncio
from playwright.sync_api import sync_playwright
from smolagents import tool

@tool
def visit_webpage(url: str) -> str:
    """
    Visits a webpage and returns its content formatted as Markdown.
    Args:
        url: The URL of the webpage to visit.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            
            # Simple extraction: title + body text
            title = page.title()
            # We use a simple script to get text content, or we could use something like readability
            content = page.evaluate("() => document.body.innerText")
            
            browser.close()
            return f"# {title}\n\n{content}"
    except Exception as e:
        return f"Error visiting webpage: {e}"

@tool
def search_web(query: str) -> str:
    """
    Performs a web search using a search engine and returns the top results.
    Args:
        query: The search query.
    """
    # For a sovereign agent, we use a simple duckduckgo or similar unauthenticated search
    search_url = f"https://duckduckgo.com/html/?q={query}"
    return visit_webpage(search_url)