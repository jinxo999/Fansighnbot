import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv

# Load the token from secrets (.env or GitHub secrets)
load_dotenv()

# Setup bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and slash commands are synced.")

# /fansign command
@bot.tree.command(name="fansign", description="Create a fansign image")
@app_commands.describe(
    style="Pick a style (1 to 5)",
    name="Name to appear on the fansign"
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
    font_path = "fonts/PatrickHand-Regular.ttf"
    output_path = f"output_{interaction.user.id}.png"

    if not os.path.exists(image_path):
        await interaction.response.send_message(f"Style {style.value} image not found.", ephemeral=True)
        return
    if not os.path.exists(font_path):
        await interaction.response.send_message("Font file not found.", ephemeral=True)
        return

    try:
        # Open and draw on image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 80)

        # Adjust position depending on your images
        text_position = (100, 100)
        draw.text(text_position, name, font=font, fill="black")

        # Save and send the result
        img.save(output_path)
        await interaction.response.send_message(file=discord.File(output_path))

        # Cleanup
        os.remove(output_path)

    except Exception as e:
        await interaction.response.send_message(f"Error creating fansign: {e}", ephemeral=True)

# Start the bot
bot.run(os.getenv("DISCORD_TOKEN"))
