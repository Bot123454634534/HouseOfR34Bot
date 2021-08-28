import discord
import os
import random
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.converter import Greedy
from discord.ext.commands.core import has_permissions
from discord.member import Member
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv

#TODO: need to get cogs working properly
#TODO: slash commands

client = commands.Bot(command_prefix = '.')
slash = SlashCommand(client)

@client.event
async def on_ready():
    print('I want Die!')

@client.command(name="load")
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command(name="unload")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@slash.slash(name='ror', description="Gernerates a Random ROR2 character to play with random artifacts")
@client.command(name="ror")
async def ror(ctx):
    characters = ["Commando", "Huntress", 'MUL-T', 'Engineer', 'Mercenary', 'REX', 'Loader', 'Acrid', 'Artificer', 'Capitan']
    artifacts = ['Chaos', 'Command', 'Death', 'Dissonance', 'Enigma' , 'Evolution', 'Frailty', 'Glass', 'Honor', 'Kin', 'Metamorphosis', 'Sacrifice', 'Soul', 'Spite', 'Swarms', 'Vengeance']
    artifact = []
    for i in artifacts:
        chance = random.randint(0, 100)
        if chance >= 75:
            artifact.append([i])
    
    await ctx.send(f'Survivor: {random.choice(characters)}\nArtifact(s): {artifact}')

# @slash.slash(name='ShuffleUser', description="shuffle user between two channels", 
# options=[create_option(name='targets', description='user(s) to shuffle', option_type=6, required=True)])
@client.command(aliases=["su"])
@has_permissions(administrator=True)
async def shuffleUser(ctx, targets: Greedy[Member]):
    channel1 = client.get_channel(803786402947923998)
 
    if not len(targets):
        await ctx.send("no members selected")
    else:
        for target in targets:
            channel2 = target.voice.channel
            i = 0
            while i < 2:
                await target.move_to(channel1)
                await target.move_to(channel2)
                i = i + 1
            await ctx.send(f'member shuffled: {target.name}')  

@shuffleUser.error
async def shuffle_user_error(ctx, exc):
    if isinstance(exc, Forbidden):
        await ctx.send("You don't have the correct permissons to use this command") 

load_dotenv()

client.run(os.getenv('TOKEN'))