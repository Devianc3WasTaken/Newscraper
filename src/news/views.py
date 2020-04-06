from django.shortcuts import render

# Create your views here.
import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

def scrape():

    #session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
    page = requests.get("https://www.theguardian.com/uk-news")
    soup = BeautifulSoup(page.content, 'html.parser')

    weblinks = soup.find_all('article')

    pagelinks = []

    for link in weblinks[5:]:
        url = link.contents[0].find_all('a')[0]
        pagelinks.app


    soup = BeautifulSoup(content, "html.parser")

    posts = soup.find_all('div', {'class': 'u-unstyled l-row'}) # return a list
    link = "nulldf"
    for i in posts:
        link = i.find_all('a', {'u-unstyled l-row  l-row--cols-4 fc-slice fc-slice--'})[1]
        #image_source = i.find_all('img',{'class', 'qa-srcset-image'})['data-src']

        print(link)
   # print(image_source)

scrape()