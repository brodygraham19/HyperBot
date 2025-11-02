
import os, asyncio, logging
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
STATUS_ROTATOR_ENABLED = os.getenv("STATUS_ROTATOR_ENABLED", "true").lower() == "true"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    guild = None
    if GUILD_ID and GUILD_ID.isdigit():
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    print("✅ Slash commands synced")

    for cog in bot.cogs.values():
        if hasattr(cog, "setup_persistent_views"):
            await cog.setup_persistent_views()

    if STATUS_ROTATOR_ENABLED:
        status_cycle.start()

@tasks.loop(seconds=15)
async def status_cycle():
    statuses = [
        "Project Hyper ✅",
        "Use /verify_panel",
        "Use /ticket_panel",
        "Protecting server 🛡"
    ]
    for s in statuses:
        await bot.change_presence(activity=discord.Game(s))
        await asyncio.sleep(12)

async def load_cogs():
    names = ["verify", "tickets", "sync", "antiraid", "welcome"]
    for n in names:
        await bot.load_extension(f"cogs.{n}")
        print(f"Loaded {n}")

async def main():
    await load_cogs()
    await bot.start(TOKEN)

asyncio.run(main())
