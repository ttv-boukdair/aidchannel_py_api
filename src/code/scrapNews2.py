from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as bfs
from dotenv import load_dotenv
from pymongo import MongoClient
# from bson.objectid import ObjectId


DB = "mongodb://aidchannel:aidchannel_password123456@51.77.134.195:27028/aidchannel?authSource=aidchannel"

client=MongoClient(DB)
db = client.aidchannel


class News:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--ignore-certificate-errors')
        self.chrome = webdriver.Chrome(options=self.options)


    def getNews(self, organization_id, organization_name, country_id):
        url = "https://news.google.com/search?q=" + organization_name
        self.chrome.get(url)
        sleep(5)
        page=self.chrome.page_source
        page_soup=bfs(page,"html.parser")

        urls = page_soup.findAll("article",{'class':"EjqUne"})
        if urls==None: return None
        dates = page_soup.findAll("time",{'class':"WW6dff uQIVzc Sksgp"})
        titles = page_soup.findAll("h3",{'class':"ipQwMb ekueJc RD0gLb"})

        articles = []
        for i in range(len(urls))  :
            if i==3 : break
            try:
                googleNewsUrl = "https://news.google.com"+urls[i].a['href'][1:]
                # articleUrl = self.forwardUrl(googleNewsUrl)
                title = titles[i].text
                date = dates[i]["datetime"]

            except Exception as e:
                # print("could not forward url ", e)
                continue

            articles.append({
                "article_url": googleNewsUrl,
                "organization": organization_id,
                "country": country_id,
                "title": title,
                "posted_at": date})
        # print(articles)
        self.chrome.close() # one tab
        self.chrome.quit()
        return articles

    def forwardUrl(self, googleNewsUrl):
        self.chrome.get(googleNewsUrl)
        sleep(2)
        url = self.chrome.current_url
        return url




def get_orgs_infos():

	# Organizations=db.organizations.find({"head_office_id":{"$nin":[None]}})
	infos=[]
	for org in Organizations:
		info= {
            # "orgId": str(org["_id"]),
            "orgName": org['name'],
            # "countryId": str(org['country'])
        }
		infos.append(info)

	return infos


def saveOrgArticles(orgInfo):
    news = News()
    articles =  news.getNews(orgInfo["orgId"], orgInfo["orgName"], orgInfo["countryId"])
    if len(articles)==0:return []
    res = []
    for article in articles:
        model = {
    		"article_url": article["article_url"],
            "article_title": article["title"],
            # "organization": ObjectId(article["organization"]),
            # "country": ObjectId(article["country"]),
            "posted_at": article["posted_at"],
            "validation":0
    	}
        res.append(model)
        document = db.news.insert_one(model)
    return res


def run():
    try:
        # orgInfos = get_orgs_infos()
        info= {
            "orgId": "",
            "orgName": "USAID",
            "countryId": ""
        }
        data = saveOrgArticles(info)
    except Exception as e:
        data = e
    return data


