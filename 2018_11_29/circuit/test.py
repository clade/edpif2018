from circuit import Resistor, Capacitor, Inductor

my_circuit = (Resistor(10)| Capacitor(10E-6) | Inductor(15E-6)) + Resistor(5)

print(my_circuit.impedance(10000))
