import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load .env (used by GitHub secret)
load_dotenv()

# Set up bot with slash command support
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Fansign command using dropdown styles
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and slash commands are synced.")

@bot.tree.command(name="fansign", description="Send a fansign with a style")
@app_commands.describe(style="Pick a style (1 to 5)")
@app_commands.choices(style=[
    app_commands.Choice(name="Style 1", value="1"),
    app_commands.Choice(name="Style 2", value="2"),
    app_commands.Choice(name="Style 3", value="3"),
    app_commands.Choice(name="Style 4", value="4"),
    app_commands.Choice(name="Style 5", value="5"),
])
async def fansign(interaction: discord.Interaction, style: app_commands.Choice[str]):
    image_path = f"images/style{style.value}.png"
    if os.path.exists(image_path):
        await interaction.response.send_message(file=discord.File(image_path))
    else:
        await interaction.response.send_message(f"Style {style.value} image not found.", ephemeral=True)

# Run the bot using the token from GitHub Secrets
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
