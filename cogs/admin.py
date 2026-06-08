import discord
import time
import random
from discord import app_commands
from discord.ext import commands
import database

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="give_player_balance", description="Add coins to a user's balance")
    @app_commands.checks.has_role("Admin")
    async def add_balance(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        await database.add_balance(target.id, amount)
        new_bal = await database.get_balance(target.id)
        await interaction.response.send_message(f"You added {amount} coins to {target.mention}'s balance")
        await database.log_transaction(target.id, f"Admin add by {interaction.user.mention}", amount, new_bal)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Admin(bot))
