import discord
from discord.ext import commands

class Admin:
   def __init__ (self, bot):
      self.bot = bot
      self.owner = None

   @commands.command(pass_context=True,hidden=True)
   async def load (self,ctx,module):
      module = "plugins."+module
      if self.owner == None:
         info = await(self.bot.application_info())
         self.owner = info.owner
      if self.owner == ctx.message.author:
         try:
            self.bot.load_extension(module)
         except Exception as e:
            await(self.bot.say("Error loading module {}:".format(module)))
            await(self.bot.say('{}: {}'.format(type(e).__name__, e)))
         else:
            await(self.bot.say("Loaded module {}".format(module)))

   @commands.command(pass_context=True,hidden=True)
   async def reload (self,ctx,module):
      """Reloads a bot module."""
      module = "plugins."+module
      if self.owner == None:
         info = await(self.bot.application_info())
         self.owner = info.owner
      if self.owner == ctx.message.author:
         try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
         except Exception as e:
            await(self.bot.say("Error reloading module {}:".format(module)))
            await(self.bot.say('{}: {}'.format(type(e).__name__, e)))
         else:
            await(self.bot.say("Reloaded module {}".format(module)))

def setup (bot):
    bot.add_cog(Admin(bot))