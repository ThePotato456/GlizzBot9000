from dis import disco
from operator import truediv
import discord
from discord.ext import commands

class PlaySound(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.joined = False
        self.playing = False
        self.bot = bot
        
    @commands.command()
    async def join(self, ctx : commands.Context):
        """Joins a voice channel"""
        if not self.joined:
            try:
                self.joined = True
                channel: discord.VoiceChannel = ctx.author.voice.channel
                await channel.connect()
            except Exception as e:
                await ctx.send('[-] User is not in a joinable voice channel!')
        else:
            self.joined = False
            await ctx.send("[-] Bot is already in another channel!")

    @commands.command()
    async def play(self, ctx : discord.TextChannel):
        if not self.playing:
            self.playing = True
            guild = ctx.guild # Gets context guild
            voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild) # Gets bot's voice_client
            audio_source = discord.FFmpegPCMAudio('audio/test.mp3') # file to play over sound
            if not voice_client.is_playing(): # if its not already playing, dont play it
                voice_client.play(audio_source, after=None) # play the audio file
        else:
            await ctx.send('Can\'t play while already playing')
            self.stop(ctx)

    @commands.command()
    async def stop(self, ctx : discord.TextChannel):
        self.playing = False
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice_client.is_playing():
            voice_client.stop()

    @commands.command()
    async def leave(self, ctx):
        self.playing = False
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice_client.is_playing():
            voice_client.stop()
            await voice_client.disconnect()
        else:
            await voice_client.disconnect()

def setup(bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(PlaySound(bot))
