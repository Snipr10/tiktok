import asyncio

from models import AccountResult
from scraper import BrowserManager, get_cookies, get_page
from utils.scraper_utils import scroll_tiktok, get_headers

NEW_PAGE_TIMEOUT = 60 * 1000
CAPTCHA_TIMEOUT = 1 * 1000
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

CHROME_REVISION = '884014'


async def parsing_by_hashtag(url):

    async with BrowserManager() as browser_manager:
        browser = browser_manager.browser
        page = await browser.newPage()
        await page.evaluateOnNewDocument(
            """() => {
            delete navigator.__proto__.webdriver;
            }"""
        )
        await page.setUserAgent(USER_AGENT)
        body = []

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
