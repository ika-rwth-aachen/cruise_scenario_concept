import math

class Inftrastructure():

    def __init__(self,
                 lane_width=4,
                 car_length=4, 
                 car_width=2):
        
        self.W_RAD = 0 * math.pi
        self.S_RAD = 0.5 * math.pi
        self.E_RAD = 1.0 * math.pi
        self.N_RAD = 1.5 * math.pi

        self.lw=lane_width

        self.cl=car_length
        self.cw=car_width



    def get_height(self):
        raise NotImplementedError("Base class has no height.")


    def get_width(self):
        raise NotImplementedError("Base class has no width.")