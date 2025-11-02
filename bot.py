
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
            return await interaction.response.send_message("✅ You're already verified!", ephemeral=True)
        await interaction.user.add_roles(role)
        await interaction.response.send_message("🎉 You are now verified!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"❌ Command sync error: {e}")

@bot.tree.command(name="verifysetup", description="Send the verification button")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def verifysetup(interaction: Interaction):
    await interaction.response.send_message("**Click the button below to verify!**", view=VerifyButton())

@bot.tree.command(name="ping", description="Check bot latency")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"🏓 `{round(bot.latency * 1000)}ms`")

@bot.tree.command(name="help", description="Show available commands")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def help_cmd(interaction: Interaction):
    embed = discord.Embed(title="Bot Commands", color=0x3498db)
    embed.add_field(name="/verifysetup", value="Send verification button", inline=False)
    embed.add_field(name="/ping", value="Show latency", inline=False)
    embed.add_field(name="/info", value="Bot info", inline=False)
    embed.add_field(name="/help", value="Show help", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info", description="Bot info")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def info(interaction: Interaction):
    await interaction.response.send_message(f"🤖 Bot running as **{bot.user}**")

bot.run(TOKEN)
