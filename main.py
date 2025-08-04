import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(bot)

class StyleDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=f"Style {i}", value=f"{i}")
            for i in range(1, 6)
        ]
        super().__init__(
            placeholder="Choose your style",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        style_number = self.values[0]
        await interaction.response.send_message(f"You selected Style {style_number}!", ephemeral=True)

class DropdownView(View):
    def __init__(self):
        super().__init__()
        self.add_item(StyleDropdown())

@tree.command(name="fansign", description="Pick a fansign style.")
async def fansign(interaction: discord.Interaction):
    await interaction.response.send_message("Choose your fansign style:", view=DropdownView(), ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user}!")

bot.run(TOKEN)
