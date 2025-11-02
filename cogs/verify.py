
import discord, os
from discord.ext import commands
from discord import app_commands

VERIFY_ROLE_ID = os.getenv("VERIFY_ROLE_ID")
VERIFY_LOGS_CHANNEL_ID = os.getenv("VERIFY_LOGS_CHANNEL_ID")

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Verify ✅", style=discord.ButtonStyle.success, custom_id="verify_btn")
    async def verify(self, i: discord.Interaction, button: discord.ui.Button):
        role = i.guild.get_role(int(VERIFY_ROLE_ID))
        await i.user.add_roles(role)
        await i.response.send_message("✅ Verified!", ephemeral=True)

class Verify(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def setup_persistent_views(self):
        self.bot.add_view(VerifyView())

    @app_commands.command(name="verify_panel", description="Send verify button")
    async def panel(self, i: discord.Interaction):
        embed = discord.Embed(title="✅ Verify", description="Press to verify", color=0x00ff00)
        await i.response.send_message("✅ Panel sent", ephemeral=True)
        await i.channel.send(embed=embed, view=VerifyView())

async def setup(bot): await bot.add_cog(Verify(bot))
