import requests

from bs4 import BeautifulSoup as Soup

class XKCDManager:
    
    @staticmethod
    def getXKCDByID(ID):
        XKCDUrl = 'https://xkcd.com/'
        if ID != "latest":
            XKCDUrl += str(ID) + '/'
        response = requests.get(XKCDUrl)
        soup = Soup(response.content, "html.parser")
        comicObject = soup.find(id="comic").img
        return comicObject
    
    @staticmethod
    def getMessageText(comic):
        text = "```asciidoc"
        text += "\n" + str(comic["alt"])
        text += "\n=====================\n"
        text += str(comic["title"])
        text += "```"
        return text


if __name__ == "__main__":
    print(XKCDManager.getXKCDByID(123))
    print(XKCDManager.getXKCDByID("latest"))
