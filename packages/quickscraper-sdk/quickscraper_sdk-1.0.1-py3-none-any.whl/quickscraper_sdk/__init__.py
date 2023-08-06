"""
quickscraper-sdk
~~~~~~
The quickscraper-sdk package - a Python package template project that is intended
to be used as a cookie-cutter for developing new Python packages.
"""

from .constant import BASE_URL


class QuickScraper:
    def __init__(self, access_token):
        self.access_token = access_token
        self.parse_url = BASE_URL + 'parse'

    def prepareRequestUrl(self):
        print(self.parse_url)
