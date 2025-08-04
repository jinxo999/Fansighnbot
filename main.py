import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(bot)

# 📁 Folder where your images are stored
IMAGE_FOLDER = "images"  # must exist in your repo

# 📐 Font settings
FONT_PATH = "arial.ttf"  # or another .ttf font file in your repo
FONT_SIZE = 60

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Bot logged in as {bot.user} (slash commands synced)")

@tree.command(name="fansign", description="Create a fansign with your name and style.")
@app_commands.describe(
    name="Enter your name",
    style="Choose a style from 1 to 5"
)
@app_commands.choices(style=[
    app_commands.Choice(name="Style 1", value=1),
    app_commands.Choice(name="Style 2", value=2),
    app_commands.Choice(name="Style 3", value=3),
    app_commands.Choice(name="Style 4", value=4),
    app_commands.Choice(name="Style 5", value=5),
])
async def fansign(interaction: discord.Interaction, name: str, style: app_commands.Choice[int]):
    try:
        image_path = os.path.join(IMAGE_FOLDER, f"style{style.value}.png")
        image = Image.open(image_path).convert("RGBA")

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

        # Text position (adjust to fit your images)
        text = name
        text_width, text_height = draw.textsize(text, font=font)
        x = (image.width - text_width) // 2
        y = image.height - text_height - 50  # bottom padding

        draw.text((x, y), text, font=font, fill="white")

        output_path = f"output_{interaction.user.id}.png"
        image.save(output_path)

        await interaction.response.send_message(
            content=f"Here’s your fansign, **{name}** (Style {style.value})!",
            file=discord.File(output_path)
        )

        os.remove(output_path)  # optional cleanup

    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}")

bot.run(TOKEN)
