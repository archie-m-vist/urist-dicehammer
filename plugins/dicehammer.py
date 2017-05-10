if __name__ == '__main__':
   import sys

import random, re, math
from discord.ext import commands
from util.flagparse import parse_flags
from util.fishutil import is_integer
from data.randList import randomFromList, lists

roll_regex = re.compile("(\d*#)?(\d*)d(\d+)((\+|-)(\d+))?")

class Dicehammer:
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
      user = ctx.message.author.mention
      if number < 1:
         message = "{} attempted to flip negative coins, and only got reminded of their debts.".format(user)
      elif number > 1:
         message = "{} flipped {} coins, and got **{} heads** and **{} tails**.".format(user, number, heads, tails)
      else:
         result = 'heads' if heads > 0 else 'tails'
         message = "{} flipped a coin and got **{}**.".format(user, result)
      await(self.bot.say(message))

   @commands.group(pass_context = True)
   async def choose(self,ctx,*options):
      """
         Chooses a single element from a list.

         Arguments:
          - options: This can either be the name of a preconstructed list, or a list of items separated by commas. Items may contain any character other than a comma.
      """
      if ctx.invoked_subcommand == None:
         user = ctx.message.author.mention
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
         await(self.bot.say(message))

   @choose.command(name='lists')
   async def _lists(self):
      """
         Lists all available preconstructed lists.
      """
      message = get_lists()
      await(self.bot.say(message))

   @commands.command(pass_context = True)
   async def shuffle(self,ctx,*options):
      """
         Randomises the ordering of the elements of a list.

         Arguments:
          - options: A list of items separated by commas. (shuffle does not accept preconstructed list names.)
      """
      user = ctx.message.author.mention
      options = " ".join(options)
      options = options.split(",")
      result = ""
      while (len(options) > 0):
         result += options.pop();
         if (len(options) > 0):
            result += ", "
      message = "{} gets: **{}**".format(user,result)
      await(self.bot.say(message))

   @commands.group(pass_context = True)
   async def roll(self,ctx,dstring,*flags):
      """
         Rolls dice.

         Arguments:
          - dstring: A dice string. dN to roll an N-sided die, MdN to roll M N-sided dice, R#MdN to roll M N-sided dice R times. Supports + afterwards for final modifiers.
          - flags: A variety of flags. See subcommands for specific flag usage.
      """
      user = ctx.message.author.mention
      matched = roll_regex.match(dstring)
      flags = " ".join(flags)
      if matched == None:
         message = "{} supplied invalid dice string: {}".format(user,dstring)
      else:
         rolls = int(matched.group(1)[0:-1]) if matched.group(1) is not None else 1
         count = int(matched.group(2)) if matched.group(2) is not '' else 1
         sides = int(matched.group(3))
         modifier = int(matched.group(4)) if matched.group(4) is not None else 0
         flags = flags.split(" ")

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
                  await(self.bot.say(message))
                  message = results.pop()
      await(self.bot.say(message))

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
         t = "+" if diff > 0 else "-"
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
   return total, results

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
      flags = parse_flags(flags)
   except Exception as e:
      return "Exception!", "Critical error during flag parsing, contact the administrator: {}".format(str(e))
   if len(flags["errors"]) > 0:
      return "Flag-parsing errors: ", flags["errors"]

   # check flag argument values and add information
   try:
      flags = check_flags(flags,count,sides,modifier)
   except exception as e:
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
   message = "**Available lists are:**"
   for lst in lists.keys():
      message += " " + lst
   return message

def main ():
   print(roll(1, int(sys.argv[1]), int(sys.argv[2]), 0, sys.argv[3:]))

if __name__ == '__main__':
   main()

def setup (bot):
   bot.add_cog(Dicehammer(bot))