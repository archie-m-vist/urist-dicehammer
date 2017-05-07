from imgurpython import ImgurClient
from discord.ext import commands
import random

from secret import imgur_client_id, imgur_client_secret
from plugins.dorfdb import cursor

def get_album_id (sid, name):
   """
      Looks up a 
   """
   command = "SELECT aid FROM albums WHERE server=%s AND name=%s;"
   cursor.execute(command, (sid,name))
   # if not found, return None
   if cursor.rowcount == 0:
      return None
   result = cursor.fetchone();
   return result[0]

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
      if self.client.credits["ClientRemaining"] < 10:
         message = "**Error:** Imgur API daily limit exceeded."
      else:
         topic = " ".join(topic)
         search = self.client.gallery_search(topic)
         if len(search) > 0:
            item = search.pop()
            message = item.link
         else:
            message = "**Error:** no Imgur search results for {}.".format(topic)
      await(self.bot.say(message))

   @commands.group(name="album", pass_context=True)
   async def album (self, ctx, name):
      """
         Pulls a random image from a known album.

         Arguments: 
          - name: Name of album to pull from.
      """
      if ctx.invoked_subcommand is None:
         if self.client.credits["ClientRemaining"] < 10:
            message = "**Error:** Imgur API daily limit exceeded."
         else:
            sid = ctx.message.server.id
            if sid == None:
               message = "**Error:** Cannot use albums by PM."
            aid = get_album_id(sid,name)
            if aid == None:
               message = "**Error:** No known album {}.".format(name)
            else:
               album = self.client.get_album_images(aid)
               if album == None:
                  message = "**Error:** invalid album ID {} for name {}. Contact the administrator.".format(aid,name)
               message = item.link
         await(self.bot.say(message))

   @album.command(pass_context=True)
   async def create (self, ctx, name, image=None):
      """
         Creates an album, containing the given image.

         If the album already exists, 

         Arguments:
          - name:    Name of album to be created to.
          - image:   Link to the image to be added.
                     If this is omitted, will check message for attached file.
      """
      sid = ctx.message.server.id
      if image == None:
         if len(ctx.message.attachments) > 0:
            image = ctx.message.attachments[0].link
         else:
            image = "**Error:** No image provided."
      await(self.bot.say(image))


def setup (bot):
    bot.add_cog(Engraver(bot))