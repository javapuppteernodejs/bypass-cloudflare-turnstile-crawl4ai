

# How to Solve Cloudflare Turnstile in Crawl4AI with CapSolver Integration

Cloudflare Turnstile is a modern, privacy-preserving CAPTCHA alternative that verifies human users invisibly by running background JavaScript challenges.
While great for security and UX, this protection can block automated crawlers and cause repeated request failures.

This guide explains how to **integrate [Crawl4AI](https://docs.crawl4ai.com/)** — an advanced web crawling framework — with **[CapSolver](https://dashboard.capsolver.com/passport/login/?utm_source=github&utm_medium=integration&utm_campaign=crawl4ai-turnstile)** to automatically bypass **Cloudflare Turnstile**.
You’ll learn both **API-based** and **browser-extension-based** integration methods, complete with practical code examples.

---

## 🚀 Overview

| Method                    | Difficulty | Key Advantage                                   |
| :------------------------ | :--------- | :---------------------------------------------- |
| **API Integration**       | ⭐⭐      | Full control over token injection and execution |
| **Extension Integration** | ⭐         | Simplified, automatic Turnstile solving         |

---

## 🧠 Method 1: CapSolver API Integration with Crawl4AI

This approach retrieves a valid Turnstile token using CapSolver’s API and injects it into the target webpage programmatically with Crawl4AI.

### 🔧 How It Works

1. Use **CapSolver SDK** to solve the `AntiTurnstileTaskProxyLess` task.
2. Inject the returned token into the `cf-turnstile-response` field via JavaScript.
3. Simulate the form submission or next step.
4. Crawl4AI continues scraping with the validated browser session.

---

### 💻 Example Code

```python
import asyncio
import capsolver
from crawl4ai import *

# --- Configuration ---
api_key = "CAP-xxxxxxxxxxxxxxxxxxxxx"
site_key = "0x4AAAAAAAGlwMzq_9z6S9Mh"
site_url = "https://clifford.io/demo/cloudflare-turnstile"
captcha_type = "AntiTurnstileTaskProxyLess"
capsolver.api_key = api_key

async def main():
    browser_config = BrowserConfig(
        verbose=True,
        headless=False,
        use_persistent_context=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        await crawler.arun(url=site_url, cache_mode=CacheMode.BYPASS)

        # 1. Solve Turnstile via CapSolver API
        solution = capsolver.solve({
            "type": captcha_type,
            "websiteURL": site_url,
            "websiteKey": site_key,
        })
        token = solution["token"]
        print("✅ Turnstile token:", token)

        # 2. Inject token & trigger submission
        js_code = f"""
            document.querySelector('input[name="cf-turnstile-response"]').value = '{token}';
            document.querySelector('button[type="submit"]').click();
        """

        wait_condition = """() => !document.querySelector('h1')"""

        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            js_code=js_code,
            js_only=True,
            wait_for=f"js:{wait_condition}"
        )

        # 3. Continue crawling
        result = await crawler.arun(url=site_url, config=run_config)
        print(result.markdown[:500])

if __name__ == "__main__":
    asyncio.run(main())
```

**🔍 Explanation:**

* `capsolver.solve()` requests a Turnstile token using your `websiteURL` and `websiteKey`.
* The token is inserted into the hidden input field (`cf-turnstile-response`).
* Crawl4AI then submits the page automatically.
* Once verified, your crawler can extract data without interruptions.

---

## 🧩 Method 2: CapSolver Browser Extension Integration

For developers who prefer automation over configuration, you can install the **CapSolver browser extension** into a persistent Crawl4AI browser profile.
It automatically detects and solves Cloudflare Turnstile challenges.

### 💻 Example Code

```python
import asyncio, time
from crawl4ai import *

# Persistent browser profile with CapSolver extension pre-installed
user_data_dir = "./browser-profile/Default1"

browser_config = BrowserConfig(
    verbose=True,
    headless=False,
    use_persistent_context=True,
    user_data_dir=user_data_dir,
)

async def main():
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://clifford.io/demo/cloudflare-turnstile",
            cache_mode=CacheMode.BYPASS,
        )

        print("🕒 Waiting for Turnstile to auto-solve...")
        time.sleep(20)

        print("✅ Turnstile solved automatically.")
        # Proceed with other scraping tasks
        # e.g. await crawler.arun(url="https://target-site.com/data")

if __name__ == "__main__":
    asyncio.run(main())
```

**🔍 Explanation:**

* The **CapSolver extension** runs within the browser context used by Crawl4AI.
* Once loaded, it automatically solves any visible or invisible Turnstile challenges.
* Suitable for long-running crawlers or browser automation workflows.

---

## ✅ Conclusion

Integrating **[Crawl4AI](https://docs.crawl4ai.com/)** with **[CapSolver](https://dashboard.capsolver.com/passport/login/?utm_source=github&utm_medium=integration&utm_campaign=crawl4ai-turnstile)** provides a seamless way to bypass Cloudflare Turnstile challenges.
Whether you need fine-grained token control or a hands-off automated experience, both methods ensure uninterrupted web scraping and data collection.

This setup allows your crawler to:

* Maintain consistent access across Turnstile-protected domains
* Automate verification and token handling
* Reduce manual intervention and scraping errors

---

## 🧾 References

* [Crawl4AI Official Documentation](https://docs.crawl4ai.com/)
* [CapSolver Official Documentation](https://docs.capsolver.com/)
* [CapSolver: Cloudflare Turnstile Guide](https://docs.capsolver.com/guide/captcha/cloudflare_turnstile/)
* [Crawl4AI × CapSolver Partnership](https://www.capsolver.com/blog/Partners/crawl4ai-capsolver)
