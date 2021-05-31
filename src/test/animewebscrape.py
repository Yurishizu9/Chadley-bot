from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
import time
import json


'''  
Objective::: SEARCH FOR ANIME WITH KEYWORD
Input::: keyword
Output::: a list of dictionaries with the animes found. which include details such as their (names, links, images, other infromation)
'''
def search_for_anime():
	web_page = requests.get('https://animenetwork.net/search/?q=promised+neverland&t=anime')
	bs4_obj = BeautifulSoup(web_page.content, 'html.parser')

	#links to animes that were found
	links = bs4_obj.select('#content-wrapper > div > div > div > div.col-12.row.anime-list > div > div > div.channels-card-body > div.channels-title > a')
	#small information about each anime
	infos = bs4_obj.select('#content-wrapper > div > div > div > div.col-12.row.anime-list > div > div > div.channels-card-body > div.channels-view')
	#picture of the anime found
	imgs = bs4_obj.select('#content-wrapper > div > div > div > div.col-12.row.anime-list > div > div > div.channels-card-image > a > img')
	#anime fouind are stored in a list with their coresponding details
	anime_list = []
	for link, info, img in zip(links, infos, imgs):
		anime_list.append({
			'name': link.text,
			'link': 'https://animenetwork.net' + link['href'],
			'img': img['src'],
			'info': info.text.strip().upper()
			})
	return anime_list


'''  
Objective::: SELECT ANIME FROM LIST
Input::: Anime list
Output::: the chosen anime url
'''
def select_anime(anime_list):
	#select anime using the counter
	counter = 1
	for x in anime_list:
		print(f'{counter}) {x["name"]}\n{x["info"]}\n')
		counter += 1
	selected = int(input(f'pick an anime by the number 1 - {len(anime_list)} ')) - 1
	anime_url = anime_list[selected]['link'] 
	print(anime_url,'\n')
	return anime_url


''' 
Objective::: GET INFORMATION ON SELECTED ANIME
Input::: anime url 
Output::: dictionary containing the following (
synopsis, episodes, duration, status, premiered, PG rating, MAL rating, english name, japanese name, image, episode links)
'''
def get_anime_information(anime_url):
	anime_webpage = requests.get(anime_url)
	bs4_obj = BeautifulSoup(anime_webpage.content, 'html.parser')

	# save the links of every episode in a list
	useless_ep_link_tags = bs4_obj.select('#episodes > div > div > div > div.video-card-body > div.video-title > a')
	#episode number, allows float example episode 5.5 for promised neverland
	ep_nums = bs4_obj.select('#episodes > div > div > div > div.video-card-body > span')
	#synopsis 
	synopsis = bs4_obj.select('#information > div > div > table > tbody > tr:nth-child(1) > td > span')
	#duration
	duration = bs4_obj.select('#information > div > div > table > tbody > tr:nth-child(5) > td > span')
	#status
	status = bs4_obj.select('#information > div > div > table > tbody > tr:nth-child(4) > td > span')
	#premiered
	premiered = bs4_obj.select('#information > div > div > table > tbody > tr:nth-child(2) > td > span')
	#pg rating
	pg_rating = bs4_obj.select('#content-wrapper > div > div.single-channel-nav > nav > span.badge.badge-primary')
	#MAL rating
	mal_rating = bs4_obj.select('#content-wrapper > div > div.single-channel-nav > nav > span:nth-child(2)')
	#english name 
	eng_name = bs4_obj.select('#content-wrapper > div > div.single-channel-nav > nav > a > span.english')
	#japanese name
	jap_name = bs4_obj.select('#content-wrapper > div > div.single-channel-nav > nav > a > span.japanese')
	#image
	image = bs4_obj.select('#content-wrapper > div > div.single-channel-image > div.channel-profile > img')

	ep_links = []
	anime_detail = {}

	for ep_num, link in zip(ep_nums, useless_ep_link_tags):
		ep_links.append({ep_num.text:'https://animenetwork.net'+link['href']})
	ep_links.reverse()# episode list has to be reversed as it in descending order

	for syn, dur, sts, prm, pgr, mal, eng, jap, img in zip(synopsis, duration, status, premiered, pg_rating, mal_rating, eng_name, jap_name, image):
		anime_detail.update({
			'synopsis': syn.text.strip(),
			'latest episode': list(ep_links[-1].keys())[0], #gets the lasst ep num
			'duration': dur.text.strip(),
			'status':	sts.text.strip(),
			'premiered': prm.text.strip(),
			'pg rating': pgr.text.strip(),
			'mal rating': mal.text.strip(),
			'eng name': eng.text.strip(),
			'jap name': jap.text.strip(),
			'image': img['src'],
			'episode links': ep_links
		})
	print(json.dumps(anime_detail, indent=4))
	return anime_detail


'''  
Objective::: SELECT ANIME EPISODE
Input::: Anime detail
Output::: episode url
'''
def select_anime_episode(anime_detail):
	ep = input(f'\ntype an episode number (latest episode is {anime_detail["latest episode"]}) ')
	for x in anime_detail['episode links']:
		if ep in x:
			import webbrowser
			webbrowser.open(x[ep])
			return x[ep]


''' 
Objective::: GET VIDEO src FOR THE EPISODE
Input::: episode url 
Output::: dictionary containing the following (video src, video thumbnail, episode name, anime image, anime name)
'''
def anime_video_src(selected_ep = 'https://4anime.to/hetalia-world-stars-episode-03?id=45445'):
	
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
	options = webdriver.ChromeOptions()
	options.headless = True
	options.add_argument(f'user-agent={user_agent}')
	options.add_argument("--window-size=1920,1080")
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--allow-running-insecure-content')
	options.add_argument("--disable-extensions")
	options.add_argument("--proxy-server='direct://'")
	options.add_argument("--proxy-bypass-list=*")
	options.add_argument("--start-maximized")
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(executable_path="./drivers/chromedriver.exe", options=options)

	driver.get(selected_ep)
	time.sleep(2)
	#print(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div[2]/div/div[2]').get_attribute('innerHTML'))
	
		
	
	
	driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/section/div/div[2]/div/div/div/div[5]').click()
	time.sleep(3)
	test = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/section/div/div[2]/div/div/div/video')
	test.screenshot('thumb.png')
	driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/section/div/div[2]/div/div/div/div[5]').click()

	#video_page = requests.get(selected_ep)
	bs4_obj = BeautifulSoup(driver.page_source, 'html.parser')
	
	video_src = bs4_obj.select('#example_video_1_html5_api')
	for x in video_src: print(x['src'])
	driver.quit()
	
	'''iframe is hidden'''
	'''iframe only becomes visible when the js file is run'''
	#print(video_src)
    '''
	i will use 4anime to webscrape, will have to redo this from scratch
	'''








'''
#returns a list of animes found
list_of_animes = search_for_anime() 
#returns the url of your chosen anime
chosen_anime_url = select_anime(list_of_animes)
#return anime details
anime = get_anime_information(chosen_anime_url)
#get episode url
episode_url = select_anime_episode(anime)

if not episode_url:
	print('episode not found')
else:
	beans = anime_video_src(episode_url)
'''
anime_video_src()
'''ongoing anime states they have 0 episodes, some anime have half episodes...
to fix this issue every episode link will have its episode number next to it as a float...for things like episode 5.5
episode number: link will be stored in a dictiuonary then put into a list so it can be reversed 
to get the episode number ill have to put episode_list through a for loop and look at each dictionary for the key value that matches 
the episode number we are looking for'''

