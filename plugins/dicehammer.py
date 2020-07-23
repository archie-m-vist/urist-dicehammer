if __name__ == '__main__':
   import sys

import random, re, math
from discord.ext import commands
from util.flagparse import parse_flags
from util.fishutil import is_integer
from data.randList import randomFromList, lists
from random_words import RandomWords

diceMode = {}

roll_regex = re.compile("(\d*#)?(\d*)d(\d+)((\+|-)(\d+))?")
rw = RandomWords()

class Dicehammer (commands.Cog):
   """
      Plugin for all dice and random-generation utilities.
   """
   def __init__ (self, bot):
      self.bot = bot

   @commands.command(pass_context = True)
   async def coinflip(self,ctx,number=1):
      """
         Flips a number of coins.
         
         Arguments:
          - number (optional): Number of coins to flip. If not provided, defaults to 1.
      """
      heads, tails = run_coinflip(number)
      user = ctx.author.mention
      if number < 1:
         message = "{} attempted to flip negative coins, and only got reminded of their debts.".format(user)
      elif number > 1:
         message = "{} flipped {} coins, and got **{} heads** and **{} tails**.".format(user, number, heads, tails)
      else:
         result = 'heads' if heads > 0 else 'tails'
         message = "{} flipped a coin and got **{}**.".format(user, result)
      await(ctx.send(message))

   @commands.group(pass_context = True)
   async def choose(self,ctx,*options):
      """
         Chooses a single element from a list.

         Arguments:
          - options: This can either be the name of a preconstructed list, or a list of items separated by commas. Items may contain any character other than a comma.
      """
      if ctx.invoked_subcommand == None:
         user = ctx.author.mention
         options = " ".join(options)
         options = options.split(",")
         if len(options) == 0:
            message = "{} gives nothing and gets nothing in return.".format(user)
         elif len(options) == 1:
            if options[0] == "lists":
               message = get_lists()
            else:
               result = randomFromList(options[0])
               if result is not None:
                  message = "{} gets: **{}**".format(user,result)
               else:
                  message = "{} unsurprisingly gets: **{}**".format(user,options[0])
         else:
            result = random.choice(options)
            message = "{} gets: **{}**".format(user,result)
         await(ctx.send(message))

   @choose.command(name='lists')
   async def _lists(self):
      """
         Lists all available preconstructed lists.
      """
      message = get_lists()
      await(ctx.send(message))

   @commands.command(pass_context = True)
   async def shuffle(self,ctx,*options):
      """
         Randomises the ordering of the elements of a list.

         Arguments:
          - options: A list of items separated by commas. (shuffle does not accept preconstructed list names.)
      """
      user = ctx.author.mention
      options = " ".join(options)
      options = options.split(",")
      random.shuffle(options)
      result = ""
      while (len(options) > 0):
         result += options.pop();
         if (len(options) > 0):
            result += ", "
      message = "{} gets: **{}**".format(user,result)
      await(ctx.send(message))

   @commands.group(pass_context = True)
   async def roll(self,ctx,dstring,*flags):
      """
         Rolls dice.

         Arguments:
          - dstring: A dice string. dN to roll an N-sided die, MdN to roll M N-sided dice, R#MdN to roll M N-sided dice R times. Supports + afterwards for final modifiers.
          - flags: A variety of flags. See subcommands for specific flag usage.
      """
      user = ctx.author.mention
      matched = roll_regex.match(dstring)
      try:
         print(diceMode[ctx.message.flags])
      except:
         pass
      if ctx.message.channel in diceMode:
         mode = diceMode[ctx.message.channel][0]
         count = diceMode[ctx.message.channel][1]
         if count == 0 and len(flags) == 0:
            flags = mode
         elif len(flags) == 1+count and flags[0] == "!":
            mode = " ".join(mode)
            flags = mode.format(*flags[1:]).split(" ")
      print("Flags: ",flags)
      if matched == None:
         message = "{} supplied invalid dice string: {}".format(user,dstring)
      else:
         rolls = int(matched.group(1)[0:-1]) if matched.group(1) is not None else 1
         count = int(matched.group(2)) if matched.group(2) is not '' else 1
         sides = int(matched.group(3))
         modifier = int(matched.group(4)) if matched.group(4) is not None else 0

         if rolls == 0 or count == 0 or sides == 0:
            message = "{} rolled 0, and shouldn't have expected anything else.".format(user)
         else:
            if rolls == 1:
               total, results = roll(count,sides,modifier,flags)
            else:
               total, results = multiroll(rolls,count,sides,modifier,flags)
            if isinstance(results,str): # normal case
               message ="{} rolled {}: **{}** {}".format(user,dstring,total,results)
            else: # verbose flag for long messages
               message = "{} rolled {}: **{}**".format(user,dstring,total)
               while len(results) > 0:
                  await(ctx.send(message))
                  message = results.pop()
      await(ctx.send(message))

   # placeholders for documentation purposes
   @roll.command(name="drop")
   async def _drop (self):
      """Automatically drop highest/lowest rolls.

      Additional Options:
       - lowest n: Drops the lowest n (default 1) dice from each MdN roll.
       - highest n: Drops the highest n (default 1) dice from each MdN roll.
      """
      return

   @roll.command(name="explode")
   async def _explode (self):
      """Toggles exploding dice (i.e., extra roll on high or low result).

      Additional Options:
       - up n: Explode up, adding the values from the total, upon rolling between n and the number of sides. Default for n is 1, and exploding up is the default behaviour.
       - down n: Explode down, subtracting the values from the total, upon rolling between 1 and n. Default for n is 1.
       - max n: Caps the number of consecutive explosions per die (default 1)."""
      return

   @roll.command(name="degrees")
   async def _degrees (self):
      """Calculates degrees of success (a la Dark Heresy) against a given skill value. Requires an integer skill value as an argument.

      Additional Options:
       - zeroes [on/off]: Sets whether to count a "regular success" as +0 or +1, and a "regular failure" as -0 or -1. Default is to use zeroes.
      """

   @roll.command(name="verbose")
   async def _verbose (self):
      """Toggles verbose output for very large rolls."""
      return

   @roll.command(name="successes")
   async def _successes (self):
      """Calculates successes for use in a dice pool system. Modifiers (+/- in dice string) will increase number of successes, not dice value.

      Additional Options:
       - threshold n: Lowest value that counts as a success. Default is 70% of the number of sides per die, rounded down.
       - botch n: Highest value that counts as a botch. Default is 1. 0 or off disables.
       - double n: Value for critical successes, counting double. Default is the number of sides per die. 0 or off disables."""
      return

   @roll.command(name="sets")
   async def _sets (self):
      """Calculates sets for use in a dice sets system.

      Additional Options:
       - expert n [shorthand: e n]: Adds a dice of value n to the relevant rolled set."""

   @commands.command(pass_context = True)
   async def word (self, ctx):
      """Generates a random word."""
      word = rw.random_word()
      message = "{} got '{}'.".format(ctx.author.mention, word)
      await(ctx.send(message))

   @commands.group(pass_context = True)
   async def mode (self, ctx, *flags):
      """
         Sets default dice flags, to be used on dice without any special settings in this channel.

         Dice mode is volatile, and will not be preserved if the bot restarts; we recommend
         setting the dice mode before a given game to be sure.
      """
      if len(flags) == 0:
         if ctx.message.channel in diceMode:
            current = diceMode[ctx.message.channel][0]
            msg = "Channel default dice mode is currently: **{}**.".format(" ".join(current))
         else:
            msg = "No dice mode set for this channel."
      elif len(flags) == 1 and flags[0] == "clear":
         diceMode.pop(ctx.message.channel,None)
         msg = "Channel default dice mode cleared."
      else:
         diceMode[ctx.message.channel] = [flags, flags.count("{}")]
         msg = "Channel default dice mode set to: **{}**.".format(" ".join(flags))
      await(ctx.send(msg))

   @mode.command(pass_context=True,name="clear")
   async def _clear (self, ctx):
      """
         Clears the dice mode for this channel.
      """
      return



# flips a number of coins, returning the number of heads and the number of tails
def run_coinflip (number):
   heads = 0
   for i in range(number):
      if random.randint(0,1) == 0:
         heads += 1
   return heads, number-heads

# breaks a string representation of a list up by length
def split_to_size (string, length, delimiter = ", "):
   string = str(string) # sanity test
   output = []
   while ( len(string) > length ):
      i = length
      while ( string[i] != delimiter[0] ):
         i -= 1
      output.append(string[0:i])
      string = string[i+len(delimiter):] # removes ", "
   output.append(string)
   return output

def check_flags (flags, count, sides, modifier):
   if "explode" in flags:
      if flags["explode"][0] < 0 or flags["explode"][0] > sides:
         flags["explode"][0] = flags["explode"][0] % sides
      if flags["explode"][0] == 0:
         flags["explode"][0] = sides
      if sides == 1 and flags["explode"][2] == -1:
         flags["errors"].append("Infinite single-sided dice explosion.")
   if "drop" in flags:
      if flags["drop"][0] > count:
         flags["errors"].append("Dropping more dice than are rolled.")
   if "successes" in flags:
         if flags["successes"][0] is None:
            flags["successes"][0] = math.ceil(0.7 * sides)
         if flags["successes"][1] is None:
            flags["successes"][1] = sides
         flags["successes"].append(modifier)
   return flags

def process_results (results, flags):
   """
   Processes results from list according to the rules in flags.
   """
   if len(str(results)) > 1500:
      if "verbose" not in flags:
         results = "[results trimmed for length]"
      else:
         results = split_to_size(results,1800)
   else:
      results = str(results)
   return results

# returns a list of extra rolls
def run_explode (roll, sides, value):
   output = []
   # break flag value
   limit = value[0]
   direction = value[1]
   maximum = value[2]
   # explode downwards
   if direction == -1:
      while roll <= limit and maximum > 0:
         roll = random.randint(1,sides)
         output.append(-1*(sides-roll+1))
         maximum -= 1
   # explode upwards
   elif direction == 1:
      while roll >= limit and maximum > 0:
         roll = random.randint(1,sides)
         output.append(roll)
         maximum -= 1
   return output

def run_drop (total, results, value):
   # break flag value
   num_dropped = value[0]
   highest = value[1] == 'h'
   # sort results
   temp = sorted(results)
   removed = ["Dropped"]
   # while there are still results to remove
   for i in range(num_dropped):
      # remove highest or lowest value from sorted list
      if highest:
         dropped = temp.pop()
      else:
         dropped = temp.pop(0)
      # subtract removed value from total, remove from results
      total -= dropped
      results.remove(dropped)
      removed.append(dropped)
   # add marked list of removed rolls to results
   results.append(removed)
   return total, results

def run_degrees (total, results, value):
   total = 0
   skill = value[0]
   zeroes = value[1]
   for index in range(len(results)):
      if is_integer(results[index]):
         diff = (skill-results[index])/10
         t = "+" if diff >= 0 else "-"
         degrees = int(diff) if zeroes is True else int(diff+math.copysign(1,diff))
         total += degrees
         results[index] = "{} ({}{})".format(results[index],t,abs(degrees))
   return total, results

def roll_parsed (count,sides,modifier,flags):
   """
   Rolls dice with preprocessed flags.

   Parameters:
      count - number of dice to roll
      sides - number of sides on dice
      modifier - number being added/subtracted from tota
      flags - dictionary returned from parse_flags
   """
   results = []
   i = 0
   mult = 1
   while i < count:
      roll = random.randint(1,sides)
      results.append(roll)
      if "explode" in flags:
         results.extend(run_explode(roll, sides, flags["explode"]))
      i += 1

   total = sum([x for x in results if is_integer(x)]) + modifier
   if "drop" in flags:
      total, results = run_drop(total, results, flags["drop"])
   if "degrees" in flags:
      total, results = run_degrees(total, results, flags["degrees"])
   if "successes" in flags:
      total, results = run_successes(total, results, flags["successes"])
   if "sets" in flags:
      total, results = run_sets(total, results, flags["sets"])
   return total, results

def run_successes (total, results, value):
   total = value[3]
   total_botch = 0
   # unpack value
   threshold = value[0]
   double = value[1]
   botch = value[2]
   for index in range(len(results)):
      success = 0
      if is_integer(results[index]):
         if double != 0 and results[index] >= double:
            success = 2
         elif results[index] >= threshold:
            success = 1
         if botch != 0 and results[index] <= botch:
            total_botch += 1
         total += success
         results[index] = "{} ({})".format(results[index],success)
   if total == 0 and total_botch > 0:
      total = "Botch {}".format(total_botch)
   return total, results

def run_sets (total, results, value):
   temp = set([])
   buckets = {}
   # expert die, if given
   if value[0] != -1:
      temp.add(value[0])
   # print results
   for result in results:
      if result not in buckets:
         if result not in temp:
            temp.add(result)
         else:
            buckets[result] = 2
      else:
         buckets[result] += 1
   keys = [x for x in buckets.keys()]
   keys.sort()
   keys.reverse()
   sets = ["{}W{}H".format(buckets[key], key) for key in keys]
   singles = [x for x in temp if x not in buckets]
   return sets, "Singles: {}".format(" ".join([str(x) for x in sorted(singles)]))

def roll (count, sides, modifier, flags):
   """
   Rolls dice directly.

   Parameters:
      count - number of dice to roll
      sides - number of sides on dice
      modifier - number being added/subtracted from tota
      flags - list of special flags such as ``explode`` or ``drop`` as a list of strings
   """
   return multiroll(1,count,sides,modifier,flags)

def multiroll (rolls, count, sides, modifier, flags):
   """
   Rolls dice directly.

   Parameters:
      rolls - number of times to roll
      count - number of dice to roll
      sides - number of sides on dice
      modifier - number being added/subtracted from tota
      flags - list of special flags such as ``explode`` or ``drop`` as a list of strings
   """

   # parse flags from input
   try:
      flags = parse_flags([x for x in flags])
   except Exception as e:
      print(e)
      return "Exception!", "Critical error during flag parsing, contact the administrator: {}".format(str(e))
   if len(flags["errors"]) > 0:
      return "Flag-parsing errors: ", flags["errors"]

   # check flag argument values and add information
   try:
      flags = check_flags(flags,count,sides,modifier)
   except exception as e:
      print(e)
      return "Exception!", "Critical error during flag checking, contact the administrator: {}".format(str(e))
   if len(flags["errors"]) > 0:
      return "Flag-processing errors: ", flags["errors"]

   totals = []
   results = []
   # roll repeatedly
   for i in range(rolls):
      try:
         total, result = roll_parsed(count,sides,modifier,flags)
      except Exception as e:
         return "Exception!", "Critical error during rolling, contact the administrator: {}".format(str(e))
      totals.append(total)
      results.append(process_results(result,flags))

   # if only one roll, remove a level of list nesting
   if rolls == 1:
      totals = totals[0]
      results = results[0]

   # process all results
   try:
      results = process_results(results,flags)
   except Exception as e:
      return "Exception!", "Critical error during result processing, contact the administrator: {}".format(str(e))

   # return
   return totals, results

def get_lists():
   message = "**Available lists are: **"
   for lst in lists.keys():
      message += lst + ", "
   return message[0:-2]

def main ():
   print(roll(1, int(sys.argv[1]), int(sys.argv[2]), 0, sys.argv[3:]))

if __name__ == '__main__':
   main()

def setup (bot):
   bot.add_cog(Dicehammer(bot))
