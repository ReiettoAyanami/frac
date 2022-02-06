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

    def __update(self):
        self.end = self.calculate_end()
        if self.parent != None:
            self.start = self.parent.end

    def generate(self):
        self.__update()
        if self.depth < self.max_depth:
            self.add_child(self)
        
        if self.right is not None:
            self.right.generate()
        if self.left is not None:
            self.left.generate()

    def calculate_end(self):
        if self.parent is None:
            end =  Vector2(self.start.x + (math.cos(self.angle) * self.r),self.start.y - (math.sin(self.angle)* self.r))
        else:
            end =  Vector2(self.parent.end.x + (math.cos(self.angle) * self.r),self.parent.end.y - (math.sin(self.angle) * self.r))
        return end

    def add_child(self, new_b):
        if self.right is None:
            self.right = Branch(start=self.end,parent=new_b, r = self.r * self.rmult, depth= self.depth + 1, angle=self.angle + self.anglemod, rmult = self.rmult, anglemod =self.anglemod, max_depth=self.max_depth)

        if self.left is None:
            self.left = Branch(start=self.end,parent=new_b, r = self.r * self.rmult, depth = self.depth + 1, angle=self.angle - self.anglemod, rmult = self.rmult, anglemod =self.anglemod, max_depth=self.max_depth)

    def rotate(self, angle):
        self.angle += angle
        self.__update()
        if self.right is not None:
            self.right.rotate(angle)
        if self.left is not None:
            self.left.rotate(angle)
    
    

    def __get_left(self):
        if self.left == None and self.right == None:
            return min(self.start.x, self.end.x)
        if self.left == None:
            return min(self.start.x, self.end.x, self.right.__get_left())
        if self.right == None:
            return min(self.start.x, self.end.x, self.left.__get_left())
        return min(self.start.x, self.end.x,self.right.__get_left(), self.left.__get_left())

    def __get_right(self):
        if self.left == None and self.right == None:
            return max(self.start.x, self.end.x)
        if self.left == None:
            return max(self.start.x, self.end.x, self.right.__get_right())
        if self.right == None:
            return max(self.start.x, self.end.x, self.left.__get_right())
        return max(self.start.x, self.end.x,self.right.__get_right(), self.left.__get_right())

    def __get_top(self):
        if self.left == None and self.right == None:
            return min(self.start.y, self.end.y)
        if self.left == None:
            return min(self.start.y, self.end.y, self.right.__get_top())
        if self.right == None:
            return min(self.start.y, self.end.y, self.left.__get_top())
        return min(self.start.y, self.end.y,self.right.__get_top(), self.left.__get_top())

    def __get_bottom(self):
        if self.left == None and self.right == None:
            return max(self.start.y, self.end.y)
        if self.left == None:
            return max(self.start.y, self.end.y, self.right.__get_bottom())
        if self.right == None:
            return max(self.start.y, self.end.y, self.left.__get_bottom())
        return max(self.start.y, self.end.y,self.right.__get_bottom(), self.left.__get_bottom())

    def get_size(self):
        l = self.__get_left()
        r = self.__get_right()
        t = self.__get_top()
        b = self.__get_bottom()
        
        w = abs(l-r)
        h = abs(t-b)

        return (l,t,w,h)

    def get_sium(self):
        l = self.__get_left()
        r = self.__get_right()
        t = self.__get_top()
        b = self.__get_bottom()
        
        

        return (l,r,t,b)

    def get_rect(self, pos):
        l,t,w,h = self.get_size()
        l += pos[0]
        t += pos[1]

        return pygame.Rect(l,t,w,h)
            

class Tree(Branch):
    def __init__(self, r=10, rotation=0, rmult=0.5, anglemod=math.pi / 4, max_depth=15) -> None:

        angle = math.pi/2 + rotation
        super().__init__(Vector2(0,0), r, None, 0, angle, rmult, anglemod, max_depth)

    
