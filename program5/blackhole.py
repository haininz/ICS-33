# Black_Hole is singly derived from Simulton, updating by finding+removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    radius = 10
    def __init__(self,x,y):
        Simulton.__init__(self,x,y,Black_Hole.radius*2,Black_Hole.radius*2)

    def contains(self,xy):
        return self.distance(xy) <= Black_Hole.radius
    
    def update(self,model):
        disappear = set()
        for i in model.find(lambda x: isinstance(x, Prey)):
            if self.contains(i.get_location()):
                disappear.add(i)
        for j in disappear:
            model.remove(j)
        return disappear
    
    def display(self, the_canvas):
        width, height = self.get_dimension()
        the_canvas.create_oval(self._x-width/2,self._y-height/2,self._x+width/2,self._y+height/2,fill = "black")
