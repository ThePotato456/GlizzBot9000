#!/usr/local/bin/python3

import discord
from discord.ext import commands
import os

from dotenv import load_dotenv

class Bot(commands.Bot):
    def __init__(self, command_prefix : str):
        description = '''GlizzyGoblins gucci bot'''
        intents = discord.Intents.default()
        intents.members = True
        self.bot = commands.Bot(command_prefix=command_prefix, description=description, intent=intents)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('\nBOT] Logged in as {0} ({0.id})'.format(self.bot.user))
        print('[!] Interact with it using the prefix \'{0}\'.'.format(self.bot.command_prefix))

    def initialize_cogs(self):
        for file in os.listdir('./cogs'):
            if file.endswith(".py"):
                name = file[:-3]
                print(f"[*] Loading cog {name}")
                self.bot.load_extension(f"cogs.{name}")

    def run(self):
        self.initialize_cogs()
        self.bot.add_listener(self.on_ready)
        load_dotenv()  
        token = os.getenv("DISCORD_TOKEN")
        self.bot.run(token)

if __name__ == "__main__":
    glizzy_bot = Bot(command_prefix='!')
    glizzy_bot.run()