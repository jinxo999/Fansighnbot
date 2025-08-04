import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os

# Get token from environment variable
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# Map number styles to image files
STYLE_IMAGES = {
    "1": "images/style1.png",
    "2": "images/style2.png",
    "3": "images/style3.png",
    "4": "images/style4.png",
    "5": "images/style5.png",
    "6": "images/style6.png"
}

@bot.command()
async def fansign(ctx, navn: str, style: str = "1"):
    if style not in STYLE_IMAGES:
        await ctx.send("Invalid style number. Use 1-6.")
        return

    image_path = STYLE_IMAGES[style]
    base_image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(base_image)

    # Font and text position
    font = ImageFont.load_default()
    text_position = (100, 100)
    draw.text(text_position, navn, fill="black", font=font)

    output_path = f"output/{navn}_style{style}.png"
    os.makedirs("output", exist_ok=True)
    base_image.save(output_path)

    await ctx.send(file=discord.File(output_path))

# Run bot using token from GitHub secrets
if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable not found.")
  
