import discord
from discord.ext import commands

class Jeweler (commands.Cog):
   """Plugin for managing pins and reactions. !pin command requires Manage Roles permission in Discord."""

   def __init__ (self, bot):
      self.bot = bot

   @commands.command()
   async def pin (self, ctx):
      """Pins a message if Urist has appropriate permissions."""
      try:
         await ctx.message.pin()
      except:
         await ctx.send("Cannot pin message; check permissions.")

def setup (bot):
   bot.add_cog(Jeweler(bot))