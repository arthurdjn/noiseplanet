
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

    import numpy as np
    import osmnx as ox
    from noiseplanet import matching

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

    graph = matching.model.graph_from_track(track)

    track_coor, route_corr, edgeid, stats = matching.match(graph, track, method='hmm')


And visualize the results :

from noiseplanet.ui import plot_html

.. code-block:: python

    # Plot the graph
    plot_html(track, track_corr=track_corr, route_corr=route_corr,
            proj=True, show_graph=True)
            


.. image:: ../../img/track_hmm.png
   :width: 500
   :alt: alternate text
   :align: center


You can change the matching method.
For example, the above method uses Hidden Markov Models, and is the best way to match a track on the OSM (see the report for more details).
However, you can use a naive method to match the track on the nearest road :

.. code-block:: python

    track_coor, route_corr, edgeid, stats = matcher.match(graph, track, method='nearest')


And visualize the results :


.. code-block:: python

    from noiseplanet.ui import plot_html

    # Plot the graph
    plot_html(track, track_corr=track_corr, route_corr=route_corr,
            proj=True, show_graph=True)



.. image:: ../../img/track_nearest.png
   :width: 500
   :alt: alternate text
   :align: center