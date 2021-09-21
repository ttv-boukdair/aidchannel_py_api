import requests
from bs4 import BeautifulSoup as bfs



def forwardUrl( googleNewsUrl):
	#r = requests.Session()
	page=requests.get(googleNewsUrl)
	print(page.url)
	return page.url
def run():
	url = "https://news.google.com/search?q=USAID%20Morocco%20when%3A50d&hl=fr&gl=MA&ceid=MA%3Afr"
	
	headers = {
	'authority': 'scrapeme.live',
	'dnt': '1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-fetch-site': 'none',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-user': '?1',
	'sec-fetch-dest': 'document',
	'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
	page=requests.get(url,headers=headers)

	#if True : return page.text

	 
	page_soup = bfs(page.text,"html.parser")

	urls=page_soup.findAll("article",{'class':"EjqUne"})

	dates=page_soup.findAll("time",{'class':"WW6dff uQIVzc Sksgp"})

	titles=page_soup.findAll("h3",{'class':"ipQwMb ekueJc RD0gLb"})
	articles=[]

	for i in range(len(urls))  :
		
		if i==3 : break
		googleNewsUrl = "https://news.google.com"+urls[i].a['href'][1:]
		
		#articleUrl = forwardUrl(googleNewsUrl)
		title = titles[i].text
		date = dates[i]["datetime"]


		articles.append({
		"article_url": googleNewsUrl,
		"organization": " ",
		"country": " ",
		"title": title,
		"posted_at": date})

	return articles

