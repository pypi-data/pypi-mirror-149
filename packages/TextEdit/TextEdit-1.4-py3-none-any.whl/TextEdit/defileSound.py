import sys
from .Sound import Point
from .Sound import Lettre
from .Sound import Espace

ponctuation = [".", "!", ";", "?", "«", "»", "-", "'", "(", ")"]
def defileSound (*x):
    for phrase in x:
        for i in phrase :
            sys.stdout.write(i)
            sys.stdout.flush()
            if i in ponctuation :
                Point()
            elif i == " ":
                Espace()        
            else :
                Lettre()

def defileInputSound (*x):
    for phrase in x:
        for i in phrase :
            sys.stdout.write(i)
            sys.stdout.flush()
            if i in ponctuation :
                Point()
            elif i == " ":
                Espace()        
            else :
                Lettre()
    response = input()
    return response