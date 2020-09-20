from prey import Prey
from random import randint, shuffle

# Special is a special kind of prey that can change its size and color during each update
class Special(Prey): 
    radius = 10
    def __init__(self,x,y):
        self.randomize_angle()
        Prey.__init__(self,x,y,20,20,self._angle,8)
        self.color = "green"
        self.color_choice = ["red", "orange", "green", "blue", "yellow", "purple"]
        
    def update(self, model):
        Special.radius = randint(5,30)
        shuffle(self.color_choice)
        self.color = self.color_choice[0]
        self.move()
        
    def display(self, canvas):
        canvas.create_oval(self._x-Special.radius, self._y-Special.radius,
                          self._x+Special.radius, self._y+Special.radius,fill=self.color)