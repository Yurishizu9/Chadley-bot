#dicord imports
import discord
from discord.ext import commands

#discord slash imports
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

# other imports
import os
import time
import json
import random
import requests
from github import Github 
from dotenv import load_dotenv # reads env. file
from bs4 import BeautifulSoup # web scrapper module
from cogs.src.WebScrapeAnime import WB_anime as anime # anime web scraper developed by me Yurishizu#1702

''' WebScrapeANime does not import'''


guild_ids = [746398170325581835]

class Anime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(
        name = 'anime',
        description = 'look for an anime',
        guild_ids = guild_ids,
        options = [
            create_option(
                name = 'title',
                description = 'the title of the anime you are looking for',
                option_type = 3,
                required = True
            )])
    async def _anime(self, ctx: SlashContext, title: str):
        '''--------------------------------------------------------------------------
        FUNCTIONS (ignore)
        '''
        

        
        
        '''--------------------------------------------------------------------------
        SEARCH for the anime 
        '''
        # start variable allows me to calculate execution speed
        start = time.time() 
        # anime_result contains a list of anime
        anime_results = anime.search(title)
        # this will be set to true only when author reacts with ✅
        selected = False


        '''--------------------------------------------------------------------------
        SHOW anime search results in an embed
        SELECT anime from the list
        '''
        if anime_results: # runs when there are anime search results
            end = round(time.time() - start, 2) # end of execution, speed calculation in miliseconds
            counter = 0 # will be used to browse through the list of animes
            result_msg = await ctx.send(embed = result_embed(anime_results, counter, end)) # send first embed msg
            
            # adding reactions to the message
            reaction_emojis = ['◀','▶','✅']
            for emoji in reaction_emojis:
                await result_msg.add_reaction(emoji)
            # makes sure the author is the only one that can intereact with msg 
            # by checking user, message id and reactions 
            def reaction_check(reaction, user):
                return user == ctx.author and result_msg.id == reaction.message.id and reaction.emoji in reaction_emojis

            # checks is user gas selected an anime
            anime_selected = False

            # Waiting for reaction
            while True: 
                try: # check reaction and user
                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 30.0, check = reaction_check)
                    # when reaction is ▶
                    #   remove reaction from author
                    #   minus 1 from counter
                    #   show the previous anime in the list
                    # if counter is less than 0
                    #   set counter to the length of anime_results 
                    #   and show the last aniime in the list
                    if reaction.emoji == '◀':
                        await result_msg.remove_reaction('◀', user)
                        counter -= 1
                        if  counter < 0:
                            counter = len(anime_results) - 1
                            await result_msg.edit(embed = result_embed(anime_results, counter, end))
                        else:
                            await result_msg.edit(embed = result_embed(anime_results, counter, end))
                    # when reaction is ▶
                    #   remove reaction from author 
                    #   add 1 to counter 
                    #   show the next anime in the list
                    # if we reach the end anime list 
                    #   set counter to 0 
                    #   and show the first anime result
                    if reaction.emoji == '▶':
                        await result_msg.remove_reaction('▶', user)
                        counter += 1
                        if  counter > len(anime_results) - 1:
                            counter = 0
                            await result_msg.edit(embed = result_embed(anime_results, counter, end))
                        else:
                            await result_msg.edit(embed = result_embed(anime_results, counter, end))
                    # select anime when reaction is ✅ 
                    # clear reactions
                    # selected = true
                    # break (waiting for reaction)
                    if reaction.emoji == '✅':
                        await result_msg.clear_reactions()
                        anime_selected = True
                        break
                except:
                    await result_msg.clear_reactions()
                    await ctx.send('you took too long', delete_after = 2.0)
                    break # stop waiting for reaction
        else: # no results, no anime found with the title
            await ctx.send(f'couldn\'t find any anime titles with `{title}`')
        
        
        '''--------------------------------------------------------------------------
        GET anime details
        SELECT anime episode
        '''
        if anime_selected: # if anime has been chosen from the list of results
            # get anime details
            anime_detail = anime.get_info(anime_results[counter]['link'])

            if anime_detail:
                # show anime details as an embed
                await result_msg.edit(embed = details_embed(anime_detail))
                # ask author to type an episode number
                player_control = await ctx.channel.send('**👇 ENTER EPISODE NUMBER**')

                # check if msg comes from the author
                def msg_check(msg):
                    return msg.author == ctx.author

                # Waiting for episode number
                while True:
                    try:# check if author responded
                        user_msg = await self.bot.wait_for('message', timeout = 15.0, check = msg_check)
                        # when authors message is a number and episode number exist
                        # delete authors message
                        # break while loop
                        if is_int(user_msg.content) and int(user_msg.content) <= len(anime_detail["episodes"]):
                            # episode number
                            episode = int(user_msg.content) 
                            # send pleaase wait msg 
                            await player_control.edit(content = '', embed = discord.Embed(title = 'PLEASE WAIT...', color=0x2F3136))
                            await user_msg.delete()
                            await result_msg.edit(content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif', embed = None)
                            break
                        else: # authors message is not a number
                            # ask author to try again
                            await player_control.edit(content = '**‼ INVALID NUMBER**')
                            time.sleep(0.2)
                            await player_control.edit(content = '**👇 ENTER EPISODE NUMBER**')
                        
                        await user_msg.delete() 
                    except:
                        # after 15 seconds stop waiting for episode number                     
                        # send a message to user then delete
                        await player_control.edit(content = '**‼ YOU TOOK LONG**')
                        time.sleep(0.5)
                        await player_control.delete()
                        # set episode to none
                        episode = None
                        # stop waiting for author to enter episode number
                        break
                
                
                '''-------------------------------------------------------------------------- 
                GET episode video src
                CREATE html website
                '''
                # this variable allows us to run the code below 
                # when user can still switch episode with emoji reactions
                allow_episode_switch = True
                # wait for episode switch
                while allow_episode_switch: 
                    print('loading episode:')
                    
                    # get video src        
                    if episode:
                        video_src = anime.get_video_src(anime_detail["episodes"][episode - 1])
                        
                        #create html file with anime info and episode link
                        anime_html_page = create_html(anime_detail, episode, video_src)

                        # generate a random link id
                        link_id = generate_id()
                        
                        ''' log into github and push a new html file '''
                        login = Github(GIT_TOKEN) # logged in with token
                        # fetches 'w-atch' repository on github account
                        repo = login.get_repo('anim-e/w-atch')
                        # a list of all files within the repository
                        contents = repo.get_contents('')
                        # check if html file already exist and delete it
                        # looping through each content
                        for c in contents:
                            if c.path == f'{link_id}.html':
                                repo.delete_file(c.path, 'Chadley BOT moderating', c.sha)
                        # push new html file
                        repo.create_file(f'{link_id}.html', 'Chadley BOT moderating', anime_html_page)


                        '''--------------------------------------------------------------------------
                        SEND link and update player_control embed message
                        '''
                        time.sleep(5)
                        await result_msg.edit(content = f'https://giddy-xylophone.cloudvent.net/{link_id}')
                        await player_control.edit(content = '', embed = episode_embed(anime_detail, episode))

                        # repost link if video embed does not show up
                        while not result_msg.embeds:
                            await result_msg.edit(content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')
                            await player_control.edit(embed = discord.Embed(title = 'PLEASE WAIT...', color=0x2F3136))
                            time.sleep(5)
                            await result_msg.edit(content = f'https://giddy-xylophone.cloudvent.net/{link_id}')
                            await player_control.edit(embed = episode_embed(anime_detail, episode))


                        '''--------------------------------------------------------------------------
                        CHANGING episodes
                        '''                 
                        # REACTIONS
                        # dont add reaction if anime only has one episode
                        # dont add right arrow if anime is on the latest episode
                        # add both reactions if episode is not last and is no the first
                        if len(anime_detail["episodes"]) > 1: # if there more than one episodes
                            if episode == len(anime_detail["episodes"]): # if on last episode
                                await player_control.add_reaction('◀')
                            elif episode == 1: # if on the first episode
                                await player_control.add_reaction('▶')
                            else: # not on the last episode or on the first
                                await player_control.add_reaction('◀')
                                await player_control.add_reaction('▶')
                        elif len(anime_detail["episodes"]) == 1:
                            # don't add reaction this is most likely a 
                            # movie since there is only one episode
                            # stop while loop
                            allow_episode_switch = False
                        
                        # overwrite reaction list
                        reaction_emojis = ['◀','▶'] 
                        def reaction_check2(reaction, user):
                            return user == ctx.author and player_control.id == reaction.message.id and reaction.emoji in reaction_emojis

                        # waiting for reaction
                        while True:    
                            try: # checks reaction and the user
                                reaction2, user2 = await self.bot.wait_for('reaction_add', timeout = 30.0, check = reaction_check2) 
                                print('user has reacted')
                                
                                # when reaction == '◀' 
                                #   go to the previous episode [episode - 1]
                                if reaction2.emoji == '◀':
                                    print('going to the previous episode')
                                    # remove minus one from episode number
                                    episode -= 1
                                    # clear rections
                                    await player_control.clear_reactions()
                                    # send a message
                                    await result_msg.edit(content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')
                                    await player_control.edit(embed = discord.Embed(title = f'LOADING EPISODE {episode}\nPLEASE WAIT...', color=0x2F3136))
                                    #stop waiting for reactions
                                    break

                                        
                                # when reaction == '▶' 
                                #   go to the next episode [episode + 1]
                                if reaction2.emoji == '▶':
                                    print('going to the next episode')
                                    # increment episode number by one
                                    episode += 1
                                    # clear reactions
                                    await player_control.clear_reactions()
                                    # send a message
                                    await result_msg.edit(content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')
                                    await player_control.edit(embed = discord.Embed(title = f'LOADING EPISODE {episode}\nPLEASE WAIT...', color=0x2F3136))
                                    # stop waiting for reactions
                                    break
                                    
                            except:
                                print('took too long to switch episode')
                                # clear reactions
                                await player_control.clear_reactions()
                                # stop while loop
                                allow_episode_switch = False
                                # update episode embed
                                embed=discord.Embed(
                                    title=f'{anime_detail["title"]}',
                                    description = f'Episode {episode}',
                                    color=0x2F3136)
                                embed.set_thumbnail(url=anime_detail["image"])
                                await player_control.edit(embed = embed)
                                break
                    else:
                        # stop while loop
                        allow_episode_switch = False
            else: # anime details doesn't load
                embed=discord.Embed(
                    title = '💔 Error: wall paint is too hard to scrape ',
                    description = f'```text\nerror: {anime_results[counter]["title"]} details page failed to load.\ncommand: /anime title: {title}```copy this error message and send it to Yurishizu#1702',
                    color=0x2F3136)                
                await result_msg.edit(content = None, embed = embed)     
            
# make an embed of anime results
def result_embed(results, counter, end = '?'):
    '''EMBED anime results
    ----------------------
    ----------------------
    Parameters
    ----------
    results : `list`
        takes a list of anime
    counter : `int`
        index of the anime in `results`
    end : `float`
        execution speed in milliseconds

    Returns
    -------
    embed : `Discord embed`
    '''
    embed=discord.Embed(
        title=f"Result #{counter + 1} ",
        color=0x2F3136)
    embed.set_image(url=results[counter]["image"])
    embed.add_field(
        name=results[counter]["title"],
        value=f'```text\n{results[counter]["details"]}```',
        inline=True)
    # the current time minus the time the execution started will give me exucution speed in milliseconds rounded to 2dp
    embed.set_footer(
        text=f'About {len(results)} results ({end} secconds)\nTIP: cycle through results with ◀ ▶\nTIP: select the anime with ✔')
    return embed

# make an embed of anime details
def details_embed(anime_detail):
    '''show anime detail as an embed
    --------------------------------
    --------------------------------

    Parameters
    ----------
    anime_detail : `dict`
        details of the anime
    
    Returns
    -------
    embed : `Discord embed`
    '''                
    embed=discord.Embed(
        title=f'{anime_detail["title"]}',
        description = f'```text\n{anime_detail["synopsis"][:200]}...```',
        color=0x2F3136)
    embed.set_thumbnail(url=anime_detail["image"])
    embed.set_footer(
    text=f'{anime_detail["type"]}・{anime_detail["status"]}・{anime_detail["season"]} {anime_detail["year"]}\n{anime_detail["genres"]}\n{anime_detail["studio"]}\n{len(anime_detail["episodes"])} episode(s)')
    return embed

# anime episode embed
def episode_embed(anime_detail, episode):
    '''show anime episode detail as an embed
    --------------------------------
    --------------------------------
    Parameters
    ----------
    anime_detail : `dict`
        details of the anime
    episode : `int`
        episode number of the anime
    
    Returns
    -------
    embed : `Discord embed`
    '''                
    embed=discord.Embed(
        title=f'{anime_detail["title"]}',
        description = f'Episode {episode}',
        color=0x2F3136)
    embed.set_thumbnail(url=anime_detail["image"])
    embed.set_footer(
    text = f'◀ previous episode\n▶ next episode')
    return embed

# create html page for anime
def create_html(anime_detail, episode, video_src):
            '''creates html website to watch anime episode
            ----------------------------------------------
            ----------------------------------------------
            Parameters
            ----------
            anime_detail : `dict`
                anime details
            episode : `int`
                current episode number
            video_src : `str`
                video source link

            Returns
            -------
            html : `str`
                html code for anime website
            '''            
            html = f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <meta property="og:url" content="{video_src}">
                    <meta property="og:video" content="{video_src}">
                    <meta property="og:video:secure_url" content="{video_src}">
                    <meta property="og:video:width" content="854">
                    <meta property="og:video:height" content="480">
                    <meta property="og:video:type" content="video/mp4">
                    <meta property="og:type" content="video.other">
                    <meta property="og:image" content="https://anim-e.tk/imgs/VIDEO%20READY.gif">
                    <link rel="stylesheet" media="screen" href="https://fontlibrary.org//face/kaushan-script" type="text/css"/>
                </head>
                <body style = "background-color: black; margin: 0; padding: 0;">
                    <video width="100%" controls autoplay>
                        <source src="{video_src}" type="video/mp4">
                    </video>
                    <h1 style = "color: white; font-family: 'KaushanScriptRegular', verdana;">{anime_detail["title"]} ・ Episode {episode}</h1>
                </body>
            </html>
            '''
            return html

# check if the input is an integer
def is_int(number):
    '''checks if input is an integer
    --------------------------------
    --------------------------------
    Parameters
    ----------
    number : `str`
        the users imput

    Returns
    -------
    True/False : `boolean`
    '''    
    try:
        int(number)
        return True
    except ValueError:
        return False

# generate random strings to be used a an id
def generate_id():
    generated_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=7))
    return generated_id


def setup(bot):
    bot.add_cog(Anime(bot))

load_dotenv()
GIT_TOKEN = os.getenv('GITHUB_TOKEN')