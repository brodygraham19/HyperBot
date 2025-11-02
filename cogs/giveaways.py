
import discord, asyncio, re, random
from discord.ext import commands
from discord import app_commands

def parse_duration(text: str) -> int:
    m = re.match(r"^(\d+)([smhd])$", text.lower())
    if not m: return 0
    n, u = int(m.group(1)), m.group(2)
    return n * {"s":1,"m":60,"h":3600,"d":86400}[u]

class Giveaways(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="gstart", description="Start a giveaway: duration like 10m, prize text")
    async def gstart(self, i: discord.Interaction, duration: str, prize: str):
        secs = parse_duration(duration)
        if secs <= 0: return await i.response.send_message("Use durations like `10m`, `2h`, `1d`.", ephemeral=True)
        embed = discord.Embed(title="🎉 Giveaway!", description=f"**Prize:** {prize}\nReact with 🎉 to enter!\nEnds in **{duration}**", color=0x9b59b6)
        msg = await i.channel.send(embed=embed)
        await msg.add_reaction("🎉")
        await i.response.send_message("✅ Giveaway started.", ephemeral=True)
        await asyncio.sleep(secs)
        msg = await i.channel.fetch_message(msg.id)
        entrants = set()
        for r in msg.reactions:
            if str(r.emoji) == "🎉":
                async for u in r.users():
                    if not u.bot: entrants.add(u)
        if not entrants: return await i.channel.send("No valid entrants. 😔")
        winner = random.choice(list(entrants))
        await i.channel.send(f"🎉 **Winner:** {winner.mention} — Prize: **{prize}**")

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
