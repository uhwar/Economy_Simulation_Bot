import discord
import time
import random
from discord import app_commands
from discord.ext import commands
import database

WORK_COOLDOWN = 3600  # 1 hour in seconds


class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="work", description="go to work")
    async def work(self, interaction: discord.Interaction):
        # Work command - earn coins with 1-hour cooldown
        user_id = interaction.user.id
        now = int(time.time())
        last = await database.get_last_work(user_id)
        in_jail = await database.get_jail_until(user_id)
        
        if in_jail > now:
            await interaction.response.send_message("You're in jail!")
            return
        elif now - last < WORK_COOLDOWN:
            remaining = WORK_COOLDOWN - (now - last)
            minutes = remaining // 60
            await interaction.response.send_message(
                f"😴 You tired. Try again in **{minutes} minutes**"
            )
            return

        earned = random.randint(50, 200)
        await database.add_balance(user_id, earned)
        await database.set_last_work(user_id, now)
        await interaction.response.send_message(
            f"💼 You worked and earned **{earned} coins**"
        )
        new_bal = await database.get_balance(user_id)
        await database.log_transaction(user_id, "Worked", earned, new_bal)


async def setup(bot):
    await bot.add_cog(Work(bot))
