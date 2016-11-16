def is_integer (str):
   try:
      int(str)
      return True
   except ValueError:
      return False