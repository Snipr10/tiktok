import logging
import os
import re
import requests

from pyppeteer import launch

logger = logging.getLogger(__name__)

FINDING_ERROR_MESSAGES_TIMEOUT = 2 * 1000

non_decimal = re.compile(r'[^\d.]+')


class BrowserManager:

    def __init__(self, **kargs):
        self.browser = None
        self.params = kargs

    async def __aenter__(self):
        headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        self.browser = await launch(headless=True,
                                    handleSIGINT=False,
                                    handleSIGTERM=False,
                                    handleSIGHUP=False,
                                    args=['--no-sandbox'])
        return self

    async def __aexit__(self, type, value, traceback):
        if self.browser:
            await self.browser.close()


def to_curl(req):
    command = "curl --location --request {method} '{uri}'\\\n"
    command += "  --header {headers}"
    method = req.method
    uri = req.url
    data = req.body
    headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
    headers = "\\\n  --header ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)


async def get_cookies(page):
    return await page._client.send('Network.getAllCookies')


def cookies_to_session(cookies, headers={}):
    session = requests.session()
    cookies_jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies:
        cookies_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

    session.cookies = cookies_jar
    session.headers.update(headers)

    return session


def cookies_jar_to_array(cookies_jar):
    cookies = []
    for cookie_jar in cookies_jar:
        cookie = {}
        for name in ("version", "name", "value",
                     "port", "port_specified",
                     "domain", "domain_specified", "domain_initial_dot",
                     "path", "path_specified",
                     "secure", "expires", "discard", "comment", "comment_url",
                     ):
            attr = getattr(cookie_jar, name)
            cookie.update({name: attr})
        cookies.append(cookie)
    return cookies