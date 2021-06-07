#discord imports
import discord
from discord.ext import commands

# slash command imports
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

# other imports
import os
import random
from dotenv import load_dotenv
import json


# decalres slash command through the client
bot = commands.Bot(intents=discord.Intents.all(), command_prefix = '!')
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('READY')


@bot.event
async def on_message(message: discord.Message):
    
    '''
    AFK RELATED CODE BELLOW
    '''
    if not message.author.bot: # if authour is not a bot
        ''' read afk_list json file '''
        json_obj = afk_list.read()

        ''' check if user is in afk_list, then removes them'''
        user = message.author
        server_id = str(message.author.guild.id)
        user_id = str(user.id)
        if server_id in json_obj:
            if json_obj[server_id].get(user_id):
                ''' change their nickname back to normal '''
                if user != message.guild.owner: # check if user is not server owner
                    if json_obj[server_id][user_id]["nickname"] == None:
                        await user.edit(nick = '')
                    else:
                        await user.edit(nick = f'{json_obj[server_id][user_id]["nickname"]}')
                
                ''' remove user from afk_list '''
                del json_obj[server_id][user_id]

                ''' send message user is no longer afk '''
                await message.channel.send(f'👋 Welcome back {message.author.mention} you are no longer set to afk.')

                ''' writing to afk_list json file '''
                afk_list.write(json_obj)

            ''' when an AFK user is mentioned, send a message that the user is afk '''
            ''' read afk_list json file '''
            json_obj = afk_list.read()
            
            for user_mentioned in message.mentions:
                mentioned_id = str(user_mentioned.id)
                mentioned_name = str(user_mentioned)
                if mentioned_id in json_obj[server_id]:
                    if mentioned_name in json_obj[server_id][mentioned_id]['name']:
                        await message.channel.send(f'__**`@{mentioned_name}`**__ has changed their status to AFK.\n*`{json_obj[server_id][mentioned_id]["reason"]}`*')


@slash.slash(name = 'ping',
    description ='see bot latency'
    )
async def _ping(ctx):
    await ctx.send(f'Pong! **{round(bot.latency*1000, 2)}ms**') 


@slash.slash(name = 'say', 
    description ='make the bot repeat what you say',
    options = [
        create_option(
            name = 'message', 
            description = 'delete original message',
            option_type = 3,
            required = True
        ),
        create_option(
            name = 'delete', 
            description = 'delete original message',
            option_type = 3,
            required = False,
            choices=[
                create_choice(
                    name = 'yes', 
                    value = 'yes'
                ),
                create_choice(
                    name = 'no', 
                    value = 'no'
                )
    ])])
async def _say(ctx, message: str, delete = 'no'):
    if delete == 'yes':
        msg = await ctx.send(content ='please wait...')
        await msg.delete()
        await ctx.channel.send(f'{message}')
    elif delete == 'no':
        await ctx.send(f'{message}')


@slash.slash(name = 'invite', 
description = 'get the bot invite link'
)
async def _invite(ctx):
    link ='https://discord.com/oauth2/authorize?client_id=730879866026590229&permissions=4294967287&scope=applications.commands%20bot'
    embed = discord.Embed(
        title = 'invite link', 
        description = f'invite {bot.user.name} to another server with this [link]({link})\n```text\n{link}```',
        color = 0x2F3136)
    embed.set_thumbnail(url = f'{bot.user.avatar_url}')
    await ctx.send(embed = embed)


def load_cogs():
    for filename in os.listdir('./cogs'): #loop through files in cog folder
        if filename.endswith('.py'): 
            bot.load_extension(f'cogs.{filename[:-3]}') #remove '.py' from filename


class afk_list():

    def __init__(self):
        pass


    def read():
        with open('./db/afk_list.json', 'r',) as afk_list:
            json_copy = json.load(afk_list)
        return json_copy


    def write(json_copy):
        with open('./db/afk_list.json', 'w',) as afk_list:
            json.dump(json_copy, afk_list, indent = 4, ensure_ascii = True)


    def update_json(ctx, server):
        if server:
            json_obj[server_id].update({
                    user_id: {
                        'server' : ctx.guild.name, 
                        'name': ctx.author.name+'#'+ctx.author.discriminator ,
                        'nickname': ctx.author.nick, 
                        'reason': reason 
                    }})          
        else:
            json_obj.update({
                    server_id: {
                        user_id: {
                            'server' : ctx.guild.name, 
                            'name': ctx.author.display_name,
                            'nickname': ctx.author.nick, 
                            'reason': reason 
                        }}})
        

'''━ MAIN PROGRAM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'''
# READS .env FILES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

load_cogs()
bot.run(TOKEN)
