'''
--------------------------------------------
web scrape 4anime.to built by Yurishizu#1702
--------------------------------------------
'''

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import time

class WB_anime():
    '''WEB SCRAPER for `https://4anime.to`
    -------------------------------
    ---

    built by Yurishizu#1702

    Methods
    -------
    search(title) : `function`
        searches for anime titles and returns a list of anime results

    get_info(link) : `function`
        from anime link it returns information of that specific anime as a dictionary
        
    get_video_src(ep_link) : `function`
        from episode link it returns the anime video src link

    Attributes
    ----------
    : None
    '''    
    def search(title):
        '''SEARCH FOR ANIME AND GET RESULTS
        --------------------------------------
        ---
        Parameters
        ----------
        title : `str`
            title of the anime example: `'Boruto'`

        Returns
        -------
        anime_results : `list`
            a list of animes found results. Each anime/item will be in stored as a dictionary.
            
            ---
                [{
                'title': 'Boruto',
                'details': 'spring 2017, ongoing',
                'link': 'https://ani.me/boruto',
                'image': 'https://ani.me/boruto.png',
                }]
        '''        
        #request webpage and make a bs4 obj with page source code
        req = requests.get('https://4anime.to/?s='+title)
        webpage = BeautifulSoup(req.content, 'html.parser')

        links = webpage.select('#headerDIV_95 > a')
        images = webpage.select('#headerDIV_95 > a > img')
        titles = webpage.select('#headerDIV_95 > a > div')
        years = webpage.select('#headerDIV_95 > a > span:nth-child(3)')
        seasons = webpage.select('#headerDIV_95 > a > span:nth-child(5)')
        statuses = webpage.select('#headerDIV_95 > a > span:nth-child(7)')

        anime_results = []
        for link, image, title, year, season, status in zip(links, images, titles, years, seasons, statuses):
            anime_results.append({
                'title': title.text,
                'details': year.text+'・'+season.text+'・'+status.text,
                'link': link['href'],
                'image': image['src']
            })
        #print(json.dumps(anime_results, indent=4))
        return anime_results


    def get_info(link):
        '''GET ANIME DEATAILS
        ---------------------
        ---

        Parameters
        ----------
        link : `str`
            link of the anime example: `'https://ani.me/boruto'`

        Returns
        -------
        anime_details : `dict`
            dictionary of anime details

            ---
                {
                'title': 'Boruto',
                'image': 'https://ani.me/boruto.png',
                'synopsis': 'A new generation of ninja are ready...',
                'genres': 'Action, Adventure, Martial Arts...',
                'type': 'TV Series',
                'studio': 'Studio Pierrot',
                'season': 'Spring',
                'year': '2017',
                'status': 'Currently Airing',
                'language': 'Subbed',
                'episodes': {[
                    'https://ani.me/boruto/ep1',
                    'https://ani.me/boruto/ep2',
                    'https://ani.me/boruto/ep3'
                    ]}
                }
        '''        
    
        req = requests.get(link)
        webpage = BeautifulSoup(req.content, 'html.parser')

        title_ = webpage.select('#head > div.content > div > div > p')
        for x in title_: title_ = x.text

        image_ = webpage.select('#details > div.cover > img')
        for x in image_: image_ = 'https://4anime.to' + x['src']

        syn = webpage.find('div', attrs={'class': 'sixteen wide column synopsis'}).findAll('p')
        syn.pop(0)
        synopsis_ = ''
        for x in syn: synopsis_ += str(x.text)
        synopsis_.replace('\n', ' ')
        
        gen = webpage.find('div', attrs={'class': 'ui tag horizontal list'}).findAll('a')
        genres_ = ''
        for x in gen: genres_ += str(x.text) + ', '
        genres_ = genres_[:-2]

        type_ = webpage.select('#details > div.ui.info.list > div > div:nth-child(3) > a')
        for x in type_: type_ = x.text
        
        studios_ = webpage.select('#details > div.ui.info.list > div > div:nth-child(4) > a')
        for x in studios_: studios_ = x.text

        season_ = webpage.select('#details > div.ui.info.list > div > div:nth-child(5) > a:nth-child(2)')
        for x in season_: season_ = x.text
        
        year_ = webpage.select('#details > div.ui.info.list > div > div:nth-child(5) > a:nth-child(4)')
        for x in year_: year_ = x.text

        status_ = webpage.select('#details > div.ui.info.list > div > div:nth-child(6) > a')
        for x in status_: status_ = x.text

        language_ = webpage.select('#details > div.ui.info.list > div > div:nth-child(7) > a')
        for x in language_: language_ = x.text

        epi = webpage.find('ul', attrs = {'class': 'episodes range active'}).findAll('a')
        episodes_ = []
        for x in epi: episodes_.append(x['href'])

        '''
        print('1 title      ',title_)
        print('2 image      ',image_)
        print('3 type       ',type_)
        print('4 studios    ',studios_)
        print('5 season     ',season_)
        print('6 year       ',year_)
        print('7 status     ',status_)
        print('8 language   ',language_)
        print('9 synopsis   ',synopsis_)
        print('10 genres    ',genres_)
        print('-'*80)
        '''

        anime_details = {
            'title': title_,
            'image': image_,
            'synopsis': synopsis_,
            'genres': genres_,
            'type': type_,
            'studio': studios_,
            'season': season_,
            'year': year_,
            'status': status_,
            'language': language_,
            'episodes': episodes_ 
        }
        
        print(json.dumps(anime_details, indent=4))
        return anime_details
        

    def get_video_src(ep_link, chromedriver_path = './drivers/chromedriver.exe'):       
        '''GET VIDEO src
        ----------------
        ---

        Parameters
        ----------
        ep_link : `str`
            episode link of the anime example: `'https://ani.me/boruto/ep1'`
        chromedriver_path : `str`
            path 

        Returns
        -------
        video_src : `str`
            video source link example: `'https://ani.me/boruto/ep1.mp4'`
        '''        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging']) #disable logging
        driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)

        driver.get(ep_link)
        time.sleep(2)
        webpage = BeautifulSoup(driver.page_source, 'html.parser')
        video_src = webpage.find('video', attrs = {'id':'example_video_1_html5_api'})['src']
        #print(video_src)
        return video_src

#print()

