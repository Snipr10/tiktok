import asyncio

from models import AccountResult
from scraper import BrowserManager, get_cookies
from utils.scraper_utils import scroll_tiktok, get_headers

NEW_PAGE_TIMEOUT = 60 * 1000
CAPTCHA_TIMEOUT = 1 * 1000
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36'


async def parsing_account(url):
    cookies = []
    async with BrowserManager() as browser_manager:
        browser = browser_manager.browser
        page = await browser.newPage()
        await page._client.send('Network.setCookies', {
            'cookies': cookies,
        })
        body = []

        await page.setUserAgent(USER_AGENT)
        page.on("response",
                lambda req: asyncio.ensure_future(get_headers(req, body, url)))
        await page.goto(url)
        try:
            await page.waitForSelector("[role='dialog'", timeout=CAPTCHA_TIMEOUT)
            return AccountResult(success=False, captcha=True)
        except Exception:
            pass
        await scroll_tiktok(len(body), page, body, attempt=0)
        # cookies = await get_cookies(page)
        return AccountResult(body=body)
