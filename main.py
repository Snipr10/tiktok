import asyncio

from scrapers.account import parsing_account

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    s = loop.run_until_complete(asyncio.wait_for(parsing_account("https://www.tiktok.com/@aicontent13"), 3000))
    print("ok")

