import discord, asyncio
from discord.ext import commands
import math, sys, os, random
import datetime, time, calendar, re
from logger import getLogger
from guild import *
from member import *
from functions import *
class player:
    def __init__(self, object):
        self.name = object.name
        self.object = object
        self.wins = 0
        self.id = object.id
        self.defeats = 0
        self.data = f"{self.name}, {self.wins}, {self.defeats}"
        self.seed = random.uniform(-100, 100)
names = []
group_stage = []
knockout_stage = []
playerspergroup = 6
winsreuiredpforgroup = 3
matchesplayedingroupstage = 5
tournament = []
with open ("names.txt", "r") as file:
    for line in file:
        try:
            line = re.sub("Â\xa0\n", "", line)
            names.append(line)
        except Exception as error:
            print(error)


client = discord.Client()
logger = getLogger()
bot = commands.Bot(command_prefix='.')
with open (r'TOKEN.txt', 'r') as file:
	TOKEN = file.read()


@bot.event
async def on_ready():
    logger.info(bot.user.id)
    logger.info("The bot started successfully! :)")
    logger.debug("Looking through all servers to make sure members and server data is correct")
    for guild in bot.guilds:
        await checkGuild(guild)
        for member in guild.members:
            checkmemberinguild(member, guild)

@bot.event
async def on_member_join(member):
    checkmemberinguild(member, member.guild)

async def appendTeam(name):
    for x in group_stage:
        if x.name == name.name:
            return True
    group_stage.append(player(name))
    return False

@bot.command(pass_context=True)
async def gg(ctx):
    guild = ctx.message.guild
    await checkGuild(guild)


@bot.command(pass_context=True)
async def createTeams(ctx, Teams = 128):
    if str(ctx.message.author.id) == "181125548389433344":
        pass
    else:
        return print("You need to be a Moderator to use this command")
    for name in range(Teams):
        x = True
        while x:
            x = await appendTeam(random.choice(ctx.message.guild.members))
    for x in group_stage:
        print(x.name)
    await createBrackets(ctx.message.guild)

async def winner(player1, player2, winner):
    if winner == 1:
        player1.wins += 1
        player2.defeats += 1
        player1.data = f"{player1.name}, {player1.wins}, {player1.defeats}"
        player2.data = f"{player2.name}, {player2.wins}, {player2.defeats}"
    if winner == 2:
        player2.wins += 1
        player1.defeats += 1
        player1.data = f"{player1.name}, {player1.wins}, {player1.defeats}"
        player2.data = f"{player2.name}, {player2.wins}, {player2.defeats}"

async def nextstage(group):
    for player in group:
        if player.wins >= 3:
            knockout_stage.append(player.name)
        else:
            print(f"Sorry {player.name} you didnt make it")


async def playgroups(groups):
    groupnumber = 0
    for group in tournament:
        print(f"Group number is {groupnumber}")
        playersingroup = len(group)
        index = -1
        games = 0

        for i in range(0, playersingroup):
            player1num = i

            index += 1
            for j in range(1, playersingroup):
                player2num = j+index

                if player2num < playersingroup and player1num < playersingroup:
                    player2 = group[player2num]
                    player1 = group[player1num]

                    games += 1
                    winnerint = random.randint(1, 2)
                    await winner(player1, player2, winnerint)
        print(f"Games that needs to be played for this group to be done: {games}")
        for player in group:
            print(player.data)





        groupnumber += 1


async def addlastplayers():
    print(f"The amount of groups in thing {len(tournament)}")
    groups = len(tournament)
    while len(group_stage) > 0:
        try:
            for group in tournament:
                player = group_stage.pop(0)
                group.append(player)
                if len(group_stage) < 1:
                    break
        except Exception as error:
            print(error)
async def createBrackets(guild):
    guildid = guild.id
    sparePlayers =  len(group_stage) % playerspergroup
    groups = int(len(group_stage) / playerspergroup)
    print(f"Groups: {groups}, spare Players: {sparePlayers}")

    for x in range(groups):
        group = []
        for x in range(playerspergroup):
            playernumber = random.randint(0, len(group_stage)-1)
            player = group_stage.pop(playernumber)
            group.append(player)

        tournament.append(group)
    print(f"These players didnt play: {group_stage}")

    if sparePlayers > 0:
        await addlastplayers()
    groupInfo = {}
    groupInfo["Groups"] = {}
    groupInfo["Groups"]["Matches To Play"] = matchesplayedingroupstage
    groupInfo["Groups"]["Wins Required"] = winsreuiredpforgroup
    for x in range(groups):

        groupInfo["Groups"][x] = {}
        groupInfo["Groups"][x]["players"] = {}
        for i in range(len(tournament[x])):
            playerid = tournament[x][i].id
            groupInfo["Groups"][x]["players"][i] = {}
            groupInfo["Groups"][x]["players"][i]["Matches_Played"] = 0
            groupInfo["Groups"][x]["players"][i]["Wins"] = 0
            groupInfo["Groups"][x]["players"][i]["Defeats"] = 0
            groupInfo["Groups"][x]["players"][i]["Id"] = playerid
            groupInfo["Groups"][x]["players"][i]["Opponents_Left"] = {}

        for i in range(len(tournament[x])):
            for player in groupInfo["Groups"][x]["players"]:
                if str(groupInfo["Groups"][x]["players"][i]["Id"]) != str(groupInfo["Groups"][x]["players"][player]["Id"]):
                    groupInfo["Groups"][x]["players"][i]["Opponents_Left"][player] = groupInfo["Groups"][x]["players"][player]["Id"]



    with open(r"Servers\{}\Tournament\Groups\groups.txt".format(guildid), "w+") as outfile:
        json.dump(groupInfo, outfile, indent=2)
    await playgroups(groups)


bot.run(TOKEN)
