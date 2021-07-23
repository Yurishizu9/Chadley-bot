# discord imports
import discord
from discord.ext import commands

# discord slash commands import
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


@cog_ext.cog_slash(
    name = 'test',
    description = 'testing new discord components',
    guild_ids = [746398170325581835]
)
async def _test(self, ctx: SlashContext):
    await ctx.send('testing ne buttons!')




def setup(bot):
    bot.add_cog(Test(bot))
