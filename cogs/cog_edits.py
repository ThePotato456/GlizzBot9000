#!/usr/local/bin/python3

import discord
from discord.ext import commands
import datetime

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[cogs.cog_edits] listening for message edits....")

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not before.author.bot:
            #fmt = '**{0.author}** edited their message:\n{0.content} -> {1.content}'
            embed = discord.Embed(title="{0}".format(before.author), url="", description='**Message edited in: #{0}**'.format(before.channel.name), color=0x109319, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Before", value="{0.content}".format(before), inline=True)
            embed.add_field(name="** **", value="->".format(before), inline=True)
            embed.add_field(name="After", value="{0.content}".format(after), inline=True)
            embed.set_footer(text="User ID: {0}".format(before.author.id))

            channel = discord.utils.get(self.bot.get_all_channels(), name="mod-log")
            await channel.send(embed=embed)    

def setup(bot: commands.Bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(CommandsCog(bot))