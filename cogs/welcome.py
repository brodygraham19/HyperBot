
import discord, os
from discord.ext import commands

WELCOME_CH = os.getenv("WELCOME_CHANNEL_ID")
DM_ENABLED = os.getenv("WELCOME_DM_ENABLED","true").lower()=="true"
DM_TEXT = os.getenv("WELCOME_DM_TEXT","Welcome! Verify to unlock. ✅")

class Welcome(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @commands.Cog.listener()
    async def on_member_join(self, m):
        if WELCOME_CH:
            ch=m.guild.get_channel(int(WELCOME_CH))
            if ch: 
                try: await ch.send(f"👋 {m.mention} {DM_TEXT}")
                except: pass
        if DM_ENABLED:
            try: await m.send(DM_TEXT)
            except: pass

async def setup(bot): await bot.add_cog(Welcome(bot))
