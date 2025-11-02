
import discord, os
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        guild = discord.Object(id=int(os.getenv("GUILD_ID")))
        cmds = await self.bot.tree.sync(guild=guild)
        await ctx.send(f"✅ Synced {len(cmds)} commands.")

async def setup(bot): await bot.add_cog(Sync(bot))
