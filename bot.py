
import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1202078664121126912  # your server

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("✅ Slash commands synced")

# ---------- VERIFY BUTTON ----------
class VerifyButton(discord.ui.View):
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ You are verified!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Verified role not found.", ephemeral=True)

@bot.tree.command(name="verifysetup", description="Send verify button")
async def verifysetup(interaction: discord.Interaction):
    await interaction.response.send_message("Click below to verify:", view=VerifyButton())

# ---------- TICKET SYSTEM ----------
class TicketButton(discord.ui.View):
    @discord.ui.button(label="🎟️ Open Ticket", style=discord.ButtonStyle.blurple)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="tickets")
        if not category:
            category = await guild.create_category("tickets")

        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)
        await channel.send(f"{interaction.user.mention} Welcome to support!")

@bot.tree.command(name="ticketsetup", description="Send ticket button")
async def ticketsetup(interaction: discord.Interaction):
    await interaction.response.send_message("Click to open support ticket:", view=TicketButton())

bot.run(TOKEN)
