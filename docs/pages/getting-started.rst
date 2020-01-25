
===============
Getting Started
===============


Dependencies
============

**Packages**

* **numpy,**
* **pandas,**
* **json,**
* **osmnx,**
* **leuvenmapmatching,** *KU Leuven - DTAI Research Group, Sirris - Elucidata Group.*

**Optional packages**

* **matplotlib,**
* **folium,**
* **sqlite3.**

Note that these packages are optional if you don't want to visualize the resulting maps. SQLite3 is used to stock all the informations of a geojson tracks or polygon into an SQL database.


Installation
============

To install, use :

``pip install noiseplanet``

If this doesn't work, clone the repository, and in the noiseplanet folder, use :

``pip install .``


Development
===========

If you want to participate to the improvement of this project, clone the repository and open it as a project. We used spyder to create the packages and modules.

Structure
=========

**NoisePlanet** is composed by internal sub-packages:

* **matcher** lets you correct tracks and match it to the Open Street Map network,
* **utils** mainly handles conversion from geojson, metadata etc. to DataFrame,
* **io** handles reading and writing files,
* **db** lets you access a SQLite3 database.
* **ui** is used to generate Leaflet maps,

