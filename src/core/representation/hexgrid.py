# -*- coding: utf-8 -*-
'''
Created on Wed Dec 18 16:34:04 2019

@author: arthurd
'''


import numpy as np
import math
import matplotlib.pyplot as plt
from pyproj import Proj, Transformer


def hexbin_grid(bbox, side_length=1, proj_init=None, proj_out=None):
    """ 
        Create a grid of pointy hexagons
        
    :param bbox: bounding box of the grid (x_lower_left, y_lower_left, x_upper_right, y_upper_right)
    type bbox: tuple
    :param side_length: length of the hexagon side.
    type side_length: float
    :param proj_init: projection id of the initial coordinates
    type proj_init: String
    :param proj_out: projection if of the output coordinates
    type proj_out: String
    
    :return : a list of hexagons. An hexagon is a list of seven point coordinates.
    rtype: list
    """
    
    
    startx = bbox[0]
    starty = bbox[1]
    endx = bbox[2]
    endy = bbox[3]
    
    proj = proj_init != proj_out  
    
    if proj:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        startx, starty = transformer.transform(startx, starty)
        endx, endy = transformer.transform(endx, endy)       

    
    # calculate coordinates of the hexagon points
    # see http://www.calculatorsoup.com/calculators/geometry-plane/polygon.php
    p = side_length * 0.5
    b = side_length * math.cos(math.radians(30))
    w = b * 2
    h = 2 * side_length
        
    # offset start and end coordinates by hex widths and heights to guarantee coverage     
    startx = startx - w
    starty = starty - h/2
    endx = endx
    endy = endy

    origx = startx

    # offsets for moving along and up rows
    xoffset = b
    yoffset = 3 * p
    
    P1 = np.empty((0, 2))
    P2 = np.empty((0, 2))
    P3 = np.empty((0, 2))
    P4 = np.empty((0, 2))
    P5 = np.empty((0, 2))
    P6 = np.empty((0, 2))
    
    row = 0

    while starty < endy:
        if row % 2 == 0:
            startx = origx + xoffset
        else:
            startx = origx + w
        while startx <= endx:
            p1 = [startx,       starty + p]
            p2 = [startx,       starty + (3 * p)]
            p3 = [startx + b,   starty + h]
            p4 = [startx + w,   starty + (3 * p)]
            p5 = [startx + w,   starty + p]
            p6 = [startx + b,   starty]
           
            P1 = np.vstack((P1, p1))
            P2 = np.vstack((P2, p2))
            P3 = np.vstack((P3, p3))
            P4 = np.vstack((P4, p4))
            P5 = np.vstack((P5, p5))
            P6 = np.vstack((P6, p6))

            startx += w
        starty += yoffset
        row += 1
        
    if proj:
        transformer = Transformer.from_proj(Proj(init=proj_out), Proj(init=proj_init))
        lon1, lat1 = transformer.transform(P1[:,0], P1[:,1])
        P1 = np.column_stack((lon1, lat1))
        lon2, lat2 = transformer.transform(P2[:,0], P2[:,1])
        P2 = np.column_stack((lon2, lat2))
        lon3, lat3 = transformer.transform(P3[:,0], P3[:,1])
        P3 = np.column_stack((lon3, lat3))
        lon4, lat4 = transformer.transform(P4[:,0], P4[:,1])
        P4 = np.column_stack((lon4, lat4))
        lon5, lat5 = transformer.transform(P5[:,0], P5[:,1])
        P5 = np.column_stack((lon5, lat5))
        lon6, lat6 = transformer.transform(P6[:,0], P6[:,1])
        P6 = np.column_stack((lon6, lat6))
    
    polygons = []
    for i in range(len(P1)):
        hexagon = [(P1[i][0], P1[i][1]), 
                   (P2[i][0], P2[i][1]),
                   (P3[i][0], P3[i][1]),
                   (P4[i][0], P4[i][1]),
                   (P5[i][0], P5[i][1]),
                   (P6[i][0], P6[i][1])]
        polygons.append(hexagon)
  
    return polygons



def get_size_hexgrid(bbox, side_length):
    startx, starty, endx, endy = bbox[0], bbox[1], bbox[2], bbox[3]
    # width & height of the bbox
    w = abs(endx - startx)
    h = abs(endy - starty)
    # parameters of the hexagon
    R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    r = R * np.cos(np.deg2rad(30))
    # number of hexagons (vertivcal & horizontal)
    Nw = int((w + r)//(2*r)) + 1
    Nh = int((h + R)//(R + side_length/2)) + 1
    
    shorter_lines = 0 if (w > 2*(Nw - 1)*r) else 1
    
    return Nw, Nh, shorter_lines


def cartesian_to_hex(point, origin=(0, 0), side_length=1,
                     proj_init=None, proj_out=None):
    
    if proj_init != proj_out:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        point = transformer.transform(point[0], point[1])
        origin = transformer.transform(origin[0], origin[1])
    
    mat = np.array([[np.sqrt(3)/3, -1/3],
                    [0           , 2/3 ]])
    point = np.array(point)
    hex_coord = np.dot(mat, point - origin)/side_length

    return hex_coord


def hex_to_cartesian(hexa, origin=(0, 0), side_length=1,
                     proj_init=None, proj_out=None):
        
    mat = np.array([[np.sqrt(3), np.sqrt(3)/2],
                    [0         , 3/2         ]])
    hex_coord = np.array(hexa)
    cart_coord = side_length * np.dot(mat, hex_coord)
        
    if proj_init != proj_out:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        cart_coord = transformer.transform(cart_coord[0], cart_coord[1])
        origin = transformer.transform(origin[0], origin[1])
        
    return cart_coord + origin


def hexs_to_cartesians(Q, R, side_length=1, origin=(0, 0), 
                       proj_init=None, proj_out=None):
        
    mat = np.array([[np.sqrt(3), np.sqrt(3)/2],
                    [0         , 3/2         ]])
    
    hex_coord = np.vstack((Q, R))

    cart_coord = side_length * np.dot(mat, hex_coord)
    
    if proj_init != proj_out:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        X, Y = transformer.transform(cart_coord[0], cart_coord[1])
        cart_coord = np.vstack((X, Y))
        origin = transformer.transform(origin[0], origin[1])
    
    origin = np.vstack(([origin[0]] * len(Q), [origin[1]] * len(R)))
    
    return cart_coord + origin


def cartesians_to_hexs(X, Y, origin=(0, 0), side_length=1,
                       proj_init=None, proj_out=None):
   
    if proj_init != proj_out:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        X, Y = transformer.transform(X, Y)
        origin = transformer.transform(origin[0], origin[1])
    
    mat = np.array([[np.sqrt(3)/3, -1/3],
                    [0           , 2/3 ]])
    coord = np.vstack((X, Y))
    origin = np.vstack(([origin[0]] * len(X), [origin[1]] * len(Y)))
    return np.dot(mat, coord - origin)/side_length



def nearest_hexagon(point, origin=(0, 0), side_length=1, 
                    proj_init=None, proj_out=None):
    
    if proj_init != proj_out:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        point = transformer.transform(point[0], point[1])
        origin = transformer.transform(origin[0], origin[1])

    # Hexagonal coordinates
    hex_coord = cartesian_to_hex(point, origin=origin, side_length=side_length)

    # Cube coordinates
    x = hex_coord[0]
    z = hex_coord[1]
    y = - x - z
    
    # Rounding cube coordinates
    rx = np.round(x)
    ry = np.round(y)
    rz = np.round(z)
    
    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
        
    # Hexagonal coordinates
    q = rx
    r = rz
    
    # # Cartesian coordinates
    # center = hex_to_cartesian((q, r), origin=origin, side_length=side_length)
    
    # if proj:
    #     transformer = Transformer.from_proj(Proj(init=proj_out), Proj(init=proj_init))
    #     center = transformer.transform(center[0], center[1])

    return q, r


def nearest_hexagons(X, Y, origin=(0, 0), side_length=1, proj_init=None, proj_out=None):
    
    if proj_init != proj_out:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        X, Y = transformer.transform(X, Y)
        origin = transformer.transform(origin[0], origin[1])

    hex_coord = cartesians_to_hexs(X, Y, origin=origin, side_length=side_length)
    # Cube coordinates
    X = hex_coord[0]
    Z = hex_coord[1]
    Y = - X - Z
    
    # Rounding cube coordinates
    rX = np.round(X)
    rY = np.round(Y)
    rZ = np.round(Z)
    
    X_diff = abs(rX - X)
    Y_diff = abs(rY - Y)
    Z_diff = abs(rZ - Z)

    for i in range(len(X)):
        if X_diff[i] > Y_diff[i] and X_diff[i] > Z_diff[i]:
            rX[i] = -rY[i] - rZ[i]
        elif Y_diff[i] > Z_diff[i]:
            rY[i] = -rX[i] - rZ[i]
        else:
            rZ[i] = -rX[i] - rY[i]
        
    # Hexagonal coordinates
    Q = rX
    R = rZ

    # # Cartesian coordinates
    # X, Y = hexs_to_cartesians(Q, R, origin=origin, side_length=side_length)

    # if proj:
    #     transformer = Transformer.from_proj(Proj(init=proj_out), Proj(init=proj_init))
    #     X, Y = transformer.transform(X, Y)

    return Q, R



def hexagon_coordinates(center, side_length=1, r=0.8660254037844389, R=1.0000000000000002,
                        proj_init=None, proj_out=None):
    
    if side_length != 1 and r == 0.8660254037844389 and  R == 1.0000000000000002:
        R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
        r = R * np.cos(np.deg2rad(30))
    elif side_length == 1 and r != 0.8660254037844389 and  R == 1.0000000000000002:
        side_length = 2*r *np.tan(np.deg2rad(30))
        R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    elif side_length == 1 and r == 0.8660254037844389 and  R != 1.0000000000000002:
        r = R * np.cos(np.deg2rad(30))
        side_length = 2*r *np.tan(np.deg2rad(30))

    
    proj = proj_init != proj_out  
    
    if proj:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        center = transformer.transform(center[0], center[1])
    
    
    point1 = [center[0], center[1] - R]
    point2 = [center[0] + r, center[1] - side_length/2]
    point3 = [center[0] + r, center[1] + side_length/2]
    point4 = [center[0], center[1] + R]
    point5 = [center[0] - r, center[1] + side_length/2]
    point6 = [center[0] - r, center[1] - side_length/2]
    
    if proj:
        transformer = Transformer.from_proj(Proj(init=proj_out), Proj(init=proj_init))
        point1 = transformer.transform(point1[0], point1[1])
        point2 = transformer.transform(point2[0], point2[1])
        point3 = transformer.transform(point3[0], point3[1])
        point4 = transformer.transform(point4[0], point4[1])
        point5 = transformer.transform(point5[0], point5[1])
        point6 = transformer.transform(point6[0], point6[1])
    
    return [point1, point2, point3, point4, point5, point6, point1]


def hexagons_coordinates(X, Y, side_length=1, r=0.8660254037844389, R=1.0000000000000002,
                         proj_init=None, proj_out=None):
    
    if side_length != 1 and r == 0.8660254037844389 and  R == 1.0000000000000002:
        R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
        r = R * np.cos(np.deg2rad(30))
    elif side_length == 1 and r != 0.8660254037844389 and  R == 1.0000000000000002:
        side_length = 2*r *np.tan(np.deg2rad(30))
        R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    elif side_length == 1 and r == 0.8660254037844389 and  R != 1.0000000000000002:
        r = R * np.cos(np.deg2rad(30))
        side_length = 2*r *np.tan(np.deg2rad(30))
    
    proj = proj_init != proj_out  
    
    if proj:
        transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
        X, Y = transformer.transform(X, Y)
    
    P1 = np.column_stack((X     ,   Y - R))
    P2 = np.column_stack((X + r ,   Y - side_length/2))
    P3 = np.column_stack((X + r ,   Y + side_length/2))
    P4 = np.column_stack((X     ,   Y + R))
    P5 = np.column_stack((X - r ,   Y + side_length/2))
    P6 = np.column_stack((X - r ,   Y - side_length/2))
    
    if proj:
        transformer = Transformer.from_proj(Proj(init=proj_out), Proj(init=proj_init))
        lon1, lat1 = transformer.transform(P1[:,0], P1[:,1])
        P1 = np.column_stack((lon1, lat1))
        lon2, lat2 = transformer.transform(P2[:,0], P2[:,1])
        P2 = np.column_stack((lon2, lat2))
        lon3, lat3 = transformer.transform(P3[:,0], P3[:,1])
        P3 = np.column_stack((lon3, lat3))
        lon4, lat4 = transformer.transform(P4[:,0], P4[:,1])
        P4 = np.column_stack((lon4, lat4))
        lon5, lat5 = transformer.transform(P5[:,0], P5[:,1])
        P5 = np.column_stack((lon5, lat5))
        lon6, lat6 = transformer.transform(P6[:,0], P6[:,1])
        P6 = np.column_stack((lon6, lat6))

    hexagons = []
    for i in range(len(P1)):
        hexagon = [(P1[i][0], P1[i][1]), 
                   (P2[i][0], P2[i][1]),
                   (P3[i][0], P3[i][1]),
                   (P4[i][0], P4[i][1]),
                   (P5[i][0], P5[i][1]),
                   (P6[i][0], P6[i][1]),
                   (P1[i][0], P1[i][1])]
        hexagons.append(hexagon)

    return hexagons




if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t         Hexbin        \n\n")
    
    # Style of the figures
    plt.style.use('seaborn-darkgrid')
    plt.figure()
    
# =============================================================================
#     1/ Create an hexagonal grid
# =============================================================================
    print("1/ Create an hexagonal grid")
    print("\t1.1/ Select the bounding box or two extremes values \n\t(lower_let, upper_right\n\tand select the hexagonal radius")

    point1 = (2, 2)
    point2 = (7, 10)
    
    print("\t1.2/ Create the grid, in the web mercator projection by default_")
    print("\t1.3/ Parameters of the grid")
    # parameters of the hexagons
    w = abs(point1[0] - point2[0])
    h = abs(point1[1] - point2[1])
    r = 0.8660254037844389
    side_length = 1
    R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    
    print("\tParameters : r = {0}, R = {1}, a = {2}".format(r, R, side_length))
    
    bbox = (point1[0], point1[1], point2[0], point2[1])
    hexagons = hexbin_grid(bbox, side_length=side_length, proj_init="epsg:4326", proj_out="epsg:4326")
    
    for i, hexagon in enumerate(hexagons):
        hexagon.append(hexagon[0])
        X = [point[0] for point in hexagon]
        Y = [point[1] for point in hexagon]
        plt.plot(X, Y, color='skyblue', label='hexagon' if i == 0 else '')
    
    print("\t1.3/ Plot the grid")
    plt.scatter(point1[0], point1[1], color='skyblue', label='start')
    plt.scatter(point2[0], point2[1], color='skyblue', label='end')
    
    # frame of the plot
    plt.xticks([point1[0] - r*30 + k*r for k in range(int(30*w))])
    plt.yticks([point1[1] - (R + side_length/2) + k*(R + side_length/2) for k in range(int(2*h))])
    plt.axis("equal")


# =============================================================================
#     2/ Get the grid indexes from the boundinc box and radius
# =============================================================================
    print("2/ Get the nearest hexagon")
    print("\t2.1/ Get the index of the hexagon")
    import random
    point = (random.random()*(point2[0] - point1[0]) + point1[0], 
             random.random()*(point2[1] - point1[1]) + point1[1])
    plt.scatter(point[0], point[1], color='darkcyan', label='random point')
    origin = point1
    
    nearest_hex = nearest_hexagon(point, origin=origin, side_length=side_length)
    center = hex_to_cartesian(nearest_hex, origin=origin, side_length=side_length)
    
    plt.scatter(center[0], center[1], color='cyan', label='hex center')
    plt.legend(loc=1, frameon=True)

    print("\t2.2/ Get nearest hexagons from a list of points")
    
    X = np.random.randint(-5, 10, 50)
    Y = np.random.randint(-5, 15, 50)
    origin = (-5, -5)
    side_length = 1.5
    
    R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    r = R * np.cos(np.deg2rad(30))
    
    Q, R = nearest_hexagons(X, Y, origin=origin, side_length=side_length)
    Xcenter, Ycenter = hexs_to_cartesians(Q, R, origin=origin, side_length=side_length)
    hexagons = hexagons_coordinates(Xcenter, Ycenter, side_length=side_length)
    
    plt.figure()
    plt.scatter(X, Y, zorder=3, color='darkcyan', label='random point')
    plt.scatter(Xcenter, Ycenter, color='cyan', label='hex center')


    for i, hexagon in enumerate(hexagons):
        hexagon.append(hexagon[0])
        X = [point[0] for point in hexagon]
        Y = [point[1] for point in hexagon]
        plt.plot(X, Y, color='skyblue', label='hexagon' if i == 0 else '')
    
    plt.legend(loc=1, frameon=True)
    plt.xticks(np.unique(Xcenter))
    plt.yticks(np.unique(Ycenter))
    plt.axis("equal")
    
    
    
# =============================================================================
#    3/ Geographic coordinates
# =============================================================================
    print("3/ Geographic coordinates")
    print("\t3.1/ Get nearest hexagons in web mercator system from a list of geographic points")
    
    proj_init="epsg:4326"
    proj_out="epsg:3857"
        
    lon = np.random.rand(40)/2 + 3
    lat = np.random.rand(40) + 45
    # origin = (-179.99999999, -89.99999999)
    origin = (0, 0)
    side_length = 15000
    
    R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    r = R * np.cos(np.deg2rad(30))
    
    
    Q, R = nearest_hexagons(lon, lat, side_length=side_length, origin=origin, 
                        proj_init=proj_init, proj_out=proj_out)
    Xcenter, Ycenter = hexs_to_cartesians(Q, R, side_length=side_length, origin=origin, 
                        proj_init=proj_out, proj_out=proj_init)              
    hexagons = hexagons_coordinates(Xcenter, Ycenter, side_length=side_length, 
                                    proj_init=proj_init, proj_out=proj_out)
    

    plt.figure()
    plt.scatter(lon, lat, zorder=3, color='darkcyan', label='random point')
    plt.scatter(Xcenter, Ycenter, color='cyan', label='hex center')

    for i, hexagon in enumerate(hexagons):
        hexagon.append(hexagon[0])
        X = [point[0] for point in hexagon]
        Y = [point[1] for point in hexagon]
        plt.plot(X, Y, color='skyblue', label='hexagon' if i == 0 else '')
    
    plt.legend(loc=1, frameon=True)
    plt.xticks(Xcenter)
    plt.yticks(Ycenter)
    plt.axis("equal")

    
    