import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import os

from dotenv import load_dotenv
load_dotenv()

# Setup bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot ready: {bot.user}")

@bot.tree.command(name="fansign", description="Send a fansign with your name and style")
@app_commands.describe(
    style="Choose a style (1 to 5)",
    name="Your name to appear on the fansign"
)
@app_commands.choices(style=[
    app_commands.Choice(name="Style 1", value="1"),
    app_commands.Choice(name="Style 2", value="2"),
    app_commands.Choice(name="Style 3", value="3"),
    app_commands.Choice(name="Style 4", value="4"),
    app_commands.Choice(name="Style 5", value="5"),
])
async def fansign(interaction: discord.Interaction, style: app_commands.Choice[str], name: str = "Luster"):
    try:
        image_path = f"images/style{style.value}.png"
        font_path = "Arial.ttf"
        
        # Check files
        if not os.path.exists(image_path):
            await interaction.response.send_message(f"Image not found: `{image_path}`", ephemeral=True)
            return
        if not os.path.exists(font_path):
            await interaction.response.send_message(f"Font not found: `{font_path}`", ephemeral=True)
            return

        # Load and draw on image
        base = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype(font_path, 80)

        # Use textbbox for Pillow compatibility
        text_box = draw.textbbox((0, 0), name, font=font)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        # Center the text
        position = ((base.width - text_width) // 2, (base.height - text_height) // 2)
        draw.text(position, name, font=font, fill="black")

        # Save to temp file
        output_path = f"fansign_output.png"
        base.save(output_path)

        await interaction.response.send_message(file=discord.File(output_path))
        os.remove(output_path)  # Clean up
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
