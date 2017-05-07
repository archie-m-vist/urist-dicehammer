import secret
from discord.ext import commands
# database setup
import pymysql as mariadb
dbase = mariadb.connect(user=secret.dbuser, password=secret.dbpass, database=secret.dbname)
cursor = dbase.cursor()

def get_group (gname, sid, lowered=False):
   if not lowered:
      gname = gname.lower()
   command = "SELECT uid FROM groups WHERE sid=%s AND name=%s"
   cursor.execute(command, (sid,gname))
   return [x[0] for x in cursor.fetchall()]

def join_or_create_group (gname, uid, sid, lowered=False):
   if not lowered:
      gname = gname.lower()
   command = "INSERT INTO groups (sid,name,uid) VALUES(%s,%s,%s)"
   try:
      cursor.execute(command, (sid,gname,uid))
      dbase.commit()
   except mariadb.err.IntegrityError:
      return False
   return True

def leave_group (gname, uid, sid, lowered=False):
   if not lowered:
      gname = gname.lower()
   command = "DELETE FROM groups WHERE uid=%s AND sid=%s AND name=%s"
   cursor.execute(command, (uid,sid,gname))
   dbase.commit()
   return True

def list_groups (sid, uid = None):
   if uid is None:
      command = "SELECT distinct name FROM groups WHERE sid=%s"
      cursor.execute(command, (sid,))
   else:
      command = "SELECT distinct name FROM groups WHERE sid=%s AND uid=%s"
      cursor.execute(command, (sid,uid))
      
   groups = [x[0] for x in cursor.fetchall()]
   return groups


class Manager:
   def __init__ (self, bot):
      self.bot = bot
      self.owner = None

   @commands.command(pass_context = True)
   async def join(self, ctx, *groups):
      """
         Join or create one or more groups.

         Group names can contain any Latin-1 character except for commas, and can be up to 30 characters in length.
         If too long, names will automatically be truncated.

         Arguments:
          - groups: Names of the group to join or create, separated by commas.
      """
      groups = " ".join(groups)
      groups = groups.split(",")
      uid = ctx.message.author.mention
      sid = ctx.message.server.id
      for group in groups:
         group = group.strip()
         if join_or_create_group(group, uid, sid):
            await self.bot.say("{} has joined group {}.".format(uid, group))
         else:
            await self.bot.say("{} is already a member of group {}.".format(uid, group))

   @commands.command(pass_context = True)
   async def leave(self,ctx,*groups):
      """
         Leave one or more groups.

         When the last member leaves, the group will no longer exist, and can be reformed using !join.

         Arguments:
          - groups: Names of the groups to leave, separated by commas.
      """
      groups = " ".join(groups)
      groups = groups.split(",")
      uid = ctx.message.author.mention
      sid = ctx.message.server.id
      for group in groups:
         group = group.strip()
         if leave_group(group, uid, sid):
            await self.bot.say("{} has left group {}.".format(uid, group))
         else:
            await self.bot.say("{} is not a member of group {}.".format(uid, group))

   @commands.command(pass_context = True)
   async def groups(self, ctx, user = None):
      """
         Lists groups available on this server.

         Arguments:
          - user [optional]: If provided, output will be the groups the given user is a member of.
      """
      sid = ctx.message.server.id
      if user is None:
         output = "Available Groups:\n"
      else:
         output = str(user) + "'s Groups:\n"

      # append list of groups
      groups = list_groups(sid, user)
      if len(groups) > 0:
         for group in groups:
            output += str(group) + ", "
         output = output[:-2]
      else:
         output = "No groups active on this server."
      await self.bot.say(output)

   @commands.command(pass_context = True)
   async def page(self, ctx, *group):
      """
         Creates a message which @mentions every member of the given group.

         Arguments:
          - group: Group to page.
      """
      sid = ctx.message.server.id
      group = " ".join(group)
      group.strip()
      members = get_group(group,sid)
      if len(members) > 0:
         output = str(members)[1:-1].replace("'","")
      else:
         output = "Group {} not found.".format(group)
      await self.bot.say(output)

def setup (bot):
=======
import secret
from discord.ext import commands
# database setup
import pymysql as mariadb
from plugins.bookkeeper import cursor, dbase

def get_group (gname, sid, lowered=False):
   if not lowered:
      gname = gname.lower()
   command = "SELECT uid FROM groups WHERE sid=%s AND name=%s"
   cursor.execute(command, (sid,gname))
   return [x[0] for x in cursor.fetchall()]

def join_or_create_group (gname, uid, sid, lowered=False):
   if not lowered:
      gname = gname.lower()
   command = "INSERT INTO groups (sid,name,uid) VALUES(%s,%s,%s)"
   try:
      cursor.execute(command, (sid,gname,uid))
      dbase.commit()
   except mariadb.err.IntegrityError:
      return False
   return True

def leave_group (gname, uid, sid, lowered=False):
   if not lowered:
      gname = gname.lower()
   command = "DELETE FROM groups WHERE uid=%s AND sid=%s AND name=%s"
   cursor.execute(command, (uid,sid,gname))
   dbase.commit()
   return True

def list_groups (sid, uid = None):
   if uid is None:
      command = "SELECT distinct name FROM groups WHERE sid=%s"
      cursor.execute(command, (sid,))
   else:
      command = "SELECT distinct name FROM groups WHERE sid=%s AND uid=%s"
      cursor.execute(command, (sid,uid))
      
   groups = [x[0] for x in cursor.fetchall()]
   return groups


class Manager:
   def __init__ (self, bot):
      self.bot = bot
      self.owner = None

   @commands.command(pass_context = True)
   async def join(self, ctx, *groups):
      """
         Join or create one or more groups.

         Group names can contain any Latin-1 character except for commas, and can be up to 30 characters in length.
         If too long, names will automatically be truncated.

         Arguments:
          - groups: Names of the group to join or create, separated by commas.
      """
      groups = " ".join(groups)
      groups = groups.split(",")
      uid = ctx.message.author.mention
      sid = ctx.message.server.id
      for group in groups:
         if join_or_create_group(group, uid, sid):
            await self.bot.say("{} has joined group {}.".format(uid, group))
         else:
            await self.bot.say("{} is already a member of group {}.".format(uid, group))

   @commands.command(pass_context = True)
   async def leave(self,ctx,*groups):
      """
         Leave one or more groups.

         When the last member leaves, the group will no longer exist, and can be reformed using !join.

         Arguments:
          - groups: Names of the groups to leave, separated by commas.
      """
      groups = " ".join(groups)
      groups = groups.split(",")
      uid = ctx.message.author.mention
      sid = ctx.message.server.id
      for group in groups:
         if leave_group(group, uid, sid):
            await self.bot.say("{} has left group {}.".format(uid, group))
         else:
            await self.bot.say("{} is not a member of group {}.".format(uid, group))

   @commands.command(pass_context = True)
   async def groups(self, ctx, user = None):
      """
         Lists groups available on this server.

         Arguments:
          - user [optional]: If provided, output will be the groups the given user is a member of.
      """
      sid = ctx.message.server.id
      if user is None:
         output = "Available Groups:\n"
      else:
         output = str(user) + "'s Groups:\n"

      # append list of groups
      groups = list_groups(sid, user)
      if len(groups) > 0:
         for group in groups:
            output += str(group) + ", "
         output = output[:-2]
      else:
         output = "No groups active on this server."
      await self.bot.say(output)

   @commands.command(pass_context = True)
   async def page(self, ctx, *group):
      """
         Creates a message which @mentions every member of the given group.

         Arguments:
          - group: Group to page.
      """
      sid = ctx.message.server.id
      group = " ".join(group)
      members = get_group(group,sid)
      if len(members) > 0:
         output = str(members)[1:-1].replace("'","")
      else:
         output = "Group {} not found.".format(group)
      await self.bot.say(output)

def setup (bot):
    bot.add_cog(Manager(bot))