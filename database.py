import pymongo
import discord
from pymongo import MongoClient
import datetime
from pytz import timezone
import config


cluster = MongoClient(config.mongo_client)

db = cluster[config.cluster_name]
collection = db[config.collection_name]


def daily_leaderboard():
    leaderboard = list(collection.find({}).sort(
 "dailyTime", pymongo.DESCENDING))[:10]
    return leaderboard


def weekly_leaderboard():
    leaderboard = list(collection.find({}).sort(
        "weeklyTime", pymongo.DESCENDING))[:10]
    return leaderboard


def monthly_leaderboard():
    leaderboard = list(collection.find({}).sort(
        "monthlyTime", pymongo.DESCENDING))[:10]
    return leaderboard


def member_leaderboard():
    leaderboard = list(collection.find({}).sort(
        "memberTime", pymongo.DESCENDING))[:10]
    return leaderboard


def member_details(member_id):
    member = collection.find_one({"_id": member_id})
    if str(member) == "none":
        return None
    else:
        return member


# Resets daily time of all members
def resetDaily():
    collection.update_many({}, {"$set": {"dailyTime": 0}})


# Resets weekly time of all members
def resetWeekly():
    collection.update_many({}, {"$set": {"weeklyTime": 0}})


# Resets monthly time of all members
def resetMonthly():
    collection.update_many({}, {"$set": {"monthlyTime": 0}})


# Updates total Study time for members when they leave.
def end(member: discord.Member):
    now = datetime.datetime.now(timezone('Asia/Kolkata')).strftime("%H:%M")
    user = collection.find_one({"_id": str(member.id)})

    join_time = str(user["startTime"])
    join_hour, join_minutes = join_time.split(':')
    join_minutes = int(join_hour) * 60 + int(join_minutes)

    current_hour, current_minutes = now.split(':')
    current_minutes = int(current_hour)*60 + int(current_minutes)

    difference = 0
    daily_time = 0
    weekly_time = 0
    monthly_time = 0
    if current_minutes < join_minutes:
        daily_time = current_minutes
        difference = (1440 - join_minutes) + current_minutes
        if int(now.weekday()) == 0:
            weekly_time = current_minutes
        else:
            weekly_time = difference
        if int(now.day) == 1:
            monthly_time = current_minutes
        else:
            monthly_time = difference
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


# Updates join data for existing members
def update_join(member: discord.Member, before_flag, after_flag):
    now = datetime.datetime.now(timezone('Asia/Kolkata')).strftime("%H:%M")
    collection.update_one(
        {"_id": str(member.id)},
        {
            "$set": {
                "startTime": now,
                "name#": str(member.name + "#" + member.discriminator)
            }
        }
    )


# Adds new entry in database for new members.
def add(member: discord.Member, before_flag, after_flag):
    now = datetime.datetime.now(timezone('Asia/Kolkata')).strftime("%H:%M")
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


# Called once member joins study channel
def join(member: discord.Member, before_flag, after_flag):
    if before_flag == after_flag:
        return

    user_exist = str(collection.find_one({"_id": str(member.id)}))

    if user_exist == "None":
        add(member, before_flag, after_flag)
    else:
        update_join(member, before_flag, after_flag)
