import requests
from bs4 import BeautifulSoup
from .chrome import *
import urllib

class google:
    def __init__(self):
        self.chrome = chrome()

    def search(self,query):
        self.chrome.reset()
        with requests.session() as c:
            url = 'https://www.google.com/search'
            query = {'q': query}
            url += '?' + urllib.parse.urlencode(query)
            self.chrome.driver.get(url)
            urllink = self.chrome.driver.page_source
            soup = BeautifulSoup(urllink)
            output = []
            for searchWrapper in soup.find_all('div', {'class':'g'}):
                if searchWrapper.find('div', {'class':'r'}):
                    url = searchWrapper.find('div', {'class':'r'}).find('a')["href"] 
                    text = searchWrapper.find('div', {'class':'r'}).find('h3').text.strip()
                    if not searchWrapper.find('', {'class':'st'}):
                        continue
                    desc = searchWrapper.find('', {'class':'st'}).text.strip()
                    result = {'text': text, 'url': url,'desc': desc}
                    output.append(result)

            return(output)
