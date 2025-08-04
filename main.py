import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load .env (used by GitHub secret)
load_dotenv()

# Set up bot with slash command support
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and slash commands are synced.")

@bot.tree.command(name="fansign", description="Send a fansign with a style and name")
@app_commands.describe(
    style="Pick a style (1 to 5)",
    name="What name to show on the fansign"
)
@app_commands.choices(style=[
    app_commands.Choice(name="Style 1", value="1"),
    app_commands.Choice(name="Style 2", value="2"),
    app_commands.Choice(name="Style 3", value="3"),
    app_commands.Choice(name="Style 4", value="4"),
    app_commands.Choice(name="Style 5", value="5"),
])
async def fansign(interaction: discord.Interaction, style: app_commands.Choice[str], name: str):
    image_path = f"images/style{style.value}.png"

    if not os.path.exists(image_path):
        await interaction.response.send_message(f"Style {style.value} image not found.", ephemeral=True)
        return

    # Open image and draw text
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Load a font
    font_path = "fonts/Arial.ttf"  # Replace with a good font file for realism
    font_size = 80  # Adjust for realistic size
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        await interaction.response.send_message("Font file not found. Make sure fonts/Arial.ttf exists.", ephemeral=True)
        return

    # Center text in the image
    text = name
    text_width, text_height = draw.textsize(text, font=font)
    image_width, image_height = image.size
    text_position = ((image_width - text_width) // 2, (image_height - text_height) // 2)

    # Add realistic text (white with black shadow)
    shadow_offset = 2
    draw.text((text_position[0] + shadow_offset, text_position[1] + shadow_offset), text, font=font, fill=(0, 0, 0))
    draw.text(text_position, text, font=font, fill=(255, 255, 255))

    # Save to temp file
    output_path = f"temp/fansign_{interaction.user.id}.png"
    os.makedirs("temp", exist_ok=True)
    image.save(output_path)

    await interaction.response.send_message(file=discord.File(output_path))

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
