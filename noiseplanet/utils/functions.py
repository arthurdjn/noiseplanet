# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:37:08 2019

@author: Utilisateur
"""

import numpy as np


def natural_to_relative(n):

    if n%2 == 0:
        return n//2
    return (-n + 1)//2


def relative_to_natural(z):

    if z < 0:
        return -2*z + 1
    return 2*z


def cantor(point):
    return .5*(point[0] + point[1])*(point[0] + point[1] + 1) + point[1]


def cantor_inv(z):

    w = np.floor((np.sqrt(8 * z + 1) - 1)/2)
    t = (w*(w + 1)) / 2
    y = int(z - t)
    x = int(w - y)
    # assert z != pair(x, y, safe=False):
    return x, y


def naturals_to_relatives(N):
    return np.where(N%2 == 0, N//2, -(N + 1)//2)

def relatives_to_naturals(Z):
    return np.where(Z < 0, -2*Z + 1, 2*Z)


def cantors(X, Y):
    return np.add(.5*(np.add(X, Y))*(np.add(X, Y) + 1), Y)



def cantors_inv(N):
    N = np.array(N)
    W = np.floor((np.sqrt(8*N + 1)- 1)/2)
    T = (W*(W + 1))/2
    Y = np.add(N,  -T)
    X = np.add(W, -Y)
    return X, Y



if __name__ == "__main__":
    print("1/ Natural / Relative Numbers")
    z = 3
    print('z =', z)
    n = relative_to_natural(z)
    print('n = ', n)
    z = natural_to_relative(n)
    print('Conversion back to relative, z =', z)
    
    
    
    print("\n2/ Cantor functions")
    print("\t2.1/ N2 to N")
    p = (47, 3)
    n = cantor(p)
    print('p =', p)
    print('n =', n)
    p = cantor_inv(n)
    print('Converting back to N2, p =', p)
    
    
    print('--------')

    print("\n3/ Z2 to N")
    p = (-115, -257)
    print('original point, p =', p)
    p2 = relative_to_natural(p[0]), relative_to_natural(p[1])
    print('p2 =', p2)
    n = cantor(p2)
    print('n =', n)
    p3 = cantor_inv(n)
    print('p3 =', p3)
    p4 = natural_to_relative(p3[0]), natural_to_relative(p3[1])
    print('converted point, p =', p4)
    
    
    
    X = [47]
    Y = [3]
    N = cantors(X, Y)
    N = [1278]
    X, Y = cantors_inv(N)
    
    
    
    
    
    
    
    
    
    