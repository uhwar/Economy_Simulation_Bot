import discord
import random
from discord import app_commands
from discord.ext import commands
import database

GAMBLE_WIN_MESSAGES = [
    "🎉 Lady Luck smiles upon you! You won big!",
    "💰 YES! The odds were in your favor!",
    "🔥 That's what I'm talking about! You're on fire!",
    "🎊 The dice gods have blessed you!",
    "⭐ Outstanding! Your fortune has multiplied!",
    "🏆 Victory is yours! The house loses this round!",
    "🌟 Incredible luck! You doubled your coins!",
    "💎 You struck gold! Lady Luck is on your side!",
    "🎯 Bull's eye! Perfect timing!",
    "👑 You're rolling hot! Another win!",
]

GAMBLE_LOSE_MESSAGES = [
    "💔 The house always wins. Better luck next time.",
    "😢 Your coins are gone. That didn't go as planned.",
    "🎰 The slots have spoken. You lost it all.",
    "😭 Lady Luck has abandoned you. Your coins vanished.",
    "💸 Ouch! Your wallet is lighter now.",
    "🔴 The wheel stops... and you lose.",
    "😞 Not your day. The dice weren't kind.",
    "🎪 The house takes their cut. You're broke.",
    "📉 Your fortune took a nosedive.",
    "🌧️ The luck ran dry. Better luck next time.",
]


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def resolve_gamba(self, user_id, amount) -> tuple[bool, int, int]:
        """Helper function for gambling logic"""
        won = random.randint(0, 1) == 1
        if won:
            payout = amount * 2
            await database.add_balance(user_id, payout)
        else:
            payout = amount
            await database.remove_balance(user_id, amount)
        new_bal = await database.get_balance(user_id)
        await database.log_transaction(user_id, f"Gambled/{'Won' if won else 'Lost'}", payout, new_bal)
        return won, payout, new_bal

    @app_commands.command(name="gamba", description="Bet your coins")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        # Gambling command - 50/50 chance to double or lose bet
        user_id = interaction.user.id
        bal = await database.get_balance(user_id)

        if bal < amount:
            await interaction.response.send_message("You don't have enough coins")
            return

        won, payout, new_bal = await self.resolve_gamba(user_id, amount)
        if won:
            msg = random.choice(GAMBLE_WIN_MESSAGES)
            await interaction.response.send_message(f"{msg} You won **{payout} coins**!")
        else:
            msg = random.choice(GAMBLE_LOSE_MESSAGES)
            await interaction.response.send_message(f"{msg} You lost **{amount} coins**.")


async def setup(bot):
    await bot.add_cog(Gambling(bot))
