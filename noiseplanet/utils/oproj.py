# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:45:45 2019

@author: arthurd
"""

import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
#   Distance computation for comparison
#   Later, the distance along the WGS84 ellipsoid will be used (from pyproj)
# =============================================================================
def distance_great_circle(pointA, pointB):
    """
    Compute the Great Circle Distance between two points.

    Parameters
    ----------
    pointA : Tuple
        Pooint A.
    pointB : Tuple
        Point B.

    Returns
    -------
    distance : Float
        Distance between A and B.
    """
    return ((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)**0.5


def distance_haversine(pointA, pointB):
    """
    Compute the Haversine distance between two points, in Lat Lon.

    Parameters
    ----------
    pointA : Tuple
        Point A in (Lat, Lon) format.
    pointB : Tuple
        Point B in (Lat, Lon) format.

    Returns
    -------
    distance : Float
        Distance between A and B.
    """
    
    lat1 = pointA[0] * np.pi/180
    lat2 = pointB[0] * np.pi/180
    lon1 = pointA[1] * np.pi/180
    lon2 = pointB[1] * np.pi/180
    
    a = (np.sin((lat1 - lat2)/2))**2 + np.cos(lat1)*np.cos(lat2)*(np.sin((lon1 - lon2)/2))**2
    c = 2*np.arctan2(a**0.5, (1 - a)**0.5)
    # Earth's radius
    r = 6378137
    
    return r*c


# =============================================================================
#     Ortho projection
# =============================================================================
def slope(pointA, pointB):
    """
    Compute the slope (directional coefficient) of a line from two points.

    Parameters
    ----------
    pointA : Tuple
        Pooint A.
    pointB : Tuple
        Point B.

    Returns
    -------
    slope : Tuple
        Slope vector from point A to point B.
    """
    
    d = distance_great_circle(pointA, pointB)
    return ((pointB[0] - pointA[0])/d, (pointB[1] - pointA[1])/d)


def orthoProj(pointA, pointB, S):
    """
    Orthogonal projection of a point on a line.

    Parameters
    ----------
    pointA : Tuple
        Point to project on the line.
    pointB : Tuple
        Point belonging to the line.
    S : Tuple
        Slope of the line.

    Returns
    -------
    projection : Tuple
        Porjection of Point A on the line (Point B, Slope).
    """

    d = (S[0]**2 + S[1]**2)**.5
    BH = ((pointA[0] - pointB[0])*S[0] + (pointA[1] - pointB[1])*S[1])/d
    
    xH = pointB[0] + BH/d*S[0]
    yH = pointB[1] + BH/d*S[1]
    
    return (xH, yH)

def orthoProjSegment(pointA, pointB, pointC):
    """
    Orthogonal projection of a point into a line.

    Parameters
    ----------
    pointA : Tuple
        Point to project on the line.
    pointB : Tuple
        Point belonging to the line.
    pointC : Tuple
        Second point belonging to the line.

    Returns
    -------
    projection : Tuple
        Porjection of Point A on the line (Point B, Slope).

    ---------------------------------------------------------------------------
    Description :
        Projection of a point A on the segment [B, C]
        There is no specific order for the input pointB or pointC
        Example :           
            Case 1 :
                a) The slope from B to C is (+.., +..)
                             C
                            x
                           /
                          /         x A
                         /
                        x
                       B        
                            
                a) The slope from B to C is (-.., -..)
                             B
                            x
                           /
                          /         x A
                         /
                        x
                       C
                       
            Case 2 :
                a) The slope from B to C is (+.., -..)
                      B
                       x
                        \
                         \         x A
                          \
                           \
                            x
                             C
                            
                b) The slope from B to C is (-.., +..)
                      C
                       x
                        \
                         \         x A
                          \
                           \
                            x
                             B  
    """    
    
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    #test if the projected point is outside the segment
    # Case 1
    if S[0] >=0 and S[1] >= 0:
        if (yH <= pointB[1]) and (xH <= pointB[0]):
            yH, xH = pointB[1], pointB[0]
        elif (yH >= pointC[1]) and (xH >= pointC[0]):
            yH, xH = pointC[1], pointC[0]
    elif S[0] <= 0 and S[1] <= 0:
        if (yH >= pointB[1]) and (xH >= pointB[0]):
            yH, xH = pointB[1], pointB[0]
        elif (yH <= pointC[1]) and (xH <= pointC[0]):
            yH, xH = pointC[1], pointC[0]
    # Case 2
    elif S[0] >= 0 and S[1] <= 0:
        if (yH >= pointB[1]) and (xH <= pointB[0]):
            yH, xH = pointB[1], pointB[0]
        elif (yH <= pointC[1]) and (xH >= pointC[0]):
            yH, xH = pointC[1], pointC[0]
    elif S[0] <= 0 and S[1] >= 0:
        if (yH <= pointB[1]) and (xH >= pointB[0]):
            yH, xH = pointB[1], pointB[0]
        elif (yH >= pointC[1]) and (xH <= pointC[0]):
            yH, xH = pointC[1], pointC[0]
    
    return (xH, yH)






if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t   Ortho-projection\n\n")  
    
    
# =============================================================================
#     1/ Create the figure
# =============================================================================
    plt.style.use('seaborn-darkgrid')
    plt.figure(num=None, figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
    
    print("1/ Draw the line / route")
    pointB = (2, 2)         # extremity of the route
    pointC = (3, 3)
    pointA = (0, 3)         # random point
    
    
# =============================================================================
#     2/ First situation
# =============================================================================
    print("2/ First Scenario")
    print("\t2.1/ First situation")
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 1)
    ax.set_xticklabels([])
    plt.title("Ortho-Projection : Case 1.1", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [0, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 5], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=4, frameon=True)
    plt.ylabel("y")
    plt.axis("equal")

    
# =============================================================================
#     3/ Second Situation
# =============================================================================
    print("\t2.2/ Second Situation")
    pointA = (2, 0)
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.title("Ortho-Projection : Case 1.2", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [0, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 5], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=4, frameon=True) 
    plt.axis("equal")
    
    
# =============================================================================
#     4/ Third Situation
# =============================================================================
    print("\t2.3/ Third Situation")
    pointA = (4.5, 4)
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.title("Ortho-Projection : Case 1.3", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [0, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 5], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=4, frameon=True) 
    plt.axis("equal")
    
    
# =============================================================================
#     5/ Fourth Situation
# =============================================================================
    print("\t2.4/ Fourth Situation")
    pointA = (3, 4)
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 4)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.title("Ortho-Projection : Case 1.4", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [0, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 5], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=4, frameon=True) 
    plt.axis("equal")
    
    
    
# =============================================================================
#     6/ First situation
# =============================================================================
    print("3/ Second Scenario")
    pointB = (2, 3)         # extremity of the route
    pointC = (3, 2)
    pointA = (0, 3)         # random point
    
    print("\t3.1/ First situation")
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 5)
    plt.title("Ortho-Projection : Case 2.1", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [5, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 0], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=1, frameon=True) 
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")

    
# =============================================================================
#     7/ Second Situation
# =============================================================================
    print("\t3.2/ Second Situation")
    pointA = (3, 1)
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 6)
    ax.set_yticklabels([])
    plt.title("Ortho-Projection : Case 2.2", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [5, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 0], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=1, frameon=True)
    plt.xlabel("x")
    plt.axis("equal")
    
    
# =============================================================================
#     8/ Third Situation
# =============================================================================
    print("\t3.3/ Third Situation")
    pointA = (2, 4)
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 7)
    ax.set_yticklabels([])
    plt.title("Ortho-Projection : Case 2.3", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [5, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 0], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=1, frameon=True) 
    plt.xlabel("x")
    plt.axis("equal")
    
    
    
# =============================================================================
#     9/ Fourth Situation
# =============================================================================
    print("\t3.4/ Fourth Situation")
    pointA = (4, 2)
    # Non-corrected projection
    S = slope(pointB, pointC)
    xH, yH = orthoProj(pointA, pointB, S)
    
    ax = plt.subplot(2, 4, 8)
    ax.set_yticklabels([])
    plt.title("Ortho-Projection : Case 2.4", fontweight="bold")
    
    # Plot the segment and its extension
    plt.plot([pointB[0], pointC[0]], [pointB[1], pointC[1]], color="black", zorder=3, label="Segment")
    plt.plot([0, pointB[0]], [5, pointB[1]], color="darkgray", zorder=2, linestyle='--', label="Segment Extension")
    plt.plot([pointC[0], 5], [pointC[1], 0], color="darkgray", zorder=2, linestyle='--')
    plt.scatter(pointB[0], pointB[1], color="black", marker='x', zorder=3)
    plt.scatter(pointC[0], pointC[1], color="black", marker='x', zorder=3)
    
    plt.scatter(pointA[0], pointA[1], color='black', zorder=3, label="Original Point")
    plt.scatter(xH, yH, color="darkcyan", zorder=4, label="Projected Point")
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, linestyle='--', label="Default Projection")
    
    # Corrected projection
    xH, yH = orthoProjSegment(pointA, pointB, pointC)
    plt.scatter(xH, yH, color="darkcyan", zorder=4)
    plt.plot([pointA[0], xH], [pointA[1], yH], color="skyblue", zorder=2, label="Corrected Projection")
        
    plt.legend(loc=1, frameon=True) 
    plt.xlabel("x")
    plt.axis("equal")
       
    plt.tight_layout()
    # plt.savefig("../../../img/ortho_projection_model.png", dpi=600)
    
    
  
    
    
    
# =============================================================================
#     10/ Projection distance
# =============================================================================
    print("4/ Distance in geographic system")
    import pyproj
    geod = pyproj.Geod(ellps='WGS84')
    lon0, lat0, lon1, lat1 = 4.8396232, 45.7532804, 4.839917548464699, 45.75345336404514
    print("\tPoint 0 : (lat, lon) =", (lat0, lon0))
    print("\tPoint 1 : (lat, lon) =", (lat1, lon1))
    azimuth1, azimuth2, dist = geod.inv(lon0, lat0, lon1, lat1)
    print("\tPyproj distance for the WGS84 ellipsoid :", dist)
    
    dist_hav = distance_haversine((lat0, lon0), (lat1, lon1))
    print("\tHaversine distance :", dist_hav)
    print("\tDifference :", abs(dist - dist_hav))
    