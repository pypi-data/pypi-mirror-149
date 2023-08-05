__version__ = '0.1.0py'

def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count

def iterate(seed, multiplier, increment, modulus):
  stepA=seed*multiplier
  stepB=stepA+increment
  stepC=stepB%modulus
  return stepC

def inputNum(text):
  n=input(text)
  try:
    # converting to integer
    int(n)
    isInt=True
  except ValueError:
    isInt=False
    
  while not isInt:
    n=input(text)
    try:
      # converting to integer
      int(n)
      isInt=True
    except ValueError:
      isInt=False
  return int(n)

def getRandomLCG(seed, multiplier, increment, modulus, n):
  newSeed=iterate(seed, multiplier, increment, modulus)
  
  for arbitrary in range(0,n):
    newSeed=iterate(newSeed, multiplier, increment, modulus)

  return newSeed

def randomInt(seed, multiplier, increment, modulus, n, mine, maxe):
  toLarge=getRandomLCG(seed, multiplier, increment, modulus, n)
  while toLarge >= 1:
    toLarge/=10
  return round(toLarge * (maxe - mine + 1) + mine)

def listOfRandoms(seed, multiplier, increment, modulus, n, mine, maxe, amount):
  lists=[]
  curSeed=seed
  for a in range(0, amount):
    lists.append(randomInt(curSeed, multiplier, increment, modulus, n, mine, maxe))
    curSeed+=1
    if curSeed >= multiplier:
      curSeed=1
  return lists

def runIt():
  seed=inputNum("Enter seed: ")
  multiplier=inputNum("Enter multiplier: ")
  increment=inputNum("Enter increment: ")
  modulus=inputNum("Enter modulus: ")
  n=inputNum("Enter amount of times to itterate: ")
  print(getRandomLCG(seed, multiplier, increment, modulus, n))
  mine=inputNum("Enter min: ")
  maxe=inputNum("Enter max: ")
  print(randomInt(seed, multiplier, increment, modulus, n, mine, maxe))
  amount=inputNum("Enter amount: ")
  randomsList=listOfRandoms(seed, multiplier, increment, modulus, n, mine, maxe, amount)
  for num in randomsList:
    print("\033[0;93m"+str(num)+'\033[0m',end=", ")
  print("")
  print("Number : Times Occured : Percent of the time")
  sumtimes=0
  sumpercent=0
  countedNums=[]
  for a in range(mine, maxe+1):
    occuredtimes=countX(randomsList, a)
    precent=(occuredtimes/amount)*100
    print(a,":",occuredtimes, f": occured {precent}% of the time")
    sumpercent+=precent
    sumtimes+=occuredtimes
    countedNums.append(a)
  print(f"{sumpercent}% accounted for ({sumtimes} numbers)")
  print("")
  uncounted=[]
  for n in randomsList:
    if not n in countedNums:
      uncounted.append(n)

  uncountedDupe=[]
  for n in uncounted:
    if not n in uncountedDupe:
      uncountedDupe.append(n)
  print("The following numbers are out of bounds:")
  for n in uncountedDupe:
    print(uncountedDupe.index(n)+1,':',n,": occured", str(countX(uncounted, n))+"% of the time")
  print("")
  amountofthem=len(randomsList)
  print(f"({amountofthem} were made)")
#not gonna use my own random since it requires a seed, and randint doesnt

from time import sleep
import os
from random import randint, choice
import subprocess
def remove():
    tput = subprocess.Popen(['tput','cols'], stdout=subprocess.PIPE)
    cols = int(tput.communicate()[0].strip())
    print("\033[A{}\033[A".format(' '*cols))

starters=["Booting ", "Starting ", "Looking for ", "Downloading ", "Fixing ", "Creating ", "Finding ", "Tracing ", "Copying ", "Recreating ", "Decompiling ", "Compiling ", "Saving ", "Teleporting ", "Transmorgifying ", "Destroying ", "Recording ", "Iterating ", "Throttling ", "Drawing "]

joiners=["a ", "a ", "a ", "an ", "the ", "the ", "the "]

singular_consonant=["monkey", "laser", "piece of cheese", "cat", "phone", "13.5", "rock band", "guitar", "black hole", "singularity"]
singular_vowel=["apple", "iphone", "android", "armadillo", "elisa fruit", "ark", "ark reactor"]
plural=["code","functions","lasers","cats","smellers","rock bands","9.6666 repeating", "cheese", "frustration", "happiness", "gramar"]

def cls():
  os.system('cls' if os.name=='nt' else 'clear')

def coolLoad():

  def getMessage():
    start=choice(starters)
    which=randint(0,6)
    joiner=joiners[which]
    if which <= 2:
      ender=choice(singular_consonant)
    elif which == 3:
      ender=choice(singular_vowel)
    elif which >= 4:
      ender=choice(plural)
    else:
      print("ERROR")
    return start+joiner+ender

  extratime=0
  repeatit=1
  notStalled=True
  prevrand=0

  for n in range(0,11):
    notStalled=True
    repeatit=1
    while repeatit > 0:
      print("----------------------")
      tn=n
      addedRan=randint(0,9)
      if not notStalled:
        addedRan=prevrand
      if addedRan >= 5:
        tn+=1
      if (n*10)+addedRan > 100:
        addedRan-=(n*10)+addedRan-100
      whites="□"*(10-tn)
      blacks="■"*tn
      percent=str((n*10)+addedRan)+"% done"
      print(":"+blacks+whites+":",percent)
      print(getMessage())
      print("----------------------")
      if (n*10)+addedRan >= 96:
        extratime=randint(100,300)/100
        if notStalled:
          notStalled=True
          repeatit=randint(1,3)
      sleep((randint(10,30)/10)+extratime)
      prevrand=addedRan
      repeatit-=1
      for n in range(4):
        remove()

