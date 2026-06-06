import discord
from discord.ext import commands
import database
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")
if not GUILD_ID:
    raise ValueError("GUILD_ID not found in .env file")

# Debug: Show token format (first 10 chars only for security)
print(f"Token loaded: {TOKEN[:10]}... (length: {len(TOKEN)})")

MY_GUILD = discord.Object(id=int(GUILD_ID))
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)


    async def setup_hook(self):
        await database.setup_db()
        await self.load_extension("cogs.economy")
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        print("Bot ready.")

bot = MyBot()
bot.run(TOKEN)
