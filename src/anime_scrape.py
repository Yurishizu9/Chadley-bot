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
episode_num = int(input(f'eneter an episode number between (0-{anime_detail["episodes"]}): '))
anime_link = anime.get_episodes_link(animeid, episode_num)
print(json.dumps(anime_link, indent=4))

