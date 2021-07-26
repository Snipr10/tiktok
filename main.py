import asyncio
import json
from bs4 import BeautifulSoup
from scraper import BrowserManager, get_cookies

NEW_PAGE_TIMEOUT = 60 * 1000



async def print_hi(name):
    cookies = [{'name': 'ttwid',
                'value': '1%7CutmGt4WCrbrBMCG2o4cENAP-DZIEmkmYt3AN5qLDlPc%7C1626964563%7C1dffcf6cfdb67820946773f478b16de9324cea2bca64ff120e6c7d016b522445',
                'domain': '.tiktok.com', 'path': '/', 'expires': 1658500563.356663, 'size': 132, 'httpOnly': True,
                'secure': True, 'session': False},
               {'name': 'MONITOR_WEB_ID', 'value': 'f63ace80-d958-4363-9159-ce57f8b43028',
                'domain': '.mon-va.byteoversea.com', 'path': '/', 'expires': 1634740531.22915, 'size': 50,
                'httpOnly': False, 'secure': True, 'session': False},
               {'name': 'csrf_session_id', 'value': 'f81edd91c46a40669e3bacc38bb873ff', 'domain': '.www.tiktok.com',
                'path': '/', 'expires': -1, 'size': 47, 'httpOnly': False, 'secure': True, 'session': True},
               {'name': 's_v_web_id', 'value': 'verify_0b4f63e7a4e43737396c7e15b27d728d', 'domain': '.tiktok.com',
                'path': '/', 'expires': -1, 'size': 49, 'httpOnly': False, 'secure': True, 'session': True},
               {'name': 'R6kq3TV7',
                'value': 'AKKRpM56AQAAPmKEtvgQ6EWA2Hh9cK7zIG_DZNTQTXA-HowlP4BTDe3TSDn4|1|0|5e66e5e50d83b166de030aae3f90f6b47d24924d',
                'domain': '.tiktok.com', 'path': '/', 'expires': 1626996086.721801, 'size': 113, 'httpOnly': True,
                'secure': True, 'session': False},
               {'name': 'MONITOR_WEB_ID', 'value': '6987759410919998981', 'domain': '.www.tiktok.com', 'path': '/',
                'expires': 1634740561.824048, 'size': 33, 'httpOnly': False, 'secure': False, 'session': False},
               {'name': 'R6kq3TV7',
                'value': 'ACOGpM56AQAAkV2d9x_ZfvnLa84bwFlsJ-33kbmRKR_c4EDzzXhw8z9yfDp3|1|0|ebcd7e548adbb0d5e68b8a453c3f183ec87cab4a',
                'domain': 's20.tiktokcdn.com', 'path': '/', 'expires': 1658521478.718227, 'size': 113,
                'httpOnly': False,
                'secure': False, 'session': False},
               {'name': 'tt_csrf_token', 'value': 'GZUWkMTAiMzDXSGCxDTUShnA', 'domain': '.tiktok.com', 'path': '/',
                'expires': -1, 'size': 37, 'httpOnly': True, 'secure': True, 'session': True, 'sameSite': 'Lax'},
               {'name': 'tt_webid', 'value': '6987759410919998981', 'domain': '.tiktok.com', 'path': '/',
                'expires': 1658500525.122976, 'size': 27, 'httpOnly': True, 'secure': True, 'session': False},
               {'name': 'tt_webid_v2', 'value': '6987759410919998981', 'domain': '.tiktok.com', 'path': '/',
                'expires': 1658500525.122941, 'size': 30, 'httpOnly': True, 'secure': True, 'session': False}]

    async with BrowserManager() as browser_manager:
        new = True
        url = "https://www.tiktok.com/@aicontent13"
        # url = "https://www.tiktok.com/@_agentgirl_?lang=ru-RU"

        browser = browser_manager.browser
        page = await browser.newPage()
        await page._client.send('Network.setCookies', {
            'cookies': cookies,
        })
        headers = []
        page.on("response",
                lambda req: asyncio.ensure_future(_get_headers(req, headers, url, new)))
        await page.goto(url)
        await asyncio.sleep(2)
        await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")


        count = headers.__len__()
        while True:
            await asyncio.sleep(1)
            await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
            if count >= headers.__len__():
                break
            else:
                count = headers.__len__()


        cookies = await get_cookies(page)


async def _get_headers(response, headers, url, new):

    if url in response.url:
        print(1)
        text = await response.text()
        soup = BeautifulSoup(text)
        json_text = soup.find(id='__NEXT_DATA__').contents[0]
        data = json.loads(json_text)
        headers += data['props']['pageProps']['items']
        print(2)
    if "https://m.tiktok.com/api/post/item_list" in response.url:
        try:
            s = await response.json()
            headers += s['itemList']
        except Exception as e:
            print(e)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    s = loop.run_until_complete(asyncio.wait_for(print_hi('PyCharm'), 3000))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
