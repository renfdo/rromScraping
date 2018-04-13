import requests
from bs4 import BeautifulSoup

class requestURL(object):
    _soup = None

    def getRequest(self, url):
        self._url = url
        self.__request = requests.get(url)
        self._soup = BeautifulSoup(self.__request.content, 'html.parser')

    def getFile(self, url):
        request = requests.get(url, stream=True)
        request.raw.decode_content = True
        return request
