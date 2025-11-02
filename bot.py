
GUILD_ID = 1202078664121126912
VERIFIED_ROLE_ID = 1431814189202018344

import os
import discord
from discord.ext import commands
from discord import app_commands, Interaction, ui

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyButton(ui.View):
    @ui.button(label="✅ Verify", style=discord.ButtonStyle.green)
    async def verify(self, interaction: Interaction, button: ui.Button):
        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        if role in interaction.user.roles:
            return await interaction.response.send_message("✅ Already verified!", ephemeral=True)
        await interaction.user.add_roles(role)
        await interaction.response.send_message("🎉 Verified!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

@bot.tree.command(name="verifysetup", description="Send verification button")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def verifysetup(interaction: Interaction):
    embed = discord.Embed(
        title="🔐 Verify To Enter",
        description=(
            "Welcome to **HyperBot Security Gateway**.\n\n"
            "**Click the button below to verify you're human.**\n"
            "Access will be granted instantly after verification."
        ),
        color=0x0A66C2
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1180236381920608276.png?size=96&quality=lossless")
    embed.set_footer(text="HyperBot Secure Verification | Cyber Shield Enabled")

    await interaction.response.send_message(embed=embed, view=VerifyButton())

@bot.tree.command(name="ping", description="Check bot latency")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"🏓 `{round(bot.latency * 1000)}ms`")

@bot.tree.command(name="help", description="Help menu")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def help(interaction: Interaction):
    embed = discord.Embed(title="🤖 HyperBot Commands", color=0x0A66C2)
    embed.add_field(name="/verifysetup", value="Send verification system", inline=False)
    embed.add_field(name="/ping", value="Show latency", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
