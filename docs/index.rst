.. toctree::
   :maxdepth: 2
   :caption: Contents:


========================================
Welcome to Noise Planet's documentation!
========================================

Python for map matching and mapping GeoJson tracks.
This library is a project within the research center UMR-AE/CNRS, working on NoisePlanet for noise mapping. 
Made in collaboration with the *École Nationale des Sciences Géographiques.*

**Citation :** Dujardin, A., Mermet, S. (2020). État de l’art et suggestions pour la cartographie des données acoustiques mobiles. *Projet de recherche.*


============
Dependencies
============

Packages
========

* numpy,
* pandas,
* json,
* osmnx,
* leuvenmapmatching, *KU Leuven - DTAI Research Group, Sirris - Elucidata Group.*

Optional packages
=================

* matplotlib,
* folium,
* sqlite3.

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

If you want to participate to the improvement of this project, clone the repository and open it as a project. We used spyder to create the packages and modules.

Structure
=========

**NoisePlanet** is composed by internal sub-packages:

* matcher lets you correct tracks and match it to the Open Street Map network,
* utils mainly handles conversion from geojson, metadata etc. to DataFrame,
* io handles reading and writing files,
* db lets you access a SQLite3 database.
* ui is used to generate Leaflet maps,

=======
Example
=======




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