import discord
from discord.ext import commands
from discord import app_commands
import os

# ============================
# ✅ SET YOUR SERVER VALUES HERE
# ============================

GUILD_ID = 1202078664121126912  # <<--- your server ID
VERIFIED_ROLE_ID = 1431814189202018344  # <<--- your verify role ID

# ============================

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyButton(discord.ui.View):
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(VERIFIED_ROLE_ID)

        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ You are now verified!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Verification role not found.", ephemeral=True)

@bot.tree.command(name="verifysetup", description="Send verify button to channel")
async def verifysetup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✅ Verify To Enter",
        description="Click the button below to verify you are human.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=VerifyButton())

@bot.event
async def on_ready():
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Force Synced {len(synced)} commands to {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync Error: {e}")

    print(f"🤖 Logged in as {bot.user}")

bot.run(TOKEN)