from math import dist, radians
import math
from tkinter.messagebox import NO
from numpy import mat, vectorize
from pygame import Vector2
import pygame


class Branch:

    def __init__(self,start = None, r = None,parent = None, depth = 0, angle = math.pi / 2, rmult = 2 / 3, anglemod = math.pi / 4, max_depth=15) -> None:
        self.start = start
        self.angle = angle
        self.parent = parent
        self.rmult = rmult 
        self.r = r
        self.anglemod = anglemod
        self.depth = depth
       
        self.max_depth = max_depth

        self.right = None
        self.left = None

    def show(self,window, pos,depth):
        if self.depth >= depth:
            return

        if self.right is not None:
            self.right.show(window, pos,depth)

        if self.left is not None:
            self.left.show(window, pos,depth)

        if self.parent is None:
            pygame.draw.line(window, (255,255,255),self.start+Vector2(pos), self.end+Vector2(pos))
        else:
            pygame.draw.line(window,(255,255,255), self.parent.end+Vector2(pos), self.end+Vector2(pos))

    def generate(self):
        self.end = self.calculate_end()
        if self.depth < self.max_depth:
            self.add_child(self)
        
        if self.right is not None:
            self.right.end = self.right.calculate_end()
            self.right.generate()
        if self.left is not None:
            self.left.end = self.left.calculate_end()
            self.left.generate()

    def calculate_end(self):
        if self.parent is None:
            end =  Vector2(self.start.x + (math.cos(self.angle) * self.r),self.start.y - (math.sin(self.angle)* self.r))
        else:
            end =  Vector2(self.parent.end.x + (math.cos(self.angle) * self.r),self.parent.end.y - (math.sin(self.angle) * self.r))
        return end

    def add_child(self, new_b):
        if self.right is None:
            self.right = Branch(parent=new_b, r = self.r * self.rmult, depth= self.depth + 1, angle=self.angle + self.anglemod, rmult = self.rmult, anglemod =self.anglemod, max_depth=self.max_depth)

        if self.left is None:
            self.left = Branch(parent=new_b, r = self.r * self.rmult, depth = self.depth + 1, angle=self.angle - self.anglemod, rmult = self.rmult, anglemod =self.anglemod, max_depth=self.max_depth)

            

class Tree(Branch):
    def __init__(self, r=10, rotation=0, rmult=0.5, anglemod=math.pi / 4, max_depth=15) -> None:

        angle = math.pi/2 + rotation
        super().__init__(Vector2(0,0), r, None, 0, angle, rmult, anglemod, max_depth)

    
