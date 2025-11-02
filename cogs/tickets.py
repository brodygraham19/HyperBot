
import discord, os, io, datetime
from discord.ext import commands
from discord import app_commands

TICKET_CATEGORY_ID = os.getenv("TICKET_CATEGORY_ID")
STAFF_ROLE_ID = os.getenv("STAFF_ROLE_ID")
TRANSCRIPT_CHANNEL_ID = os.getenv("TRANSCRIPT_CHANNEL_ID")

class OpenTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Open Ticket 🎟️", style=discord.ButtonStyle.primary, custom_id="open_ticket"))

class Ticket(commands.Cog):
    def __init__(self, bot): self.bot = bot

    async def setup_persistent_views(self): self.bot.add_view(OpenTicketView())

    def _staff_role(self, guild: discord.Guild):
        return guild.get_role(int(STAFF_ROLE_ID)) if STAFF_ROLE_ID and STAFF_ROLE_ID.isdigit() else None

    def _category(self, guild: discord.Guild):
        return guild.get_channel(int(TICKET_CATEGORY_ID)) if TICKET_CATEGORY_ID and TICKET_CATEGORY_ID.isdigit() else None

    @app_commands.command(name="ticket_panel", description="Send a ticket open panel")
    async def ticket_panel(self, i: discord.Interaction):
        em = discord.Embed(title="🎟 Support Tickets", description="Press **Open Ticket** below.", color=0x2b2d31)
        await i.response.send_message("✅ Panel sent.", ephemeral=True)
        await i.channel.send(embed=em, view=OpenTicketView())

    @app_commands.command(name="ticket_close", description="Close this ticket and save transcript")
    async def ticket_close(self, i: discord.Interaction):
        if not i.channel.name.startswith("ticket-"):
            return await i.response.send_message("❌ This isn't a ticket channel.", ephemeral=True)
        await i.response.defer(ephemeral=True)
        messages = [m async for m in i.channel.history(limit=None, oldest_first=True)]
        buf = io.StringIO()
        buf.write(f"Transcript for #{i.channel.name}\nGenerated: {datetime.datetime.utcnow().isoformat()}Z\n\n")
        for m in messages:
            ts = m.created_at.strftime("%Y-%m-%d %H:%M")
            buf.write(f"[{ts}] {m.author}: {m.clean_content}\n")
        file = discord.File(fp=io.BytesIO(buf.getvalue().encode()), filename=f"{i.channel.name}.txt")
        if TRANSCRIPT_CHANNEL_ID and TRANSCRIPT_CHANNEL_ID.isdigit():
            tchan = i.guild.get_channel(int(TRANSCRIPT_CHANNEL_ID))
            if tchan: await tchan.send(file=file, content=f"📄 Transcript: {i.channel.mention}")
        await i.channel.delete(reason=f"Closed by {i.user}")

    @app_commands.command(name="ticket_add", description="Add a user to this ticket")
    async def ticket_add(self, i: discord.Interaction, user: discord.Member):
        if not i.channel.name.startswith("ticket-"):
            return await i.response.send_message("❌ Not a ticket.", ephemeral=True)
        await i.channel.set_permissions(user, view_channel=True, send_messages=True, read_message_history=True)
        await i.response.send_message(f"✅ Added {user.mention}.", ephemeral=True)

    @app_commands.command(name="ticket_remove", description="Remove a user from this ticket")
    async def ticket_remove(self, i: discord.Interaction, user: discord.Member):
        if not i.channel.name.startswith("ticket-"):
            return await i.response.send_message("❌ Not a ticket.", ephemeral=True)
        await i.channel.set_permissions(user, overwrite=None)
        await i.response.send_message(f"✅ Removed {user.mention}.", ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, i: discord.Interaction):
        if not (i.type == discord.InteractionType.component and i.data.get("custom_id") == "open_ticket"):
            return
        guild = i.guild
        category = self._category(guild)
        staff = self._staff_role(guild)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            i.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }
        if staff:
            overwrites[staff] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        ch = await guild.create_text_channel(f"ticket-{i.user.name}".replace(' ','-')[:95], category=category, overwrites=overwrites)
        await ch.send(f"{i.user.mention} thanks for opening a ticket. Staff will be with you shortly.")
        await i.response.send_message("✅ Ticket created.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
