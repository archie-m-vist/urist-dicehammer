import secret
from discord.ext import commands
# database setup
import pymysql as mariadb
dbase = mariadb.connect(user=secret.dbuser, password=secret.dbpass, database=secret.dbname)
cursor = dbase.cursor()

toggle_fields = ["memes", "verbose"]
config_fields = []

def check_field(field, sid, lowered=False):
   # make sure field is a trusted value
   if not lowered:
      field = field.lower();
   if field not in toggle_fields and field not in config_fields:
      return None
   # select result from table
   command = "SELECT {} FROM config WHERE server=%s".format(field)
   cursor.execute(command, (sid,))
   # if not found, add a new row and repeat, getting default value
   if cursor.rowcount == 0:
      cursor.execute("INSERT INTO config (server) VALUES (%s)", (sid,))
      cursor.execute(command, (sid,))
      dbase.commit()
   result = cursor.fetchone();
   return result[0]

"""Configuration commands, including database access."""
class Bookkeeper:
   def __init__ (self,bot):
      self.bot = bot

   @commands.command(pass_context = True)
   async def toggle(self, ctx, field, value="flip"):
      """
         Toggle the value of a boolean field.

         Arguments:
          - field: Field to be toggled.
          - value: Can be true, on, false, off, or flip.
                   true and on are equivalent, as are false and off.
                   flip is the default, and will set the value to the opposite of its current value.
      """
      # process arguments
      field = field.lower();
      value = value.lower();
      # discord context information
      sid = ctx.message.server.id
      if sid == None:
         await(self.bot.say("Cannot configure bot by PM."))
         return
      # make sure field is a trusted value
      if field not in toggle_fields:
         await(self.bot.say("**Error:** Unknown field {}.".format(field)))
         return
      # make VALUE an sql TRUE/FALSE
      onstrings = ["on", "true"]
      offstrings = ["off", "false"]
      if value in onstrings:
         value = 1
      elif value in offstrings:
         field = 0
      elif value == "flip":
         command = "SELECT {} FROM config WHERE server=%s;".format(field)
         cursor.execute(command, (sid,))
         if cursor.rowcount == 0: # if server has no record, toggle on by default
            value = 1
         else:
            value = 0 if cursor.fetchone()[0] else 1
      else:
         await(self.bot.say("**Error:** Invalid argument {} to !toggle.".format(value)))
         return
      # insert data into table
      command = "INSERT INTO config (server,{}) VALUES (%s, %s) ON DUPLICATE KEY UPDATE {}=%s;".format(field,field)
      cursor.execute(command, (sid, value, value))
      dbase.commit()

   @commands.command(pass_context = True)
   async def check(self, ctx, field):
      """
         Check the value of a configuration field.
         
         Arguments:
          - field: field to query.
      """
      # process arguments and get server ID
      field = field.lower();
      sid = ctx.message.server.id
      if sid == None:
         await(self.bot.say("Cannot configure bot by PM."))
         return
      # fetch and return result
      result = check_field(field,sid,True)
      if result == None:
         message = "**Error:** Unknown field {}.".format(field)
      else:
         message = "Value of {}: {}".format(field,result)
      await(self.bot.say(message))

def setup (bot):
   bot.add_cog(Bookkeeper(bot))