from discordwebhook import Discord


def discord_push(
        url,
        embeds,
):
    """Post a message to Discord"""

    discord = Discord(url=url)
    discord.post(
        embeds=embeds,
    )

    return True
