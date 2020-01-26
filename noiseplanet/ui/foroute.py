# -*- coding: utf-8 -*-

# Created on Thu Dec 5 16:49:20 2019

# @author: arthurd

"""
FoRoute Module.

Visualize Map Matching routes on HTML maps.
"""

from matplotlib import collections as mc
import matplotlib.pyplot as plt
import osmnx as ox
import webbrowser
import folium
import numpy as np

import noiseplanet.matcher as matching


def linesProjection(track, track_corr):
    lines = []
    if len(track) != len(track_corr):
        print("\n>>> WARNING:",
              "\nAn error occured while drawing lines for each projection.",
              "\nPlease make sure the dimensions of your original track and corrected one are equals.")
    else:
        lines = [[(track[i][1], track[i][0]), (track_corr[i][1], track_corr[i][0])] for i in range(len(track))]
    return lines


def plot_graph(track, track_corr=[],
             track_color="black", track_corr_color="darkcyan",
             route_color="black", route_corr_color="darkcyan",
             track_size=20, track_corr_size=20,
             track_marker="x", track_corr_marker="x",
             proj=False, proj_color="skyblue", proj_size=1, proj_alpha=1,
             route_corr=np.array([[None, None]]),
             route_size=4, route_corr_size=4, route_opacity=.6,
             title_fig="", title_color="#999999", title_fontweight="bold"
             ):
    """
    Create a matplotlib graph of the map matching algorithm.

    Parameters
    ----------
    graph : NetworkX MultiDiGraph
        Graph of the area.
    track : TYPE
        DESCRIPTION.
    track_corr : TYPE, optional
        DESCRIPTION. The default is [].
    track_color : TYPE, optional
        DESCRIPTION. The default is "black".
    track_corr_color : TYPE, optional
        DESCRIPTION. The default is "darkcyan".
    route_color : TYPE, optional
        DESCRIPTION. The default is "black".
    route_corr_color : TYPE, optional
        DESCRIPTION. The default is "darkcyan".
    track_size : TYPE, optional
        DESCRIPTION. The default is 20.
    track_corr_size : TYPE, optional
        DESCRIPTION. The default is 20.
    track_marker : TYPE, optional
        DESCRIPTION. The default is "x".
    track_corr_marker : TYPE, optional
        DESCRIPTION. The default is "x".
    proj : TYPE, optional
        DESCRIPTION. The default is False.
    proj_color : TYPE, optional
        DESCRIPTION. The default is "skyblue".
    proj_size : TYPE, optional
        DESCRIPTION. The default is 1.
    proj_alpha : TYPE, optional
        DESCRIPTION. The default is 1.
    route_corr : TYPE, optional
        DESCRIPTION. The default is np.array([[None, None]]).
    route_size : TYPE, optional
        DESCRIPTION. The default is 4.
    route_corr_size : TYPE, optional
        DESCRIPTION. The default is 4.
    route_opacity : TYPE, optional
        DESCRIPTION. The default is .6.
    title_fig : TYPE, optional
        DESCRIPTION. The default is "".
    title_color : TYPE, optional
        DESCRIPTION. The default is "#999999".
    title_fontweight : TYPE, optional
        DESCRIPTION. The default is "bold".

    Returns
    -------
    None.
    """
    
    fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=20, annotate=True, margin=0, show=False, close=False)
    plt.title(title_fig, color=title_color, fontweight=title_fontweight)

    # add track points
    plt.scatter(track[:][1], track[:][0], s=track_size, marker=track_marker, color=track_color)
    ax.scatter(track_corr[:][1], track_corr[:][0], s=track_corr_size, marker=track_corr_marker, color=track_corr_color)
    # plot the route
    ax.plot(track[:][1], track[:][0], marker='x', linewidth=route_size, alpha=.7, color=route_color)
    ax.plot(route_corr[:][1], route_corr[:][0], linewidth=route_corr_size, alpha=.7, color=route_corr_color)

    #projection between the two tracks
    if proj:
        lines_proj_HMM = linesProjection(track, track_corr)
        lc = mc.LineCollection(lines_proj_HMM, colors=proj_color, alpha=proj_alpha, linewidths=proj_size)
        ax.add_collection(lc)
        
    return fig, ax


def plot_html(track, track_corr=[],
             track_color="black", track_corr_color="darkcyan",
             track_size=2, track_corr_size=2,
             route_corr=[],
             route_size=2, route_corr_size=2,
             route_color="black", route_corr_color="darkcyan",
             route_opacity=.6, route_corr_opacity=.6,
             proj=False, proj_color="skyblue", proj_size=1, proj_alpha=1,
             show_graph=False, graph=None,
             file_name="my_map.html", save=True
             ):
    """
    

    Parameters
    ----------
    track : TYPE
        DESCRIPTION.
    track_corr : TYPE, optional
        DESCRIPTION. The default is [].
    track_color : TYPE, optional
        DESCRIPTION. The default is "black".
    track_corr_color : TYPE, optional
        DESCRIPTION. The default is "darkcyan".
    track_size : TYPE, optional
        DESCRIPTION. The default is 2.
    track_corr_size : TYPE, optional
        DESCRIPTION. The default is 2.
    route_corr : TYPE, optional
        DESCRIPTION. The default is [].
    route_size : TYPE, optional
        DESCRIPTION. The default is 2.
    route_corr_size : TYPE, optional
        DESCRIPTION. The default is 2.
    route_color : TYPE, optional
        DESCRIPTION. The default is "black".
    route_corr_color : TYPE, optional
        DESCRIPTION. The default is "darkcyan".
    route_opacity : TYPE, optional
        DESCRIPTION. The default is .6.
    route_corr_opacity : TYPE, optional
        DESCRIPTION. The default is .6.
    proj : TYPE, optional
        DESCRIPTION. The default is False.
    proj_color : TYPE, optional
        DESCRIPTION. The default is "skyblue".
    proj_size : TYPE, optional
        DESCRIPTION. The default is 1.
    proj_alpha : TYPE, optional
        DESCRIPTION. The default is 1.
    show_graph : TYPE, optional
        DESCRIPTION. The default is False.
    graph : TYPE, optional
        DESCRIPTION. The default is None.
    file_name : TYPE, optional
        DESCRIPTION. The default is "my_map.html".
    save : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    my_map : TYPE
        DESCRIPTION.

    """
        # Create an interactive HTML map with Open Street Map showing the track

        # :param track: GPS track, containing the coordinates for each points.
        #         The latitude is the first index of the coordinates,
        #         followed by the longitude : coord = [lat, lon]
        #         Example :  track = [[lat1, lon1],
        #                             [lat2, lon2],
        #                             [lat3, lon3],
        #                             ...
        #                             [latn, lonn]]
        # type track: list (two columns, n lines)
        # :param track_corr: Corrected track. This track need to have the same
        #         length than 'track', and in the same format (ie [lat, lon]).
        # type track_corr: list (two columns, n rows)
        # :param track_color: Color of the track.
        # type track_color: String
        # :param track_corr_color: Color of the corrected track.
        # type track_color: String
        # :param track_size: Size for each GPS points of the track.
        # type track_size: float
        # :param track_corr_size: Size for each points of the corrected track.
        # type track_corr_size: float
        # :param route_corr: Route of the corrected path, linking edges together.
        #         Format : [lat, lon]
        # type route_corr: numpy.array like
        # :param route_size: Size of the main route.
        # type route_size: float
        # :param route_corr_size: Size of the corrected route.
        # type route_corr_size: float
        # :param route_color: Color of the main route.
        # type route_color: String
        # :param route_corr_color: Color of the corrected route.
        # type route_corr_color: String
        # :param route_opacity: Opacity of the main route.
        # type route_opacity: float
        # :param route_corr_opacity: Opacity of the corrected route.
        # type route_corr_opacity: float
        # :param proj: Draw the projection from track's point to the corrected ones.
        # type proj: boolean
        # :param proj_color: Color of the projection lines.
        # type proj_color: String
        # :param proj_size: Size of the projection lines.
        # type proj_size: float
        # :param proj_alpha: Opacity of the projection lines.
        # type proj_alpha: float
        # :param file_name: Name or path to save the HTML file
        # type file_name: String
        # :param show_graph: Show the OSMNX graph on top of the OSM layer.
        # type show_graph: boolean

        # return: folium maps


    med_lat = track[len(track)//2][0]
    med_lon = track[len(track)//2][1]

    # Load map centred on central coordinates
    my_map = folium.Map(location=[med_lat, med_lon], zoom_start=20)

    if show_graph or graph is not None:
        if graph is None:
            graph = matching.graph_from_track(track, network='drive')
        my_map = ox.plot_graph_folium(graph, popup_attribute='name', edge_width=1, edge_color='darkgrey')

        
        
        
    if proj:
        for i in range(len(track)):
            folium.PolyLine([(track[i][0], track[i][1]), (track_corr[i][0], track_corr[i][1])],
                            color=proj_color, weight=proj_size, opacity=proj_alpha).add_to(my_map)
    # If the route is given in input, plot both (original and corrected)
    if len(route_corr) > 0:
        # add lines
        folium.PolyLine(track, color=route_color, weight=route_size, opacity=route_opacity).add_to(my_map)
        folium.PolyLine(route_corr, color=route_corr_color, weight=route_corr_size, opacity=route_corr_opacity).add_to(my_map)


    # add dots
    for i in range(len(track)):
        folium.CircleMarker(location=[track[i][0], track[i][1]],
                            radius=track_size,
                            weight=1,
                            color=track_color,
                            fill=True,
                            fill_opacity=1).add_to(my_map)
    for i in range(len(track_corr)):
        folium.CircleMarker(location=[track_corr[i][0], track_corr[i][1]],
                            radius=track_corr_size,
                            weight=1,
                            color=track_corr_color,
                            fill=True,
                            fill_opacity=1).add_to(my_map)


    # add the OSM light grey background
    folium.TileLayer('cartodbpositron').add_to(my_map)

    # plot the legend in the HTML page
    legend_html = """
    <div style="position: fixed;
                width: 210px;
                top: 10px; right: 10px;
                border: 2px solid lightgrey;
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.85);
                z-index:9999;
                font-size: 15px; color: slategrey;
     ">
         &nbsp; <span style="font-weight: bold">Legend</span>
         <br>
             &nbsp; Original Point &nbsp;
             <i class="fa fa-circle"
                 style="float: right;
                         margin-right: 19px; margin-top: 4px;
                         color: black">
             </i>
         <br>
             &nbsp; Projected Point &nbsp;
             <i class="fa fa-circle"
                 style="float: right;
                         margin-right: 19px; margin-top: 4px;
                         color: darkcyan">
             </i>
         <br>
             &nbsp; Projection &nbsp;
             <div class="line"
                 style="float: right;
                         margin-right: 10px; margin-top: 10px;
                         width: 30px; height: 2px;
                         background-color: skyblue">
             </div>
    </div>
    """
    my_map.get_root().html.add_child(folium.Element(legend_html))

    if save:
        my_map.save(file_name)
        # Plot in new tab
        webbrowser.open(file_name, new=2)  # open in new tab

    return my_map
