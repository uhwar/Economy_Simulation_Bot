import discord
from discord import app_commands
from discord.ext import commands
import database


class Transfers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="money_wire", description="Wire coins to another player")
    async def money_wire(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        # Send coins to another player (admin/development command)
        await database.add_balance(target.id, amount)
        await interaction.response.send_message(f"💰 {target.mention} was sent **{amount} coins**!")
        new_bal = await database.get_balance(target.id)
        await database.log_transaction(target.id, f"User sent {amount} to player", amount, new_bal)


async def setup(bot):
    await bot.add_cog(Transfers(bot))
