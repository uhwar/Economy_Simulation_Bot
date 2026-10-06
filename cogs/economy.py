import discord
import time
import random
from discord import app_commands
from discord.ext import commands
import database

WORK_COOLDOWN = 3600 # 1 hour in seconds

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

# Contains all functions
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # ~~~ Helper functions ~~~
    async def resolve_heist(self, user_id, amount) -> tuple [bool, int]:
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
        # Get user's coin balance from database
        bal = await database.get_balance(interaction.user.id)
        await interaction.response.send_message(
            f"💰 {interaction.user.mention}, you have **{bal} coins**"
        )
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

    @app_commands.command(name="money_wire", description="Wire coins to another player")
    async def money_wire(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        # Send coins to another player (admin/development command)
        await database.add_balance(target.id, amount)
        await interaction.response.send_message(f"💰 {target.mention} was sent **{amount} coins**!")
        new_bal = await database.get_balance(target.id)
        await database.log_transaction(target.id, f"User sent {amount} to player", amount, new_bal)

    @app_commands.command(name="jailbreak", description="risk jail time to rescue a homie (higher chance to fail if your also in jail")
    async def jailbreak(self, interaction: discord.Interaction, target: discord.Member):
        # Jailbreak command - try to free another player from jail
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
                        jail_msg = random.choice(JAIL_MESSAGES)
                        await interaction.response.send_message(f"{jail_msg} **2 hours jail time**")
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
                        jail_msg = random.choice(JAIL_MESSAGES)
                        await interaction.response.send_message(f"{jail_msg} **2 hours jail time**")
                        new_bal = await database.get_balance(user_id)
                        await database.log_transaction(user_id, "Caught Jailbreaking", 0, new_bal)
            else:  # ( Target not in jail )
                await interaction.response.send_message(f"{target.mention} is already free!")
        else:
            await interaction.response.send_message(f" You can't jailbreak yourself!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
