import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

# Define available styles as choices for dropdown
style_choices = [
    app_commands.Choice(name="Style 1", value="style1.png"),
    app_commands.Choice(name="Style 2", value="style2.png"),
    app_commands.Choice(name="Style 3", value="style3.png"),
    app_commands.Choice(name="Style 4", value="style4.png"),
    app_commands.Choice(name="Style 5", value="style5.png"),
]

@bot.tree.command(name="fansign", description="Create a fansign with your name and a selected style")
@app_commands.describe(name="Your name to display", style="Select a fansign style")
@app_commands.choices(style=style_choices)
async def fansign(interaction: discord.Interaction, name: str, style: app_commands.Choice[str]):
    try:
        image_path = os.path.join("images", style.value)

        if not os.path.exists(image_path):
            await interaction.response.send_message(f"❌ Style image not found: {style.value}", ephemeral=True)
            return

        # Load the image and draw the text
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        font_path = "arial.ttf"  # Make sure this font file is in the repo or use default
        font_size = 40
        font = ImageFont.truetype(font_path, font_size)

        # Calculate position for centered text
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

        draw.text(position, name, font=font, fill="black")

        output_path = "output.png"
        image.save(output_path)

        await interaction.response.send_message(file=discord.File(output_path))
        os.remove(output_path)

    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

# Run the bot using the secret token from GitHub Actions or env
bot.run(os.getenv("DISCORD_TOKEN"))
