import discord
from discord.ext import commands
import random
import asyncio

class Spyfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = dict()
        self.wait_game_start_confirmation = 0
        self.spy = None
        self.roles = dict()
        
        self.load_roles()

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
        if len(self.players) == 1:
            await ctx.send("I can't start a game with only 1 player you fool")
            return
        if len(self.players) == 0:
            await ctx.send("There's no one in the game.")
            return
        if len(self.players) < 4:
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
        print('len(players): ' + str(len(self.players)))
        print('number of locations: ' + str(len(self.roles)))
        self.start_timer(ctx)
        
    # game logic
    async def start_game(self, ctx):
        await ctx.send("starting game.")
        await self.assign_spy(ctx)
        await self.assign_roles(ctx)
    
    async def initiate_player(self, ctx, new_player):
        dm = new_player.dm_channel
        if dm == None:
            await new_player.create_dm()
            dm = new_player.dm_channel
        self.players[new_player] = dm
        
        await dm.send("Hello! Welcome to Spyfall. If you are chosen as the spy, you will be notified here.")
        await ctx.send(new_player.name + ' has joined the game.')
        
    async def assign_spy(self, ctx):
        index = random.randrange(len(self.players)-1)
        self.spy = list(self.players.keys())[index]
        await self.players[self.spy].send("shhhh, you're the spy...")
        
    async def assign_roles(self, ctx):
        #for player in self.players:
        print('assing_roles')
        
    # util methods
    def load_roles(self):
        print("loading roles from file.")
        with open('roles') as f:
            locations = f.readlines()
            index = 0
            while index < len(locations):
                location = locations[index].strip() #location name
                index+=1
                while index < len(locations) and locations[index].strip() != '-':
                    if location not in self.roles:
                        self.roles[location] = [locations[index].strip()]
                    else:
                        self.roles[location].append(locations[index].strip())
                    index+=1
                index+=1
    
    def start_timer(self, ctx, duration = 10): # duration in minutes
        print('in start_timer')
        self.bot.loop.create_task(self.start_timer_helper(ctx, duration))
    
    async def start_timer_helper(self, ctx, duration):
        print('in helper')
        time_left = duration
        while not self.bot.is_closed:
            # reminder every minute
            await ctx.send(str(time_left) + " minutes left!")
            await asyncio.sleep(10)
            time_left -= 1
            if time_left >= 0:
                return

if __name__=="__main__":
    bot = commands.Bot(command_prefix='!')
    with open("token") as f:
        token = f.read()
    bot.add_cog(Spyfall(bot))
    bot.run(token)