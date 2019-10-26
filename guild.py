import json, sys, os, datetime, asyncio
import discord
from functions import createdir, createjson, idtochannel
from logger import getLogger
logger = getLogger()
def genGuildSettings(guild):
    GuildInfo = {}

    GuildInfo["ChannelId"] = False
    GuildInfo["Botowner"] = 181125548389433344
    GuildInfo["Guildid"] = guild.id
    GuildInfo["DeleteAllOnCatDel"] = True
    GuildInfo["DelOnMsg"] = False
    GuildInfo["MatchmakerId"] = False
    GuildInfo["GameRooms"] = 0
    GuildInfo["JoinedAt"] = "{}".format(datetime.datetime.now())


    with open(r"Servers\{}\Settings\data.txt".format(guild.id), "w+") as outfile:
        json.dump(GuildInfo, outfile, indent=2)

class Dguild:
    memberid = 0
    def __init__(self, guildid):

        with open(r"Servers\{}\Settings\data.txt".format(guildid), "r") as outfile:
            GuildInfo = json.load(outfile)
        self.data = GuildInfo
        self.ChannelId = GuildInfo["ChannelId"]
        self.Botowner = GuildInfo["Botowner"]
        self.Guildid = GuildInfo["Guildid"]
        self.DeleteAllOnCatDel = GuildInfo["DeleteAllOnCatDel"]

        self.DelOnMsg = GuildInfo["DelOnMsg"]
        self.MatchmakerId = GuildInfo["MatchmakerId"]
        self.GameRooms = GuildInfo["GameRooms"]
        self.JoinedAt = GuildInfo["JoinedAt"]


    def read(self):

        with open(r"Servers\{}\Settings\data.txt".format(self.Guildid), "r") as outfile:
            GuildInfo = json.load(outfile)
        self.data = GuildInfo
        self.ChannelId = GuildInfo["ChannelId"]
        self.Botowner = GuildInfo["Botowner"]
        self.Guildid = GuildInfo["Guildid"]
        self.DelOnMsg = GuildInfo["DelOnMsg"]
        self.DeleteAllOnCatDel = GuildInfo["DeleteAllOnCatDel"]
        self.MatchmakerId = GuildInfo["MatchmakerId"]
        self.GameRooms = GuildInfo["GameRooms"]
        self.JoinedAt = GuildInfo["JoinedAt"]

    def write(self):
        GuildInfo = {}
        GuildInfo["DeleteAllOnCatDel"] = self.DeleteAllOnCatDel
        GuildInfo["ChannelId"] = self.ChannelId
        GuildInfo["Botowner"] = self.Botowner
        GuildInfo["Guildid"] = self.Guildid
        GuildInfo["DelOnMsg"] = self.DelOnMsg
        GuildInfo["MatchmakerId"] = self.MatchmakerId
        GuildInfo["GameRooms"] = self.GameRooms
        GuildInfo["JoinedAt"] = self.JoinedAt

        with open(r"Servers\{}\Settings\data.txt".format(self.Guildid), "w+") as outfile:
            json.dump(GuildInfo, outfile, indent=2)


async def getguilddata(guildid):
    guilddata = Dguild(guildid)
    return guilddata

async def checkGuild(guild):
    logger.debug("Checking files for the guild {}".format(guild.id))
    createdir(guild.id, "Servers")
    createdir("Users", "Servers\{}".format(guild.id))
    createdir("Rooms", "Servers\{}".format(guild.id))
    createdir("Settings", "Servers\{}".format(guild.id))
    createdir("Tournament", "Servers\{}".format(guild.id))
    createdir("Groups", "Servers\{}\Tournament".format(guild.id))
    createdir("knockout_Stage", "Servers\{}\Tournament".format(guild.id))

    try:
        with open(r"Servers\{}\Settings\data.txt".format(guild.id), "r"):
            pass
    except FileNotFoundError:
        genGuildSettings(guild)
