import discord
import time
import random
from discord import app_commands
from discord.ext import commands
import database

HEIST_SUCCESS_MESSAGES = [
    "🎯 You snuck past the guards and grabbed the loot!",
    "💼 In and out like a pro! The heist was flawless!",
    "🕵️ You cracked the vault! Nobody even noticed!",
    "🚀 Mission impossible? More like mission accomplished!",
    "🏃 You made a clean getaway with the goods!",
    "🔓 You picked the lock and claimed your prize!",
    "🎪 The perfect crime! You're in and out!",
    "⚡ Lightning quick reflexes! You got away clean!",
    "🌙 Under cover of darkness, you made your escape!",
    "🎭 Oscar-worthy performance! Nobody suspected a thing!",
]

HEIST_FAIL_MESSAGES = [
    "🚔 The cops spotted you! You're going to jail!",
    "🔒 Security caught you red-handed! Straight to lockup!",
    "⚠️ The alarm went off! The guards are everywhere!",
    "🛡️ You couldn't escape the guards. Jail time!",
    "💥 Your cover was blown! You're under arrest!",
    "📹 The cameras caught everything! You're busted!",
    "🚨 Sirens wailing! You didn't make it out in time!",
    "😱 Trapped! The exit was sealed! Off to jail!",
    "🎪 The heist went south real quick. You got caught!",
    "⛓️ No escape! The authorities have you surrounded!",
]


class Heist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def resolve_heist(self, user_id, amount) -> tuple[bool, int]:
        """Helper function for heist logic"""
        got_away = random.randint(0, 10) <= 5
        if got_away:
            await database.rob_bank(user_id, amount)
            new_bal = await database.get_balance(user_id)
            await database.log_transaction(user_id, "Robbed a bank", amount, new_bal)
        else:
            jail_until = int(time.time()) + 3600
            await database.set_jail_until(user_id, jail_until)
            new_bal = await database.get_balance(user_id)
            await database.log_transaction(user_id, "Thrown in jail", 0, new_bal)
        return got_away, new_bal

    @app_commands.command(name="heist", description="risk jail time for a big payout")
    async def heist(self, interaction: discord.Interaction):
        # Bank heist command - 50% chance to get 500 coins or get jailed for 1 hour
        user_id = interaction.user.id
        bank_value = 500
        jail_time = await database.get_jail_until(user_id)

        if jail_time > int(time.time()):
            await interaction.response.send_message("You're in jail! Can't do the time? Don't do the crime!")
            return

        got_away, new_bal = await self.resolve_heist(user_id, bank_value)
        if got_away:
            msg = random.choice(HEIST_SUCCESS_MESSAGES)
            await interaction.response.send_message(f"{msg}\n💰 You collected **{bank_value} coins**!")
        else:
            msg = random.choice(HEIST_FAIL_MESSAGES)
            await interaction.response.send_message(msg)


async def setup(bot):
    await bot.add_cog(Heist(bot))
