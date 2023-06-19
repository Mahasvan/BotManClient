import discord
from discord.ext import commands

import json
import os
from pathlib import Path

from assets import internet, shell

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

with open("config.json") as f:
    config = json.load(f)

host = config["server-ip"]
port = config["server-port"]
bot.internet = internet.Internet(host=host, port=port)


@bot.slash_command(name="ping", description="Pong!", guild_ids=[861259655011237939])
async def ping(interaction):
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)}ms")


@bot.slash_command(name="reload", description="Reload a cog", guild_ids=[861259655011237939])
@commands.is_owner()
async def reload(interaction, cog: str = None):
    if not cog:
        cog = [x for x in os.listdir("cogs") if x.endswith(".py") and not x.startswith("_")]
    else:
        cog = []

    successes = []
    failures = []
    for c in cog:
        try:
            bot.reload_extension(f"cogs.{c[:-3]}")
            successes.append(c[:-3])
        except:
            failures.append(c[:-3])
    embed = discord.Embed(
        title="Reload Results",
        color=interaction.guild.me.color,
    )
    if successes:
        embed.add_field(name="Successes", value="\n".join(successes), inline=False)
    if failures:
        embed.add_field(name="Failures", value="\n".join(failures), inline=False)
    await interaction.response.send_message(embed=embed)
    await bot.sync_commands()


@bot.slash_command(name="load", description="Load a cog", guild_ids=[861259655011237939])
@commands.is_owner()
async def load(interaction, cog: str):
    try:
        bot.load_extension(f"cogs.{cog}")
        await interaction.response.send_message(f"Loaded cog `{cog}`")
        await bot.sync_commands()
    except Exception as e:
        bot.failed_cogs.append(cog)
        await interaction.response.send_message(f"Failed to load cog `{cog}`: {str(e)[:100] + '...'}")


@bot.slash_command(name="unload", description="Unload a cog", guild_ids=[861259655011237939])
@commands.is_owner()
async def unload(interaction, cog: str):
    try:
        bot.unload_extension(f"cogs.{cog}")
        await interaction.response.send_message(f"Unloaded cog `{cog}`")
    except Exception as e:
        await interaction.response.send_message(f"Failed to unload cog `{cog}`: {str(e)[:100] + '...'}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
    await bot.sync_commands()
    print("Slash Commands Synced!")


if __name__ == '__main__':
    cwd = str(Path(__file__).parents[0])
    cogs_to_load = [file[:-3] for file in os.listdir(os.path.join(cwd, "cogs"))
                    if file.endswith(".py") and not file.startswith("_")]
    bot.failed_cogs = []

    for cog in cogs_to_load:
        print(f"Loading {cog}...")
        try:
            bot.load_extension(f"cogs.{cog}")  # load the cog
            print(shell.colour_green("        |--- Success!"))  # if the cog loaded successfully, print this
        except Exception as e:
            print(shell.colour_red(f"        |--- Failed: {str(e)}"))
            bot.failed_cogs.append(cog)  # add cog to failed list

    if len(bot.failed_cogs) != 0:  # print out the cogs which failed to load
        print('====================')
        print('These cogs failed to load:')
        for x in bot.failed_cogs:
            print(shell.colour_yellow(x))
    print(shell.colour_pink("===================="))

    bot.run(config["token"])
