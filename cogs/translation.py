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

    translation = discord.SlashCommandGroup("translation", description="Commands for translating text")

    async def populate_langs(self):
        self.lang_dict = await self.bot.internet.get_json("/translate/languages")
        self.lang_dict = self.lang_dict.get("response")

    @translation.command(name="translate", description="Translate text to another language",
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

    @translation.command(name="detect", description="Detect the language of a text",
                         guild_ids=[861259655011237939])
    async def detect(self, interaction: discord.Interaction, message: str):
        response = await self.bot.internet.post_json("/translate/detect",
                                                     data=json.dumps({"text": message}))
        response = response.get("response")
        embed = discord.Embed(
            title=f"Detected: {response.get('language').title()}",
            description=None,
            color=interaction.user.color,
        )
        embed.add_field(name="Source Text", value=message, inline=False)
        confidence = round(response.get("confidence"), 2)
        embed.set_footer(text=f"Confidence: {confidence}%")
        await interaction.response.send_message(embed=embed)

    # TODO: list all languages


def setup(bot):
    bot.add_cog(Translate(bot))
