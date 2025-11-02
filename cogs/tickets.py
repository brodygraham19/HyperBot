
import discord, os, io
from discord.ext import commands
from discord import app_commands

SUPPORT_CATEGORY_ID = int(os.getenv("SUPPORT_CATEGORY_ID"))
CLOSED_CATEGORY_ID = int(os.getenv("CLOSED_CATEGORY_ID"))
STAFF_ROLE_ID = os.getenv("STAFF_ROLE_ID")
TRANSCRIPT_CHANNEL_ID = os.getenv("TRANSCRIPT_CHANNEL_ID")

class TicketOpenView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="🎟️ Open Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket_btn"))

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn"))

class Ticket(commands.Cog):
    def __init__(self, bot): self.bot = bot

    async def setup_persistent_views(self):
        self.bot.add_view(TicketOpenView())
        self.bot.add_view(TicketCloseView())

    @app_commands.command(name="ticket_panel", description="Send ticket panel")
    async def ticket_panel(self, i: discord.Interaction):
        em = discord.Embed(title="🎟 Support Tickets", description="Press **Open Ticket** below.", color=0x2b2d31)
        await i.response.send_message("✅ Panel sent.", ephemeral=True)
        await i.channel.send(embed=em, view=TicketOpenView())

    async def _close_and_archive(self, guild: discord.Guild, channel: discord.TextChannel, closer: discord.Member):
        # Make transcript
        messages = [m async for m in channel.history(limit=None, oldest_first=True)]
        transcript = "\n".join([f"[{m.created_at:%Y-%m-%d %H:%M}] {m.author}: {m.clean_content}" for m in messages])
        data = io.BytesIO(transcript.encode())
        file = discord.File(data, filename=f"{channel.name}.txt")

        if TRANSCRIPT_CHANNEL_ID and TRANSCRIPT_CHANNEL_ID.isdigit():
            tchan = guild.get_channel(int(TRANSCRIPT_CHANNEL_ID))
            if tchan:
                await tchan.send(f"📄 Transcript for `{channel.name}` (closed by {closer.mention})", file=file)

        closed_category = guild.get_channel(CLOSED_CATEGORY_ID)
        if closed_category:
            user_suffix = channel.name[7:] if channel.name.startswith("ticket-") else channel.name
            await channel.edit(category=closed_category, name=f"closed-{user_suffix}")
        await channel.send("✅ Ticket closed & archived.")

    @commands.Cog.listener()
    async def on_interaction(self, i: discord.Interaction):
        if i.type == discord.InteractionType.component and i.data.get("custom_id") == "open_ticket_btn":
            guild = i.guild
            user = i.user
            category = guild.get_channel(SUPPORT_CATEGORY_ID)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            }
            staff_role = guild.get_role(int(STAFF_ROLE_ID)) if STAFF_ROLE_ID and STAFF_ROLE_ID.isdigit() else None
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
            ch = await guild.create_text_channel(f"ticket-{user.name}".replace(' ','-')[:95], category=category, overwrites=overwrites)
            await ch.send(f"{user.mention} thanks for opening a ticket. Staff will be with you shortly.", view=TicketCloseView())
            return await i.response.send_message("✅ Ticket created.", ephemeral=True)

        if i.type == discord.InteractionType.component and i.data.get("custom_id") == "close_ticket_btn":
            return await self._close_and_archive(i.guild, i.channel, i.user)

async def setup(bot): await bot.add_cog(Ticket(bot))
