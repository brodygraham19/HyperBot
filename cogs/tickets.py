
import discord, os, io
from discord.ext import commands
from discord import app_commands

SUPPORT_CATEGORY_ID = int(os.getenv("SUPPORT_CATEGORY_ID"))
CLOSED_CATEGORY_ID = int(os.getenv("CLOSED_CATEGORY_ID"))
STAFF_ROLE_ID = os.getenv("STAFF_ROLE_ID")
TRANSCRIPT_CHANNEL_ID = os.getenv("TRANSCRIPT_CHANNEL_ID")

class OpenView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🎟 Open Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket_btn")
    async def open(self, i: discord.Interaction, button: discord.ui.Button):
        guild = i.guild
        category = guild.get_channel(SUPPORT_CATEGORY_ID)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            i.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }
        if STAFF_ROLE_ID:
            staff = guild.get_role(int(STAFF_ROLE_ID))
            if staff: overwrites[staff] = discord.PermissionOverwrite(view_channel=True)

        ch = await guild.create_text_channel(f"ticket-{i.user.name}", category=category, overwrites=overwrites)

        await ch.send(f"{i.user.mention} ticket opened.", view=CloseView())
        await i.response.send_message("✅ Ticket created", ephemeral=True)

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn")
    async def close(self, i: discord.Interaction, button: discord.ui.Button):
        guild = i.guild
        channel = i.channel

        msgs = [m async for m in channel.history(limit=None, oldest_first=True)]
        txt = "\n".join([f"{m.author}: {m.content}" for m in msgs])
        file = discord.File(io.BytesIO(txt.encode()), filename=f"{channel.name}.txt")

        if TRANSCRIPT_CHANNEL_ID:
            tchan = guild.get_channel(int(TRANSCRIPT_CHANNEL_ID))
            if tchan: await tchan.send(file=file)

        closed_cat = guild.get_channel(CLOSED_CATEGORY_ID)
        await channel.edit(category=closed_cat, name=f"closed-{channel.name}")
        await channel.send("✅ Closed")

class Tickets(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def setup_persistent_views(self):
        self.bot.add_view(OpenView())
        self.bot.add_view(CloseView())

    @app_commands.command(name="ticket_panel", description="Send ticket panel")
    async def panel(self, i: discord.Interaction):
        embed = discord.Embed(title="🎟 Support", description="Press to open ticket", color=0x00ff00)
        await i.response.send_message("✅ Sent", ephemeral=True)
        await i.channel.send(embed=embed, view=OpenView())

async def setup(bot): await bot.add_cog(Tickets(bot))
