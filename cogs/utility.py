import discord
from discord.ext import commands

import datetime
import random


class Utility(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Latency/ping of the bot"""
        embed = discord.Embed(title=f"Pong! {round(self.bot.latency * 1000)}ms",
                              colour = discord.Color.from_rgb(random.randint(0,255), 
                                                              random.randint(0,255),
                                                              random.randint(0,255)))
        embed.set_footer(text=f'Called by: {ctx.author}')    
        await ctx.message.delete()    
        return await ctx.send(embed=embed)

    @commands.command()
    async def creator(self, ctx):
        """Creator's github"""
        embed = discord.Embed(title="Creator's Github:", 
                               description="""Hey, I am the creator of the bot.
                               [This](https://github.com/VishankSingh) is my github account.""",
                               colour = discord.Color.from_rgb(92, 51, 255),
                               timestamp=datetime.datetime.now())
        embed.set_footer(text=f'Called by: {ctx.author}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))