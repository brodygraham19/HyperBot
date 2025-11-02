
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = "MTQzNDM4NTU0MzM2NTM5NDU0Ng.GXLVrM.uSUVuQSFTs2UfOZBeXCJkpr0BuEpB2ahSLfl4Q"

GUILD_ID = 1202078664121126912
VERIFIED_ROLE_ID = 1431814189202018344
STAFF_ROLE_ID = 1202078664137646131
TICKET_CATEGORY_ID = 1434362164944175144
CLOSED_CATEGORY_ID = 1434362164944175144

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyView(discord.ui.View):
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ Verified!", ephemeral=True)

class CloseView(discord.ui.View):
    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        channel = interaction.channel
        closed = guild.get_channel(CLOSED_CATEGORY_ID)
        await channel.edit(category=closed, name=f"closed-{channel.name}")
        await interaction.response.send_message("✅ Closed ticket", ephemeral=True)

class TicketView(discord.ui.View):
    @discord.ui.button(label="🎟 Open Ticket", style=discord.ButtonStyle.green)
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        cat = guild.get_channel(TICKET_CATEGORY_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        staff = guild.get_role(STAFF_ROLE_ID)
        if staff:
            overwrites[staff] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        ch = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=cat, overwrites=overwrites)
        await ch.send(f"{interaction.user.mention} thanks for opening a ticket.", view=CloseView())
        await interaction.response.send_message("✅ Ticket created!", ephemeral=True)

@bot.event
async def on_ready():
    print("✅ Bot Ready", bot.user)
    guild = discord.Object(id=GUILD_ID)
    bot.add_view(VerifyView())
    bot.add_view(TicketView())
    bot.add_view(CloseView())
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

@bot.tree.command()
async def verify_panel(interaction: discord.Interaction):
    await interaction.response.send_message("Press to verify:", view=VerifyView())

@bot.tree.command()
async def ticket_panel(interaction: discord.Interaction):
    await interaction.response.send_message("Press to open a ticket:", view=TicketView())

bot.run(TOKEN)
