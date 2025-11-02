
import discord
from discord.ext import commands
from discord import app_commands

class RoleButton(discord.ui.View):
    def __init__(self, role_id: int, label: str):
        super().__init__(timeout=None)
        btn = discord.ui.Button(label=label, style=discord.ButtonStyle.secondary, custom_id=f"rolebtn:{role_id}")
        self.add_item(btn)

class Roles(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="rolebutton", description="Create a role-toggle button for a role ID")
    async def rolebutton(self, i: discord.Interaction, role_id: str, label: str="Get Role"):
        if not role_id.isdigit():
            return await i.response.send_message("❌ Provide a numeric role ID.", ephemeral=True)
        view = RoleButton(int(role_id), label)
        embed = discord.Embed(title="Role Button", description=f"Click to toggle <@&{role_id}>", color=0x2b2d31)
        await i.channel.send(embed=embed, view=view)
        await i.response.send_message("✅ Role button created.", ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, i: discord.Interaction):
        if i.type != discord.InteractionType.component: return
        cid = i.data.get("custom_id", "")
        if cid.startswith("rolebtn:"):
            rid = int(cid.split(":")[1])
            role = i.guild.get_role(rid)
            if not role: return await i.response.send_message("Role missing.", ephemeral=True)
            if role in i.user.roles:
                await i.user.remove_roles(role); msg = f"❎ Removed {role.mention}"
            else:
                await i.user.add_roles(role); msg = f"✅ Added {role.mention}"
            await i.response.send_message(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roles(bot))
