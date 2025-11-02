
import discord, os, re, time
from discord.ext import commands

ANTI_INVITE = os.getenv("ANTI_INVITE_ENABLED", "true").lower() == "true"
ANTI_SPAM = os.getenv("ANTI_SPAM_ENABLED", "true").lower() == "true"

INVITE_RE = re.compile(r"(discord\.gg/|discord\.com/invite/)", re.I)
GIFT_RE = re.compile(r"(discord\.gift/)", re.I)  # allowed, no timeout

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg_times = {}

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if not m.guild or m.author.bot:
            return

        # allow gift links entirely
        if GIFT_RE.search(m.content):
            return

        # delete invites if enabled
        if ANTI_INVITE and INVITE_RE.search(m.content):
            try: await m.delete()
            except: pass

        if not ANTI_SPAM: return
        now = time.time()
        window, limit = 6, 7  # safe thresholds
        bucket = self.msg_times.setdefault(m.author.id, [])
        bucket.append(now)
        self.msg_times[m.author.id] = [t for t in bucket if now - t <= window]
        if len(self.msg_times[m.author.id]) > limit:
            try:
                until = discord.utils.utcnow() + discord.timedelta(minutes=5)
                await m.author.timeout(until, reason="Auto anti-spam (safe mode)")
            except: pass

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
