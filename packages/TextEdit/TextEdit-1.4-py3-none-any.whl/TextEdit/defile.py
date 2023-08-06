import time
import sys
default_speed = 0.05
speed = default_speed
reset = True

def Speed(x):
    global speed
    global reset
    if x == "no_reset":
        reset = False
    elif x == "reset":
        reset = True
    elif x == "def":
        speed = default_speed
    else:
        speed = x

def defile (*y):
    global speed
    global reset
    for phrase in y:
        #sys.stdout.write("[phrase = " + phrase + "]\n")
        for i in phrase :
            #sys.stdout.write("i = " + i + "\n")
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(speed)
    if reset == True:
        speed = default_speed

def defileInput (*z):
    global speed
    for phrase in z:
        #sys.stdout.write("[phrase = " + phrase + "]\n")
        for i in phrase :
            #sys.stdout.write("i = " + i + "\n")
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(speed)
    if reset == True:
        speed = default_speed
    response = input()
    return response