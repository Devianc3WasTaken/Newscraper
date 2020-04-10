from datetime import datetime, timezone
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from account.models import ScraperData

### PLACEHOLDER CLASSES FOR SOURCE. WILL FIX AFTER SCRAPER CONFIRMED TO BE WORKING PROPERLY ###
class Source:

    # @name : name of the source itself (eg, BBC)
    # @url : regular url of the source itself (eg, www.bbc.co.uk)
    # @container : class name of the html news container element
    # @headline : class name of the html headline container element
    # @text : class name of the html text container element
    # @link : class name of the html article link container element
    # @image: class name of the html image container element

    def __init__(self, name, url, container, headline, text, link, image):
        self.name = name
        self.url = url
        self.containerClass = container
        self.headlineClass = headline
        self.textClass = text
        self.linkClass = link
        self.imageClass = image

class Scraper:
    def __init__(self, s, c):
        self.driver = None
        self.sources = s
        self.categories = c

    def start(self):
        # Give options to chromedriver
        # --headless does not visibly display a window
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome()

    # search() performs a request for the target url and creates a GeneratedArticle(t, s, b, src) object
    def search(self):
        if (self.driver == None):
            self.start()

        # For every source...
        for i in range(len(self.sources)):
            # For every category...
            for j in range(len(self.categories)):
                try:
                    # Perform a request for the url and store the raw page source
                    urlRequest = self.sources[i].url + "/" + self.categories[j]
                    self.driver.get(urlRequest)
                    pageSource = self.driver.page_source
                except:
                    print("ERROR :: CONNECTION ERROR FOR CATEGORY " + self.categories[j])
                    continue

                # Run the source through the BeautifulSoup html parser so we can look for html elements
                soup = BeautifulSoup(pageSource, "html.parser")

                # For ease of use, I store the source details in a set of variables
                sourceContainer = self.sources[i].containerClass
                sourceHeadline = self.sources[i].headlineClass
                sourceText = self.sources[i].textClass
                sourceLink = self.sources[i].linkClass

                containerAmount = 2

                # Find all containers of news articles, then their respective elements for title, subtitle, source, body
                containers = soup.findAll(sourceContainer[0], {"class": sourceContainer[1]})[:containerAmount]

                print("\n\n[SCRAPING FROM: " + self.sources[i].name + "] : \n\n")

                for container in containers:
                    try:
                        headline = container.find(sourceHeadline[0], {"class": sourceHeadline[1]}).text
                        text = container.find(sourceText[0], {"class" : sourceText[1]}).text
                        link = container.find(sourceLink[0], {"class" : sourceLink[1]})['href']

                        print("\n\nHeadline: " + headline)
                        print("Text: " + text)
                        print("Source: " + link + "\n\n\n")

                    except AttributeError:
                        continue

        # Save the last scrape time and quit
        self.saveScrapeTime()
        self.driver.quit()

    #### Not in use currently
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

            print("last scrape: " + str(last))
            print("time now : " + str(now))
            print("diff in mins: " + str(diffInMins))

            if (diffInMins > 30):
                return False
            else:
                return True
        elif force == "force-yes":
            return True

    def getScrapeTime(self):
        last = ScraperData.objects.get(name="lastScraped")
        actualDate = last.lastScraped

        ### Debug
        #print("Last scraped: " + str(last))
        return actualDate

    def saveScrapeTime(self):
        last = ScraperData.objects.get(name="lastScraped")
        last.lastScraped = datetime.now(timezone.utc)
        last.save()
