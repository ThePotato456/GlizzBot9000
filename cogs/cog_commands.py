from dis import disco
import json
import discord
from discord.ext import commands

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


class CommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, *args):
        arguments = ', '.join(args)
        await ctx.send(f'{len(args)} arguments: {arguments}')

    @commands.command(name="btcprice")
    async def getbtcprice(self, ctx: commands.Context):
        btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
        btc_price = btc_price['bitcoin']['usd']
        await ctx.send(f'[!] Current BTC to USD: 1.0 BTC = ${btc_price}')

def setup(bot: commands.Bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(CommandsCog(bot))