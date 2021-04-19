import random

import discord
from discord.ext import commands

from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [722932395682168913,746398170325581835]

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(
        name = 'rps',
        description ='play rock, paper, scissors against me',
        guild_ids =guild_ids,
        options=[
            create_option(
                name='hand',
                description='pick a hand.',
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name='Rock', 
                        value='🤜'
                    ),
                    create_choice(
                        name='Paper', 
                        value= '✋'
                    ),
                    create_choice(
                        name='Scissors', 
                        value= '✌'
                    )])])
    async def _rps(self, ctx: SlashContext, hand: str):
        computers_hand = random.choice(['🤜','✋','✌'])
        content = f'`{ctx.author.name}` {hand} **vs** {computers_hand} `{self.bot.user.name}`'
        if hand == '🤜' and computers_hand == '✌':
            content += '\nYou **won!**'
        if hand == '✌' and computers_hand == '✋':
            content += '\nYou **won!**'
        if hand == '✋' and computers_hand == '🤜':
            content += '\nYou **won!**'
        if hand == '🤜' and computers_hand == '✋':
            content += '\nYou **lost!**'
        if hand == '✌' and computers_hand == '🤜':
            content += '\nYou **lost!**'
        if hand == '✋' and computers_hand == '✌':
            content += '\nYou **lost!**'
        if hand == computers_hand:
            content += '\nit\'s a **draw!**'
        msg = await ctx.send(content = content)


    @cog_ext.cog_slash(
        name = 'lfg',
        description = 'looking for game',
        guild_ids = guild_ids,
        options = [
            create_option(
                name = 'game',
                description = 'name of the game you are playing',
                option_type=3,
                required = False
            ),
            create_option(
                name = 'message',
                description = 'description',
                option_type=3,
                required = False
            )])
    async def _lfg(self, ctx: SlashContext, message: str = None, game: str = None):
        
        '''error message'''
        if ctx.author.voice == None:
            await ctx.send('⚠ you need to be in a voice channel to use that command')
        
        else:
            # get the voice channel the author is in and create invite link
            VoiceChannel = ctx.author.voice.channel
            channel_invite = await VoiceChannel.create_invite(destination = VoiceChannel)

            '''send invite link to the voice channel'''
            lfg_message = ''
            if message: lfg_message += f'\n MESSAGE: `{message}`'
            if game: lfg_message += f'\n GAME: `{game}`'

            await ctx.send(f'{ctx.author.mention} sent an invitation link to **{VoiceChannel}**.{lfg_message}\n{channel_invite}')


def setup(bot):
    bot.add_cog(Games(bot))
