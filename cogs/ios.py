import datetime
import os
import re
import subprocess

import discord
from discord.ext import commands, tasks

sent_to_owner = False


class IOS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ios = discord.SlashCommandGroup("ios", description="Designed for use with the iPad, internal")

    @ios.command(name="battery", description="Get the battery percentage of the iPad")
    async def battery(self, interaction: discord.Interaction):
        output = subprocess.check_output("ioreg -l -w0 | grep Capacity", shell=True)
        current = re.compile(r"\"CurrentCapacity\" = (\d+)")
        stateofcharge = re.compile(r"\"StateOfCharge\"=(\d+)")
        CurrentCapacity = current.search(str(output))
        StateOfCharge = stateofcharge.search(str(output))
        if CurrentCapacity or StateOfCharge:
            await interaction.response.send_message(f"CurrentCapacity: {CurrentCapacity.group(1)}mAh\n"
                                                    f"StateOfCharge: {StateOfCharge.group(1)}%")

    @tasks.loop(seconds=30)
    async def keep_alive(self):

        global sent_to_owner

        output = subprocess.check_output("ioreg -l -w0 | grep Capacity", shell=True)
        current = re.compile(r"\"CurrentCapacity\" = (\d+)")
        stateofcharge = re.compile(r"\"StateOfCharge\"=(\d+)")

        CurrentCapacity = current.search(str(output)).group(1)
        StateOfCharge = stateofcharge.search(str(output)).group(1)
        actual_charge = sorted([CurrentCapacity, StateOfCharge])[0]
        embed = discord.Embed(title="iPad is on!", color=discord.Color.yellow())
        channel = self.bot.get_channel(1123241205581492244)
        embed.add_field(name="Battery Charge", value=f"{actual_charge}%", inline=True)
        if int(actual_charge) < 25 and sent_to_owner is False:
            owner = self.bot.owner
            embed.color = discord.Color.red()
            await owner.send(f"iPad is at {actual_charge}% battery!")
            sent_to_owner = True
        if int(actual_charge) > 75:
            sent_to_owner = False
            embed.color = discord.Color.green()
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        self.keep_alive.start()


def setup(bot):
    if os.name == "posix":
        bot.add_cog(IOS(bot))
    else:
        raise OSError("Not running on iOS!")
