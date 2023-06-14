import asyncio

import discord
from discord.ext import commands

import json


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang_dict = {}
        loop = asyncio.get_event_loop()
        loop.create_task(self.populate_langs())

    async def populate_langs(self):
        self.lang_dict = await self.bot.internet.get_json("/translate/languages")
        self.lang_dict = self.lang_dict.get("response")

    @commands.slash_command(name="translate", description="Translate text to another language",
                            guild_ids=[861259655011237939])
    async def translate(self, interaction: discord.Interaction,
                        message: str, from_language: str = "auto", to_language: str = "en"):
        response = await self.bot.internet.post_json("/translate/translate",
                                                     data=json.dumps(
                                                         {"text": message, "src": from_language, "dest": to_language}))
        response = response.get("response")
        embed = discord.Embed(
            title=f"{interaction.user.display_name}, your translation is",
            description=response.get("text"),
            color=interaction.user.color,
        )
        embed.add_field(name="Source Text", value=message, inline=False)
        embed.set_footer(text=f"{self.lang_dict.get(response.get('src')).title()}"
                              f" -> {self.lang_dict.get(response.get('dest')).title()}")

        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Translate(bot))
