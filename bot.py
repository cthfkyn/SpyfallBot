import discord
from discord.ext import commands
import random

class Spyfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = dict()
        self.wait_game_start_confirmation = 0
        self.locations = [
            
        ]

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as {0.user}'.format(self.bot))
        self.players.clear()
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        self.players.clear()

    # commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('you\'ve pinged me, are you proud of yourself')
    
    @commands.command()
    async def joinGame(self, ctx):
        new_player = ctx.message.author
        if new_player in self.players:
            await ctx.send(new_player.name + ' is already in the game.')
            return
        await self.initiate_player(ctx, new_player)
        
    @commands.command()
    async def leaveGame(self, ctx):
        self.players.pop(ctx.message.author)
        await ctx.send(ctx.message.author.name + " has left the game.")
        
    @commands.command()
    async def startGame(self, ctx):
        if len(self.players.keys()) < 4:
            await ctx.send("there are less than 4 players. are you sure you want to start? send 'y' to continue.")
            print('setting waiting for confirmation flag')
            self.wait_game_start_confirmation = 1
            return
        else:
            await self.start_game(ctx)
        
    @commands.command()
    async def y(self, ctx):
        print('in confirmation')
        if self.wait_game_start_confirmation:
            print("starting game??????")
            await self.start_game(ctx)
        
    @commands.command()
    async def reset(self, ctx):
        await ctx.send("resetting game state.")
        self.players.clear()
        
    @commands.command()
    async def debug(self, ctx):
        print(self.wait_game_start_confirmation)
        print(self.players)
        
    # game logic
    async def start_game(self, ctx):
        await ctx.send("starting game.")
        await self.assign_spy(ctx)
    
    async def initiate_player(self, ctx, new_player):
        dm = new_player.dm_channel
        if dm == None:
            await new_player.create_dm()
            dm = new_player.dm_channel
        self.players[new_player] = dm
        
        await dm.send("Hello! Welcome to Spyfall. If you are chosen as the spy, you will be notified here.")
        await ctx.send(new_player.name + ' has joined the game.')
        
    async def assign_spy(self, ctx):
        if len(self.players.keys()) <= 1:
            index = 0
        else:
            index = random.randrange(len(self.players.keys())-1)
        spy = list(self.players.keys())[index]
        await self.players[spy].send("shhhh, you're the spy...")

if __name__=="__main__":
    bot = commands.Bot(command_prefix='!')
    f = open('token')
    token = f.read()
    bot.add_cog(Spyfall(bot))
    bot.run(token)
