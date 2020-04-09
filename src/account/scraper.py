from datetime import datetime, timezone
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from account.models import ScraperData

class Scraper:
    def __init__(self, s, c):
        self.driver = None
        self.source = s
        self.category = c
        self.generatedArticles = []

    def start(self):
        # Give options to chromedriver
        # --headless does not visibly display a window
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chromeOptions)

    # search() performs a request for the target url and creates a GeneratedArticle(t, s, b, src) object
    def search(self):
        if (self.driver == None):
            self.start()

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

    # Checks recent scrape time (the last time the scraper ran)
    def checkRecent(self, force=None):
        if force is None:
            last = self.getScrapeTime()
            now = datetime.now(timezone.utc)
            diffInMins = abs((now-last).seconds) / 60
            if (diffInMins > 30):
                return False
            else:
                return True
        elif force == "force-yes":
            return True

    ############ fix this ###################
    def saveScrapeTime(self):
        time = ScraperData(lastScraped=datetime.now())
        time.save()

    def getScrapeTime(self):
        last = ScraperData.objects.get(name="lastScraped")
        actualDate = last.lastScraped

        ### Debug
        #print("Last scraped: " + str(last))
        return actualDate
