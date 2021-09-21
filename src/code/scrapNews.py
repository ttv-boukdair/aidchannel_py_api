from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bfs
from dotenv import load_dotenv
from pymongo import MongoClient

DB = "mongodb://aidchannel:aidchannel_password123456@51.77.134.195:27028/aidchannel?authSource=aidchannel"

client=MongoClient(DB)
db = client.aidchannel


def forwardUrl(googleNews_url, chrome):
	chrome.get(googleNews_url)
	time.sleep(2)
	url = chrome.current_url
	return url




def getNews(organizationId, organizationName, countryId, chrome):
	url = "https://github.com"
	chrome.get(url)
	actualTitle = chrome.title
	return actualTitle
	time.sleep(2)
	page=chrome.page_source
	page_soup=bfs(page,"html.parser")

	urls=page_soup.findAll("div",{'class':"NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"})
	if urls==None:
		return None
	dates=page_soup.findAll("time",{'class':"WW6dff uQIVzc Sksgp"})
	titles=page_soup.findAll("h3",{'class':"ipQwMb ekueJc RD0gLb"})

	articles = []

	for i in range(len(urls))  :
		if i==3 : break

		try:
			googleNewsUrl = "https://news.google.com"+urls[i].div.article.a['href'][1:]
			articleUrl = forwardUrl(googleNewsUrl, chrome)
			title = titles[i].text
			date = dates[i]["datetime"]

		except Exception as e:
			continue

		articles.append({
                "article_url": articleUrl,
                "organization": organizationId,
                "country": countryId,
                "title": title,
                "posted_at": date
            })
	print(articles)
	return articles

def getOrgInfo():

	Organizations=db.organizations.find({"head_office_id":{"$nin":[None]}})
	infos=[]
	for org in Organizations:
		info= {
            "orgId": str(org["_id"]),
            "orgName": org['name'],
            "countryId": str(org['country']),
        }
		infos.append(info)

	return infos

def saveOrgArticles(orgInfo, chrome):
	articles =  getNews(orgInfo["orgId"], orgInfo["orgName"], orgInfo["countryId"], chrome)
	res = []
	if len(articles)==0:
		return []
	for article in articles :
		model = {
    		"article_url": article["article_url"],
            "article_title": article["title"],
            "organization": article["organization"],
            "country": article["country"],
            "posted_at": article["posted_at"],
            "validation":0
    	}
		res.append(model)
		document = db.news.insert_one(model)
	return res

def addOrgArticles():
	options = Options()
	#options.add_argument("--disable-notifications")
	options.add_argument('--disable-gpu')
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	chrome = webdriver.Chrome(options=options)
	res = []
	# OrgInfos =  getOrgInfo()
	
	# # return OrgInfos
	# for orginfo in OrgInfos[:3] :
	# 	time.sleep(10)
	# 	res += saveOrgArticles(orginfo, chrome)
	res = getNews("","USAID","", chrome)
	chrome.close()
	return res
#addOrgArticles()

