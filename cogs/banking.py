import discord
import time
from discord import app_commands
from discord.ext import commands
import database

class Banking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bank_balance", description="Check your bank balance and interest")
    async def bank_balance(self, interaction: discord.Interaction):
        # Show wallet + bank balance with interest calculation
        user_id = interaction.user.id
        interest_earned = await database.calculate_interest(user_id)
        wallet_bal = await database.get_balance(user_id)
        bank_bal = await database.get_bank_balance(user_id)
        interest_rate = await database.get_interest_rate(user_id)
        last_calc = await database.get_last_interest_calculation(user_id)
        now = int(time.time())
        if last_calc > 0:
            next_calc = last_calc + 86400
            hours_until = (next_calc - now) // 3600
        else:
            hours_until = 24
        message = f"💰 **Bank Statement for {interaction.user.mention}**\n"
        message += f"**Wallet:** {wallet_bal} coins\n"
        message += f"**Bank:** {bank_bal} coins\n"
        message += f"**Total Wealth:** {wallet_bal + bank_bal} coins\n"
        if interest_earned > 0:
            message += f"📈 **Interest Earned:** +{interest_earned} coins\n"
        message += f"**Interest Rate:** {interest_rate*100:.1f}% daily\n"
        message += f"**Next Interest:** in ~{hours_until} hours"
        await interaction.response.send_message(message)

    @app_commands.command(name="bank_deposit", description="Deposit coins to your bank account")
    @app_commands.describe(amount="How many coins to deposit")
    async def bank_deposit(self, interaction: discord.Interaction, amount: int):
        # Deposit specific amount from wallet to bank
        user_id = interaction.user.id
        if amount <= 0:
            await interaction.response.send_message("Amount must be more than 0.")
            return
        wallet_bal = await database.get_balance(user_id)
        if amount > wallet_bal:
            await interaction.response.send_message("You don't have enough coins in your wallet.")
            return
        await database.calculate_interest(user_id)
        await database.deposit_to_bank(user_id, amount)
        new_wallet = await database.get_balance(user_id)
        new_bank = await database.get_bank_balance(user_id)
        await interaction.response.send_message(
            f"✅ Deposited **{amount} coins** to your bank.\n"
            f"**Wallet:** {new_wallet} coins\n"
            f"**Bank:** {new_bank} coins"
        )

    @app_commands.command(name="bank_deposit_all", description="Deposit all coins to your bank")
    async def bank_deposit_all(self, interaction: discord.Interaction):
        # Deposit entire wallet balance to bank
        user_id = interaction.user.id
        wallet_bal = await database.get_balance(user_id)
        if wallet_bal <= 0:
            await interaction.response.send_message("You don't have any coins to deposit.")
            return
        await database.calculate_interest(user_id)
        await database.deposit_to_bank(user_id, wallet_bal)
        new_wallet = await database.get_balance(user_id)
        new_bank = await database.get_bank_balance(user_id)
        await interaction.response.send_message(
            f"✅ Deposited **{wallet_bal} coins** to your bank.\n"
            f"**Wallet:** {new_wallet} coins\n"
            f"**Bank:** {new_bank} coins"
        )

    @app_commands.command(name="bank_withdraw", description="Withdraw coins from your bank")
    @app_commands.describe(amount="How many coins to withdraw")
    async def bank_withdraw(self, interaction: discord.Interaction, amount: int):
        # Withdraw specific amount from bank to wallet
        user_id = interaction.user.id
        if amount <= 0:
            await interaction.response.send_message("Amount must be more than 0.")
            return
        await database.calculate_interest(user_id)
        bank_bal = await database.get_bank_balance(user_id)
        if amount > bank_bal:
            await interaction.response.send_message("You don't have enough coins in your bank.")
            return
        await database.withdraw_from_bank(user_id, amount)
        new_wallet = await database.get_balance(user_id)
        new_bank = await database.get_bank_balance(user_id)
        await interaction.response.send_message(
            f"✅ Withdrew **{amount} coins** from your bank.\n"
            f"**Wallet:** {new_wallet} coins\n"
            f"**Bank:** {new_bank} coins"
        )

    @app_commands.command(name="bank_withdraw_all", description="Withdraw all coins from your bank")
    async def bank_withdraw_all(self, interaction: discord.Interaction):
        # Withdraw entire bank balance to wallet
        user_id = interaction.user.id
        await database.calculate_interest(user_id)
        bank_bal = await database.get_bank_balance(user_id)
        if bank_bal <= 0:
            await interaction.response.send_message("You don't have any coins in your bank.")
            return
        await database.withdraw_from_bank(user_id, bank_bal)
        new_wallet = await database.get_balance(user_id)
        new_bank = await database.get_bank_balance(user_id)
        await interaction.response.send_message(
            f"✅ Withdrew **{bank_bal} coins** from your bank.\n"
            f"**Wallet:** {new_wallet} coins\n"
            f"**Bank:** {new_bank} coins"
        )

    @app_commands.command(name="bank_interest", description="Check your interest details")
    async def bank_interest(self, interaction: discord.Interaction):
        # Show detailed interest information and projections
        user_id = interaction.user.id
        interest_earned = await database.calculate_interest(user_id)
        bank_bal = await database.get_bank_balance(user_id)
        interest_rate = await database.get_interest_rate(user_id)
        last_calc = await database.get_last_interest_calculation(user_id)
        now = int(time.time())
        if last_calc > 0:
            days_since = (now - last_calc) // 86400
            next_calc = last_calc + 86400
            hours_until = (next_calc - now) // 3600
        else:
            days_since = 0
            hours_until = 24
        message = f"📊 **Interest Details for {interaction.user.mention}**\n"
        message += f"**Bank Balance:** {bank_bal} coins\n"
        message += f"**Daily Interest Rate:** {interest_rate*100:.1f}%\n"
        if days_since > 0:
            message += f"**Days since last interest:** {days_since}\n"
        if interest_earned > 0:
            message += f"✅ **Interest Earned:** +{interest_earned} coins\n"
        else:
            message += f"**Next Interest Calculation:** in ~{hours_until} hours\n"
        if bank_bal > 0:
            daily_interest = int(bank_bal * interest_rate)
            weekly_interest = int(bank_bal * ((1 + interest_rate) ** 7) - bank_bal)
            message += f"\n**Projected Earnings:**\n"
            message += f"Daily: ~{daily_interest} coins\n"
            message += f"Weekly: ~{weekly_interest} coins"
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Banking(bot))