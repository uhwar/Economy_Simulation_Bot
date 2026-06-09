import discord
import time
import random
from discord import app_commands
from discord.ext import commands
import database

WORK_COOLDOWN = 3600

# Contains all functions
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def resolve_gamba(self, user_id, amount) -> tuple [bool, int, int]:
        won = random.randint(0,1) == 1
        if won:
            payout = amount * 2
            await database.add_balance(user_id, payout)
        else:
            payout = amount
            await database.remove_balance(user_id, amount)
        new_bal = await database.get_balance(user_id)
        await database.log_transaction(user_id, f"Gambled/{'Won' if won else 'Lost'}", payout, new_bal)
        return won, payout, new_bal


    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        bal = await database.get_balance(interaction.user.id)
        await interaction.response.send_message(
            f"💰 {interaction.user.mention}, you have **{bal} coins**"
        )
    @app_commands.command(name="work", description="go to work")
    async def work(self, interaction: discord.Interaction):
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
                f" You tired. Try again in **{minutes} minutes**"
            )
            return

        earned = random.randint(50, 200)
        await database.add_balance(user_id,earned)
        await database.set_last_work(user_id, now)
        await interaction.response.send_message(
            f" You worked and earned **{earned} coins**"
        )
        new_bal = await database.get_balance(user_id)
        await database.log_transaction(user_id, "Worked", earned, new_bal)
    @app_commands.command(name="gamba", description="Bet your coins")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        user_id = interaction.user.id
        bal = await database.get_balance(user_id)

        if bal < amount:
            await interaction.response.send_message("You don't have enough coins")
            return

        won, payout, new_bal = await self.resolve_gamba(user_id, amount)
        if won:
            await interaction.response.send_message(f"You WON **{amount} coins**")
        else:
            await interaction.response.send_message(f"You lost **{amount} coins**")
    @app_commands.command(name="heist", description="risk jail time for a big payout")
    async def heist(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        bank_value = 500
        get_away_time = random.randint(0, 10)
        jail_time = await database.get_jail_until(user_id)
        if jail_time < int(time.time()):
            if get_away_time > 5:
                # Await update jail_time
                now = int(time.time())
                jail_until = 0
                await database.set_jail_until(user_id, jail_until)
                await interaction.response.send_message(
                    "You got caught! You will serve an hour in jail.")
                new_bal = await database.get_balance(user_id)
                await database.log_transaction(user_id, "Thrown in jail", 0, new_bal)
            else:
                await database.rob_bank(user_id, bank_value)
                await interaction.response.send_message(
                    f"You got away! You collected **{bank_value}**"
                )
                new_bal = await database.get_balance(user_id)
                await database.log_transaction(user_id, "Robbed a bank", 500, new_bal)

        else:
            await interaction.response.send_message(
                "You're in jail! Can't do the time? Don't do the crime!")
    @app_commands.command(name="money_wire", description="Wire coins to another player")
    async def money_wire(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        await database.add_balance(target.id, amount)
        await interaction.response.send_message(f" {target.id} was sent {amount} coins!")
        new_bal = await database.get_balance(target.id)
        await database.log_transaction(target.id, f"User sent {amount} to player", amount, new_bal)

    @app_commands.command(name="jailbreak", description="risk jail time to rescue a homie (higher chance to fail if your also in jail")
    async def jailbreak(self, interaction: discord.Interaction, target: discord.Member):
        user_id = interaction.user.id
        homie = target.id
        get_away_time = random.randint(0, 10)
        j_time = await database.get_jail_until(user_id)
        homie_j_time = await database.get_jail_until(target.id)
        now = int(time.time())
        if homie != user_id:
            if homie_j_time > now:  # ( Target is locked up ) ( PATCH IN JAILBREAKING SELF )
                if j_time < now:  # ( User not in jail )
                    if get_away_time < 6:  # ( Successful Attempt )
                        jail_until = 0
                        await database.set_jail_until(homie, jail_until)
                        await interaction.response.send_message(f" {target.mention} is free!")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, f"Jailbroke {homie}", 0, new_bal)
                    else:  # ( Failed Attempt )
                        jail_until = now + 7200
                        await database.set_jail_until(user_id, jail_until)
                        await interaction.response.send_message("You were caught and given 2 hours jail time.")
                else:  # ( User is in jail )
                    if get_away_time < 3:  # ( Successful Attempt )
                        jail_until = 0
                        await database.set_jail_until(homie, jail_until)
                        await interaction.response.send_message(f" {target.mention} is free!")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, f"Jailbroke {homie}", 0, new_bal)
                    else:  # ( Failed Attempt )
                        jail_until = now + 7200
                        await database.set_jail_until(user_id, jail_until)
                        await interaction.response.send_message("You're caught and given 2 hours jail time.")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, "Caught Jailbreaking", 0, new_bal)
            else:  # ( Target not in jail )
                await interaction.response.send_message(f"{target.mention} is already free!")
        else:
            await interaction.response.send_message(f" You can't jailbreak yourself!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
