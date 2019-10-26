import json
import os, sys, datetime, random
from logger import getLogger
from functions import idtouser, idtoguild

logger = getLogger()

class Dmember:

    def __init__(self, memberid, guildid):

        with open(r"Servers\{}\Users\{}.txt".format(guildid, memberid), "r") as outfile:
            data = json.load(outfile)

        self.memberid = memberid
        self.guildid = guildid
        self.data = data
        self.Wins = data["Wins"]
        self.Defeats = data["Defeats"]
        self.Leaves = data["Leaves"]
        self.Tournaments_Played = data["Tournaments Played"]
        self.Surrenders = data["Surrenders"]
        self.Disputes = data["Disputes"]
        self.Warnings = data["Warnings"]
        self.Read_Rules = data["Read_Rules"]
        self.JoinedAt = data["JoinedAt"]

    def read(self):

        with open(r"Servers\{}\Users\{}.txt".format(self.guildid, self.memberid), "r") as outfile:
            data = json.load(outfile)

        self.memberid = memberid
        self.guildid = guildid
        self.data = data
        self.Wins = data["Wins"]
        self.Defeats = data["Defeats"]
        self.Leaves = data["Leaves"]
        self.Tournaments_Played = data["Tournaments Played"]
        self.Surrenders = data["Surrenders"]
        self.Disputes = data["Disputes"]
        self.Warnings = data["Warnings"]
        self.Read_Rules = data["Read_Rules"]
        self.JoinedAt = data["JoinedAt"]

    def write(self):
        UserInfo = {}
        UserInfo["Wins"] = self.Wins
        UserInfo["Defeats"] = self.Defeats
        UserInfo["Leaves"] = self.Leaves
        UserInfo["Tournaments Played"] = self.Tournaments_Played
        UserInfo["Surrenders"] = self.Surrenders
        UserInfo["Disputes"] = self.Disputes
        UserInfo["Warnings"] = self.Warnings
        UserInfo["Read_Rules"] = self.Read_Rules
        UserInfo["JoinedAt"] = self.JoinedAt

        with open(r"Servers\{}\Users\{}.txt".format(self.guildid, self.memberid), "w+") as outfile:
            json.dump(UserInfo, outfile, indent=2)

    def calcelo(self, otherplayersElo):
        '''Elo calc'''



def getuserdata(memberid, guildid):
    userdata = Dmember(memberid, guildid)
    return userdata



def checkmemberinguild(member, guild):
    try:
        with open(r"Servers\{}\Users\{}.txt".format(guild.id, member.id), "r"):
            pass
    except FileNotFoundError:
        logger.debug("creating file for {}".format(member.id))
        genUserSettings(member, guild)

def logmember(member, guildid):
    memberData = Dmember(member.id, guildid)


def genUserSettings(member, guild):
    UserInfo = {}

    UserInfo["Wins"] = 0
    UserInfo["Defeats"] = 0
    UserInfo["Leaves"] = 0
    UserInfo["Surrenders"] = 0
    UserInfo["Disputes"] = 0
    UserInfo["Tournaments Played"] = 0
    UserInfo["Warnings"] = 0
    UserInfo["Read_Rules"] = True
    UserInfo["JoinedAt"] = "{}".format(datetime.datetime.now())


    with open(r"Servers\{}\Users\{}.txt".format(guild.id, member.id), "w+") as outfile:
        json.dump(UserInfo, outfile, indent=2)

    logmember(member, guild.id)
