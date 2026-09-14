import discord
import random
from discord import app_commands
from discord.ext import commands

WOW_GREETINGS = [
    "Greetings, friend!",
    "Well met!",
    "Hail and well met!",
    "Greetings, traveler!",
    "Welcome, adventurer!",
    "Hello there, hero!",
    "Salutations!",
    "Hiya, pal!",
    "Greetings and salutations!",
    "Howdy, partner!",
    "Well, what do we have here?",
    "Greetings, brave one!",
    "Hello, my friend!",
    "Ah, welcome!",
    "Well, hello there!",
    "Greetings, noble one!",
    "Hail, adventurer!",
    "Welcome to our realm!",
    "Greetings, warrior!",
    "Hello, champion!",
]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Greet the bot and get a World of Warcraft greeting")
    async def hello(self, interaction: discord.Interaction):
        greeting = random.choice(WOW_GREETINGS)
        await interaction.response.send_message(f"{greeting} {interaction.user.mention}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
