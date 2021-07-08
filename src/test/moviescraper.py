import requests
from bs4 import BeautifulSoup
import cloudscraper

def search_soap2day(movie):
	site_url = "https://soap2day.cc"
	search_url = site_url+"/search/keyword/"+movie.replace(' ','%20')
	results_page = BeautifulSoup(requests.get(search_url).text,'lxml')
    
	print(results_page.find_all('div',class_="col-lg-2 col-md-3 col-sm-4 col-xs-6 no-padding"))
    
	for result in results:
		url = site_url+result.a['href']
		result_page = BeautifulSoup(requests.get(url).text,'lxml')
		title = result_page.find('div',class_='col-sm-12 col-lg-12 text-center').h4.text
		desc = result_page.find('p',id='wrap').text.strip()
		img = result_page.find('div',class_='thumbnail').img['src']
		print(url,title,desc,img)


def movie(title = 'harry potter'):
    url = "https://soap2day.cc/search/keyword/" + title
    req = scraper.get(url)
    web_results = BeautifulSoup(req.content, 'html.parser')
    #web_results = web_results.select('body > div.content > div:nth-child(3) > div > div.col-sm-8.col-lg-8.col-xs-12 > div:nth-child(1) > div.panel-body > div > div > div > div')
    print(web_results)

#movie()
scraper = cloudscraper.create_scraper(
  captcha={
    'provider': '2captcha',
    'api_key': '86cf45f835d902c1e12896f8e4384b60'
  })
print('hey')
import requests
url = 'https://cdn2.cloud9xx.com/user1342/c2c793835d1264cb7a5773e2de1fa3f4/EP.1.1080p.mp4?token=JarxdPTVBzX7IBvQObtQAg&expires=1625844454&id=99211'

resp = requests.head(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
print(resp.headers)
print(resp.cookies)
