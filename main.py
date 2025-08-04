import discord
from discord.ext import commands
from discord import app_commands
import random
import os
from PIL import Image, ImageDraw, ImageFont

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

IMAGE_DIR = "images"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync: {e}")

@tree.command(name="tag", description="Generate a name tag with a random style")
@app_commands.describe(name="Your name to appear on the tag")
async def tag(interaction: discord.Interaction, name: str = "Player"):
    try:
        styles = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]
        if not styles:
            await interaction.response.send_message("No tag styles found.")
            return

        chosen_style = random.choice(styles)
        image_path = os.path.join(IMAGE_DIR, chosen_style)
        base = Image.open(image_path).convert("RGBA")

        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype(FONT_PATH, size=64)

        # Draw name centered
        text_width, text_height = draw.textsize(name, font=font)
        x = (base.width - text_width) // 2
        y = (base.height - text_height) // 2
        draw.text((x, y), name, font=font, fill="white")

        output_path = "output.png"
        base.save(output_path)

        await interaction.response.send_message(
            content=f"Here's your name tag, {name}!",
            file=discord.File(output_path)
        )

    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

import os
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    print("DISCORD_TOKEN environment variable not set.")
else:
    bot.run(TOKEN)
    
