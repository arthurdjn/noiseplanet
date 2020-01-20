# noiseplanet
#### Python for map matching and mapping geojson tracks

This library is a project within the research center *UMR-AE/CNRS*, working on NoisePlanet for noise mapping.
Made in collaboration with the *École Nationale des Sciences Géographiques*.

**Citation :** Dujardin, A., Mermet, S.(2020). État de l’art et suggestions pour la cartographie des données acoustiques mobiles. *Projet de recherche*.

## Overview

**noiseplanet** is a Python package that let you extract, correct, and plot geojson data on Leaflet maps.


## Installing
#### Dependencies
This module use several packages :
- **numpy**,
- **pandas**,
- **json**,
- **osmnx**,
- **leuvenmapmatching**, *KU Leuven - DTAI Research Group, Sirris - Elucidata Group*.

To install, use :
```
pip install noiseplanet
```
If this doesn't work, clone the repository, and in the *noiseplanet* folder, use :
```
pip install .
```

#### Optional dependencies

For plotting and interface, the following packages are used :
- **matplotlib**,
- **folium**,
- **sqlite3**.

Note that these packages are optional if you don't want to visualize the resulting maps. *SQLite3* is used to stock all the informations of a geojson tracks or polygon into an SQL database.


#### Development

If you want to participate to the improvement of this project, clone the repository and open it as a project. We used *spyder* to create the packages and modules.

#### Structure

*noiseplanet* is composed by internal sub-packages:
- **matching** let you correct tracks and match it to the *Open Street Map* network,
- **utils** mainly handles conversion from geojson, metadata etc. to *DataFrame*,
- **ui** is used to generate *Leaflet* maps,
- **io** handles reading and writing files,
- **db** let you access a *SQLite3* database.

### Usage

This project was created to provide new ways of mapping for the *UMR-AE/CNRS* team.

