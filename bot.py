import discord, os
from discord.ext import commands
import random
import asyncio

class Spyfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = list()
        self.dm_channels = dict
        self.wait_game_start_confirmation = False
        self.pause_timer = False
        self.spy = None
        self.rolesMap = dict()
        self.scores = dict()
        self.game_started = False
        
        self.load_roles()

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as {0.user}'.format(self.bot))
        self._reset()
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        self._reset()

    # commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('you\'ve pinged me, are you proud of yourself')
    
    @commands.command()
    async def joinGame(self, ctx):
        print("command \'joinGame\' called.")
        new_player = ctx.message.author
        
        if new_player in self.players:
            await ctx.send(new_player.name + ' is already in the game.')
            return
        
        await self.initiate_player(ctx, new_player)
        
        
    @commands.command()
    async def leaveGame(self, ctx):
        print("command \'leaveGame\' called.")
        self.players.remove(ctx.message.author)
        await ctx.send(ctx.message.author.name + " has left the game.")
        
    @commands.command()
    async def startGame(self, ctx):
        print("command \'startGame\' called.")
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
        print("command \'y\' called.")
        if self.wait_game_start_confirmation:
            await self.start_game(ctx)
        
    @commands.command()
    async def reset(self, ctx):
        print("command \'reset\' called.")
        await ctx.send("resetting game state.")
        self._reset()
        
    @commands.command()
    async def debug(self, ctx):
        print("command \'debug\' called.")
        print('len(players): ' + str(len(self.players)))
        print('number of locations: ' + str(len(self.rolesMap)))
        #self.start_timer(ctx)
        
    @commands.command()
    async def newRound(self, ctx):
        print("command \'newRound\' called.")
        await self._new_round(ctx)
    
    # game logic
    async def start_game(self, ctx):
        await ctx.send("Starting game.")
        self.game_started = True
        await self.newRound(ctx)
        
    async def _new_round(self, ctx):
        self.pause_timer = False
        if(game_started) :
            await self.assign_spy(ctx)
            await self.assign_roles(ctx)
    
    async def initiate_player(self, ctx, new_player):
        print("function \'initiate_player\' called.")
        self.players.append(new_player)
        
        dm = new_player.dm_channel
        if dm == None:
            await new_player.create_dm()
            dm = new_player.dm_channel
        self.dm_channels[new_player] = dm
        self.scores[new_player] = 0
        
        await dm.send("Hello! Welcome to Spyfall. If you are chosen as the spy, you will be notified here.")
        await ctx.send(new_player.name + ' has joined the game.')
        
    async def assign_spy(self, ctx):
        self.spy = self.choose_random_player()
        await self.dm_channels[self.spy].send("shhhh, you're the spy...")
        
    async def assign_roles(self, ctx):
        # choose location
        index = rand(len(rolesMap)-1)
        location = rolesMap.keys()[index]
        available_roles = list(rolesMap[index])
        for player in self.players:
            if player is not self.spy:
                await dm_channels[player].send("The location is: " + location + ".")
                roleIndex = rand(len(available_roles)-1)
                role = available_roles[roleIndex]
                await self.dm_channels[player].send("Your role is: " + role+".")
                available_roles.remove(role)
        
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
                    if location not in self.rolesMap:
                        self.rolesMap[location] = [locations[index].strip()]
                    else:
                        self.rolesMap[location].append(locations[index].strip())
                    index+=1
                index+=1
    
    def start_timer(self, ctx, duration = 10): # duration in minutes
        print('in start_timer')
        self.bot.loop.create_task(self.start_timer_helper(ctx, duration))
    
    async def start_timer_helper(self, ctx, duration):
        print('in helper')
        time_left = duration
        while not self.bot.is_closed() and not self.pause_timer:
            # reminder every minute
            await ctx.send(str(time_left) + " minutes left!")
            await asyncio.sleep(10)
            time_left -= 1
            if time_left >= 0:
                return
    
    def _reset(self):
        self.players.clear()
        self.dm_channels = dict()
        self.scores = dict()
        self.wait_game_start_confirmation = False
        self.pause_timer = False
        self.spy = None
        
    def choose_random_player(self):
        index = random.randrange(len(self.players)-1)
        return self.players[index]
        

if __name__=="__main__":
    bot = commands.Bot(command_prefix='!')
    
    #get key from file
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    keyPath = 'key.txt'
    keyFile = open(os.path.join(__location__, keyPath), 'r')
    key = keyFile.read()
    keyFile.close()
    
    print(key)

    #bot.add_cog(Spyfall(bot))
    #bot.run(key)