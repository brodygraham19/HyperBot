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
    await interaction.response.send_message("Click below to verify ✅", view=VerifyButton())

@bot.tree.command(name="ping", description="Ping")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"🏓 `{round(bot.latency * 1000)}ms`")

@bot.tree.command(name="help", description="Help menu")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def help(interaction: Interaction):
    embed = discord.Embed(title="Commands", color=0x3498db)
    embed.add_field(name="/verifysetup", value="Send verify button", inline=False)
    embed.add_field(name="/ping", value="Latency", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
