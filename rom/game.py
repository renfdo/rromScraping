from rom.request import requestURL

class gamelist(requestURL):
    __games = []

    def __init__(self, url):
        # Load the page One
        self.getRequest(url)
        self.setPages()

    @property
    def games(self):
        return self.__games

    @property
    def actualPage(self):
        return self.__actualPage

    @property
    def finalPage(self):
        return self.__finalPage

    def gameList(self):
        listTable = self._soup.find('table', class_="table").tbody.find_all('a')
        return listTable

    def addGame(self, r):
        for item in r:
            self.__games.append(Game(item.get_text(), item['href']))

    def setPages(self):
        pagination = self._soup.find('div', class_='pagination').ul
        self.__actualPage = int(pagination.find('li', class_='pagination__el is-active').get_text().strip())
        pages = list(pagination.find_all('li', class_='pagination__el'))

        if pages[-1].get_text().strip() == "Next":
            self.__finalPage = int(pages[-2].get_text().strip())
        else:
            self.__finalPage = int(pages[-1].get_text().strip())

    def run(self, isTest=False):
        for i in range(1, self.__finalPage):
            print("\t\tPágina {} de {}".format(self.__actualPage, self.__finalPage))
            self.addGame(self.gameList())

            if isTest:
                break

            oldParam = "page={}".format(str(self.__actualPage))
            newParam = "page={}".format(str(self.__actualPage + 1))

            self._url = self._url.replace(oldParam, newParam)

            self.getRequest(self._url)
            self.__actualPage += 1

class Game(requestURL):

    def __init__(self, name, link):
        self.__name = name
        self.__link = link

    def __str__(self):
        return "Jogo: {} Link: {}".format(self.__name, self.__link)

    @property
    def name(self):
        return self.__name

    @property
    def link(self):
        return self.__link

    @property
    def linkFile(self):
        return self.__linkFile

    def getLinkFile(self):
        self.getRequest(self.__link)
        linkDowload = self._soup.find('a', id='download_link')['href']

        self.__linkDowload = self.getRequest(linkDowload)

        self.__linkFile = self._soup.find('a', class_="wait__link")['href']

        return self.__linkFile
        # boto= boto('name', file)
        # boto.put()