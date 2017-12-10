from discord.ext import commands
class Manager:
   """
      Plugin for managing Discord roles. Requires "Manage Roles" permission in Discord, and must be above any roles it wishes to add.
   """

   def __init__ (self,bot):
      self.bot = bot

   @commands.command(pass_context = True)
   async def join (self, ctx, name):
      """
         Joins a role which is manageable by the bot.
      """
      roles = ctx.message.server.roles
      joinrole = None
      for role in roles:
         if role.name.lower() == name.lower():
            joinrole = role
            break
      if joinrole is None:
         await(self.bot.say("Role {} not found. Check with your server admin. (Names are *not* case-sensitive.)"))
         return
      await(self.bot.add_roles(ctx.message.author, joinrole))
      await(self.bot.say("{} has joined role {}.".format(ctx.message.author.mention, joinrole.name)))

def setup (bot):
   bot.add_cog(Manager(bot))