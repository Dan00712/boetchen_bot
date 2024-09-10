from discord.ext.commands import Bot

__bot: Bot | None = None


def set_bot(bot: Bot):
    global __bot
    if __bot:
        raise ValueError("bot is already set and may not be set again")
    __bot = bot


def get_bot() -> Bot:
    return __bot
