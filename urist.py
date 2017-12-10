import discord
from discord.ext import commands
from secret import token, prefix

description = '''Urist Dicehammer, providing highly-featured dice and Dwarf Fortress memes since 2016.'''.format(prefix,prefix)

bot = commands.Bot(command_prefix=prefix, description=description)

extensions = ['plugins.admin','plugins.dicehammer','plugins.jeweler', 'plugins.manager']

@bot.event
async def on_ready():
   print("Connected to Discord.")
   print(bot.user.name)
   print(bot.user.id)
   print("-- loading extensions --")
   for extension in extensions:
      try:
         bot.load_extension(extension)
         print("Successfully loaded extension '{}'".format(extension))
      except Exception as e:
         print("Error loading extension '{}'".format(extension))
         print("{}: {}".format(type(e).__name__, e))
   print("-- beginning log --")

@bot.command()
async def admin():
   """Gives administrator contact information."""
   info = await(bot.application_info())
   mention = info.owner.mention
   message = "My administrator is the glorious {}. Fear him, for he is mighty.".format(mention)
   await(bot.say(message))

def main ():
   while True:
      try:
         bot.run(token)
      except KeyboardInterrupt:
         raise
      except Exception as e:
         print(e)
         continue

if __name__ == '__main__':
   main()