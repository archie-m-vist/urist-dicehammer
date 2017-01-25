from util.fishutil import is_integer

def parse_flags (flags):
   output = {}
   output["errors"] = []
   # iterate across flags
   index = 0
   while index < len(flags):
      # get the current flag
      flag = flags[index].lower()
      # exploding dice
      if flag == "explode":
         index, output["explode"], errors = parse_explode(flags,index+1)
         output["errors"].extend(errors)
      # drop highest/lowest
      if flag == "drop":
         index, output["drop"], errors = parse_drop(flags,index+1)
      # verbose output
      elif flag == "verbose":
         output["verbose"] = True
         index += 1
      # if word is not a flag, move to next index
      else:
         index += 1
   return output

def parse_drop (flags, index):
   """
   Processes the arguments to the ``drop`` keyword.
   
   Parameters:
      flags - list of flags
      index - index of the first flag after the ``drop`` keyword

   Returns:
       index - the index of the fist keyword after the last explode argument
       value - a list containing parsed arguments, to be stored in ``output["drop"]`` by parse_flags
             - value[0]: number of dice to drop (will error if > count)
             - value[1]: 'h' for drop highest, 'l' for drop lowest
      errors - a list of errors, to be added to ``output[errors]`` with extend().
   """
   value = [1, 'l']
   errors = []
   while index < len(flags):
      temp = flags[index].lower()
      if temp == "highest" or temp == "high":
         value[1] = 'h'
      if temp == "lowest" or temp == "low":
         value[1] = 'l'
      if is_integer(temp):
         value[0] = int(temp)
      else:
         break
      index += 1
   return index, value, errors


def parse_explode (flags, index):
   """
   Processes the arguments to the ``explode`` keyword.
   
   Parameters:
         flags - list of flags
         index - index of the first flag after the ``explode`` keyword
   
   Returns:
       index - the index of the first keyword after the last explode argument
       value - a list containing parsed arguments, to be stored in ``output["explode"]`` by parse_flags
             - value[0]: minimum (for explode up)/maximum (for explode down) value to explode on.
                         Will be reduced by modular arithmetic to be between 1 and max sides.
             - value[1]: 1 if exploding upwards, -1 if exploding downwards
             - value[2]: Maximum number of times to explode, set with ``max n``.
      errors - a list of errors, to be added to ``output["errors"]`` with extend().
   """
   # default to exploding up on the highest roll possible
   value = [0,1,1]
   errors = []
   # check for arguments to explode
   while ( index < len(flags) ):
      temp = flags[index].lower()
      # explode up
      if temp == "up":
         # explode up n
         if index+1 < len(flags) and is_integer(flags[index+1]):
            index += 1
            value[0] = int(flags[index])
      # explode up
      elif temp == "down":
         value[0] = 1
         value[1] = -1
         # explode down n
         if index+1 < len(flags) and is_integer(flags[index+1]):
            index += 1
            value[0] = int(flags[index])
      # explode max n
      elif temp == "max":
         if index+1 < len(flags) and is_integer(flags[index+1]):
            index += 1
            value[2] = int(flags[index])
         else:
            errors.append("Error: no integer argument to explode max")
      else:
         break
      index += 1
   return index, value, errors