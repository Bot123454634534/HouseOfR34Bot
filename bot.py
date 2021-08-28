import discord
import os
import random
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.converter import Greedy
from discord.ext.commands.core import has_permissions
from discord.guild import Guild
from discord.user import User
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv

#TODO: need to get cogs working properly

client = commands.Bot(command_prefix = '.')
slash = SlashCommand(client, sync_commands=True)

load_dotenv()

guild_ids= [int(os.getenv('TEST_SERVER')), int(os.getenv('R34_SERVER'))]

@client.event
async def on_ready():
    print('I want Die!')

@client.command(name="load")
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command(name="unload")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# random commands

@slash.slash(name='ror', description="Gernerates a Random ROR2 character to play with random artifacts", guild_ids= guild_ids)
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

@slash.slash(name='PSR', description='Play paper sissors rock against the bot', guild_ids= guild_ids,
options=[create_option(name='choice',
                        description='select your weapon',
                        option_type=3,
                        required=True,
                        choices=[
                            create_choice(name='paper', value='paper'),
                            create_choice(name='sissors', value='sissors'),
                            create_choice(name='rock', value='rock')
                        ])])
@client.command(name='PSR')
async def psr(ctx, choice: str):
    options = ['paper', 'sissors', 'rock']
    player = choice.lower()
    bot = random.choice(options)
    if player == bot:
        await ctx.send(f'Bot chose:{bot}\nDraw!')
    elif (player == 'paper' and bot == 'rock') or (player == 'sissors' and bot == 'paper') or (player == 'rock' and bot == 'sissors'):
        await ctx.send(f'Bot chose:{bot}\nYou Win!')
    else:
        await ctx.send(f'Bot chose:{bot}\nYou Lose!')


# Admin commands

@slash.slash(name='ShuffleUser', description="shuffle user between two channels", guild_ids= guild_ids,
options=[create_option(name='target', description='user(s) to shuffle', option_type=6, required=True)])
@client.command(aliases=["su"])
@has_permissions(administrator=True)
async def shuffleUser(ctx, target: User):
    channel1 = client.get_channel(int(os.getenv('SHUFFLE_CHANNEL')))
    if not target:
        await ctx.send("no member selected")
    else:
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

client.run(os.getenv('TOKEN'))