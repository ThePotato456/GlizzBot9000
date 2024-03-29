import tarfile
import discord
from discord.ext import commands
import os, json, wget
from subprocess import run, PIPE
from moviepy.editor import *

class PlaySound(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.joined = False
        self.playing = False
        self.bot = bot
        
    @commands.command()
    async def join(self, ctx: commands.Context):
        """Joins a voice channel"""
        if not self.joined:
            try:
                self.joined = True
                channel: discord.VoiceChannel = ctx.author.voice.channel
                await channel.connect()
            except Exception as e:
                print(e)
                await ctx.send('[-] User is not in a joinable voice channel!')
        else:
            await ctx.send("[-] Bot is already in another channel!")

    @commands.command()
    async def play(self, ctx: discord.TextChannel, arg):
        valid_song = False
        song = ''
        for file in os.listdir('audio/'):
            if arg == file:
                valid_song = True
                song = f'audio/{file}'

        if self.joined:
            if valid_song:
                guild = ctx.guild # Gets context guild
                voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild) # Gets bot's voice_client
                audio_source = discord.FFmpegPCMAudio(song) # file to play over sound
                if not voice_client.is_playing(): # if its not already playing, dont play it
                    voice_client.play(audio_source, after=None) # play the audio file
                else:
                    await ctx.send('Can\'t play while already playing')
            else:
                await ctx.send('[!] Invalid song, song doesn\'t exist!')
        else:
            await ctx.send('[-] Bot isn\'t in any voice channel')

    @commands.command(name='playurl')
    async def play_url(self, ctx: commands.Context, url: str):
        p = run(['python3', 'RDtool.py', f'{url}', '-s'], stdout=PIPE, stdin=PIPE)
        output = p.stdout.decode().split('\n')
        track = {
            'file_name' : output[0].replace(' ', '_').replace('-', '_').replace('__', '').lower(),
            'url'       : output[1]
        }

        song = ''
        if not track['file_name'] in os.listdir('downloads/'):
            track_info = json.dumps(track, indent=4)
            track_info = json.loads(track_info)
            wget.download(track['url'], 'downloads/{0}'.format(track['file_name']))
            video = VideoFileClip(os.path.join("downloads/",'{0}'.format(track['file_name'])))
            video.audio.write_audiofile(os.path.join("audio", '{0}.mp3'.format(track['file_name'].replace('.mp4', ''))), logger=None, verbose=True)
            song = '{0}.mp3'.format(track['file_name'].replace('.mp4', ''))
            print(" downloaded song: " + str(song))
        else:
            song = '{0}.mp3'.format(track['file_name'].replace('.mp4', ''))
            print(" loaded song: " + str(song))

        valid_song = False
        for file in os.listdir('audio/'):
            if file == song:
                valid_song = True
                song = f'audio/{song}'
        if self.joined:
            if valid_song:
                guild = ctx.guild # Gets context guild
                voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild) # Gets bot's voice_client
                audio_source = discord.FFmpegPCMAudio(song) # file to play over sound
                if not voice_client.is_playing(): # if its not already playing, dont play it
                    voice_client.play(audio_source, after=None) # play the audio file
                else:
                    await ctx.send('Can\'t play while already playing')
            else:
                await ctx.send('[!] Invalid song, song doesn\'t exist!')
        else:
            await ctx.send('[-] Bot isn\'t in any voice channel')

    @commands.command()
    async def stop(self, ctx: discord.TextChannel):
        if self.joined:
            guild = ctx.guild
            voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
            if voice_client.is_playing():
                voice_client.stop()
            else:
                await ctx.send('[!] Bot isn\'t playing anything')
        else:
            await ctx.send('[!] Bot isn\'t in any voice channels')

    @commands.command()
    async def leave(self, ctx):
        if self.joined:
            self.playing = False
            self.joined = False
            guild = ctx.guild
            voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
            if voice_client.is_playing():
                voice_client.stop()
                await voice_client.disconnect()
            else:
                await voice_client.disconnect()
        else:
            await ctx.send('[!] Bot isn\'t in any voice channels')
    
    @commands.command()
    async def list_songs(self, ctx: commands.Context):
        songs = []
        for file in os.listdir('audio/'):
            songs.append(file)
        await ctx.send('[+] Currently Playable Files: `{0}`'.format(songs))

def setup(bot: commands.Bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(PlaySound(bot))
