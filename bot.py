import discord
from discord.ext import commands
from discord import app_commands
import os

# ---- YOUR SERVER SETTINGS ----
GUILD_ID = 1202078664121126912
VERIFIED_ROLE_ID = 1431814189202018344

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Verify Button View
class VerifyButton(discord.ui.View):
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Verified!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Role missing.", ephemeral=True)

# Slash command to post verify panel
@bot.tree.command(name="verifysetup", description="Send verify button")
async def verifysetup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✅ Verify To Enter",
        description="Click verify to gain access.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=VerifyButton())

# Force sync commands to guild
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Synced {len(synced)} slash commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync error: {e}")
    print(f"🤖 Logged in as {bot.user}")

bot.run(TOKEN)
