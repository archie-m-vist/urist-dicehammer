import discord
from discord.ext import commands

class BadWagerStartException (RuntimeError):
   def __str__ (self):
      return "Wager is already running in this channel! Use `!wager join` to join in."

class WagerNotRunningException (RuntimeError):
   def __str__ (self):
      return "There is no wager running in this channel! Use `!wager start` to create one."

class NotPlayingException (RuntimeError):
   def __str__ (self):
      return "Player is not participating in the wager! Use `!wager join` to join in."

class NotEnoughPointsException (RuntimeError):
   def __init__ (self, bet, score):
      self.bet = bet
      self.score = score

   def __str__ (self):
      return "Cannot bet {} points; you only have {}.".format(self.bet,self.score)

class WagerTracker:
   def __init__ (self):
      self.scores = {}
      self.defaults = {}

   def score (self, channel, player = None):
      """Gets the current score of the given player in the given channel.

      If no player is provided, gives number of points in the pot."""
      if channel not in self.scores:
         return None
      else:
         if player not in self.scores[channel]:
            return None
         else:
            return self.scores[channel][player]

   def playing (self, channel, player = None):
      """Checks if the given player is playing the game in this channel.

      If player is None, returns True if the game is being played at all."""
      return channel in self.scores and player in self.scores[channel]

   def start (self, channel, default):
      """
         Starts a game in this channel.
      """
      if channel in self.defaults:
         raise BadWagerStartException()
      self.defaults[channel] = default
      self.scores[channel] = { None : 0 }

   def join (self, channel, player):
      if channel not in self.scores:
         raise WagerNotRunningException()
      self.scores[channel][player] = self.defaults[channel]

   def claim (self, channel, player):
      if channel not in self.scores:
         raise WagerNotRunningException()
      if player not in self.scores[channel]:
         raise NotPlayingException()
      self.scores[channel][player] += self.scores[channel][None]
      self.scores[channel][None] = 0

   def bet (self, channel, player, points):
      if channel not in self.scores:
         raise WagerNotRunningException()
      if player not in self.scores[channel]:
         raise NotPlayingException()
      if self.scores[channel][player] < points:
         raise NotEnoughPointsException(points, self.scores[channel][player])
      self.scores[channel][player] -= points
      self.scores[channel][None] += points

   def stop (self, channel):
      if channel in self.scores:
         self.defaults.pop(channel)
         score = self.scores.pop(channel)
         return score
      else:
         raise WagerNotRunningException()

class Performer:
   """Module with support for various games involving cards or points."""

   def __init__ (self, bot):
      self.bot = bot
      self.tracker = WagerTracker()

   @commands.group(pass_context = True)
   async def wager (self, ctx):
      """Run games that involve a points pool. Use !wager start to create a game, and !wager join to join one."""
      if ctx.invoked_subcommand is None:
         channel = ctx.message.channel
         player = ctx.message.author
         if not self.tracker.playing(channel):
            msg = "To start a game in this channel with `n` points per player, use `!wager start n`."
         else:
            if self.tracker.playing(channel, player):
               msg = "You are a player in this channel. Use `!wager bet` to bet points and `!wager claim` to claim the pot."
            else:
               msg = "A game is running in this channel. To join this channel's game, use `!wager join`."
         msg = "No wager subcommand given.\n{}".format(msg)
         await self.bot.say(msg)

   @wager.command(name = "start", pass_context = True)
   async def start (self, ctx, points = 10):
      channel = ctx.message.channel
      player = ctx.message.author
      msg = None
      try:
         self.tracker.start(channel, points)
      except Exception as e:
         msg = "Error: {}".format(str(e))
      if msg is None:
         try:
            self.tracker.join(channel,player)
         except Exception as e:
            msg = "Game started, but join error: {}".format(str(e))
         if msg is None:
            msg = "{} has started a game!".format(player.mention)
      await self.bot.say(msg)

   @wager.command(pass_context = True)
   async def join (self, ctx):
      channel = ctx.message.channel
      player = ctx.message.author
      msg = None
      try:
         self.tracker.join(channel,player)
      except Exception as e:
         msg = "Error: {}".format(str(e))
      if msg is None:
         msg = "{} has joined the game!".format(player.mention)
      await self.bot.say(msg)

   @wager.command(pass_context = True)
   async def bet (self, ctx, points = 1):
      channel = ctx.message.channel
      player = ctx.message.author
      msg = None
      try:
         self.tracker.bet(channel,player,points)
      except Exception as e:
         msg = "Error: {}".format(str(e))
      if msg is None:
         msg = "{} adds {} points to the pool!".format(player.mention,points)
      await self.bot.say(msg)

   @wager.command(pass_context = True)
   async def claim (self, ctx):
      channel = ctx.message.channel
      player = ctx.message.author
      msg = None
      # try to get pot from channel; check if game is running
      try:
         pot = self.tracker.score(channel)
      except Exception as e:
         msg = "Error: {}".format(str(e))
      # if pot was found, update player score
      if msg is None:
         # try to claim
         try:
            self.tracker.claim(channel,player)
         # handle errors
         except Exception as e:
            msg = "Error: {}".format(str(e))
         # if claim was successful, inform player
         if msg is None:
            msg = "{} has claimed the pot, worth {} points.".format(player.mention,pot)
      await self.bot.say(msg)

   @wager.command(pass_context = True)
   async def score (self, ctx):
      channel = ctx.message.channel
      player = ctx.message.author
      msg = None
      # get score
      try:
         score = self.tracker.score(channel,player)
      # handle errors
      except Exception as e:
         msg = "Error: {}".format(str(e))
      # if no error found, give result
      if msg is None:
         msg = "Current score for {} is {} points.".format(player.mention, score)
      await self.bot.say(msg)

   @wager.command(pass_context = True)
   async def stop (self, ctx):
      """Ends the game in this channel."""
      channel = ctx.message.channel
      msg = None
      try:
         scores = self.tracker.stop(channel)
      except Exception as e:
         msg = "Error: {}".format(str(e))
      if msg is None and scores is not None:
         msg = "Game ended! Scores are:"
         scores = sorted(scores.items(), key=lambda x: -1*x[1])
         for score in scores:
            if score[0] is None:
               mention = "Pool"
            else:
               mention = score[0].mention
            msg += "**\n{}**: {} points".format(mention, score[1])
      await self.bot.say(msg)

def setup (bot):
   bot.add_cog(Performer(bot))