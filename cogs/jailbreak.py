import discord
import time
import random
from discord import app_commands
from discord.ext import commands
import database

JAIL_MESSAGES = [
    "🚔 You got caught red-handed! Off to jail you go!",
    "🔒 The authorities caught up with you. Time to face the music.",
    "⚔️ You were apprehended! Looks like crime doesn't pay.",
    "🛡️ The guards have you surrounded. You're going to jail!",
    "💀 You didn't see that coming. Straight to the dungeon!",
    "🎲 Your luck ran out. Locked up for 1 hour!",
    "⛓️ Busted! The warden has a cell waiting for you.",
    "👮 You're under arrest! Welcome to jail!",
    "🔐 The plan went sideways. You're doing time now.",
    "😤 Caught in the act! Jail time it is.",
]


class Jailbreak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="jailbreak", description="risk jail time to rescue a homie (higher chance to fail if you're also in jail)")
    async def jailbreak(self, interaction: discord.Interaction, target: discord.Member):
        # Jailbreak command - try to free another player from jail
        user_id = interaction.user.id
        homie = target.id
        get_away_time = random.randint(0, 10)
        j_time = await database.get_jail_until(user_id)
        homie_j_time = await database.get_jail_until(target.id)
        now = int(time.time())
        
        if homie != user_id:
            if homie_j_time > now:  # Target is locked up
                if j_time < now:  # User not in jail
                    if get_away_time < 6:  # Successful attempt
                        jail_until = 0
                        await database.set_jail_until(homie, jail_until)
                        await interaction.response.send_message(f"🎉 {target.mention} is free!")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, f"Jailbroke {homie}", 0, new_bal)
                    else:  # Failed attempt
                        jail_until = now + 7200
                        await database.set_jail_until(user_id, jail_until)
                        jail_msg = random.choice(JAIL_MESSAGES)
                        await interaction.response.send_message(f"{jail_msg} **2 hours jail time**")
                else:  # User is in jail
                    if get_away_time < 3:  # Successful attempt (lower odds)
                        jail_until = 0
                        await database.set_jail_until(homie, jail_until)
                        await interaction.response.send_message(f"🎉 {target.mention} is free!")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, f"Jailbroke {homie}", 0, new_bal)
                    else:  # Failed attempt
                        jail_until = now + 7200
                        await database.set_jail_until(user_id, jail_until)
                        jail_msg = random.choice(JAIL_MESSAGES)
                        await interaction.response.send_message(f"{jail_msg} **2 hours jail time**")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, "Caught Jailbreaking", 0, new_bal)
            else:  # Target not in jail
                await interaction.response.send_message(f"{target.mention} is already free!")
        else:
            await interaction.response.send_message("You can't jailbreak yourself!")


async def setup(bot):
    await bot.add_cog(Jailbreak(bot))
