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


=============
Dependencies
============

This module use several packages :

* numpy,
* pandas,
* json,
* osmnx,
* leuvenmapmatching, *KU Leuven - DTAI Research Group, Sirris - Elucidata Group.*

For plotting and interface, the following packages are used :

* matplotlib,
* folium,
* sqlite3.

Note that these packages are optional if you don't want to visualize the resulting maps. SQLite3 is used to stock all the informations of a geojson tracks or polygon into an SQL database.

===========
Instalation
===========

To install, use :

``pip install noiseplanet``

If this doesn't work, clone the repository, and in the noiseplanet folder, use :

``pip install .``

=======
Example
=======

===========
Development
===========

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