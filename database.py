from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Union, Optional, TYPE_CHECKING

import pymongo
from pymongo import MongoClient
from pytz import timezone
import config

if TYPE_CHECKING:
    import discord

JsonData = Dict[str, Union[str, int]]

cluster = MongoClient(config.mongo_client)
db: MongoClient = cluster[config.cluster_name]
collection: MongoClient = db[config.collection_name]


def daily_leaderboard() -> List[JsonData]:
    print(
        list(collection.find({}).sort(
            "dailyTime", pymongo.DESCENDING)
        )[:10]
    )
    return list(collection.find({}).sort(
        "dailyTime", pymongo.DESCENDING)
    )[:10]


def weekly_leaderboard() -> List[JsonData]:
    return list(collection.find({}).sort(
        "weeklyTime", pymongo.DESCENDING)
    )[:10]


def monthly_leaderboard() -> List[JsonData]:
    return list(collection.find({}).sort(
        "monthlyTime", pymongo.DESCENDING)
    )[:10]


def member_leaderboard() -> List[JsonData]:
    return list(collection.find({}).sort(
        "memberTime", pymongo.DESCENDING)
    )[:10]


def member_details(member_id) -> Optional[JsonData]:
    member = collection.find_one({"_id": member_id})
    return member if str(member) != "none" else None


def resetDaily():
    """
    Resets daily time of all members
    """
    collection.update_many({}, {"$set": {"dailyTime": 0}})


def resetWeekly():
    """
    Resets weekly time of all members
    """
    collection.update_many({}, {"$set": {"weeklyTime": 0}})


def resetMonthly():
    """
    Resets monthly time of all members.
    """
    collection.update_many({}, {"$set": {"monthlyTime": 0}})


def end(member: discord.Member):
    """
    Updates total Study time for members when they leave.

    :param member:
        The member that left the voice channel.
    """
    now: datetime = datetime.now(timezone('Asia/Kolkata'))
    now_str: str = now.strftime("%H:%M")

    user = collection.find_one({"_id": str(member.id)})

    join_time = str(user["startTime"])
    join_hour, join_minutes = join_time.split(':')
    join_minutes = int(join_hour) * 60 + int(join_minutes)

    current_hour, current_minutes = now_str.split(':')
    current_minutes = int(current_hour) * 60 + int(current_minutes)

    if current_minutes < join_minutes:
        daily_time = current_minutes
        difference = (1440 - join_minutes) + current_minutes
        weekly_time = current_minutes if int(now.weekday()) == 0 else difference
        monthly_time = current_minutes if int(now.day) == 1 else difference
    else:
        difference = current_minutes - join_minutes
        daily_time = difference
        weekly_time = difference
        monthly_time = difference

    collection.update_one(
        {"_id": str(member.id)},
        {
            "$inc": {
                "memberTime": int(difference),
                "monthlyTime": int(monthly_time),
                "weeklyTime": int(weekly_time),
                "dailyTime": int(daily_time)
            }
        }
    )

    collection.update_one(
        {"_id": str(member.id)},
        {"$set": {"startTime": 0}}
    )


def update_join(member: discord.Member, _before_flag, _after_flag):
    """
    Updates join data for existing members

    :param member:
        The member who joined the study channel

    :param _before_flag:
        The flag before the member joined the study channel

    :param _after_flag:
        The flag after the member joined the study channel

    """
    now: str = datetime.now(timezone('Asia/Kolkata')).strftime("%H:%M")
    collection.update_one(
        {"_id": str(member.id)},
        {
            "$set": {
                "startTime": now,
                "name#": str(member.name + "#" + member.discriminator)
            }
        }
    )


def add(member: discord.Member, _before_flag, _after_flag):
    """
    Adds new entry in database for new members.

    :param member:
        The member who joined the study channel

    :param _before_flag:
        The flag before the member joined the study channel

    :param _after_flag:
        The flag after the member joined the study channel
    """
    now: str = datetime.now(timezone('Asia/Kolkata')).strftime("%H:%M")
    post = {
        "_id": str(member.id),
        "memberTime": 0,
        "monthlyTime": 0,
        "weeklyTime": 0,
        "dailyTime": 0,
        "startTime": now,
        "name#": str(member.name + "#" + member.discriminator)
    }
    collection.insert_one(post)


def join(member: discord.Member, before_flag, after_flag):
    """
    Called once member joins study channel.

    :param member:
        The member who joined the study channel

    :param before_flag:
        The flag before the member joined the study channel

    :param after_flag:
        The flag after the member joined the study channel
    """
    if before_flag == after_flag:
        return

    user_exist = str(collection.find_one({"_id": str(member.id)}))

    if user_exist == "None":
        add(member, before_flag, after_flag)
    else:
        update_join(member, before_flag, after_flag)
