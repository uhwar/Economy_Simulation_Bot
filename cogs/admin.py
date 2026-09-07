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
        # Admin command - add coins to any player's balance
        await database.add_balance(target.id, amount)
        new_bal = await database.get_balance(target.id)
        await interaction.response.send_message(f"You added {amount} coins to {target.mention}'s balance")
        await database.log_transaction(target.id, f"Admin add by {interaction.user.mention}", amount, new_bal)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

    @app_commands.command(name="admin_bailout", description="Removes a players from the jail")
    @app_commands.checks.has_role("Admin")
    async def admin_bailout(self, interaction: discord.Interaction, target: discord.Member):
        # Admin command - free a player from jail
        now = int(time.time())
        in_jail = await database.get_jail_until(target.id)
        user_id = interaction.user.id
        if in_jail > now:
            await database.set_jail_until(target.id, 0)
            await database.log_transaction(user_id, "Admin bailed out user",0,0)
            await interaction.response.send_message(f"{target.mention} is free now!")
        else:
            await interaction.response.send_message("User is already free!")

    @app_commands.command(name="jail_player", description="Place a player in jail")
    @app_commands.checks.has_role("Admin")
    async def jail_player(self, interaction: discord.Interaction, target:discord.Member):
        now = int(time.time())
        jail_until = int(time.time()) + 3600
        in_jail = await database.get_jail_until(target.id)
        user_id = interaction.user.id
        if in_jail < now:
            await database.set_jail_until(target.id, jail_until)
            await database.log_transaction(user_id, f"Admin put {target.id} in jail", 0, 0)
            await interaction.response.send_message(f"{target.mention} has been sent to jail")
        else:
            await interaction.response.send_message(f"{target.mention} is currently a free man")

async def setup(bot):
    await bot.add_cog(Admin(bot))
