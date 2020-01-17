# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 21:47:43 2019

@author: arthurd
"""

from matplotlib import collections as mc
import matplotlib.pyplot as plt
import osmnx as ox
import webbrowser
import folium
import numpy as np

from utils import io
from model import mapmatching as mm

def linesProjection(track, track_corr):
    lines = []
    if len(track) != len(track_corr):
        print("\n>>> WARNING:",
              "\nAn error occured while drawing lines for each projection.",
              "\nPlease make sure the dimensions of your original track and corrected one are equals.")
    else:
        lines = [[(track[i][1], track[i][0]), (track_corr[i][1], track_corr[i][0])] for i in range(len(track))]
    return lines


def plot_graph(graph, track, track_corr=[],
             track_color="black", track_corr_color="darkcyan",
             route_color="black", route_corr_color="darkcyan",
             track_size=20, track_corr_size=20,
             track_marker="x", track_corr_marker="x",
             proj=False, proj_color="skyblue", proj_size=1, proj_alpha=1,
             route_corr=np.array([[None, None]]),
             route_size=4, route_corr_size=4, route_opacity=.6,
             title_fig="", title_color="#999999", title_fontweight="bold",
             save=True,
             filename="my_track.png", dpi=300):

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

    plt.show()

    if save:
        plt.savefig(filename, dpi=dpi)


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
        Create an interactive HTML map with Open Street Map showing the track

        :param track: GPS track, containing the coordinates for each points.
                The latitude is the first index of the coordinates,
                followed by the longitude : coord = [lat, lon]
                Example :  track = [[lat1, lon1],
                                    [lat2, lon2],
                                    [lat3, lon3],
                                    ...
                                    [latn, lonn]]
        type track: list (two columns, n lines)
        :param track_corr: Corrected track. This track need to have the same
                length than 'track', and in the same format (ie [lat, lon]).
        type track_corr: list (two columns, n rows)
        :param track_color: Color of the track.
        type track_color: String
        :param track_corr_color: Color of the corrected track.
        type track_color: String
        :param track_size: Size for each GPS points of the track.
        type track_size: float
        :param track_corr_size: Size for each points of the corrected track.
        type track_corr_size: float
        :param route_corr: Route of the corrected path, linking edges together.
                Format : [lat, lon]
        type route_corr: numpy.array like
        :param route_size: Size of the main route.
        type route_size: float
        :param route_corr_size: Size of the corrected route.
        type route_corr_size: float
        :param route_color: Color of the main route.
        type route_color: String
        :param route_corr_color: Color of the corrected route.
        type route_corr_color: String
        :param route_opacity: Opacity of the main route.
        type route_opacity: float
        :param route_corr_opacity: Opacity of the corrected route.
        type route_corr_opacity: float
        :param proj: Draw the projection from track's point to the corrected ones.
        type proj: boolean
        :param proj_color: Color of the projection lines.
        type proj_color: String
        :param proj_size: Size of the projection lines.
        type proj_size: float
        :param proj_alpha: Opacity of the projection lines.
        type proj_alpha: float
        :param file_name: Name or path to save the HTML file
        type file_name: String
        :param show_graph: Show the OSMNX graph on top of the OSM layer.
        type show_graph: boolean

        return: folium maps
    """

    med_lat = track[len(track)//2][0]
    med_lon = track[len(track)//2][1]

    # Load map centred on central coordinates
    my_map = folium.Map(location=[med_lat, med_lon], zoom_start=20)

    if show_graph or graph is not None:
        if graph is None:
            graph = mm.graph_from_track(track, network='all')
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




if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t     Visualization\n\n")
# =============================================================================
#     1/ Plot one track
# =============================================================================
    print("1/ Test")


# =============================================================================
#     2/ Real track
# =============================================================================
    print("2/ Real track")
    import json

    trackname = 'track(101)'

    file_name_raw = '..\\..\\data\\track\\' + trackname + '.geojson'
    file_name_nearest = '..\\..\\data\\track_nearest\\' + trackname + '_nearest.geojson'
    file_name_hmm = '..\\..\\data\\track_hmm\\' + trackname + '_hmm.geojson'

    with open(file_name_raw) as f:
        geojson_raw = json.load(f)
    with open(file_name_nearest) as f:
        geojson_nearest = json.load(f)
    with open(file_name_hmm) as f:
        geojson_hmm = json.load(f)

    # convert in dataframe
    df_raw = io.geojson_to_df(geojson_raw, extract_coordinates=True)
    df_nearest = io.geojson_to_df(geojson_nearest, extract_coordinates=True)
    df_hmm = io.geojson_to_df(geojson_hmm, extract_coordinates=True)

    # Fill None values by interpolation
    df_raw = df_raw.interpolate(method='quadratic', axis=0)
    df_nearest = df_nearest.interpolate(method='quadratic', axis=0)
    df_hmm = df_hmm.interpolate(method='quadratic', axis=0)

    # Delete rows where no positions
    df_raw = df_raw[df_raw['type'].notnull()]
    df_nearest = df_nearest[df_nearest['type'].notnull()]
    df_hmm = df_hmm[df_hmm['type'].notnull()]

    track_raw = np.column_stack((df_raw['latitude'].values, df_raw['longitude'].values))
    track_nearest = np.column_stack((df_nearest['latitude'].values, df_nearest['longitude'].values))
    track_hmm = np.column_stack((df_hmm['latitude'].values, df_hmm['longitude'].values))

    # track length
    print("\tTrack length :", len(track_raw))

    graph = mm.graph_from_track(track_raw)

    route_nearest, statesid_nearest, stats_nearest = mm.get_route_from_track(graph, track_nearest)
    route_hmm, statesid_hmm, stats_hmm = mm.get_route_from_track(graph, track_hmm)

    # plot
    plot_html(track_raw, track_corr=track_nearest, route_corr=route_nearest,
              proj=True,
              graph=graph,
              file_name='my_map_nearest_' + trackname + '.html'
              )

    plot_html(track_raw, track_corr=track_hmm, route_corr=route_hmm,
              proj=True,
              graph=graph,
              file_name='my_map_hmm_' + trackname + '.html'
              )


