import re
from functools import cached_property

from api_helper import BaseClient, login_required
from bs4 import BeautifulSoup

from . import settings, exceptions


class LvsClient(BaseClient):
    @property
    def default_domain(self):
        return settings.LVS_AGENT_DOMAIN

    @property
    def root(self):
        return self.profile[0]

    @property
    def date_time_pattern(self):
        return '%Y-%m-%d'

    @property
    def login_url(self):
        return self._url('auth')

    def login(self):
        self.headers.update(settings.DEFAULT_HEADERS)
        r = self.post(self.login_url, params={
            'account': self.username,
            'passwd': self.password
        })
        if 'alert' in r.text:
            error = re.findall("alert\('(.*)'\)", r.text)[0]
            raise exceptions.AuthenticationError(error)
        print(r.text)
        print(r.url)
        self.is_authenticated = True

    @staticmethod
    def get_name_rank(html):
        soup = BeautifulSoup(html, 'html.parser')
        info = soup.find(attrs={'id': 'login-info'}).find_all('span')
        info2 = soup.find(attrs={'class': 'rep navlink'})
        return info2.text.lower(), ''
        # return [i.text.lower().split('sub')[0] for i in info]

    @cached_property
    @login_required
    def profile(self):
        r = self.get(self._url('report/info'))
        return self.get_name_rank(r.text)

    @property
    def win_lose_url(self):
        return self._url('report/info')

    @staticmethod
    def parse_reports(html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            rows = soup.find('tbody').find_all('tr', attrs={'class': 'report-info'})

            for row in rows:
                cols = row.find_all('td')

                username = cols[1].text.lower()

                yield {
                    'username': username,
                    'turnover': LvsClient.format_float(cols[5].text),
                    'net_turnover': LvsClient.format_float(cols[12].text),
                    'commission': LvsClient.format_float(cols[7].text),
                    'win_lose': LvsClient.format_float(cols[9].text),
                }

        except AttributeError:
            pass

    @login_required
    def win_lose(self, from_date, to_date):

        r = self.get(self.win_lose_url, params={
            'start': self.format_date(from_date),
            'end': self.format_date(to_date),
            'timetype': 0,
            'servo': ''
        }, headers={'x-requested-with': 'XMLHttpRequest'})

        yield from self.parse_reports(r.text)
