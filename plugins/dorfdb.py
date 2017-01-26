from secret import dbuser, dbpass, dbname
# database setup
import pymysql as mariadb
dbase = mariadb.connect(user=dbuser, password=dbpass, database=dbname)
cursor = dbase.cursor()

# disco setup
from disco.bot import Bot, Plugin

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

class DorfDB(Plugin):
   @Plugin.command('toggle', '<field:str> [value:str]')
   def on_toggle_command(self, event, field, value="flip"):
      # process arguments and get server ID
      field = field.lower();
      value = value.lower();
      sid = event.msg.guild.id;
      print(sid)
      # make sure field is a trusted value
      if field not in toggle_fields:
         event.msg.reply("**Error:** Unknown field {}.".format(field))
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
         event.msg.reply("**Error:** Invalid argument {} to !toggle.".format(value))
         return
      # insert data into table
      command = "INSERT INTO config (server,{}) VALUES (%s, %s) ON DUPLICATE KEY UPDATE {}=%s;".format(field,field)
      cursor.execute(command, (sid, value, value))
      dbase.commit()

   @Plugin.command('check', '<field:str>')
   def on_check_command(self, event, field):
      # process arguments and get server ID
      field = field.lower();
      sid = event.msg.guild.id;
      # fetch and return result
      result = check_field(field,sid,True)
      if result == None:
         event.msg.reply("**Error:** Unknown field {}.".format(field))
      else:
         event.msg.reply("Value of {}: {}".format(field,result))