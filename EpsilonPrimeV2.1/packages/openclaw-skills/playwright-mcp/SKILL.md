---
name: playwright-mcp
description: "Advanced web automation and scraping via Playwright MCP. Replaces standard browser."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["npx"] },
        "homepage": "https://github.com/openclaw/openclaw-skills"
      }
  }
---

# Playwright MCP Skill

Use this skill for advanced web scraping, handling Single Page Applications (SPAs), and executing complex browser interactions.

## Tools
- `playwright_open`: Navigates to a URL.
- `playwright_scrape`: Extracts text and HTML from the current page.
- `playwright_click`: Clicks elements using CSS selectors or text.
- `playwright_type`: Types text into input fields.
- `playwright_screenshot`: Captures a visual snapshot of the page.

## Usage
When the standard `browser` tool fails due to JavaScript or bot detection, switch to `playwright`.
Always prefer `playwright_scrape` for information-dense sites.
