import time
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.db import models

# Try to implement this with the Scraper
class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=120)
    body = models.CharField(max_length=5000)
    url = models.TextField()
    image = models.ImageField()
    category = models.CharField(max_length=100)
    favourite = models.BooleanField(default=False)
    def __str__(self):
        return self.title





# # Our article that gets generated at the end of a scraper search
# class GeneratedArticle:
#     def __init__(self, t, s, b, src):
#         self.title = t
#         self.subtitle = s
#         self.body = b
#         self.source = src
#
#     def __str__(self):
#         return "Title: {0} \nSubtitle: {1} \nBody: {2} \nSource: {3} \n".format(self.title, self.subtitle, self.body, self.source)

class Scraper:
    def __init__(self, s, c):
        # Give options to chromedriver
        # --headless does not visibly display a window
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.source = s
        self.category = c
        self.generatedArticles = []

    # search() performs a request for the target url and creates a GeneratedArticle(t, s, b, src) object
    def search(self):
        # Perform a request for the url and store the raw page source
        self.driver.get(self.source)
        pageSource = self.driver.page_source

        # Run the source through the BeautifulSoup html parser so we can look for html elements
        soup = BeautifulSoup(pageSource, "html.parser")

        ##### FROM HERE ON, ALL VALUES ARE HARD CODED FOR THE SAKE OF TESTING THE SCRAPER. #####

        # Find all containers of news articles, then their respective elements for title, subtitle, source, body
        containers = soup.findAll("div", {"class": "fc-item__container"})
        for container in containers:
            try:
                title = container.find("span", {"class": "js-headline-text"}).text
                subtitle = container.find("div", {"class" : "fc-item__standfirst"}).text
                source = container.find("a",{"class" : "fc-item__link"})['href']
                body = self.getBody(source)
                article = GeneratedArticle(title, subtitle, body, source)
                self.generatedArticles.append(article)

                # Prints the object itself: title, subtitle, body, source texts
                print(article)

                self.driver.quit()
            except AttributeError:
                continue

        self.driver.quit()

    def getBody(self, url):
        self.driver.get(url)
        pageSource = self.driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")

        bodySource = soup.findAll("p")
        bodyText = ""
        for paragraph in bodySource:
            bodyText += paragraph.text
        return bodyText


