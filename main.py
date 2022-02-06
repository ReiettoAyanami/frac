import math
import pygame
from pygame.constants import MOUSEBUTTONDOWN
from pygame.time import Clock

from src.branch import Branch

TIME_SUS = 2
MAX_DEPTH = 15
MIN_DEPTH = 0

pygame.init()
pygame.font.init()
SIZE = WIDTH, HEIGHT = (600,600)
BGCOLOR = (50,50,50)
GFONT = pygame.font.SysFont("Comic Sans MS", 30)
window = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
pygame.display.set_caption('test')
clock = Clock()

b = Branch(start = pygame.Vector2(WIDTH//2,HEIGHT*4/5), r = 200, rmult=0.8, anglemod=30/180*math.pi, max_depth=MAX_DEPTH) 
b.generate()

def main():
    
    time = TIME_SUS
    depth = 0
    depth_dir = 1
    global MAX_DEPTH
    
    running = True
    while running:
        clock.tick(60)
        
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        window.fill(BGCOLOR)

        if time > TIME_SUS:
            depth = depth+depth_dir
            time = 0
        time +=1

        if depth == MAX_DEPTH and depth_dir == 1:
            depth_dir = -1
            
        if depth == MIN_DEPTH and depth_dir == -1:
            depth_dir = 1


        
        b.show(window,depth)    

        pygame.display.update()

if __name__ == '__main__':
    main()
    