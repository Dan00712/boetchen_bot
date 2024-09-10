import datetime as dt
import dateutil
from dateutil.parser import parse as datetime_parse

import boetchen.bot_manager as bm

import discord
from discord.ext import commands
import logging

from collections import abc

logger = logging.getLogger(__name__)


class DateConverter(commands.Converter):
    async def convert(self, ctx, arg) -> dt.date:
        try:
            return datetime_parse(arg).date()
        except dateutil.parser._parser.ParserError:
            logger.critical("Error in parsing DateTime with arg: %s", arg)
            await ctx.response.send(f'Error in parameter {arg}', ephemeral=True)


async def date_poll(
        ctx: discord.Interaction,
        start_date: DateConverter,
        end_date: DateConverter,
        closes_in_hours: int,
        message: str = "", *,
        no_time=True,
        not_interested=False):
    channel = ctx.channel
    dates = list(date_range(start_date, end_date))
    partitioned_dates = list(partition_list(dates, 10))

    tmp = []
    if no_time:
        tmp.append('no time')
    if not_interested:
        tmp.append('not interested')

    partitioned_dates.append(tmp)

    await channel.send(message)
    for date_l in partitioned_dates:
        # TODO: send polls
        pass


def date_range(
        sd: dt.date,
        ed: dt.date,
        dt: dt.timedelta = dt.timedelta(days=1)):
    if sd > ed:
        return

    cur = sd-dt
    while (cur := cur + dt) < ed:
        yield cur


def partition_list(l: list, subsize):
    for i in range(0, len(l), subsize):
        yield l[i:i+subsize]


def register_commands():
    bot = bm.get_bot()
    logger.debug("registering poll dates with bot %s", bot)

    bot.command(name="date_poll")(date_poll)

