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
    date = models.DateTimeField()

    def __str__(self):
        return self.title
    # OR THIS
    #def __str__(self):
        #return "Title: {0} \nImage: {1} \nSubtitle: {2} \nBody: {3} \nSource: {4} \nDate: {5} \nCategory: {6}".format(self.title, self.image, self.subtitle, self.body, self.source, self.date, self.category)
