from dis import disco
import json
from pydoc import describe
import shutil
import discord
from discord.ext import commands
import datetime
import wget 
import os
from subprocess import run, PIPE
from moviepy.editor import *


from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

class CommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[cogs.cog_commands] Commands loaded!")

    @commands.command()
    async def test(self, ctx: commands.Context, *args):
        arguments = ', '.join(args)
        await ctx.send(f'{len(args)} arguments: {arguments}')

    @commands.command(name='download')
    async def download_url(self, ctx: commands.Context, url: str):
        p = run(['python3', 'RDtool.py', f'{url}', '-s'], stdout=PIPE, stdin=PIPE)
        output = p.stdout.decode().split('\n')
        track = {
            'file_name' : output[0].replace(' ', '_').replace('-', '_').replace('__', '').lower(),
            'url'       : output[1]
        }

        if not track['file_name'] in os.listdir('downloads/'):
            track_info = json.dumps(track, indent=4)
            track_info = json.loads(track_info)
            wget.download(track['url'], 'downloads/{0}'.format(track['file_name']))
            video = VideoFileClip(os.path.join("downloads/",'{0}'.format(track['file_name'])))
            video.audio.write_audiofile(os.path.join("audio", '{0}.mp3'.format(track['file_name'].replace('.mp4', ''))), logger=None, verbose=True)
            # Rewrite
            file = discord.File('audio/{0}.mp3'.format(track['file_name'].replace('.mp4', '')))
            await ctx.send(file=file)
        else:
            file = discord.File('audio/{0}.mp3'.format(track['file_name'].replace('.mp4', '')))
            await ctx.send(file=file)


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