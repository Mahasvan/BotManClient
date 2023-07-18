import json

import discord

from discord.ext import commands

from assets import time_assets


def embed_builder(
        query: str,
        found: bool,
        items: dict,
        color: discord.Color = discord.Color.blurple()
):
    embed = discord.Embed(
        title=f"Top Result For: \"{query}\"",
        color=color,
    )

    if not found:
        embed.description = "No results found."
        return embed

    type = items.get("type")
    name = items.get("name")
    url = items.get("external_urls").get("spotify")

    embed.description = f"## [{name}]({url})"

    if type == "track":
        image = items.get("album").get("images")[0].get("url")
    else:
        image = items.get("images")[0].get("url")

    embed.set_image(url=image)

    embed.set_footer(text=f"Spotify ID: {items.get('id')}")

    if type != "artist":
        artist_urls = {x.get('name'): x.get("external_urls").get("spotify") for x in items.get("artists")}
        embed.add_field(name="Artists" if len(artist_urls) != 1 else "Artist",
                        value=", ".join([f"[{x}]({artist_urls.get(x)})" for x in artist_urls.keys()]),
                        inline=True)

    release_date = items.get("release_date") if items.get("release_date_precision") == "day" else None
    if release_date:
        embed.add_field(name="Release Date", value=time_assets.format_date_yyyymmdd(release_date), inline=True)

    if type == "album":
        tracks = items.get("total_tracks")
        album_type: str = items.get("album_type")
        if album_type != "album":
            embed.description += f"\n\n**Album Type:** {album_type.title()}\n"
        embed.add_field(name="Tracks", value=tracks, inline=True)

    if type == "artist":
        genres = items.get("genres")
        embed.add_field(name="Genres", value=", ".join(genres), inline=True)
        followers: int = items.get("followers").get("total")
        embed.add_field(name="Followers", value=f"{followers:,}", inline=True)

    if type == "track":
        duration = int(items.get("duration_ms") / 1000)
        embed.add_field(name="Duration", value=time_assets.pretty_time_from_seconds(duration), inline=True)
        preview_url = items.get("preview_url")
        if preview_url:
            embed.description += f"\n\n[Preview]({preview_url})"

    return embed


class Spotify(commands.Cog):
    spotify = discord.SlashCommandGroup("spotify", description="Commands that make use of the Spotify API")

    def __init__(self, bot):
        self.bot = bot

    @spotify.command(name="track")
    async def search_track(self, interaction: discord.Interaction, query: str):
        """Search for a track on Spotify"""
        response = await self.bot.internet.get_json("/spotify/search/track", params={"query": query})

        with open("track.json", "w") as f:
            json.dump(response, f, indent=4)

        items = response.get("response").get("tracks", {}).get("items", [])

        if len(items) == 0:
            embed = embed_builder(query, False, color=interaction.user.color)
            return await interaction.response.send_message(embed=embed)

        items = items[0]

        embed = embed_builder(query=query,
                              found=True,
                              items=items,
                              color=interaction.user.color)

        await interaction.response.send_message(embed=embed)

    @spotify.command(name="album")
    async def search_album(self, interaction: discord.Interaction, query: str):
        """Search for an album on Spotify"""
        response = await self.bot.internet.get_json("/spotify/search/album", params={"query": query})

        items = response.get("response").get("albums", {}).get("items", [])
        if len(items) == 0:
            embed = embed_builder(query, False, color=interaction.user.color)
            return await interaction.response.send_message(embed=embed)

        items = items[0]

        embed = embed_builder(query=query,
                              found=True,
                              items=items,
                              color=interaction.user.color)

        await interaction.response.send_message(embed=embed)

    @spotify.command(name="artist")
    async def search_artist(self, interaction: discord.Interaction, query: str):
        """Search for an artist on Spotify"""
        response = await self.bot.internet.get_json("/spotify/search/artist", params={"query": query})

        with open("artist.json", "w") as f:
            json.dump(response, f, indent=4)

        items = response.get("response").get("artists", {}).get("items", [])
        if len(items) == 0:
            embed = discord.Embed(
                title=f"Top Result For: {query}",
                description="No results found",
                color=interaction.user.color,
            )
            return await interaction.response.send_message(embed=embed)

        items = items[0]
        embed = embed_builder(query=query,
                              found=True,
                              items=items,
                              color=interaction.user.color)

        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Spotify(bot))
