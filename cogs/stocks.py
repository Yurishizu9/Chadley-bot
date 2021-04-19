#dsicord imports
import discord
from discord.ext import commands

#discord slash imports
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

#other imports
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

guild_ids = [722932395682168913,746398170325581835]

class Stocks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(
        name = 'stocks',
        description ='find the action price of a stock and additional information',
        guild_ids =guild_ids,
        options = [
            create_option(
                name = 'symbol',
                description = 'ticker symbol of the stock',
                option_type = 3,
                required = True
            ),
            create_option(
                name = 'info',
                description = 'get more information about this stock',
                option_type = 5,
                required = False
            )])
    async def _stock(self, ctx: SlashContext, symbol: str, info: bool = False):
        if not info: # when info option is false
            '''requests ticker symbol price'''
            req = quote(symbol) 

            if not req: # when quote request fails
                '''send error message with list of suggested company stocks '''
                await ctx.send(f'no result for the symbol __`{symbol}`__')
                req = search(symbol)

                if req: 
                    results = ''
                    for x in req:
                        results += f'**{x["symbol"]}** - **`{x["name"]}`** `{x["currency"]}` `{x["exchangeShortName"]}`  \n'
                    await ctx.channel.send(f'*did you mean:*\n\n{results}')
                
            else: # when quote request is succesful
                for x in req: 
                    ''' this embed display stock Price '''
                    if x['changesPercentage'] > 0:
                        colour = '🟩'
                    else:
                        colour = '🟥'

                    embed=discord.Embed(
                        title = f'{colour} {x["price"]} USD ', 
                        description = f'{x["change"]} ({x["changesPercentage"]}%)\n```{x["exchange"]}: {x["symbol"]}\n{x["name"]}```',
                        color = 0x2F3136)
                    embed.set_thumbnail(url='https://financialmodelingprep.com/image-stock/'+ x['symbol'] + '.png')
                    embed.add_field(name='OPEN', value=f'`{x["open"]}`', inline=True)
                    embed.add_field(name='P. CLOSE', value=f'`{x["previousClose"]}`', inline=True)
                    embed.add_field(name='HIGH', value=f'`{x["dayHigh"]}`', inline=True)
                    embed.add_field(name='LOW', value=f'`{x["dayLow"]}`', inline=True)
                    embed.add_field(name='Y. HIGH', value=f'`{x["yearHigh"]}`', inline=True)
                    embed.add_field(name='Y. LOW', value=f'`{x["yearLow"]}`', inline=True)
                    embed.set_footer(text=f'VOL {x["volume"]} • MKT CAP {x["marketCap"]}')
                await ctx.send(embed=embed)

        else: # when info option is true
            '''request company stock information'''
            req = profile(symbol)

            if not req: # when info request fails
                '''send error message with list of suggested company stocks '''
                await ctx.send(f'no result for the symbol __`{symbol}`__')
                req = search(symbol)
                if req: 
                    results = ''
                    for x in req:
                        results += f'**{x["symbol"]}** - **`{x["name"]}`** `{x["currency"]}` `{x["exchangeShortName"]}`  \n'
                    await ctx.channel.send(f'*did you mean:*\n\n{results}')

            else: # when info request is succesful
                '''display stock company information'''
                for x in req:
                    embed = discord.Embed(
                        title=x["symbol"], 
                        description=f'{x["price"]} {x["currency"]}\n\n**{x["companyName"]}** [🔗]({x["website"]})\n```{x["description"][0:1000]}...```', 
                        timestamp = datetime.strptime(x["ipoDate"], '%Y-%m-%d'),
                        color = 0x2F3136)
                    embed.set_thumbnail(url = x["image"])
                    embed.set_footer(text = f'Currently trading: {x["isActivelyTrading"]},  IPO date')
                    embed.add_field(name = 'Company details', value=f'```asciidoc\n:::CEO {x["ceo"]}\n:::EMPLOYEES {x["fullTimeEmployees"]}\n:::HEADQUARTER {x["city"]}, {x["state"]}, {x["country"]}\n:::SECTOR {x["sector"]}\n:::INDUSTRY {x["industry"]}```', inline=True)
                    embed.add_field(name = 'More details', value=f'```asciidoc\n:::MARKET CAP {x["mktCap"]}\n:::AVERAGE_VOLUME {x["volAvg"]}\n:::BETA {x["beta"]}\n:::ANUAL DIVIDEND {x["lastDiv"]}%\n:::EXCHANGE {x["exchange"]} ({x["exchangeShortName"]})```', inline=True)
                await ctx.send(embed = embed)


'''returns the price of a stock'''
def quote(s):
    s = str(s).upper()
    url = 'https://financialmodelingprep.com/api/v3/quote/'+s+'?apikey='+key
    fmp = requests.get(url) # api request
    quote = list(fmp.json()) # quote results
    #print(url)
    #print(quote)
    return quote

'''searches for companies and their ticker symbol'''
def search(s):
    url = 'https://financialmodelingprep.com/api/v3/search?query='+s+'&limit=10&apikey='+key
    fmp = requests.get(url) # api request
    symbols = list(fmp.json()) # list of company tickers symbols
    #print(url)
    #print(symbols)
    return symbols

'''gets more information on a stock company'''
def profile(s):
    url  = 'https://financialmodelingprep.com/api/v3/profile/'+s+'?apikey='+key
    fmp = requests.get(url) # api request
    company_info = list(fmp.json()) # stock company profile
    #print(url)
    #print(company_info)
    return company_info


def setup(bot):
    bot.add_cog(Stocks(bot))


'''━ MAIN PROGRAM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'''
load_dotenv() # loads env. file
key = os.getenv('FMP') # api key for fmp
