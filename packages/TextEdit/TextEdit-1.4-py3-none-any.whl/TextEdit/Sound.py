import os
import pygame
import time
MODULE_PATH = os.path.dirname(__file__)
AUDIO_DIR = os.path.join(MODULE_PATH)

pygame.mixer.init()
def Lettre ():
    pygame.mixer.music.load(os.path.join(AUDIO_DIR, "sound/lettre.wav"))
    pygame.mixer.music.play()
    time.sleep(0.05)
def Point ():
    pygame.mixer.music.load(os.path.join(AUDIO_DIR, "sound/point.wav"))
    pygame.mixer.music.play()
    time.sleep(0.1)
def Espace ():
    pygame.mixer.music.load(os.path.join(AUDIO_DIR, "sound/espace.wav"))
    pygame.mixer.music.play()
    time.sleep(0.05)