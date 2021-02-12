import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MissingRole, MissingRequiredArgument

import asyncio
import logging
from config import *
import os
import json


#logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



###################################################
with open('config.json') as con:
    config = json.load(con)

token = config["BotToken"]
prefix = config["BotPrefix"]
###################################################




print('Bot is connecting...')

class bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=prefix,
                         case_insensitive=True,
                         #intents=discord.Intents.all(),
                         **kwargs)


    # EVENTS
    async def on_ready(self):
        """Prints 'Bot is live!' to the console when the bot is ready"""
        await self.change_presence(status=discord.Status.online, 
                                   activity=discord.Activity(type=discord.ActivityType.playing, 
                                                             name=f"use prefix '{prefix}'"))

        # loads all cogs in the cogs folder
        for cog in os.listdir('./cogs'):
            if cog.endswith('.py'):
                self.load_extension(f"cogs.{cog[:-3]}")

        print(f"Bot is live!")


    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message=message)

        await self.invoke(ctx)


    async def on_command_error(self, ctx, error):
        """When someone tries to access a unknown command"""
        if isinstance(error, CommandNotFound):
            return await ctx.send("Error: Command Not Found!")
        elif isinstance(error, MissingPermissions):
            return await ctx.send("Error: You can't use that command. Reason: Missing Perms")
        elif isinstance(error, MissingRole):
            return await ctx.send("Error: You can't use that command. Reason: Missing Role")
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.send("Error: Missing Required Parameter")
        else:
            raise error

    async def setup(self, **kwargs):
        try:
            await self.start(token, **kwargs)
        except KeyboardInterrupt:
            await self.close()

    
        



bot = bot()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.setup())