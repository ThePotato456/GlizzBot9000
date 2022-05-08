"""
Author: eddy22
Altered By: ThePotato456
"""

import discord
from discord.ext import commands
from sys import version_info as sysv
from os import listdir

class Dev(commands.Cog):
    """This is a cog with owner-only commands.
        Note:
                All cogs inherits from `commands.Cog`_.
                All cogs are classes, so they need self as first argument in their methods.
                All cogs use different decorators for commands and events (see example below).
                All cogs needs a setup function (see below).
    Documentation:
        https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
    """

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    # This is the decorator for events (inside of cogs).
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[cog_cogs_module] Eddie's cog_module loading.... Python {sysv.major}.{sysv.minor}.{sysv.micro} - Disord.py {discord.__version__}")
        # Prints on the shell the version of Python and Discord.py installed in our computer.

    
    # This command is hidden from the help menu.
    # This is the decorator for commands (inside of cogs).
    # Only the owner (or owners) can use the commands decorated with this.
    @commands.command(name="reloadall", hidden=True)
    @commands.is_owner()
    async def reload_all(self, ctx):
        """This commands reloads all the cogs in the `./cogs` folder.

        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds."""

        message = await ctx.send("Reloading...")

        try:
            for cog in listdir("./cogs"):
                if cog.endswith(".py") == True:
                    self.bot.reload_extension(f"cogs.{cog[:-3]}")
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content="All cogs have been reloaded.")

    def check_cog(self, cog):
        """Returns the name of the cog in the correct format.
        Args:
                self
                cog (str): The cogname to check

        Returns:
                cog if cog starts with `cogs.`, otherwise an fstring with this format`cogs.{cog}`_.
        Note:
                All cognames are made lowercase with `.lower()`_.
        """
        if (cog.lower()).startswith("cogs.") == True:
            return cog.lower()
        return f"cogs.{cog.lower()}"

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """This commands loads the selected cog, as long as that cog is in the `./cogs` folder.

        Args:
                cog (str): The name of the cog to load. The name is checked with `.check_cog(cog)`_.

        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds.
        """
        message = await ctx.send("Loading...")
        await ctx.message.delete()
        try:
            self.bot.load_extension(self.check_cog(cog))
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content=f"{self.check_cog(cog)} has been loaded.")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """This commands unloads the selected cog, as long as that cog is in the `./cogs` folder.

        Args:
                cog (str): The name of the cog to unload. The name is checked with `.check_cog(cog)`_.
        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds.
        """
        message = await ctx.send("Unloading...")
        await ctx.message.delete()
        try:
            self.bot.unload_extension(self.check_cog(cog))
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content=f"{self.check_cog(cog)} has been unloaded.")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """This commands reloads the selected cog, as long as that cog is in the `./cogs` folder.

        Args:
                cog (str): The name of the cog to reload. The name is checked with `.check_cog(cog)`_.
        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds.
        """
        message = await ctx.send("Reloading...")
        await ctx.message.delete()
        try:
            self.bot.reload_extension(self.check_cog(cog))
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content=f"{self.check_cog(cog)} has been reloaded.")

def setup(bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(Dev(bot))
