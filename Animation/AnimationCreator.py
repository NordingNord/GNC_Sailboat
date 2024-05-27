import pandas as pd
import array
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import numpy as np
import math
from celluloid import Camera
from tqdm import tqdm
import time

st = time.time()

#Load data
data = pd.read_excel('AutoRouteSquare.xlsx')

#Arrays and consts:
waypoints_x = [50,50,-50,-50,0]
waypoints_y = [50,-50,-50,50,0]

#waypoints_x = [50,0,50,50,-50]
#waypoints_y = [0,0,0,50,0]

#waypoints_x = [50,0,50,50,-50]
#waypoints_y = [0,0,0,50,0]


wind_dir = data['Wind_dir'].iloc[0]

Index_Next_Waypoint = []

pos_x = []
pos_y = []
rotation = []
button = []

boat_width = 3
boat_length = 6
track_line_list = []
prev_waypoint_index = 0

#Plot setup
fig = plt.figure()
ax = fig.add_subplot(111)
camera = Camera(fig)

ax.set_xlabel('X Position in meters')
ax.set_ylabel('Y Position in meters')

Last_state = 0
manual_lists = []
auto_lists = []
Current_list = []


#Extract the data
for i in range(len(data)):
    pos_x.append(data['Pos(1)'].iloc[i])
    pos_y.append(data['Pos(2)'].iloc[i])
    rotation.append(data['Rotation'].iloc[i])
    Index_Next_Waypoint.append(data['IndexPoint'].iloc[i])
    if 'Button' in data.columns:
        button.append(data['Button'].iloc[i])


#Animation loop
for i in tqdm(range(len(data)-1300)):
    #IF ANIMATION: COMMENT OUT ax.clear()
    ax.clear()
    ax.set_xlabel('X Position in meters')
    ax.set_ylabel('Y Position in meters')
    
    #Draw line between last and next waypoint
    next_waypoint_index = Index_Next_Waypoint[i]-1
    prev_waypoint_index = next_waypoint_index - 1
    if next_waypoint_index == 0:
        plt.plot([0, waypoints_x[next_waypoint_index]], 
                [0, waypoints_y[next_waypoint_index]], color='steelblue', linewidth=1)
    else:
        plt.plot([waypoints_x[prev_waypoint_index], waypoints_x[next_waypoint_index]], 
        [waypoints_y[prev_waypoint_index], waypoints_y[next_waypoint_index]], color='steelblue', linewidth=1)

    #Draw waypoints
    for points in range(len(waypoints_x)):
        ax.plot(waypoints_x[points], waypoints_y[points], marker='o', markersize=10, markeredgecolor="red", markerfacecolor="green")

    if button:
        if manual_lists:
            for lists in manual_lists:
                if lists:
                    x_coords, y_coords = zip(*lists)
                    ax.plot(x_coords, y_coords, linestyle='--', color='red', linewidth=1)

        if auto_lists:
            for lists in auto_lists:
                if lists:
                    x_coords, y_coords = zip(*lists)
                    ax.plot(x_coords, y_coords, linestyle='--', color='chartreuse', linewidth=1)

        if button[i] == False:
            if Last_state == 0:
                Current_list.append((pos_x[i], pos_y[i]))
                x_coords, y_coords = zip(*Current_list)
                ax.plot(x_coords, y_coords, linestyle='--', color='red', linewidth=1)
            else:
                auto_lists.append(Current_list)
                Current_list = []
                Last_state = 0

                Current_list.append((pos_x[i], pos_y[i]))
                x_coords, y_coords = zip(*Current_list)
                ax.plot(x_coords, y_coords, linestyle='--', color='red', linewidth=1)
        elif math.isnan(button[i]):
                Current_list.append((pos_x[i], pos_y[i]))
                x_coords, y_coords = zip(*Current_list)
                ax.plot(x_coords, y_coords, linestyle='--', color='red', linewidth=1)
        else:
            if Last_state == 0:
                manual_lists.append(Current_list)
                Current_list = []
                Last_state = 1

                Current_list.append((pos_x[i], pos_y[i]))
                x_coords, y_coords = zip(*Current_list)
                ax.plot(x_coords, y_coords, linestyle='--', color='chartreuse', linewidth=1)

            else:
                Current_list.append((pos_x[i], pos_y[i]))
                x_coords, y_coords = zip(*Current_list)
                ax.plot(x_coords, y_coords, linestyle='--', color='chartreuse', linewidth=1)
    else:
        track_line_list.append((pos_x[i], pos_y[i]))          
        x_coords, y_coords = zip(*track_line_list)
        ax.plot(x_coords, y_coords, linestyle='--', color='red', linewidth=1)

    #Draw boat with rotation
    rot = math.degrees(rotation[i])
    boat = patches.Rectangle((pos_x[i]-(boat_width/2), pos_y[i]-(boat_length/2)), boat_width, boat_length, color="blue",zorder=10)
    transformation = mpl.transforms.Affine2D().rotate_deg_around(pos_x[i], pos_y[i], rot) + ax.transData
    boat.set_transform(transformation)
    ax.add_patch(boat)

    # Draw arrow for wind direction
    arrow_length = 7
    offset = -5  # Adjust the offset distance here
    arrow_start_x = pos_x[i] + offset 
    arrow_start_y = pos_y[i]
    arrow_end_x = arrow_start_x + arrow_length * math.cos(math.radians(wind_dir+180))
    arrow_end_y = arrow_start_y + arrow_length * math.sin(math.radians(wind_dir+180))
    ax.annotate('', xy=(arrow_end_x, arrow_end_y), xytext=(arrow_start_x, arrow_start_y),
                arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->'))


    #Save each frame
    camera.snap()


#Animate the frames UNCOMMOENT ONLY IF YOU WANT TO SAVE ANIMATION
#nim = camera.animate()
#anim.save('test.mp4',dpi=300, fps=60)

#UNCOMMENT IF ONLY LAST FIGURE SHOULD BE SAVED
plt.savefig('SquareAuto2D.png')

et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')