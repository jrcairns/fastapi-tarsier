import asyncio
import datetime
from playwright.async_api import async_playwright
from agent import setup_agent
from tools import setup_tools
from config import load_config

async def main():
    config = load_config()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        tools = await setup_tools(page, config)
        agent_chain = await setup_agent(tools)

        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")

        # Create the email with the current timestamp
        email = f"test-{current_time}@gmail.com"

        await page.goto("http://127.0.0.1:8000/")
        result = await agent_chain.ainvoke(
            f"""
            Tasks:
            1. Account Registration:
            - Email: {email}
            - Record all account details
            - Report complete account information

            2. Premium Plan Registration:
            - Credit Card: 4242 4242 4242 4242
            - Expiry: 04/25
            - CVC: 424
            - Name: Frodo Baggins
            - Postal Code: T2T 6V1
            - Complete any additional required fields

            Report all details once finished.
            """
        )
        print(result)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())