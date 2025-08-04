import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os

# Constants
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Safe default for GitHub Actions
FONT_SIZE = 45
IMAGE_FOLDER = "images"

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user}")

@tree.command(name="fansign", description="Create a fansign image with your name and style.")
@app_commands.describe(name="Your name to appear on the fansign", style="Choose a style image")
@app_commands.choices(
    style=[
        app_commands.Choice(name="Style 1", value=1),
        app_commands.Choice(name="Style 2", value=2),
        app_commands.Choice(name="Style 3", value=3),
        app_commands.Choice(name="Style 4", value=4),
        app_commands.Choice(name="Style 5", value=5),
    ]
)
async def fansign(interaction: discord.Interaction, name: str, style: app_commands.Choice[int]):
    await interaction.response.defer()

    image_path = os.path.join(IMAGE_FOLDER, f"style{style.value}.png")

    if not os.path.exists(image_path):
        await interaction.followup.send(f"❌ Style {style.value} not found.")
        return

    # Open image and draw text
    with Image.open(image_path).convert("RGBA") as img:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Font load failed: {e}")
            return

        # Center the text
        text = name
        text_width, text_height = draw.textsize(text, font=font)
        x = (img.width - text_width) // 2
        y = img.height - text_height - 40

        draw.text((x, y), text, font=font, fill="white")

        output_path = f"fansign_{interaction.user.id}.png"
        img.save(output_path)

    await interaction.followup.send(file=discord.File(output_path))
    os.remove(output_path)

# Run bot using GitHub Actions secret
if __name__ == "__main__":
    import asyncio

    async def start_bot():
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("❌ DISCORD_TOKEN environment variable not set.")
        else:
            await bot.start(token)

    asyncio.run(start_bot())
    
