import logging
import os

import dotenv
import discord
from discord.ext import commands

import boetchen.logging
import boetchen.bot_manager as bm

boetchen.logging.load_config()

#import boetchen.date_poller

logger = logging.getLogger(__name__)

logger.debug("loading .env...")
dotenv.load_dotenv()
logger.info("loaded .env")


logger.debug("loading bot...")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
bm.set_bot(bot)


logger.info("loaded bot")

# load other modules that are needed


@bot.event
async def on_ready():
    logger.info("bot ready")
    logger.debug("synced")


@bot.command()
async def sync_boetchen(ctx):
    logger.debug("syncing cmds...")
    await bot.tree.sync()
    logger.debug("synced cmds")


logger.debug("registering commands")
#boetchen.date_poller.register_commands()

logger.info("registered additional commands")


def main():
    logger.info("starting bot")
    token = os.environ["DISCORD_BOT_TOKEN"]
    bot.run(token)


if __name__ == '__main__':
    main()
