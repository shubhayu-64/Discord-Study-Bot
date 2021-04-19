import discord
from discord.ext import commands, tasks
from database import *
import schedule
import time
import config

# List of Study Voice Channels in the server
studyList = [
    'study-room-1', 'study-room-2 (24/7 Lofi)', 'study-room-3',
    'Programming-VC (Screensharing)'
]

# The prefix set for the bot
client = commands.Bot(command_prefix='+')
client.remove_command('help')

# Replace with your bot icon image.
bot_image_url = "https://i.pinimg.com/564x/c9/4e/e1/c94ee183a2e635e5b8972bc0240ad23a.jpg"

# Replace with your study text channel ID. Takes an integer.
study_text_channel = 817450164234878987


# Prints a message once bot becomes ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("+help"))
    print(f'{client.user} is running')
    reset.start()


# Resets leaderboards everyday.
@tasks.loop(minutes=60)
async def reset():
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    if now.hour == 0:
        resetDaily()
        if now.weekday() == 0:
            resetWeekly()
        if now.day == 1:
            resetMonthly()


# Shows the ping (in mili-seconds) of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f'pong : {round(client.latency * 1000)} ms')


# Returns embeded text of a member's overall data
@client.command()
async def mystats(ctx):
    member_id = str(ctx.author.id)
    channel = client.get_channel(study_text_channel)
    member = member_details(member_id)
    if member == None:
        await channel.send(
            f"Sorry, no records found for **{ctx.author.name}#{ctx.author.discriminator}**"
        )
    else:
        embed = discord.Embed(title=f"Study stats for {member['name#']}",
                              color=0x4be96d)
        minutes = int(member['memberTime'])
        embed.add_field(name='MEMBER TIME',
                        value=f"{minutes//60} Hours {minutes - 60*(minutes//60)} Minutes",
                        inline=False)
        minutes = int(member['monthlyTime'])
        embed.add_field(name='MONTHLY TIME',
                        value=f'{minutes//60} Hours {minutes - 60*(minutes//60)} Minutes',
                        inline=False)
        minutes = int(member['weeklyTime'])
        embed.add_field(name='WEEKLY TIME',
                        value=f'{minutes//60} Hours {minutes - 60*(minutes//60)} Minutes',
                        inline=False)
        minutes = int(member['dailyTime'])
        embed.add_field(name='DAILY TIME',
                        value=f'{minutes//60} Hours {minutes - 60*(minutes//60)} Minutes',
                        inline=False)
        embed.set_footer(
            icon_url=bot_image_url,
            text="Study-Bot")
        await channel.send(embed=embed)


# Returns embeded text of daily leaderboard. Top 10 members with highest study time in the day.
@client.command()
async def lb_d(ctx):
    channel = client.get_channel(study_text_channel)
    leaderboard = daily_leaderboard()
    description = ""
    rank = 1
    for members in leaderboard:
        minutes = members["dailyTime"]
        description = description + \
            str(f"#{rank}\t|\t**{members['name#']}**\t|\t**{minutes//60}** Hours **{minutes - 60*(minutes//60)}** Minutes\n")
        rank = rank + 1
    embed = discord.Embed(
        title='Study Stats Leaderboard (DAILY TIME)', color=0x4be96d, description=description)
    embed.set_footer(icon_url=bot_image_url,
                     text="Study-Bot\nOther Valid Commands : leaderboard, lb_m, lb_w")
    await channel.send(embed=embed)


# Returns embeded text of weekly leaderboard. Top 10 members with highest study time in the week.
@client.command()
async def lb_w(ctx):
    channel = client.get_channel(study_text_channel)
    leaderboard = weekly_leaderboard()
    description = ""
    rank = 1
    for members in leaderboard:
        minutes = members["weeklyTime"]
        description = description + \
            str(f"#{rank}\t|\t**{members['name#']}**\t|\t**{minutes//60}** Hours **{minutes - 60*(minutes//60)}** Minutes\n")
        rank = rank + 1
    embed = discord.Embed(title='Study Stats Leaderboard (WEEKLY TIME)',
                          color=0x4be96d, description=description)
    embed.set_footer(icon_url=bot_image_url,
                     text="Study-Bot\nOther Valid Commands : leaderboard, lb_m, lb_d")
    await channel.send(embed=embed)


# Returns embeded text of monthly leaderboard. Top 10 members with highest study time in the month.
@client.command()
async def lb_m(ctx):
    channel = client.get_channel(study_text_channel)
    leaderboard = monthly_leaderboard()
    description = ""
    rank = 1
    for members in leaderboard:
        minutes = members["monthlyTime"]
        description = description + \
            str(f"#{rank}\t|\t**{members['name#']}**\t|\t**{minutes//60}** Hours **{minutes - 60*(minutes//60)}** Minutes\n")
        rank = rank + 1
    embed = discord.Embed(title='Study Stats Leaderboard (MONTHLY TIME)',
                          color=0x4be96d, description=description)
    embed.set_footer(icon_url=bot_image_url,
                     text="Study-Bot\nOther Valid Commands : leaderboard, lb_w, lb_d")
    await channel.send(embed=embed)


# Returns embeded text of overall leaderboard. Top 10 members with highest study time overall.
@client.command()
async def leaderboard(ctx):
    channel = client.get_channel(study_text_channel)
    leaderboard = member_leaderboard()
    description = ""
    rank = 1
    for members in leaderboard:
        minutes = members["memberTime"]
        description = description + \
            str(f"#{rank}\t|\t**{members['name#']}**\t|\t**{minutes//60}** Hours **{minutes - 60*(minutes//60)}** Minutes\n")
        rank = rank + 1
    embed = discord.Embed(title='Study Stats Leaderboard (MEMBER TIME)',
                          color=0x4be96d, description=description)
    embed.set_footer(icon_url=bot_image_url,
                     text="Study-Bot\nOther Valid Commands : lb_m, lb_w, lb_d")
    await channel.send(embed=embed)


# Returns embeded text of details of all commands.
@client.command()
async def help(ctx):
    embed = discord.Embed(color=0x4be96d, description='Need help??')
    embed.add_field(name="**__ABOUT__**", value="Prefix : `+`")
    embed.add_field(name="**__STUDY BOT__**", value="`mystats` : shows overall stats of the user\n`lb_m/w/d` : shows top 10 studytime leaderboard of \nm - monthly, w - weekly, d - daily\n`leaderboard` : shows overall top 10 studytime leaderboard")
    embed.set_footer(
        icon_url=bot_image_url, text="Study-Bot")
    await ctx.send(embed=embed)


def check_before_flag(before_channel):
    if before_channel != "None" and before_channel in studyList:
        return True
    else:
        return False


def check_after_flag(after_channel):
    if after_channel != "None" and after_channel in studyList:
        return True
    else:
        return False


# Assigns a discord role -> "studying" to everyone who joins study channels. Sends messages on user join and leave.
@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    # Checks if before and after channels were study channels
    before_flag = check_before_flag(str(before.channel))
    after_flag = check_after_flag(str(after.channel))

    if not before_flag and not after_flag:
        return
    if before.channel == after.channel:
        return

    if before_flag:
        Guild = before.channel.guild
    if after_flag:
        Guild = after.channel.guild

    # Sets roles for study channels.
    role = discord.utils.get(Guild.roles, name="studying")
    txt_channel = client.get_channel(study_text_channel)

    # When user joins the voice channel
    if before.channel == None and after.channel != None and after_flag:
        await member.add_roles(role)
        await (await txt_channel.send(
            f"{member.mention} I restricted your access to distracting channels because you joined **{after.channel.name}** \nHappy Studying :smile:"
        )).delete(delay=60)
        join(member, before_flag, after_flag)

    # When user leaves the voice channel
    elif before.channel != None and after.channel == None and before_flag:
        await member.remove_roles(role)
        await (await txt_channel.send(
            f"**{member.name}#{member.discriminator}** has left **{before.channel.name}**"
        )).delete(delay=60)
        end(member)

    # When user changes study voice channels
    elif before_flag and after_flag:
        print("changed study rooms")

    # When user joins Study Voice Channel from different voice channel
    elif after_flag:
        await member.add_roles(role)
        await (await txt_channel.send(
            f"{member.mention} I restricted your access to distracting channels because you joined **{after.channel.name}** \nHappy Studying :smile:"
        )).delete(delay=60)
        join(member, before_flag, after_flag)

    # When user leaves Study voice channel
    elif before_flag:
        await member.remove_roles(role)
        await (await txt_channel.send(
            f"**{member.name}#{member.discriminator}** has left **{before.channel.name}**"
        )).delete(delay=60)
        end(member)


if __name__ == "__main__":
    client.run(config.discordToken)
