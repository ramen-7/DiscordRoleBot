import discord


def make_embed(text, color=discord.Colour.blue(), url=None):
    embed = discord.Embed(color=color, description=text)
    if url != None:
        embed.set_image(url=f"{url}")
    return embed
