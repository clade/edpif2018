import numpy as np

from .circuit import BipolarCircuit

class Device(BipolarCircuit):
    pass

class Resistor(Device):
    def __init__(self, resistance):
        self.resistance = resistance
        
    def impedance(self, freq):
        return self.resistance
    
    def __repr__(self):
        return "Resistor({})".format(self.resistance)
    
class Capacitor(Device):
    def __init__(self, capacity):
        self.capacity = capacity
        
    def impedance(self, freq):
        return 1/(2J*np.pi*self.capacity*freq)

    def __repr__(self):
        return "Capacitor({})".format(self.capacity)    
    
class Inductor(Device):
    def __init__(self, inductance):
        self.inductance = inductance
        
    def impedance(self, freq):
        return (2J*np.pi*self.inductance*freq) 
    
    def __repr__(self):
        return "Inductor({})".format(self.inductance)        
