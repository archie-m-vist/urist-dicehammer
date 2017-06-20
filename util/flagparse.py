from util.fishutil import is_integer

def parse_flags (flags):
   output = {}
   output["errors"] = []
   # iterate across flags
   index = 0
   while index < len(flags):
      # get the current flag
      flag = flags[index].lower()
      errors = None
      # exploding dice
      if flag == "explode":
         index, output["explode"], errors = parse_explode(flags,index+1)
      # drop highest/lowest
      elif flag == "drop":
         index, output["drop"], errors = parse_drop(flags,index+1)
      # degrees of success/failure
      elif flag == "degrees":
         index, output["degrees"], errors = parse_degrees(flags,index+1)
      # verbose output
      elif flag == "successes":
         index, output["successes"], errors = parse_successes(flags,index+1)
      elif flag == "verbose":
         output["verbose"] = True
         index += 1
      # if word is not a flag, move to next index
      else:
         index += 1
      if errors is not None and len(errors) > 0:
         output["errors"].extend(errors)
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
      elif temp == "lowest" or temp == "low":
         value[1] = 'l'
      elif is_integer(temp):
         value[0] = int(temp)
      else:
         break
      index += 1
   print(index,value)
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

def parse_degrees (flags, index):
   """
   Processes the arguments to the ``degrees`` keyword.
   
   Parameters:
         flags - list of flags
         index - index of the first flag after the ``degrees`` keyword
   
   Returns:
       index - the index of the first keyword after the last degrees argument
       value - a list containing parsed arguments, to be stored in ``output["degrees"]`` by parse_flags
             - value[0]: minimum (for explode up)/maximum (for explode down) value to explode on.
                         Will be reduced by modular arithmetic to be between 1 and max sides.
             - value[1]: True if zeroes are on, otherwise False.
      errors - a list of errors, to be added to ``output["errors"]`` with extend().
   """
   value = [None, True]
   errors = []
   while ( index < len(flags) ):
      temp = flags[index]
      if temp == "zeroes":
         if index+1 < len(flags) and flags[index+1] == "off":
            index += 1
            value[1] = False
      elif is_integer(temp):
         value[0] = int(temp)
      else:
         break
      index += 1
   if value[0] is None:
      errors.append("Expected skill value after degrees flag.")
   return index, value, errors

def parse_successes (flags, index): 
   """
   Processes the arguments to the successes keyword.

   Parameters:
         flags - list of flags
         index - index of the first flag after the degrees keyword

   Returns: 
       index - the index of the first keyword after the last degrees argument
       value - a list containing parsed arguments, to be stored in output["successes"] by parse_flags
             - value[0]: Minimum value to count as a success. Default None (set to 70% maximum value, rounded up, by check_flags).
             - value[1]: Minimum value to count as a double success. Default None (set to maximum value by check_flags). 0 or off disables.
             - value[2]: Maximum value to cause a botch if there are no successes. Default 1. 0 or off disables.
      errors - a list of errors, to be added to output["errors"] with extend().
   """ 
   value = [None, None, 1]
   errors = []
   while ( index < len(flags) ):
      temp = flags[index]
      if temp == "threshold":
         if index+1 < len(flags):
            try:
               value[0] = int(flags[index+1])
               index += 1
            except ValueError:
               errors.append("Threshold value must be integer.")
         else:
            errors.append("Expected value after successes threshold flag.")
      elif temp == "double":
         if index+1 < len(flags):
            if flags[index+1] == "off":
               flags[index+1] = 0
            try:
               value[1] = int(flags[index+1])
               index += 1
            except ValueError:
               errors.append("Double value must be integer or off.")
         else:
            error.append("Expected value after successes double flag.")
      elif temp == "botch":
         if index+1 < len(flags):
            if flags[index+1] == "off":
               flags[index+1] = 0
            try:
               value[2] = int(flags[index+1])
               index += 1
            except ValueError:
               errors.append("Botch value must be integer or off.")
         else:
            errors.append("Expected value after successes botch flag.")
      else:
         break
      index += 1
   return index, value, errors