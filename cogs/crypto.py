'''
use coinmarket cap api
use metadata to get infromation about a crypto
use quotes latest to get the price, supply, marketcap, percentage change


'''
# discord imports
import discord
from discord.ext import commands

# discord slash commands import
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option



class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





def setup(bot):
    bot.add_cog(Crypto(bot))