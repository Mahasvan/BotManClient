import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Only the owner can use this command.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have the required permissions to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("You are missing a required argument.")
        else:
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
