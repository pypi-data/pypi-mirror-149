import re

import requests
from pyquery import PyQuery

__version__ = '0.1.0'


def verify(douban_id, sig_pattern):
    page = _get_dou_people_page(douban_id)
    signature = _extract_signature(page)
    return re.match(sig_pattern, signature) is not None


def _get_dou_people_page(douban_id):
    url = f'https://www.douban.com/people/{douban_id}'
    resp = requests.get(url)
    return resp.content


def _extract_signature(page):
    pq = PyQuery(page)
    return pq('#display').text()