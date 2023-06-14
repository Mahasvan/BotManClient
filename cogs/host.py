import discord
from discord.ext import commands


class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="info", description="Info about the machine in which I am hosted.", guild_ids=[861259655011237939, 830456831183945778])
    async def hostinfo(self, interaction: discord.Interaction):
        data = await self.bot.internet.get_json("/host/info")
        embed = discord.Embed(
            title=data.get("hostname", "Host Info"),
            color=interaction.guild.me.color,
        )
        embed.add_field(name="Operating System", value=data["os"], inline=False)
        embed.add_field(name="CPU Threads", value=data["cpu_threads"], inline=False)
        embed.add_field(name="CPU Usage", value=f"{data['cpu_usage']}%", inline=False)
        embed.add_field(name="Memory Usage", value=f"{data['memory_usage']}%", inline=False)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Host(bot))

