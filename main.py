import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Use existing command tree
tree = bot.tree

class StyleDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Style 1", value="style1"),
            discord.SelectOption(label="Style 2", value="style2"),
            discord.SelectOption(label="Style 3", value="style3"),
            discord.SelectOption(label="Style 4", value="style4"),
            discord.SelectOption(label="Style 5", value="style5"),
        ]
        super().__init__(placeholder="Choose a style", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected **{self.values[0]}**!", ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(StyleDropdown())

@tree.command(name="fansign", description="Choose a fansign style")
async def fansign_command(interaction: discord.Interaction):
    await interaction.response.send_message("Pick a style for your fansign:", view=DropdownView(), ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user} and synced commands.")

bot.run("YOUR_BOT_TOKEN")
