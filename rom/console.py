from rom.request import requestURL
from rom.game import gamelist
import re
from rom.boto import boto

class Console(object):
    __games = []

    def __init__(self, name, link):
        self.__name = name
        self.__link = link

    def __str__(self):
        return "Console: {} Link: {}".format(self.__name, self.__link)

    @property
    def name(self):
        return self.__name

    @property
    def link(self):
        return self.__link

    @property
    def games(self):
        return self.__games

    def countGames(self):
        return len(self.__games)

    def run(self, isTest=False):
        gl = gamelist(self.__link)
        gl.run(isTest)
        self.__games = gl.games

    def to_s3(self):
        for game in self.__games:
            linkFile = game.getLinkFile()

            bin_file= requestURL().getFile(linkFile)
            extension = bin_file.headers['content-type'].split("/")[1]

            dest = str.lower(re.sub(r' ', '_', "file_roms/{}/{}".format(self.__name, game.name[0])))
            dest = dest + "/" + game.name + "." + extension

            boto().put(dest, bin_file.raw)

class consoleList(requestURL):
    __consoles = []

    def __init__(self, url, urlGameParam):
        self.__consoles = []
        self.__url = url
        self.__urlGameParam = urlGameParam
        self.getRequest(url)
        self.addConsole(self.consoleList())

    @property
    def consoles(self):
        return self.__consoles

    def getConsole(self, name):
        for console in self.__consoles:
            if console.name == name:
                return console

    def addConsole(self, console):
        for item in console:

            if (re.search(r"\/roms\/", item['href'])) is not None:
                self.__consoles.append(Console(item.get_text(), item['href'] + self.__urlGameParam))

    def consoleList(self):
        header = self._soup.find_all('ul', class_='nav')
        consoles = header[0].find_all('a', class_='dropdown__link')
        return consoles

    def countConsoles(self):
        return len(self.__consoles)

    def countGames(self):
        games = 0
        for i in self.__consoles:
            games = games + i.countGames()
        return games

    def dowloadGames(self):
        for console in self.__consoles:
            for game in console.games:
                print(game)
                game.run()

    def run(self):
        i = 1
        print("Inicio dowload games")
        # self.__consoles[8].run()
        for console in self.__consoles:
            print("{} de {} Obtendo jogos do console {}".format(i, self.countConsoles(), console.name))
            console.run()
            i += 1