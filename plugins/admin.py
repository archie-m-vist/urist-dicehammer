import discord
from discord.ext import commands

class Admin (commands.Cog):
   def __init__ (self, bot):
      self.bot = bot
      self.owner = None

   @commands.command(pass_context=True,hidden=True)
   async def load (self,ctx,module):
      """Loads a bot module."""
      module = "plugins."+module
      if self.owner == None:
         info = await(self.bot.application_info())
         self.owner = info.owner
      if self.owner == ctx.author:
         try:
            self.bot.load_extension(module)
         except Exception as e:
            await(ctx.send("Error loading module {}:".format(module)))
            await(ctx.send('{}: {}'.format(type(e).__name__, e)))
         else:
            await(ctx.send("Loaded module {}".format(module)))
      else:
         ctx.send("that's a grudgin', {}".format(ctx.author.mention))
         f = open("urist-grudges.txt", "a")
         f.write("GRUDGED [!load]: {ctx.author.name}#{ctx.author.discriminator}")
         f.close()
         print("BOOK OF GRUDGES:",ctx.author,"load")

   @commands.command(pass_context=True,hidden=True)
   async def unload (self,ctx,module):
      """Reloads a bot module."""
      module = "plugins."+module
      if self.owner == None:
         info = await(self.bot.application_info())
         self.owner = info.owner
      if self.owner == ctx.author:
         try:
            self.bot.unload_extension(module)
         except Exception as e:
            await(ctx.send("Error unloading module {}:".format(module)))
            await(ctx.send('{}: {}'.format(type(e).__name__, e)))
         else:
            await(ctx.send("Unloaded module {}".format(module)))
      else:
         ctx.send("that's a grudgin', {}".format(ctx.author.mention))
         f = open("urist-grudges.txt", "a")
         f.write("GRUDGED [!load]: {ctx.author.name}#{ctx.author.discriminator}")
         f.close()
         print("BOOK OF GRUDGES:",ctx.author,"unload")

   @commands.command(pass_context=True,hidden=True)
   async def reload (self,ctx,module):
      """Reloads a bot module."""
      module = "plugins."+module
      if self.owner == None:
         info = await(self.bot.application_info())
         self.owner = info.owner
      if self.owner == ctx.author:
         try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
         except Exception as e:
            await(ctx.send("Error reloading module {}:".format(module)))
            await(ctx.send('{}: {}'.format(type(e).__name__, e)))
         else:
            await(ctx.send("Reloaded module {}".format(module)))
      else:
         await ctx.send("that's a grudgin', {}".format(ctx.author.mention))
         print("BOOK OF GRUDGES:",ctx.author,"reload")

   @commands.command(pass_context=True,hidden=True)
   async def stop (self,ctx):
      """Remotely shuts down bot instances."""
      if self.owner == None:
         info = await(self.bot.application_info())
         self.owner = info.owner
      if self.owner == ctx.author:
         await(ctx.send("Shutting down."))
         raise SystemExit()
      else:
         await ctx.send("that's a grudgin', {}".format(ctx.author.mention))
         print("BOOK OF GRUDGES:",ctx.author,"stop")

def setup (bot):
    bot.add_cog(Admin(bot))