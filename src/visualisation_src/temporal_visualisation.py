import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import ipywidgets as widgets
import os
import cv2

# ----------------------------------------------------------------------------------------

def plot_temporal_graphs(temporal_graphs):
    """
    :Function: Plot the dynamic temporal graphs on a map using a slider
    :param temporal_graphs: List of NetworkX Digraphs
    :return: Matplotlib plot with slider
    """
    # Create a figure and subplot
    fig, ax = plt.subplots()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    # Draw the first graph
    china.plot(ax=ax, color='white', edgecolor='black')
    colors = nx.get_edge_attributes(temporal_graphs[0], 'color').values()
    nx.draw(temporal_graphs[0], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), edge_color=colors,
            with_labels=False, node_size=1,
            node_color='red', width=0.5, ax=ax)
    ax.set_title(f"Temporal Graph at {0 // 1440}:{(0 // 60) % 24:02d}:{0 % 60:02d}")

    # Create a slider widget
    slider = widgets.IntSlider(min=0, max=len(temporal_graphs) - 1, value=0, description='Timeframe')

    # Define a function to update the plot when the slider is changed
    def update_plot(val):
        val = val['new']
        ax.clear()
        china.plot(ax=ax, color='white', edgecolor='black')
        colors = nx.get_edge_attributes(temporal_graphs[val], 'color').values()
        nx.draw(temporal_graphs[val], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), with_labels=False,
                node_size=1, node_color='red', edge_color=colors, width=0.5, ax=ax)
        ax.set_title(f"Temporal Graph at {val // 1440}:{(val // 60) % 24:02d}:{val % 60:02d}")
        plt.show()

    # Attach the update function to the slider
    slider.observe(update_plot, names='value')
    display(slider)
    plt.show()
    return [slider, plt]
    # # Display the slider widget and plot
    # display(slider)
    # plt.show()

# ----------------------------------------------------------------------------------------


def create_frames(temporal_graphs):
    """
    :Function: Create a list of frames for the dynamic temporal graphs
    :param temporal_graphs: List of NetworkX Digraphs
    :return: List of frames
    """
    path = "frames/"
    for i in range(len(temporal_graphs)):
        fig, ax = plt.subplots()
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        china = world[world['name'] == 'China']
        china.plot(ax=ax, color='white', edgecolor='black')
        colors = nx.get_edge_attributes(temporal_graphs[i], 'color').values()
        nx.draw(temporal_graphs[i], pos=nx.get_node_attributes(temporal_graphs[i], 'pos'), edge_color=colors,
                with_labels=False, node_size=0.5,
                node_color='red', width=1.5, ax=ax)
        ax.set_title(f"Temporal Graph")
        plt.savefig(path + f"{i}.png")
        plt.close()
        # free memory
        del fig
        del ax
        print(f"\rCreating frames: {i + 1}/{len(temporal_graphs)}", end="")

    return 1

# ----------------------------------------------------------------------------------------


def create_mp4():
    """
    :Function: Create a video from the frames
    :return: 1 if successful
    """
    frames_folder = 'frames/'
    frame_filenames = os.listdir(frames_folder)
    frame_filenames.sort(key=lambda x: int(x[:-4]))

    # Read the first frame to get its dimensions
    frame = cv2.imread(frames_folder + frame_filenames[0])
    height, width, layers = frame.shape

    # Create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('output.mp4', fourcc, 30, (width, height))

    # Loop through the frames and add them to the video
    i = 0
    for filename in frame_filenames:
        frame = cv2.imread(frames_folder + filename)
        video.write(frame)
        print(f"\r{i / 2764 * 100:.2f}%", end="")
        i += 1

    video.release()
    print('\nVideo saved as output.mp4')

    return 1
