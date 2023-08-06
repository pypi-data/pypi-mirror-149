black =  "\u001b[30m"
red =  "\u001b[31m"
green =  "\u001b[32m"
yellow =  "\u001b[33m"
blue =  "\u001b[34m"
magenta =  "\u001b[35m"
cyan = "\u001b[36m"
white = "\u001b[37m"
reset = "\u001b[0m"

def color(msg, color):
  color = color.lower()
  if color == "red":
    print(red + msg + reset)
  elif color == "black":
    print(black + msg + reset)
  elif color == "green":
    print(green + msg + reset)
  elif color == "yellow":
    print(yellow + msg + reset)
  elif color == "blue":
    print(blue + msg + reset)
  elif color == "magenta":
    print(magenta + msg + reset)
  elif color == "cyan":
    print(cyan + msg + reset)
  elif color == "white":
    print(white + msg + reset)