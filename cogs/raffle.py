import asyncio
import discord
import random
from typing import Dict, List
from discord import app_commands
from discord.ext import commands
import database


class RaffleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Structure: {guild_id: {"ticket_price": int, "entries": [user_id, ...], "active": bool}}
        self.raffles: Dict[int, dict] = {}

    @app_commands.command(
        name="raffle_start", description="Start a timed raffle"
    )
    async def start_raffle(
        self, interaction: discord.Interaction, ticket_price: int, minutes: int
    ):
        guild_id = interaction.guild_id

        if guild_id in self.raffles and self.raffles[guild_id].get("active"):
            await interaction.response.send_message(
                "A raffle is already active in this server!", ephemeral=True
            )
            return

        self.raffles[guild_id] = {
            "ticket_price": ticket_price,
            "entries": [],
            "active": True,
        }

        await interaction.response.send_message(
            f"🎉 **Raffle Started!** 🎉\n"
            f"Ticket Price: **{ticket_price} coins**\n"
            f"Duration: **{minutes} minute(s)**\n"
            f"Use `/raffle_enter` to buy a ticket!"
        )

        # Handle the timer
        await asyncio.sleep(minutes * 60)
        await self._end_raffle(interaction.channel, guild_id)

    @app_commands.command(name="raffle_enter", description="Buy a raffle ticket")
    async def enter_raffle(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        raffle = self.raffles.get(guild_id)

        if not raffle or not raffle.get("active"):
            await interaction.response.send_message(
                "There is no active raffle right now.", ephemeral=True
            )
            return

        user_id = interaction.user.id
        price = raffle["ticket_price"]
        bal = await database.get_balance(user_id)

        if bal < price:
            await interaction.response.send_message(
                f"You need **{price} coins** to enter, but you only have **{bal}**.",
                ephemeral=True,
            )
            return

        # Deduct entry fee using your existing database logic
        await database.remove_balance(user_id, price)
        raffle["entries"].append(user_id)

        await interaction.response.send_message(
            f"🎫 You bought 1 ticket for **{price} coins**! Total entries: **{len(raffle['entries'])}**"
        )

    async def _end_raffle(
        self, channel: discord.TextChannel, guild_id: int
    ) -> None:
        raffle = self.raffles.get(guild_id)
        if not raffle or not raffle.get("active"):
            return

        raffle["active"] = False
        entries: List[int] = raffle["entries"]

        if not entries:
            await channel.send("🏆 The raffle ended, but nobody entered!")
            return

        winner_id = random.choice(entries)
        total_pot = len(entries) * raffle["ticket_price"]

        # Award the pot to the winner
        await database.add_balance(winner_id, total_pot)

        await channel.send(
            f"🎉 **RAFFLE RESULTS** 🎉\n"
            f"Winner: <@{winner_id}>\n"
            f"Prize Pot: **{total_pot} coins** ({len(entries)} entries)"
        )


async def setup(bot):
    await bot.add_cog(RaffleCog(bot))
