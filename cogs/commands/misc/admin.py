import traceback
import discord
import requests
from discord import app_commands, Color
from discord.ext import commands
from data.services import guild_service
from utils import GIRContext, cfg, transform_context, logger
from utils.framework import admin_and_up, guild_owner_and_up
from utils.framework.transformers import ImageAttachment


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @admin_and_up()
    @app_commands.guilds(cfg.guild_id)
    @app_commands.command(description="Change the bot's profile picture")
    @app_commands.describe(image="Image to use as profile picture")
    @transform_context
    async def setpfp(self, ctx: GIRContext, image: ImageAttachment):
        await self.bot.user.edit(avatar=await image.read())
        await ctx.send_success("Done!", delete_after=5)

    @guild_owner_and_up()
    @app_commands.guilds(cfg.guild_id)
    @app_commands.command(description="Show message when Aaron is pinged on Sabbath")
    @app_commands.describe(mode="Set mode on or off")
    @transform_context
    async def sabbath(self, ctx: GIRContext, mode: bool = None):
        g = guild_service.get_guild()
        g.sabbath_mode = mode if mode is not None else not g.sabbath_mode
        g.save()

        await ctx.send_success(f"Set sabbath mode to {'on' if g.sabbath_mode else 'off'}!")

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        if ctx.author.id != cfg.owner_id:
            return

        try:
            async with ctx.typing():
                await self.bot.tree.sync(guild=discord.Object(id=cfg.guild_id))
        except Exception as e:
            await ctx.send(f"An error occured\n```{e}```")
            logger.error(traceback.format_exc())
        else:
            await ctx.send("Done!")

    @commands.command()
    @commands.is_owner()
    async def ban(self, ctx: commands.Context):
        if ctx.author.id != cfg.owner_id:
            return

        await ctx.reply("Asserting dominance by threatening to ban.")
        
    @app_commands.guilds(cfg.guild_id)  
    @app_commands.command(description="Push the latest commit of the Permasigner repo to Docker hub")
    @transform_context
    async def pushdocker(self, ctx):
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'token {cfg.github_workflow_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(
            'https://api.github.com/repos/itsnebulalol/permasigner/actions/workflows/docker.yml/dispatches', 
            headers=headers, 
            data='{"ref":"main"}')
        
        if response.text:
            desc = f"Made the request, but something might have gone wrong...\n\nWorkflow response:\n{response.text}"
            color=Color.red()
        else:
            desc = f"The request succeeded! The Docker container is now being built and pushed."
            color=Color.green()
        
        embed = discord.Embed(title="Push to Docker Hub", 
                              description=desc, color=color)
        
        await ctx.respond(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
