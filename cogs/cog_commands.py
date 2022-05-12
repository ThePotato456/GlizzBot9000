from dis import disco
import json
from pydoc import describe
import string
import discord
from discord.ext import commands
import datetime

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

class CommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context, *args):
        arguments = ', '.join(args)
        await ctx.send(f'{len(args)} arguments: {arguments}')

    @commands.command(name="cryptoprice")
    async def get_crypto_price(self, ctx: commands.Context, *args):
        if not len(args) == 0:
            cryptos = []
            for arg in args:
                cryptos.append(arg)
            currency_prices = cg.get_price(ids=cryptos, vs_currencies='usd')
            embed = discord.Embed(title='Crypto to USD'.format(), url="", description=f'', color=0x109319, timestamp=datetime.datetime.utcnow())
            for currency in currency_prices:
                currency_name = currency.capitalize()
                price = currency_prices[currency]['usd']
                price = '${:,}'.format(price)
                embed.add_field(name=f'{currency_name}', value=f'1 {currency} = {price}', inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send('[!] No currency specified.')

def setup(bot: commands.Bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(CommandsCog(bot))