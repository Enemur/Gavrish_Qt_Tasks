import requests
from PyQt5.QtCore import QObject, pyqtSignal

from ArticleInfo import ArticleInfo
from Sites import Sites
from bs4 import BeautifulSoup


class AppModel(QObject):
    changeArticlesSignal = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.articlesModels: [ArticleInfo] = []
        self.sitesParsers = {
            Sites.Habr: self._parseHabr,
        }

    def parseSite(self, site: Sites, numberOfArticle: int):
        if site in self.sitesParsers:
            articleInfo = self.sitesParsers[site](numberOfArticle)
            self.articlesModels.append(articleInfo)
            self.changeArticlesSignal.emit()
        else:
            raise Exception("Method didn't implemented for this site")

    def _parseHabr(self, numberOfArticle: int) -> ArticleInfo:
        url = "https://habr.com/ru/post/" + str(numberOfArticle)
        page = requests.get(url)

        if page.status_code == 200:
            try:
                articleInfo = ArticleInfo()
                parser = BeautifulSoup(page.text)

                articleInfo.site = Sites.Habr
                articleInfo.url = url
                articleInfo.header = parser.find('span', {'class': 'post__title-text'}).text
                articleInfo.author = parser.find('a', {'class': 'user-info__fullname'}).text
                articleInfo.countLikes = int(parser.find('span', {'class': 'voting-wjt__counter_positive'}).text)
                articleInfo.countComments = int(parser.find('span', id='comments_count').text)

                return articleInfo
            except Exception as error:
                raise Exception("Error parsing site, site could be changed")
        else:
            raise Exception("Incorrect number of article")
