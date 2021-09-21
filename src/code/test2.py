from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as bfs
from dotenv import load_dotenv
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


DB = "mongodb://aidchannel:aidchannel_password123456@51.77.134.195:27028/aidchannel?authSource=aidchannel"

client=MongoClient(DB)
db = client.aidchannel

class News:
    def __init__(self):
        # self.organizationId = organizationId
        self.options = Options()
        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        self.options.headless = True
        # self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.chrome = webdriver.Chrome(options=self.options)

        # self.chrome.get("")

    def getNews(self, organization_name):
        url = "https://news.google.com/search?q=" + organization_name
        self.chrome.get(url)
        return self.chrome.current_url

        sleep(5)
        # page=self.chrome.page_source
        # page_soup=bfs(page,"html.parser")
        # urls=page_soup.findAll("article",{'class':"EjqUne"})
        # data = []
        # for i in range(len(urls))  :
        #     if i==3 : break
        #     googleNewsUrl = "https://news.google.com"+urls[i].a['href'][1:]
        #     data.append(googleNewsUrl)
        # self.chrome.quit()
        # return data


def run():
    options = Options()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    #options.add_argument('--allow-running-insecure-content')
    #options.add_argument("--disable-extensions")
    #options.add_argument("--proxy-server='direct://'")
    #options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--proxy-server=socks5://132.148.129.108:5048')


    chrome = webdriver.Chrome(options=options)

    #chrome.get("https://news.google.com")
    #sleep(4)
    chrome.get("https://news.google.com/search?q=giz%20maroc")
    sleep(2)
    #myElem = WebDriverWait(chrome, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'EjqUne')))


    page=chrome.page_source
    page_soup=bfs(page,"html.parser")

    if True : return page_soup

    else :
        hrefs=page_soup.find("article",{'class':"EjqUne"}).a['href']

        # news = News()
        # urls = news.getNews("USAID")
        model = {
            "article_url": hrefs,
            "article_title": "test",
            # "organization": ObjectId(article["organization"]),
            # "country": ObjectId(article["country"]),
            "posted_at": "teest",
            "validation":0
        }
        #document = db.news.insert_one(model)
        return model 
    # return urls[1]
