from cloudscraper.user_agent import User_Agent
from gogoanimeapi import gogoanime as anime
import json

querry = input('search for an anime: ')
anime_search = anime.get_search_results(querry)
print(anime_search)

# pick anime
counter = 1
for x in anime_search: 
    print(f'{counter}) {x["name"]}')
    counter += 1
sel = int(input('enter a number: '))
animeid = anime_search[sel - 1]["animeid"]

anime_detail = anime.get_anime_details(animeid)
print(f'\n{json.dumps(anime_detail, indent=4)}\n')


# pick episode
episode_num = int(input(f'enter an episode number between (1-{anime_detail["episodes"]}): '))
anime_link = anime.get_episodes_link(animeid, episode_num)
print(json.dumps(anime_link, indent=4))




'''
import cloudscraper
import helheim
from dotenv import load_dotenv # reads env. file
import os
url = 'https://streamani.net/download?id=OTg0NjQ=&typesub=Gogoanime-SUB&title=Boruto%3A+Naruto+Next+Generations+Episode+9'


load_dotenv()
HELHEIM_KEY = os.getenv('HELHEIM_KEY')

helheim.auth(HELHEIM_KEY)

def injection(session, response):
    if helheim.isChallenge(session, response):
        # solve(session, response, max_tries=5)
        return helheim.solve(session, response)
    else:
        return response

session = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome', # we want a chrome user-agent
        'mobile': False, # pretend to be a desktop by disabling mobile user-agents
        'platform': 'windows' # pretend to be 'windows' or 'darwin' by only giving this type of OS for user-agents
    },
    requestPostHook=injection,
    captcha={
        'provider' : 'vanaheim'
    }
)


print(session.get(url).text)
'''