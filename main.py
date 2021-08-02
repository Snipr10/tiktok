import asyncio

from scraper_with_signature.tiktok import TikTokApi
from scrapers.account import parsing_account
from scrapers.hashtag import parsing_by_hashtag


if __name__ == '__main__':


    loop = asyncio.new_event_loop()
    s1 = loop.run_until_complete(asyncio.wait_for(parsing_account("https://www.tiktok.com/@v.milonov"), 3000))

    s2 = loop.run_until_complete(asyncio.wait_for(parsing_by_hashtag("https://www.tiktok.com/tag/%D0%BB%D1%83%D0%BA%D0%B0%D1%88%D0%B5%D0%BD%D0%BA%D0%BE"), 3000))
    print("ok")
    # api = TikTokApi()
    #
    # z = TikTokApi.byHashtag("hashtag", count=30, language='en', proxy=None)


