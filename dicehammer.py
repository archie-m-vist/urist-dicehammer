if __name__ == '__main__':
   import sys

import random
from flagparse import parse_flags
from fishutil import is_integer

import re

from disco.bot import Bot, Plugin, BotConfig
roll_regex = re.compile("(\d*#)?(\d*)d(\d+)((\+|-)(\d+))?")

class Dicehammer(Plugin):
   @Plugin.command('coinflip', '[number:int]')
   def on_coinflip_command(self,event,number="1"):
      heads, tails = coinflip(number)
      if number < 1:
         event.msg.reply("{} attempted to flip negative coins, and only got reminded of their debts.".format(event.msg.author.mention))
      elif number > 1:
         event.msg.reply("{} flipped {} coins, and got **{} heads** and **{} tails**.".format(event.msg.author.mention, number, heads, tails))
      else:
         result = 'heads' if heads > 0 else 'tails'
         event.msg.reply("{} flipped a coin and got **{}**.".format(event.msg.author.mention, result))

   @Plugin.command('roll', '<dstring:str> [flags:str...]')
   def on_roll_command(self,event,dstring,flags=""):
      matched = roll_regex.match(dstring)
      if matched == None:
         event.msg.reply("invalid dice string: "+dstring)
      else:
         rolls = int(matched.group(1)[0:-1]) if matched.group(1) is not None else 1
         count = int(matched.group(2))
         sides = int(matched.group(3))
         modifier = int(matched.group(4)) if matched.group(4) is not None else 0
         flags = flags.split(" ")

         if rolls == 0 or count == 0 or sides == 0:
            event.msg.reply("{} rolled 0, and shouldn't have expected anything else.".format(event.msg.author.mention))
            return

         if rolls == 1:
            total, results = roll(count,sides,modifier,flags)
         else:
            total, results = multiroll(rolls,count,sides,modifier,flags)

         if isinstance(results,str): # normal case
            event.msg.reply("{} rolled {}: **{}** {}".format(event.msg.author.mention,dstring,total,results))
         else: # verbose flag for long messages
            event.msg.reply("{} rolled {}: **{}**".format(event.msg.author.mention,dstring,total))
            while len(results) > 0:
               event.msg.reply(results.pop())

   @Plugin.command('ping')
   def on_ping_command(self, event):
      event.msg.reply('pong!')

# flips a number of coins, returning the number of heads and the number of tails
def coinflip (number):
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
   flags = parse_flags(flags)
   if len(flags["errors"]) > 0:
      return "Flag-parsing errors: ", flags["errors"]
   flags = check_flags(flags,count,sides,modifier)
   if len(flags["errors"]) > 0:
      return "Flag-processing errors: ", flags["errors"]
   total, results = roll_parsed(count,sides,modifier,flags)
   # process results
   results = process_results(results,flags)
   return total, results

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
   flags = parse_flags(flags)
   if len(flags["errors"]) > 0:
      return "Flag-parsing errors: ", flags["errors"]
   flags = check_flags(flags,count,sides,modifier)
   if len(flags["errors"]) > 0:
      return "Flag-processing errors: ", flags["errors"]
   totals = []
   results = []
   # roll repeatedly
   for i in range(rolls):
      total, result = roll_parsed(count,sides,modifier,flags)
      totals.append(total)
      results.append(process_results(result,flags))
   # process all results
   results = process_results(results,flags)
   # return
   return totals, results

def main ():
   print(roll(1, int(sys.argv[1]), int(sys.argv[2]), 0, sys.argv[3:]))

if __name__ == '__main__':
   main()