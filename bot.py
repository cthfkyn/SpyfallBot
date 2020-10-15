import discord, os
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='>')

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
keyPath = 'key.txt'
keyFile = open(os.path.join(__location__, keyPath), 'r')
key = keyFile.read()
keyFile.close()

print(key)

players = dict()
wait_game_start_confirmation = False

# events
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    players.clear()

@bot.event
async def on_disconnect():
    players.clear()

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('ping'):
#         await message.channel.send('ping urself')

#     await bot.process_commands(message)

# commands
@bot.command()
async def ping(ctx):
    await ctx.send('you\'ve pinged me, are you proud of yourself')

@bot.command()
async def joinGame(ctx):
    new_player = ctx.message.author
    if new_player in players:
        await ctx.send(new_player.name + ' is already in the game.')
        return
    await initiate_player(ctx, new_player)

@bot.command()
async def leaveGame(ctx):
    players.pop(ctx.message.author)
    await cxt.send(ctx.message.author.name + " has left the game.")

@bot.command()
async def startGame(ctx):
    if len(players.keys()) < 4:
        await ctx.send("there are less than 4 players. are you sure you want to start? send 'y' to continue.")
        wait_game_start_confirmation = True
        return
    await start_game(ctx)

@bot.command()
async def y(ctx):
    if wait_game_start_confirmation:
        print("starting game??????")
        await start_game(ctx)

@bot.command()
async def reset(ctx):
    await ctx.send("resetting game state.")
    players.clear()

# game logic
async def start_game(ctx):
    await ctx.send("starting game.")
    await assign_spy(ctx)

async def initiate_player(ctx, new_player):
    dm = new_player.dm_channel
    if dm == None:
        await new_player.create_dm()
        dm = new_player.dm_channel
    players[new_player] = dm

    await dm.send("Hello! Welcome to Spyfall. If you are chosen as the spy, you will be notified here.")
    await ctx.send(new_player.name + ' has joined the game.')

async def assign_spy(ctx):
    index = random.randrange(len(players.keys())-1)
    spy = list(players.keys())[index]
    await players[spy].send("shhhh, you're the spy...")

#bot.run(key)
