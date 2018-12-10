import numpy as np
from numpy import sqrt, pi
import matplotlib.pyplot as plt

def second_order_equation(a,b,c, sign=1):
    delta = b**2 - 4*a*c
    if sign>0:
        return (-b + np.sqrt(delta))/(2*a)
    else:
        return (-b - np.sqrt(delta))/(2*a)


class SphericalInterface(object):
    diameter = 25.4
    def __init__(self, z0, R, n_1, n_2, diameter=None):
        self.z0 = z0
        self.R = R
        if diameter is not None:
            self.diameter = diameter
        self.n_1 = n_1
        self.n_2 = n_2
        self.z_center = z0 + R

    def __repr__(self):
        s = "SphericalInterface(z0={self.z0}, R={self.R}, n_1={self.n_1}, n_2={self.n_2})"
        return s.format(self=self)

    def interface(self, y):
        "Returns the position z of the interface at y"
        R = self.R
        return self.z_center - np.sign(R)*np.sqrt(R**2 - y**2)

    def plot(self):
        y = np.linspace(-self.diameter/2, self.diameter/2)
        z = self.interface(y)
        plt.plot(z, y, 'k')   

    def translated(self, d):
        return SphericalInterface(z0=self.z0+d, R=self.R, n_1=self.n_1, n_2=self.n_2, diameter=self.diameter)  

    def intersection(self, ray):
        p0 = ray.p0
        k = ray.k
        R = self.R
        center = np.array([0, 0, self.z_center])
        a = norm(k)**2
        b = 2*np.dot(k, p0-center)
        c = norm(p0-center)**2 - R**2
        t = second_order_equation(a, b, c, -np.sign(self.R))
        return p0 + t*k

    def refract(self, ray):
        p2 = self.intersection(ray)
        n = p2 - np.array([0, 0, self.z_center])
        n = -n/norm(n) * np.sign(self.R)
        k_par = ray.k - np.dot(ray.k, n)*n
        alpha = sqrt(self.n_2**2 - norm(k_par)**2)
        return Ray(p2, k_par + alpha*n)

def norm(a):
    """ Return the norm of a """
    return np.sqrt(np.dot(a,a))

class Ray(object):
    def __init__(self, p0, k, n=None):
        self.p0 = np.array(p0)
        self.k = np.array(k)
        if n is not None:
            self.normalize(n)
    def normalize(self, n):
        """Normalize k such that ||k||=n"""
        self.k = n*self.k/norm(self.k)
    def __repr__(self):
        return "Ray(p0={p0}, k={k})".format(p0=self.p0, k=self.k)

class Beam(list):
    #There is no __init__ method.
    def plot(self):
        for r1, r2 in zip(self[:-1], self[1:]):
            plt.plot([r1.p0[2], r2.p0[2]], [r1.p0[1], r2.p0[1]], 'k')

class OpticalSystem(list):
    def calculate_beam(self, r0):
        beam = Beam()
        beam.append(r0)
        for interface in self:
            beam.append(interface.refract(beam[-1]))
        return beam
    def plot(self):
        for interf in self:
            interf.plot()

    def translated(self, d):
        return OpticalSystem([interf.translated(d) for interf in self])
        

if __name__=="__main__":
    plt.ion()
    n_LAH64 = 1.77694
    n_SF11 = 1.76583
    n_air = 1.0002992
    S1 = SphericalInterface(0,-4.7, n_air, n_SF11, diameter=3)
    S2 = SphericalInterface(1.5,1E10, n_SF11, n_air, diameter=3)

    LC2969 = OpticalSystem()
    LC2969.append(S1)
    LC2969.append(S2)

    screen = SphericalInterface(20, 1e10, n_air, n_air, diameter=15)
    system = OpticalSystem()
    system.extend(LC2969)
    system.append(screen)
    system = system.translated(2)

    plt.clf()
    system.plot()

    for height in np.linspace(-1.25, 1.25, 11):
        r0 = Ray(p0=np.array([0,height,-5]), k=np.array([0,0,1]), n=n_air)
        beam = system.calculate_beam(r0)

        beam.plot()


    plt.axes().set_aspect('equal')
    
    plt.savefig('output.pdf')







