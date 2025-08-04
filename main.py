import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont

# Load environment variables from .env
load_dotenv()

# Bot setup with slash command support
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and slash commands are synced.")


@bot.tree.command(name="fansign", description="Send a fansign with a name and style")
@app_commands.describe(
    name="The name to write on the fansign",
    style="Choose a style (1 to 5)"
)
@app_commands.choices(style=[
    app_commands.Choice(name="Style 1", value="1"),
    app_commands.Choice(name="Style 2", value="2"),
    app_commands.Choice(name="Style 3", value="3"),
    app_commands.Choice(name="Style 4", value="4"),
    app_commands.Choice(name="Style 5", value="5"),
])
async def fansign(interaction: discord.Interaction, name: str, style: app_commands.Choice[str]):
    image_path = f"images/style{style.value}.png"
    font_path = "fonts/PatrickHand-Regular.ttf"
    output_path = "output/final_fansign.png"

    if not os.path.exists(image_path):
        await interaction.response.send_message(f"Style {style.value} image not found.", ephemeral=True)
        return

    if not os.path.exists(font_path):
        await interaction.response.send_message("Font file not found. Make sure fonts/PatrickHand-Regular.ttf exists.", ephemeral=True)
        return

    # Open and edit the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=64)

    # Position: adjust to your preferred spot
    draw.text((120, 120), name, font=font, fill=(0, 255, 0))  # Light green

    os.makedirs("output", exist_ok=True)
    img.save(output_path)

    await interaction.response.send_message(file=discord.File(output_path))


# Start the bot
bot.run(os.getenv("DISCORD_TOKEN"))
