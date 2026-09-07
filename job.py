import discord
import random
import time
from discord import app_commands
from discord.ext import commands
import database

class Job(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="get_job", description="choose from a list of jobs")
    async def get_job(self, interaction: discord.Interaction, job: str):
        current_job = await database.get_job(user_id)
        if current_job == "None":
            if job == "Mage" or "Warrior" or "Mage":
                await database.set_job(user_id, job)
                await interaction.response.send_message(
                    f"Your new job is {job}"
                )
        else:
            await interaction.response.send_message(
                f"You current have a job: {current_job}"
            )

    @app_commands.command(name="job_list", description="see all job options")
    async def job_list(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Current jobs: Mage, Warrior, Hunter"
        )

    @app_command.command(name="set_title", description="a term the bot will use to refer to the player")
    async def set_title(self, interaction: discord.Interaction, title:str):
        await database.set_title(user.id, title)
        await interaction.response.send_message(
            f"I shall refer to you as {title}"
        )

