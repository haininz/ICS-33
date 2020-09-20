# Hunter is doubly-derived from the Mobile_Simulton and Pulsator classes:
#   updating/displaying like its Pulsator base, but also moving (either in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.
from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):
    def __init__(self,x,y):
        Pulsator.__init__(self,x,y)
        width, height = self.get_dimension()
        Mobile_Simulton.__init__(self,x,y,width,height,0,5)
        self.randomize_angle()
        
    def update(self,model):
        eaten = Pulsator.update(self,model)
        to_eat = model.find(lambda x: isinstance(x, Prey) and self.distance(x.get_location()) <= 200)
        if to_eat:
            _ , catch = min([(self.distance(i.get_location()),i) for i in to_eat])
            sx,sy = self.get_location()
            x,y = catch.get_location()
            self.set_angle(atan2(y-sy, x-sx))
        self.move()
        return eaten