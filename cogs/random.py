import os
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Random(commands.Cog):

    guild_ids= [int(os.getenv('TEST_SERVER')), int(os.getenv('R34_SERVER'))]

    def __init__(self, client):
        self.client = client
        
    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send("it work!")

def setup(client):
    client.add_cog(Random(client))
    print("Random Loaded")