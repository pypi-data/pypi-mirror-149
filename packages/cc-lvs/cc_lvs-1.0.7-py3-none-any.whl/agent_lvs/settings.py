import os

DEFAULT_HEADERS = {
    # 'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept': 'text/html, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

CAPTCHA_API = os.getenv('CAPTCHA_API', 'http://captcha.lehongnam.com/')
LVS_AGENT_DOMAIN = os.getenv('LVS_AGENT_DOMAIN', 'https://edy688.com/')
