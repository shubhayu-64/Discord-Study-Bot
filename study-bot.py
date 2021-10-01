from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from pytz import timezone

import config
from database import datetime
from database import (
    resetDaily, resetWeekly, resetMonthly, member_details, daily_leaderboard,
    weekly_leaderboard, monthly_leaderboard, member_leaderboard, end, join
)

if TYPE_CHECKING:
    from discord import TextChannel, Member, Guild, Role


# The prefix set for the bot
client = commands.Bot(command_prefix='+')
client.remove_command('help')

# Replace with your bot icon image.
BOT_IMAGE_URL: str = (
    "https://i.pinimg.com/564x/c9/4e/e1/c94ee183a2e635e5b8972bc0240ad23a.jpg"
)


@client.event
async def on_ready():
    """
    Prints a message once bot becomes ready.
    """
    await client.change_presence(activity=discord.Game("+help"))
    print(f'{client.user} is running')
    reset.start()


@tasks.loop(minutes=60)
async def reset():
    """
    Resets leaderboards everyday.
    """
    now: datetime = datetime.now(timezone('Asia/Kolkata'))
    if now.hour != 0:
        return

    resetDaily()

    if now.weekday() == 0:
        resetWeekly()

    if now.day == 1:
        resetMonthly()


@client.command()
async def ping(ctx: Context):
    """
    Shows the ping (in milli-seconds) of the bot.

    :param ctx:
        The command context

    """
    await ctx.send(f'pong : {round(client.latency * 1000)} ms')


@client.command(name="mystats")
async def my_stats_command(ctx: Context):
    """
    Returns embedded text of a member's overall data.

    :param ctx:
        The command context

    """
    member_id = str(ctx.author.id)
    channel: TextChannel = client.get_channel(config.study_text_channel)
    member = member_details(member_id)

    if member is None:
        await channel.send(
            f"Sorry, no records found for "
            f"**{ctx.author.name}#{ctx.author.discriminator}**"
        )
        return

    minutes: Dict[str, int] = {
        'member': int(member['memberTime']),
        'monthly': int(member['monthlyTime']),
        'weekly': int(member['weeklyTime']),
        'daily': int(member['dailyTime'])
    }

    embed = discord.Embed(
        title=f"Study stats for {member['name#']}",
        color=0x4be96d
    )

    for minutes_type, minute_count in minutes.items():
        embed.add_field(
            name=f'{minutes_type.upper()} TIME',
            value=f"{minute_count // 60} Hours "
                  f"{minute_count - 60 * (minute_count // 60)} Minutes",
            inline=False
        ).set_footer(
            icon_url=BOT_IMAGE_URL,
            text="Study-Bot"
        )

    await channel.send(embed=embed)


async def send_leaderboard(key: str, leaderboard):
    channel = client.get_channel(config.study_text_channel)
    description = ""

    for rank, members in enumerate(leaderboard, start=1):
        minutes = members[f'{key}Time']

        description += str(
            f"#{rank}\t|\t**{members['name#']}**\t|"
            f"\t**{minutes // 60}** Hours "
            f"**{minutes - 60 * (minutes // 60)}** Minutes\n"
        )

    await channel.send(
        embed=discord.Embed(
            title=f'Study Stats Leaderboard ({key.upper()} TIME)',
            color=0x4be96d,
            description=description
        ).set_footer(
            icon_url=BOT_IMAGE_URL,
            text="Study-Bot\nOther Valid Commands : leaderboard, lb_m, lb_w"
        )
    )


@client.command()
async def lb_d(_ctx: Context):
    """
    Returns embedded text of daily leaderboard.
    Top 10 members with highest study time in the day.

    :param _ctx:
        The command context, unused but needed.

    """
    await send_leaderboard('daily', daily_leaderboard())


@client.command()
async def lb_w(_ctx: Context):
    """
    Returns embedded text of weekly leaderboard.
    Top 10 members with highest study time in the week.

    :param _ctx:
        The command context, unused but needed.

    """
    await send_leaderboard("weekly", weekly_leaderboard())


@client.command()
async def lb_m(_ctx: Context):
    """
    Returns embedded text of monthly leaderboard.
    Top 10 members with highest study time in the month.

    :param _ctx:
        The command context, unused but needed.

    """
    await send_leaderboard("monthly", monthly_leaderboard())


@client.command(name="leaderboard")
async def leaderboard_command(_ctx: Context):
    """
    Returns embedded text of overall leaderboard.
    Top 10 members with highest study time overall.

    :param _ctx:
        The command context, unused but needed.

    """
    await send_leaderboard("member", member_leaderboard())


@client.command(name="help")
async def help_command(ctx: Context):
    """
    Returns embedded text of details of all commands.

    :param ctx:
        The command context

    """
    await ctx.send(
        embed=discord.Embed(
            color=0x4be96d,
            description='Need help??'
        ).add_field(
            name="**__ABOUT__**",
            value="Prefix : `+`"
        ).add_field(
            name="**__STUDY BOT__**",
            value="`mystats` : shows overall stats of the user\n"
                  "`lb_m/w/d` : shows top 10 studytime leaderboard of \n"
                  "m - monthly, w - weekly, d - daily\n"
                  "`leaderboard` : shows overall top 10 studytime leaderboard"
        ).set_footer(
            icon_url=BOT_IMAGE_URL,
            text="Study-Bot"
        )
    )


def check_before_flag(before_channel: str) -> bool:
    return before_channel != "None" and before_channel in config.study_list


def check_after_flag(after_channel: str) -> bool:
    return after_channel != "None" and after_channel in config.study_list


@client.event
async def on_voice_state_update(member: Member, before, after):
    """
    Assigns a discord role -> "studying" to everyone who joins study channels.
    Sends messages on user join and leave.

    :param member:
        The guild member that updated his voice state

    :param before:
        The state before the voice state was updated

    :param after:
        The state after the voice was updated

    """
    if member.bot:
        return

    # Checks if before and after channels were study channels
    before_flag = check_before_flag(str(before.channel))
    after_flag = check_after_flag(str(after.channel))

    if not before_flag and not after_flag:
        return

    if before.channel == after.channel:
        return

    guild: Optional[Guild] = None

    if before_flag:
        guild: Guild = before.channel.guild

    if after_flag:
        guild: Guild = after.channel.guild

    # Sets roles for study channels.
    role: Role = discord.utils.get(guild.roles, name="studying")
    txt_channel: TextChannel = client.get_channel(config.study_text_channel)

    # When user joins the voice channel
    if before.channel is None and after.channel is not None and after_flag:
        await member.add_roles(role)
        await txt_channel.send(
            f"{member.mention} I restricted your access to distracting "
            f"channels because you joined **{after.channel.name}** \n"
            f"Happy Studying :smile:", delete_after=60
        )
        join(member, before_flag, after_flag)

    elif before.channel is not None and after.channel is None and before_flag:
        await member.remove_roles(role)
        await txt_channel.send(
            f"**{member.name}#{member.discriminator}**"
            f" has left **{before.channel.name}**",
            delete_after=60
        )
        end(member)

    elif before_flag and after_flag:
        print("changed study rooms")

    elif after_flag:
        await member.add_roles(role)
        await txt_channel.send(
            f"{member.mention} I restricted your access to distracting "
            f"channels because you joined **{after.channel.name}** \n"
            f"Happy Studying :smile:", delete_after=60
        )
        join(member, before_flag, after_flag)

    elif before_flag:
        await member.remove_roles(role)
        await txt_channel.send(
            f"**{member.name}#{member.discriminator}**"
            f" has left **{before.channel.name}**",
            delete_after=60
        )
        end(member)


if __name__ == "__main__":
    client.run(config.discord_token)
