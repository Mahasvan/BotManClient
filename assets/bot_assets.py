import discord


def get_color(interaction: discord.Interaction):
    if interaction.guild:
        return interaction.guild.me.color
    else:
        return discord.Color.random()
