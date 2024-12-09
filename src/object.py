import os
import pygame

from AngryBirdsGame import AngryBirds
current_path = os.getcwd()
from characters import Bird
from level import Level

song1 = './resources/sounds/angry-birds.ogg'

def main():
    """Start the game"""
    game = AngryBirds(song1)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()