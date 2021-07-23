import requests
from bs4 import BeautifulSoup
import cloudscraper
import helheim
from dotenv import load_dotenv # reads env. file
import os

load_dotenv()
HELHEIM_KEY = os.getenv('HELHEIM_KEY')


def injection(session, response):
	if helheim.isChallenge(session, response):
		return helheim.solve(session, response)
	else:
		return response

helheim.auth(HELHEIM_KEY)
session = cloudscraper.create_scraper(
	browser={
		'browser': 'chrome', # we want a chrome user-agent
		'mobile': False, # pretend to be a desktop by disabling mobile user-agents
		'platform': 'windows' # pretend to be 'windows' or 'darwin' by only giving this type of OS for user-agents
	},
	requestPostHook=injection,
	captcha={
		'provider' : 'vanaheim'
	})


def search_soap2day(movie):
	site_url = "https://soap2day.cc"
	search_url = site_url + "/search/keyword/" + movie.replace(' ','%20')
	results_page = BeautifulSoup(requests.get(search_url).text,'lxml')
    
	print(results_page.find_all('div',class_="col-lg-2 col-md-3 col-sm-4 col-xs-6 no-padding"))
    
	for result in results:
		url = site_url+result.a['href']
		result_page = BeautifulSoup(requests.get(url).text,'lxml')
		title = result_page.find('div',class_='col-sm-12 col-lg-12 text-center').h4.text
		desc = result_page.find('p',id='wrap').text.strip()
		img = result_page.find('div',class_='thumbnail').img['src']
		print(url,title,desc,img)

''''''
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
url = 'https://cdn5.cloud9xx.com/user1342/90cdb2a8dd302bea073b94a37f18f64b/EP.1.720p.mp4?token=YO2iXO-8uRT1m7jEDvea0w&expires=1625744905&id=82204'

resp = requests.head(url, headers={
	'Accept-Encoding': 'identity;q=1, *;q=0',
	'Range': 'bytes=0-',
	'Referer': 'https://anim-e.tk/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' })
print(resp.headers)
print(resp.request.headers)
print(resp)
print(resp.text)
