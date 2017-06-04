from discord.ext import commands
class Noble:
   """
      Plugin for managing Discord roles. Requires "Manage Roles" permission in Discord, and must be above any roles it wishes to add.
   """

   def __init__ (self,bot):
      self.bot = bot

   @commands.command(pass_context = True)
   async def ff (self, ctx):
      roles = ctx.message.server.roles
      ffRole = None
      for role in roles:
         if role.name == "FF":
            ffRole = role
            break
      if ffRole is None:
         await(self.bot.say("Fantasy football is not enabled on this server."))
         return
      await(self.bot.add_roles(ctx.message.author, ffRole))
      await(self.bot.say("{} has joined fantasy football.".format(ctx.message.author.mention)))

def setup (bot):
   bot.add_cog(Noble(bot))