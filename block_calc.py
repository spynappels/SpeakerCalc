#!/usr/bin/python3
import numpy as np
from math import sqrt, log, atan, degrees
import evid42_2k
import evid62_2k
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import config

# path length function
def path_length_calc(fl,hght):
    floor = float(fl)
    height = float(hght)
    path = sqrt((floor**2)+(height**2))
    return(path)

# path loss function
def path_loss_calc(path):
    loss = abs(20*log(1/path,10))
    return(loss)

# floor length function
def floor_length_calc(x, y):
    length = sqrt((x**2)+(y**2))
    return(length)

# horizontal angle cal
def hor_angle_calc(x, y):
    hor = int(degrees(atan(y/x)))
    return(hor)

# Off-axis loss calculation
def axis_loss_calc(horangle, vertangle, speaker_type):
    hor = int(horangle)
    if hor < 0:
        raw_ha = 360+hor
    else:
        raw_ha = hor
    rem = (raw_ha % 2.5)
    if rem == 0:
        hor_ang = raw_ha
    elif rem < 1.25:
        hor_ang = raw_ha-rem
    else:
        hor_ang = raw_ha+(2.5-rem)
    if speaker_type == 0:
        horizontal_loss = abs(evid42_2k.horizontal[hor_ang])
    elif speaker_type == 1:
        horizontal_loss = abs(evid62_2k.horizontal[hor_ang])
    vert = int(vertangle)
    if vert < 0:
        raw_va = 360+vert
    else:
        raw_va = vert
    rem = (raw_va % 2.5)
    if rem == 0:
        vert_ang = raw_va
    elif rem < 1.25:
        vert_ang = raw_va-rem
    else:
        vert_ang = raw_va+(2.5-rem)
    if speaker_type == 0:
        vertical_loss = abs(evid42_2k.vertical[vert_ang])
    elif speaker_type == 1:
        vertical_loss = abs(evid62_2k.vertical[vert_ang])
    loss = (horizontal_loss+vertical_loss)
    return(loss)

# Calculate Speaker SPL function
def calculate_speaker_spl(x,y):
    xc = x_preload+x
    yc = abs(y-speaker_y)
    floor_length = floor_length_calc(xc,yc)
    path_length = path_length_calc(floor_length,speaker_height)
    path_loss = path_loss_calc(path_length)
    horangle = hor_angle_calc(xc,yc)
    vertangle = int(degrees(atan(speaker_height/xc)))-speaker_angle
    axis_loss = axis_loss_calc(horangle, vertangle, speaker_type)
    #print("Path Length: "+str(np.round(path_length,2))+"m")
    #print("Path Loss: "+str(np.round(path_loss,1))+"dB")
    #print("Horizontal Angle: "+str(horangle)+"deg")
    #print("Vertical Angle: "+str(vertangle)+"deg")
    #print("Axis Loss: "+str(axis_loss)+"dB")
    total_loss = path_loss + axis_loss
    #print("Total Loss: "+str(np.round(total_loss,1))+"dB")
    speaker_spl = tgt_min_spl + total_loss
    return(speaker_spl)

# Calculate Seat SPL given a speaker SPL
def calculate_seat_spl(x,y,speaker_spl):
    xc = x_preload+x
    yc = abs(y-speaker_y)
    floor_length = floor_length_calc(xc,yc)
    path_length = path_length_calc(floor_length,speaker_height)
    path_loss = path_loss_calc(path_length)
    horangle = hor_angle_calc(xc,yc)
    vertangle = int(degrees(atan(speaker_height/xc)))-speaker_angle
    axis_loss = axis_loss_calc(horangle, vertangle, speaker_type)
    total_loss = path_loss + axis_loss
    seat_spl = speaker_spl - total_loss
    return(seat_spl)

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):


    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):


    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


# define variables
seat_width = config.seat_width
seat_pitch = config.seat_pitch
seats = config.seats
rows = config.rows
# speaker data
speaker_type = config.speaker_type
speaker_x = config.speaker_x
speaker_y = config.speaker_y
x_preload = config.first_row
speaker_height = config.speaker_height
aim_row = config.aim_row

tgt_min_spl = config.tgt_min_spl
heatmap_array = []

seat_labels = [ "Seat 1", "Seat 2", "Seat 3", "Seat 4", "Seat 5", "Seat 6", "Seat 7", "Seat 8"
          , "Seat 9", "Seat 10", "Seat 11", "Seat 12", "Seat 13", "Seat 14"]
row_labels = [ "Row 1", "Row 2", "Row 3", "Row 4", "Row 5", "Row 6", "Row 7", "Row 8",
         "Row 9", "Row 10", "Row 11", "Row 12" ]

y_coords = np.linspace(np.round((seat_width/2), 2), (np.round((seat_width/2), 2)+((seats-1)*seat_width)), seats)
#print(y_coords[len(y_coords)-1])
x_coords = np.linspace(np.round((seat_pitch/2), 2), (np.round((seat_pitch/2), 2)+((rows-1)*seat_pitch)), rows)
#print(x_coords)
speaker_angle = int(degrees(atan(speaker_height/(x_preload+x_coords[len(x_coords)-1]))))
print("Speaker Angle: "+str(speaker_angle)+"deg below horizontal.")
#Speaker SPL
speaker_spl = calculate_speaker_spl(x_coords[len(x_coords)-1],y_coords[len(y_coords)-1])
print("Calculated Speaker SPL is "+str(np.round(speaker_spl,1))+"dB-SPL.")

# Calculate Input Power
if speaker_type == 0:
    sensitivity = evid42_2k.sensitivity
elif speaker_type == 1:
    sensitivity = evid62_2k.sensitivity
power = int(10 ** ((speaker_spl - sensitivity)/10))
print("Calculated Speaker Power is "+str(np.round(power,1))+"W.")

for y in np.flip(y_coords):
    col = []
    for x in x_coords:
       col.append(calculate_seat_spl(x, y, speaker_spl))
    if len(heatmap_array)==0:
        heatmap_array = np.array(col)
    else:
        heatmap_array = np.vstack([heatmap_array, col])

#print(heatmap_array)
fig, ax = plt.subplots()

im, cbar = heatmap(heatmap_array, np.flip(seat_labels), row_labels, ax=ax,
                   cmap="YlGn", cbarlabel="SPL Level (dB-SPL)")
texts = annotate_heatmap(im, valfmt="{x:.1f}")
fig.set_size_inches(9,7)
#fig.tight_layout()
plt.show()        
