import asyncio
import time

from crawl4ai import *


# TODO: Set your configuration
user_data_dir = "/browser-profile/Default1" # Ensure this path is correctly set and contains your configured extension

browser_config = BrowserConfig(
    verbose=True,
    headless=False,
    user_data_dir=user_data_dir,
    use_persistent_context=True,
    proxy="http://127.0.0.1:13120", # Optional: configure proxy if needed
)

async def main():
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result_initial = await crawler.arun(
            url="https://clifford.io/demo/cloudflare-turnstile", # Use the Cloudflare Turnstile demo URL
            cache_mode=CacheMode.BYPASS,
            session_id="session_captcha_test"
        )

        # The extension will automatically solve the CAPTCHA upon page load.
        # You might need to add a wait condition or time.sleep for the CAPTCHA to be solved
        # before proceeding with further actions.
        time.sleep(30) # Example wait, adjust as necessary for the extension to operate

        # Continue with other Crawl4AI operations after CAPTCHA is solved
        # For instance, check for elements or content that appear after successful verification
        # print(result_initial.markdown) # You can inspect the page content after the wait


if __name__ == "__main__":
    asyncio.run(main())

