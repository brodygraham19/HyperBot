import discord
from discord.ext import commands
from discord import app_commands
import datetime

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket 🎫", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        support_category = guild.get_channel(int(SUPPORT_CATEGORY_ID))
        staff_role = guild.get_role(int(STAFF_ROLE_ID))

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            staff_role: discord.PermissionOverwrite(view_channel=True),
            interaction.user: discord.PermissionOverwrite(view_channel=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=support_category,
            overwrites=overwrites
        )

        close_view = CloseTicketView()
        await ticket_channel.send(
            f"{interaction.user.mention} thanks for opening a ticket. Staff will be with you shortly.",
            view=close_view
        )

        await interaction.response.send_message(f"✅ Ticket opened: {ticket_channel.mention}", ephemeral=True)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket ❌", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        channel = interaction.channel
        closed_category = guild.get_channel(int(CLOSED_CATEGORY_ID))
        transcript_channel = guild.get_channel(int(TRANSCRIPT_CHANNEL_ID))

        # Create transcript
        messages = [f"{m.author}: {m.content}" async for m in channel.history(limit=None)]
        transcript = "\n".join(messages)
        file = discord.File(fp=bytes(transcript, "utf-8"), filename=f"{channel.name}_transcript.txt")

        await transcript_channel.send(f"📁 Transcript for {channel.name}", file=file)

        # Move channel
        await channel.edit(category=closed_category)
        await interaction.response.send_message("✅ Ticket closed and archived.", ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket_panel", description="Create the ticket panel")
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎟 Support Tickets",
            description="Click the button below to open a support ticket.",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Ticket(bot))
