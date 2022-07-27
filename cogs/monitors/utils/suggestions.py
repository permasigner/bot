from datetime import datetime

import pytz
from data.services import guild_service, user_service
from discord.ext import commands, tasks

from utils import GIRContext, cfg


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id != guild_service.get_guild().channel_suggestions:
            return
            
        reactions = ['✅', '❌']
        for emoji in reactions: 
            await msg.add_reaction(emoji)
        
        await msg.create_thread(name=f"[{msg.author.name}] Suggestion Discussion")


async def setup(bot):
    await bot.add_cog(Suggestions(bot))
