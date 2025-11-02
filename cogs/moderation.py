
import discord, os, json, pathlib
from discord.ext import commands
from discord import app_commands

LOGS_CHANNEL_ID = os.getenv("LOGS_CHANNEL_ID")
STAFF_ROLE_ID = os.getenv("STAFF_ROLE_ID")

WARN_FILE = pathlib.Path("data/warnings.json")
WARN_FILE.parent.mkdir(parents=True, exist_ok=True)
if not WARN_FILE.exists(): WARN_FILE.write_text("{}")

def mod_only():
    async def predicate(i: discord.Interaction) -> bool:
        if STAFF_ROLE_ID and i.user.get_role(int(STAFF_ROLE_ID)):
            return True
        return i.user.guild_permissions.manage_guild
    return app_commands.check(predicate)

async def send_log(guild: discord.Guild, embed: discord.Embed):
    try:
        if LOGS_CHANNEL_ID and LOGS_CHANNEL_ID.isdigit():
            ch = guild.get_channel(int(LOGS_CHANNEL_ID))
            if ch: await ch.send(embed=embed)
    except Exception: pass

class Moderation(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="clear", description="Delete a number of messages")
    @mod_only()
    async def clear(self, i: discord.Interaction, amount: int):
        await i.response.defer(ephemeral=True)
        deleted = await i.channel.purge(limit=amount)
        await i.followup.send(f"🧹 Deleted {len(deleted)}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
