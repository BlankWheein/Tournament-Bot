import os, sys, json, discord, asyncio
from discord.ext import commands

def createjson(dirname, path):
    try:
        with open(r"{}\{}.txt".format(path, dirname), "r") as temp:
            pass
    except FileNotFoundError:
        with open(r"{}\{}.txt".format(path, dirname), "w+") as temp:
            pass
    with open(r"{}\{}.txt".format(path, dirname), "w+") as outfile:
        temp = {}
        json.dump(temp, outfile, indent=2)

def createdir(dirname, path):
    dirname = str(dirname)
    try:
        os.mkdir(r'{}\{}'.format(path, dirname))
    except FileExistsError:
        pass

async def idtorole(roles, id):
    id = int(id)
    try:
        mention : discord.Role = discord.utils.get(roles,id = id)
        return mention
    except Exception as error:
        print(error)

async def idtouser(members, id):
    id = int(id)
    try:
        mention : discord.Member = discord.utils.get(members,id = id)
        return mention
    except Exception as error:
        print(error)


async def idtochannel(channels, id):
    id = int(id)
    try:
        mention : discord.Member = discord.utils.get(channels,id = id)
        return mention
    except Exception as error:
        print(error)

def idtoguild(guilds, id):
    id = int(id)
    try:
        mention : discord.Member = discord.utils.get(guilds,id = id)
        return mention
    except Exception as error:
        print(error)

def getfilesinpath(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    return files