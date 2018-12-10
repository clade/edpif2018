class BipolarCircuit(object):
    def __add__(self, other):
        return Serial(self, other)
    
    def __or__(self, other):
        return Parallel(self, other)

class Combination(BipolarCircuit):
    def __init__(self, *args):
        list_of_circuit = []
        for elm in args:
            if isinstance(elm, self.__class__):
                list_of_circuit.extend(elm.list_of_circuit)
            else:
                list_of_circuit.append(elm)
        self.list_of_circuit = list_of_circuit

    def __repr__(self):
        s = ', '.join([repr(elm) for elm in self.list_of_circuit])
        return '{}({})'.format(self.__class__.__name__, s)        
        
class Serial(Combination):
    def impedance(self, freq):
        list_of_impedance = [elm.impedance(freq) 
                             for elm in self.list_of_circuit]
        return sum(list_of_impedance)

        
class Parallel(Combination):
    def impedance(self, freq):
        list_of_admittance = [1/elm.impedance(freq) 
                             for elm in self.list_of_circuit]
        return 1/sum(list_of_admittance)


    

