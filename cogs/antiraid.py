
import discord, os, re, time
from discord.ext import commands

ANTI_INVITE = os.getenv("ANTI_INVITE_ENABLED","true").lower()=="true"
ANTI_SPAM = os.getenv("ANTI_SPAM_ENABLED","true").lower()=="true"
INV_RE = re.compile(r"(discord\.gg|discord\.com/invite)")
GIFT_RE = re.compile(r"(discord\.gift)", re.I)

class AntiRaid(commands.Cog):
    def __init__(self,bot): self.bot=bot
        # msg tracking
        self.msg = {}

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.author.bot: return
        if GIFT_RE.search(msg.content): return
        if ANTI_INVITE and INV_RE.search(msg.content):
            try: await msg.delete()
            except: pass

        if not ANTI_SPAM: return
        t=time.time(); uid=msg.author.id
        self.msg.setdefault(uid,[]).append(t)
        self.msg[uid]=[x for x in self.msg[uid] if t-x<6]
        if len(self.msg[uid])>7:
            try:
                until=discord.utils.utcnow()+discord.timedelta(minutes=5)
                await msg.author.timeout(until,reason="Auto anti-spam")
            except: pass

async def setup(bot): await bot.add_cog(AntiRaid(bot))
