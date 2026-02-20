import asyncio
from playwright.async_api import async_playwright

async def debug_ui():
    console_logs = []
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Capture console messages
            page.on("console", lambda msg: console_logs.append(f"[{msg.type.upper()}] {msg.text}"))
            
            print("[DEBUGGER] Navigating to http://localhost:5000...")
            await page.goto("http://localhost:5000", wait_until="networkidle")
            
            print("[DEBUGGER] Waiting for 2 seconds for async data to load...")
            await asyncio.sleep(2)
            
            screenshot_path = "ui_debug_screenshot.png"
            await page.screenshot(path=screenshot_path)
            
            print(f"[DEBUGGER] Screenshot saved to: {screenshot_path}")
            await browser.close()

            print("\n--- BROWSER CONSOLE LOGS ---")
            if console_logs:
                for log in console_logs:
                    print(log)
            else:
                print("No console logs captured.")
            print("--------------------------")
            
        except Exception as e:
            print(f"An error occurred during UI debugging: {e}")

if __name__ == "__main__":
    asyncio.run(debug_ui())
