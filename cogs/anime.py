# discord imports
import discord
from discord.ext import commands

# discord slash commands import
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

# other imports


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

    # anime slash command
    @cog_ext.cog_slash(
        name = 'anime-by-genre',
        description = 'search for anime by genre',
        guild_ids = [746398170325581835],
        options = [
            create_option(
                name = 'genres1',
                description = 'a list of genres',
                option_type = 2,
                required = False,
            ),
            create_option(
                name = 'genres2',
                description = 'additional list of genres',
                option_type = 3,
                required = False,
                choices = genres2()
            ),
        ]
    )
    async def anime_genre(self, ctx):
        pass

    @slash.subcommand(base="group", name="say")
    async def _group_say(self, ctx, _str):
        await ctx.send(content=_str)

    # /group kick user <user>
    @slash.subcommand(base="group",
                    subcommand_group="kick",
                    name="user")
    async def _group_kick_user(self, ctx, user):
        pass


    @cog_ext.cog_slash(
        name = 'anime-by-genre3',
        description = 'search for anime',
        guild_ids = [746398170325581835],
        options = [
            create_option(
                name = 'colours',
                description = 'title of the anime',
                option_type = 3,
                required = True,
               
            )
        ]
    )
    async def anium2():
        pass

    def tyrtyrt():
        pass

def setup(bot):
    bot.add_cog(Anime(bot))