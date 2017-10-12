import discord
from discord.ext import commands

class Jeweler:
   """Plugin for managing pins and reactions. !pin command requires Manage Roles permission in Discord."""

   def __init__ (self, bot):
      self.bot = bot

   @commands.command(pass_context = True)
   async def pin (self, ctx):
      print("Test!")
      try:
         await self.bot.pin_message(ctx.message)
      except:
         await self.bot.say("Cannot pin message; check permissions.")


def setup (bot):
   bot.add_cog(Jeweler(bot))