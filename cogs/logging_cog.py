
import discord, os
from discord.ext import commands

LOGS_CHANNEL_ID = os.getenv("LOGS_CHANNEL_ID")

class LoggingCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    async def send_log(self, guild: discord.Guild, embed: discord.Embed):
        try:
            if LOGS_CHANNEL_ID and LOGS_CHANNEL_ID.isdigit():
                ch = guild.get_channel(int(LOGS_CHANNEL_ID))
                if ch: await ch.send(embed=embed)
        except Exception: pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.send_log(member.guild, discord.Embed(description=f"👋 **Join:** {member.mention}", color=0x3498db))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.send_log(member.guild, discord.Embed(description=f"🚪 **Leave:** {member}", color=0xe74c3c))

async def setup(bot): await bot.add_cog(LoggingCog(bot))
