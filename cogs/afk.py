# %%
#dsicord imports
import discord
from discord.ext import commands

#discord slash imports
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

#other imports
import random
import json


class Stocks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name = 'afk',
        description = 'let others know you are afk',
        options = [
            create_option(
                name = 'reason',
                description = 'let others know why you are afk',
                option_type = 3,
                required = False
            )])
    async def _brb(self, ctx: SlashContext, reason: str = None):
        ''' 
        this class updates afk_list json file 
        '''
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
 
        # get bot id and bot ctx 
        # check if bot role is above the authors role
        bot_id = ctx.guild.me.id 
        my_bot = ctx.guild.get_member(bot_id)
        if my_bot.top_role > ctx.author.top_role:

            # get user id and server id
            user_id = str(ctx.author_id)
            server_id = str(ctx.guild_id)

            # reading afk_list json file 
            json_obj = afk_list.read()

            '''
            IF USER EXISTS in afk_list
            removing their ass
            '''
            user_exists = False
            server_exists = False
            if server_id in json_obj:
                server_exists = True
            
                if json_obj[server_id].get(user_id):
                    user_exists = True
                    # change user nickname back to normal
                    if ctx.author != ctx.guild.owner: # check if user is not server owner
                        if json_obj[server_id][user_id]["nickname"] == None:
                            await ctx.author.edit(nick = '')
                        else:
                            await ctx.author.edit(nick = f'{json_obj[server_id][user_id]["nickname"]}')
                            
                    # remove user from afk_list
                    if user_id in json_obj[server_id]:
                        del json_obj[server_id][user_id]
                
                    # send a message that the user is no longer afk
                    msg = await ctx.send('please wait...')
                    await msg.delete()
                    await ctx.channel.send(f'👋 welcome back {ctx.author.mention} you are no longer set to afk.*')
                else:
                    user_exists = False
            else:
                server_exist = False
            
            ''' 
            IF USER DOES NOT EXISTS 
            add their ass
            '''
            while not user_exists:         
                # give random reason if not provided
                if not reason:
                    reason_list = [
                        'Ran out of toothpaste and soap, trust me!'
                        'Waiting for the maid to arrive. Will be firing her today. Wish me luck. Failed twice at it already.',
                        'Can\'t find my headphones.',
                        'Morning wood not going away.',
                        'Fish died, need to bury it.',
                        'My barber couldn\'t understand my instructions, new hair cut looks horrible.',
                        'My astrologer asked me to stay off Discord, star alignment is not good.',
                        'Need to work peacefully without disturbance.',
                        'Cat is sick. Need to take care of him.',
                        'Someone is coming home for my address proof verification.',
                        'Someone painted a d@ck on my car :(.',
                        'My ankle got handcuffed to the bedframe since last night.',
                        'Waiting for broadband connection to be setup.',
                        'Uninterested but unavoidable familiy event.',
                        'My cat somehow ate marijuana and is behaving wierd.',
                        'My landlord is shouting at me. Need to kick him out of the house!',
                        'Have lots of pending work, no time to come online.',
                        'Roomate caught high fever. Need to visit a doctor.',
                        'Rain water flooding in. Need to take care of home.',
                        'Had a heavy breakfast, dont feel like moving',
                        'no wifi',
                        'no electric',
                        'no pc']
                    reason = random.choice(reason_list)
                
                # send a message that user is now afk
                msg = await ctx.send('please wait...')
                await msg.delete()
                await ctx.channel.send(f'{ctx.author.mention} has changed their status to AFK. *`"{reason}"`*')

                # add user to afk_list                               
                if server_id in json_obj: # existing server
                    if user_id in json_obj[server_id]: # existing server, existing user
                        afk_list.update_json(ctx, server_exists)
                    else: # existing server, new user
                        afk_list.update_json(ctx, server_exists)      
                else: # new server, new user
                    afk_list.update_json(ctx, server_exists)

                #change user nickname
                if ctx.author != ctx.guild.owner: # check if user is not server owner
                    if ctx.author.nick: # when user has nickname
                        await ctx.author.edit(nick = f'AFK | {ctx.author.nick}')
                    else: # when user does not have nickname
                        await ctx.author.edit(nick = f'AFK | {ctx.author.name}')
                break

            # writing to afk_list json file 
            afk_list.write(json_obj)
        else: 
            msg = await ctx.send('please wait...')
            await msg.delete()
            await ctx.channel.send(f'_`@{my_bot.top_role}`_ role needs to be above _`@{ctx.author.top_role}`_ role to use this command')
        
        


        



def setup(bot):
    bot.add_cog(Stocks(bot))
