import time

import discord
from discord.ext import commands

import platform
import random

from assets import constants


class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    host = discord.SlashCommandGroup("host", description="Commands related to the host machine.")

    @host.command(name="info", description="Info about the machine in which I am hosted.",
                  guild_ids=[861259655011237939, 830456831183945778])
    async def host_info(self, interaction: discord.Interaction):
        data = await self.bot.internet.get_json("/host/info")
        embed = discord.Embed(
            title=data.get("hostname", "Host Info"),
            color=interaction.guild.me.color,
            description=f"My front-end runs on {platform.system()}.\n"
                        f"## Back-end"
        )
        embed.add_field(name="OS", value=data["os"], inline=False)
        embed.add_field(name="CPU", value=data["cpu"], inline=False)
        embed.add_field(name="CPU Threads", value=data["cpu_threads"], inline=False)
        embed.add_field(name="CPU Usage", value=f"{data['cpu_usage']}%", inline=False)
        embed.add_field(name="Memory Usage", value=f"{data['memory_usage']}%", inline=False)
        await interaction.response.send_message(embed=embed)

    @host.command(name="uptime")
    async def uptime(self, interaction):
        """How long have I been awake?"""
        now = time.monotonic()
        response = await self.bot.internet.get_json("/host/uptime")

        embed = discord.Embed(title="I have been awake for:", description=f"_{response['response']['text']}_",
                              color=interaction.guild.me.color)
        embed.set_footer(text=random.choice(constants.uptime_footers))
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Host(bot))
