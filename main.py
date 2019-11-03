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
playerspergroup = 5
winsreuiredpforgroup = 4
matchesplayedingroupstage = 7
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
        Teams = 15
        if str(guild.id) == "493279314377441290":
            for name in range(Teams):
                x = True
                while x:
                    x = await appendTeam(random.choice(guild.members))
            await createBrackets(guild)
    print("Done")

@bot.event
async def on_member_join(member):
    checkmemberinguild(member, member.guild)

async def appendTeam(name):
    for x in group_stage:
        if x.name == name.name:
            print("True")
            return True
    group_stage.append(player(name))
    print("False")
    return False

@bot.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    deletedchannel = channel
    print(type(channel))
    if type(channel) == discord.CategoryChannel:
        roomsdata = json.load(open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "r"))
        print(f"The Category {channel.name} was deleted")
        for catid in roomsdata["Cat_Groups"]:
            if str(channel.id) == str(catid):
                for channelid in roomsdata["Cat_Groups"][str(channel.id)]:
                    try:
                        print(channelid)
                        channel = await idtochannel(guild.channels, int(channelid))
                        try:
                            await channel.delete()
                        except Exception:
                            pass
                    except Exception as error:
                        logger.debug(error)

        try:
            del roomsdata["Cat_Groups"][str(deletedchannel.id)]
        except Exception as error:
            print(error)

        with open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "w+") as outfile:
            json.dump(roomsdata, outfile, indent=2)
    elif type(channel) == discord.TextChannel:
        print(f"The textchannel {channel.name} was deleted")

@bot.command(pass_context=True)
async def gg(ctx):
    guild = ctx.message.guild
    await checkGuild(guild)
async def createCat(guild, name):

    cat = await guild.create_category_channel(name = name, overwrites = None)
    roomsdata = json.load(open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "r"))
    roomsdata["Cat_Groups"][str(cat.id)] = {}
    roomsdata["Cat_Groups"][str(cat.id)]["Id"] = str(cat.id)
    with open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "w+") as outfile:
        json.dump(roomsdata, outfile, indent=2)



    return cat
async def creategameroom(cat, player1, player2, name):
    guild = cat.guild

    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages = False,
    read_message_history = True, send_tts_messages = False, manage_messages = False, embed_links = False, attach_files = False,
    mention_everyone = False, create_instant_invite = False, manage_channels = False, manage_webhooks = False, administrator = False, add_reactions = False ),

    player1 : discord.PermissionOverwrite(read_messages=True, send_messages = True, read_message_history = True),
    player2 : discord.PermissionOverwrite(read_messages=True, send_messages = True, read_message_history = True),
    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages = True, read_message_history = True)
    }
    channel = await cat.create_text_channel(name = name, overwrites = overwrites)
    overwrites = discord.PermissionOverwrite(read_messages = True, send_messages = True, read_message_history = True, add_reactions = False)
    await channel.send(content = f"Welcome {player1.mention} and {player2.mention}")
    roomsdata = json.load(open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "r"))
    roomsdata["Cat_Groups"][str(cat.id)][str(channel.id)] = {}
    roomsdata["Cat_Groups"][str(cat.id)][str(channel.id)]["Player1"] = str(player1.id)
    roomsdata["Cat_Groups"][str(cat.id)][str(channel.id)]["Player2"] = str(player2.id)
    roomsdata["Cat_Groups"][str(cat.id)][str(channel.id)]["Id"] = str(channel.id)
    with open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "w+") as outfile:
        json.dump(roomsdata, outfile, indent=2)
@bot.command(pass_context=True)
async def startgroups(ctx):
    guild = ctx.message.guild
    groupfile = json.load(open (r"Servers\{}\Tournament\Groups\groups.txt".format(guild.id)))
    print("Starting group")
    StatsData = groupfile["Stats"]
    for group in groupfile["Groups"]:
        print("This is group", group)
        roomsdata = json.load(open(r"Servers\{}\Settings\rooms.txt".format(guild.id), "r"))
        category_found = False
        for id in roomsdata["Cat_Groups"]:
            for channel in guild.channels:
                if str(channel.id) == str(id) and str(channel.name) == f"Group-{group}":
                    cat = channel
                    category_found = True
        if category_found == False:
            cat = await createCat(guild, f"Group-{group}")
        groupData = groupfile["Groups"][group]
        playersingroup = int(groupData["playersingroup"])
        playerstoplay = []
        for player in range(playersingroup):
            playerstoplay.append(int(groupData["players"][f"{player}"]["Id"]))
        print(f"These are the players that needs to play {playerstoplay}")

        if playersingroup % 2 == 1:
            print("There will be 1 player who wont be able to play at the start!")
        while len(playerstoplay) > 1:

            player1id = playerstoplay.pop(0)
            player2id = playerstoplay.pop(0)
            try:
                player1 = await idtouser(guild.members, player1id)
            except Exception as error:
                logger.debug(error)
                player1 = player1id
            try:
                player2 = await idtouser(guild.members, player2id)
            except Exception as error:
                logger.debug(error)
                player2 = player2id
            player2 = await idtouser(guild.members, player2id)
            name = f"{player1.name} VS {player2.name}"
            client.loop.create_task(creategameroom(cat, player1, player2, name))



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



async def addlastplayers():
    print(f"The amount of groups in thing {len(tournament)}")
    groups = len(tournament)
    for player in group_stage:
        print((group_stage))
        try:
            for group in range(len(tournament)):
                tournament[group].append(group_stage.pop(0))
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
    groupInfo["Stats"] = {}
    groupInfo["Groups"] = {}

    groupInfo["Stats"]["Matches To Play"] = matchesplayedingroupstage
    groupInfo["Stats"]["Wins Required"] = winsreuiredpforgroup
    for x in range(groups):

        groupInfo["Groups"][x] = {}
        groupInfo["Groups"][x]["playersingroup"] = len(tournament[x])
        groupInfo["Groups"][x]["available_players"] = {}
        groupInfo["Groups"][x]["players"] = {}

        for i in range(len(tournament[x])):
            playerid = tournament[x][i].id
            groupInfo["Groups"][x]["available_players"][str(playerid)] = True

            groupInfo["Groups"][x]["players"][i] = {}
            groupInfo["Groups"][x]["players"][i]["Matches_Played"] = 0
            groupInfo["Groups"][x]["players"][i]["Wins"] = 0
            groupInfo["Groups"][x]["players"][i]["Defeats"] = 0
            groupInfo["Groups"][x]["players"][i]["Id"] = playerid
            groupInfo["Groups"][x]["players"][i]["Opponents_Left"] = {}

        for i in range(len(tournament[x])):
            for player in groupInfo["Groups"][x]["players"]:
                if str(groupInfo["Groups"][x]["players"][i]["Id"]) != str(groupInfo["Groups"][x]["players"][player]["Id"]):
                    playerid = groupInfo["Groups"][x]["players"][player]["Id"]
                    groupInfo["Groups"][x]["players"][i]["Opponents_Left"][playerid] = 0



    with open(r"Servers\{}\Tournament\Groups\groups.txt".format(guildid), "w+") as outfile:
        json.dump(groupInfo, outfile, indent=2)
    print("Playing groups")


bot.run(TOKEN)
