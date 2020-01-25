.. toctree::
   :maxdepth: 2
   :caption: Contents:


========================================
Welcome to Noise Planet's documentation!
========================================

Overview
========

Python for map matching and mapping GeoJson tracks.
This library is a project within the research center UMR-AE/CNRS, working on NoisePlanet for noise mapping. 
Made in collaboration with the *École Nationale des Sciences Géographiques.*

**Citation :** Dujardin, A., Mermet, S. (2020). État de l’art et suggestions pour la cartographie des données acoustiques mobiles. *Projet de recherche.*

Study
=====

The Noise Planet platform can be found at : http://noise-planet.org/. 

Our study was focused and tested on Lyon. The dataset used is visible at : http://noise-planet.org/map_noisecapture/index.html#15/45.7578/4.8320/

===================================


============
Dependencies
============

Packages
========

* **numpy,**
* **pandas,**
* **json,**
* **osmnx,**
* **leuvenmapmatching,** *KU Leuven - DTAI Research Group, Sirris - Elucidata Group.*

Optional packages
=================

* **matplotlib,**
* **folium,**
* **sqlite3.**

Note that these packages are optional if you don't want to visualize the resulting maps. SQLite3 is used to stock all the informations of a geojson tracks or polygon into an SQL database.

============
Installation
============

To install, use :

``pip install noiseplanet``

If this doesn't work, clone the repository, and in the noiseplanet folder, use :

``pip install .``

===========
Development
===========

Getting Started
===============

If you want to participate to the improvement of this project, clone the repository and open it as a project. We used spyder to create the packages and modules.

Structure
=========

**NoisePlanet** is composed by internal sub-packages:

* **matcher** lets you correct tracks and match it to the Open Street Map network,
* **utils** mainly handles conversion from geojson, metadata etc. to DataFrame,
* **io** handles reading and writing files,
* **db** lets you access a SQLite3 database.
* **ui** is used to generate Leaflet maps,


======================================================

=======
Example
=======

Map Matching
============

The noiseplanet package provides different tools for matching a track to the Open Street Map network.

* matching to the **nearest edge**,
* **hmm** based matching. To match a track, composed by latitudes and longitudes, use :

Firt, import the following packages :

.. code-block:: python

    import numpy as np
    import osmnx as ox
    from noiseplanet import matcher


.. code-block:: python

    track = np.array([[45.7584882 ,  4.83585996],
                      [45.75848068,  4.83586747],
                      [45.75849549,  4.83585205],
                      [45.75849134,  4.83584647],
                      [45.75848135,  4.8358245 ],
                      # ...
                      [45.75846756,  4.83580848],
                      [45.75844998,  4.83580936],
                      [45.7584067 ,  4.83580086],
                      [45.7584067 ,  4.83580086],
                      [45.75839346,  4.83579883]])

    graph = matcher.model.graph_from_track(track)

    track_coor, route_corr, edgeid, stats = matcher.match(graph, track, method='nearest')


.. image:: ../img/track_nearest.png
   :width: 500
   :alt: alternate text
   :align: center

.. code-block:: python

    track_coor, route_corr, edgeid, stats = matcher.match(graph, track, method='nearest')

.. image:: ../img/track_hmm.png
   :width: 500
   :alt: alternate text
   :align: center



============================

========
Packages
========


matcher
=======

.. automodule:: noiseplanet.matcher.datacleaner
    :members:

.. automodule:: noiseplanet.matcher.matching
    :members:


model
=====

.. automodule:: noiseplanet.matcher.model.route
    :members:

.. automodule:: noiseplanet.matcher.model.nearest
    :members:

.. automodule:: noiseplanet.matcher.model.leuven
    :members:


utils
=====

.. automodule:: noiseplanet.utils.functions
    :members:

.. automodule:: noiseplanet.utils.oproj
    :members:

.. automodule:: noiseplanet.utils.hexgrid
    :members:


io
==

.. automodule:: noiseplanet.io.inputoutput
    :members:

db
==

.. automodule:: noiseplanet.db.connect
    :members:

.. automodule:: noiseplanet.db.commit
    :members:



==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`