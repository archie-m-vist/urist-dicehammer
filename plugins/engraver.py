from imgurpython import ImgurClient
from secret import imgur_client_id, imgur_client_secret
from discord.ext import commands

from plugins.dorfdb import cursor

def get_album (sid, name):
   command = "SELECT aid FROM albums WHERE server=%s AND name=%s;"


"""General image library."""
class Engraver:
   def __init__(self, bot):
      self.bot = bot
      self.client = ImgurClient(imgur_client_id,imgur_client_secret)

   @commands.command()
   async def imgur (self, *topic):
      """
         Performs an Imgur search on the given topic.
         
         Arguments:
          - topic: Topic to search for.
      """
      topic = " ".join(topic)
      search = self.client.gallery_search(topic)
      if len(search) > 0:
         item = search.pop()
         message = item.link
      else:
         message = "**Error:** no Imgur search results for {}.".format(topic)
      await(self.bot.say(message))

def setup (bot):
    bot.add_cog(Engraver(bot))