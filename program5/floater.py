# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random, uniform


class Floater(Prey): 
    radius = 5
    def __init__(self,x,y):
        self.randomize_angle()
        self._image = PhotoImage(file='ufo.gif')
        Prey.__init__(self,x,y,Floater.radius*2,Floater.radius*2,self._angle,5)
    
    def update(self,model):
        if random() <= 0.3:
            self._angle = uniform(self._angle-0.5,self._angle+0.5)
            while True:
                speed = uniform(self._speed-0.5,self._speed+0.5)
                if 3 <= speed <= 7:
                    self._speed = speed
                    break
        self.move()
        
    def display(self,the_canvas):     
        the_canvas.create_image(*self.get_location(),image=self._image) 
