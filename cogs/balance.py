import discord
from discord import app_commands
from discord.ext import commands
import database


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        # Get user's coin balance from database
        bal = await database.get_balance(interaction.user.id)
        await interaction.response.send_message(
            f"💰 {interaction.user.mention}, you have **{bal} coins**"
        )


async def setup(bot):
    await bot.add_cog(Balance(bot))
