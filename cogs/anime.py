# discord imports
import discord
from discord.ext import commands

# discord slash commands import
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

# other imports
from src.gogoanimeapi import gogoanime as anime
from dotenv import load_dotenv # reads env. file
import os
from github import Github 
import random
import time


def genres1():
    return ['action', 
            'adventure', 
            'cars', 
            'comedy', 
            'dementia', 
            'demons', 
            'drama', 
            'dub', 
            'ecchi', 
            'fantasy', 
            'game', 
            'harem', 
            'hentai', 
            'historical', 
            'horror', 
            'josei', 
            'kids', 
            'magic', 
            'martial-arts', 
            'mecha', 
            'military', 
            'music']

def genres2():
    return ['mystery', 
            'parody', 
            'police', 
            'psychological', 
            'romance', 
            'samurai', 
            'school', 
            'sci-fi', 
            'seinen', 
            'shoujo', 
            'shoujo-ai', 
            'shounen-ai', 
            'shounen', 
            'slice-of-life', 
            'space', 
            'sports', 
            'super-power', 
            'supernatural', 
            'thriller', 
            'vampire', 
            'yaoi', 
            'yuri']


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(
        name = 'anime',
        description = 'search for an anime',
        options = [
            create_option(
                name = 'title',
                description = 'the title of the anime',
                option_type = 3,
                required =True,
            )])
    async def anime(self, ctx: SlashContext, title: str):
        # search for anime
        anime_search_result = anime.get_search_results(query = title)
        
        # check for 404 and 204 errors
        if 'status' in anime_search_result:
            if anime_search_result["status"] == '204':
                await ctx.send(f'No search results found for `{title}`' )
            if anime_search_result["status"] == '404':
                await ctx.send(f'I\'m having connection issues... please try again later...' )
        else:
            # organise anime results
            counter = 1
            results = ''
            for x in anime_search_result:
                results += f'`{counter}.` `{x["name"]}`\n'
                counter += 1
            
            # show anime results
            embed = discord.Embed(
                title = f'search results for __{title}__',
                description = results,
                color = 0x2F3136)
            embed.set_footer(text = '👇ENTER A NUMBER BELOW  数字を入力')

            msg_results = await ctx.send(embed = embed)

            # waiting for user to pick an anime by number
            def msg_checker(msg):
                '''checks if message is sent from the author'''
                return msg.author == ctx.author
            
            anime_id = None
            while True:
                try:
                    user_msg = await self.bot.wait_for('message', timeout = 15.0, check = msg_checker)
                    if int_checker(user_msg.content) and int(user_msg.content) <= len(anime_search_result):
                        # get the animeid of the selected anime
                        anime_id = anime_search_result[int(user_msg.content) - 1]["animeid"]
                        await user_msg.delete()
                        break
                    else:
                        await msg_results.edit(embed = embed.set_footer(text = '‼INVALID NUMBER try again...  再試行...'))
                        await user_msg.delete()    
                except:
                    await msg_results.edit(embed = embed.set_footer(text = ''))
                    break
                
            # show anime details
            if anime_id:
                anime_detail = anime.get_anime_details(anime_id)
                
                # format synopsis and genre and alternative name
                synopsis = '' if 'No synopsis information has been added to this title' in anime_detail["plot_summary"] else f'```{anime_detail["plot_summary"][1:200]}...```'
                genres = anime_detail["genre"].replace('[', "").replace(']', '').replace("'", "")
                alt_name = anime_detail["other_names"].replace('Other name: ', '')

                # make embed and show anime details
                embed = discord.Embed(
                    title=f'{anime_detail["title"]}',
                    description = synopsis,
                    color = 0x2F3136)
                embed.set_thumbnail(url = anime_detail["image_url"])
                embed.set_footer(
                text = f'{alt_name}\n{anime_detail["type"]}・{anime_detail["status"]}・{anime_detail["year"]}\n{genres}\n{anime_detail["episodes"]} episode(s)')
                await msg_results.edit(embed = embed)
                
                # wait for episode
                msg_results2 = await ctx.channel.send('`👇ENTER EPISODE NUMBER BELOW`  `エピソード番号を入力`')

                while True:
                    try: 
                        user_msg2 = await self.bot.wait_for('message', timeout = 15.0, check = msg_checker)
                        if int_checker(user_msg2.content) and int(user_msg2.content) <= int(anime_detail["episodes"]):
                            episode_num = int(user_msg2.content)
                            await user_msg2.delete()
                            await msg_results.edit(embed = None, content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')
                            await msg_results2.edit(content = '`LOADING VIDEO PLEASE WAIT...`  `お待ちください...`')
                            break
                        else:
                            await msg_results2.edit(content = '`‼INVALID NUMBER try again...`  `再試行...`')
                            await user_msg2.delete()
                            await msg_results2.edit(content = '`👇ENTER EPISODE NUMBER BELOW`  `エピソード番号を入力`')  

                    except:
                        episode_num = None
                        await msg_results2.delete()
                        await ctx.channel.send(content = '`❗TOOK TOO LONG`  `長すぎる`', delete_after = 5)
                        
                        break

            # upload html to github        
            # this while loops allows episode switch
            while episode_num:
                
                #try get the best video link
                try:
                    video_src = anime.get_episodes_link(anime_id, episode_num)["(HDP-mp4)"]
                    ep_quality = 'HD'
                except KeyError:
                    video_src = None
                    episode_num = None
                    await msg_results2.delete()
                    embed = discord.Embed(
                        title = '💔  i bwoke something',
                        description = f'```text\newwow message:\ncouwd nyot get video wink fow {anime_detail["title"]} episode {episode_num}\n\ncommand + options:\n/anime {user_msg.content} {user_msg2.content} ```',
                        color = 0x2F3136)
                    bot_owner = await self.bot.fetch_user(240566530239234049)
                    embed.set_footer(text = 'send this error message to Yurishizu#1702', icon_url = bot_owner.avatar_url )
                    await msg_results.edit(content = None, embed = embed)

                    '''
                    try:
                        video_src = anime.get_episodes_link(anime_id, episode_num)["(1080P-mp4)"]
                        ep_quality = '1080P'
                    except KeyError:
                        try:
                            video_src = anime.get_episodes_link(anime_id, episode_num)["(720P-mp4)"]
                            ep_quality = '720P'
                        except KeyError:
                            try:
                                video_src = anime.get_episodes_link(anime_id, episode_num)["(480P-mp4)"]
                                ep_quality = '480P'
                            except KeyError:
                                try:
                                    video_src = anime.get_episodes_link(anime_id, episode_num)["(360P-mp4)"]
                                    ep_quality = '360P'
                                except KeyError: # no video links found, stop loop and send an error message
                    '''                

                # successfully have a video link       
                if video_src:                    
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
                            <h1 style = "color: white; font-family: 'KaushanScriptRegular', verdana;">{anime_detail["title"]} ・ Episode {episode_num} ⭐{ep_quality}</h1>
                        </body>
                    </html>
                    '''

                    # create a random 7 character ID
                    html_name = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=7))
                    
                    login = Github(GIT_TOKEN)
                    repo = login.get_repo('anim-e/w-atch')
                    contents = repo.get_contents('videos')
                    
                    # delete hmtl files with the same name in my repo
                    for c in contents:
                        if c.path == f'videos/{html_name}.html':
                            
                            repo.delete_file(c.path, 'Chadley BOT moderating', c.sha)
                    # push new html file to my repo
                    repo.create_file(f'videos/{html_name}.html', 'Chadley BOT moderating', html)

                    # show video player
                    while True: 
                        time.sleep(5)
                        embed=discord.Embed(description = '```text\n◀ previous episode     前のエピソード\n▶ next episode         次のエピソード\n```', color=0x2F3136)
                        embed.set_thumbnail(url = anime_detail["image_url"])
                        #embed.set_footer(text = '')
                        await msg_results2.edit(content = f'**`{anime_detail["title"]}`  `📺 Episode: {episode_num}`  `⭐{ep_quality}`**' , embed = embed)
                        await msg_results.edit(content = f'https://anim-e.tk/videos/{html_name}')
                        time.sleep(1)

                        # break while loop if video player loads up
                        if msg_results.embeds:
                            break
                        else:
                            await msg_results2.edit(embed = None, content = '`LOADING VIDEO PLEASE WAIT...`  `お待ちください...`')
                            await msg_results.edit(embed = None, content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')        

                    # add reactions
                    if int(anime_detail["episodes"]) > 1: # more than 1 episode
                        if episode_num == int(anime_detail["episodes"]): # on last episode
                            await msg_results2.add_reaction('◀')
                        elif episode_num == 1: # on first episode_num
                            await msg_results2.add_reaction('▶')
                        else: 
                            await msg_results2.add_reaction('◀')
                            await msg_results2.add_reaction('▶')

                    # checks that reactions are from the author on a specific message
                    def reaction_checker(reaction, user):
                        return user == ctx.author and msg_results2.id == reaction.message.id and reaction.emoji in ['◀','▶'] 

                    # waiting for reactons to switch episode
                    while True:
                        
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout = 1800.0, check = reaction_checker)
                            if reaction.emoji == '◀':
                                episode_num -= 1
                                await msg_results2.clear_reactions()
                                await msg_results.edit(embed = None, content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')
                                await msg_results2.edit(embed = None, content = '`LOADING VIDEO PLEASE WAIT...`  `お待ちください...`')
                                break

                            if reaction.emoji == '▶':
                                episode_num += 1
                                await msg_results2.clear_reactions()
                                await msg_results.edit(embed = None, content = 'https://anim-e.tk/imgs/VIDEO%20LOADING.gif')
                                await msg_results2.edit(embed = None, content = '`LOADING VIDEO PLEASE WAIT...`  `お待ちください...`')
                                break

                        except:
                            await msg_results2.clear_reactions()
                            await msg_results2.edit(embed = embed.set_footer(text = '\nENJOY YOUR SESSION セッションをお楽しみください'))
                            episode_num = None
                            break
                
        print('end of')





def int_checker(num):
    '''check if input is a whole number'''
    try:
        int(num)
        return True
    except ValueError:
        return False


def setup(bot):
    bot.add_cog(Anime(bot))

load_dotenv()
GIT_TOKEN = os.getenv('GITHUB_TOKEN')