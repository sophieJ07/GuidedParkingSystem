# Part 1: importing libraries & set up global variables 

# matplotlib for illustration
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# dash for web app
from dash import html, dcc, Input, Output
import base64

# ArduinoCloudClient for Arduino Cloud 
import time
import logging
import asyncio
import numpy as np
import sys
sys.path.append("lib")
import nest_asyncio
nest_asyncio.apply()
from arduino_iot_cloud import ArduinoCloudClient

# Set entrance and original occupancy status 
entrance = (0, 0)
original_matrix = np.array([[False, False, False, False, False, False]])

# Define the positions in the 5x6 matrix that are sensor-equip
positions = [(0, 5), (1, 1), (2, 0), (3, 2), (4, 3)]

# Load the car icon
car_image_path = 'red_car.png'  
car_image = mpimg.imread(car_image_path)

######################################################################################
# Part 2: Functions for updating and generating parking lot visuals 

# Function to update matrix & illustration
def update():
  # Create a 5x6 grid of subplots with added space between rows
  fig, axs = plt.subplots(5, 6, figsize=(5, 10), gridspec_kw={'hspace': 0.7})

  # Loop over the grid and initially fill specified cells with highlighter color
  for row, col in positions:
      axs[row, col].set_facecolor('yellow')  

  # Place car image in all cells including the first cell (0,0)
  for i in range(5):
      for j in range(6):
          ax = axs[i, j]
          ax.set_xticks([])
          ax.set_yticks([])
          ax.spines['top'].set_visible(True)
          ax.spines['right'].set_visible(True)
          ax.spines['left'].set_visible(True)
          ax.spines['bottom'].set_visible(True)

          imagebox = OffsetImage(car_image, zoom=0.15)
          ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, box_alignment=(0.5, 0.5))
          ax.add_artist(ab)

  # Add an entrance label
  fig.text(-0.1, 0.95, 'Entrance', ha='center', va='center', fontsize=20, color='blue')

  # Highlight the borders and replace the car with an open green circle at specified positions if the status value is True
  for index, (row, col) in enumerate(positions):
    if original_matrix[0, index]:
        axs[row, col].clear()  # Clear the car image
        # Use a thicker stroke for the green circle
        circle = plt.Circle((0.5, 0.5), 0.3, color='lightgreen', fill=False, linewidth=4)  
        axs[row, col].add_artist(circle)
        axs[row, col].set_xticks([])  # Ensure no x-axis labels
        axs[row, col].set_yticks([])  # Ensure no y-axis labels
    else:
        imagebox = OffsetImage(car_image, zoom=0.15)
        ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, box_alignment=(0.5, 0.5))
        ax.add_artist(ab)

  plt.savefig('status.png', bbox_inches='tight') # save the illustration 
  draw_path_to_empty_spot(fig, axs) # call the next function to draw path

# Define the find_nearest_empty_spot function 
def find_nearest_empty_spot(positions, original_matrix):
    distances = []
    for index, (row, col) in enumerate(positions):
        if original_matrix[0, index]:
            distance = (0.167 * (row - entrance[0]) + 0.133 * (col - entrance[1]))
            distances.append((distance, index))

    if distances:
        _, nearest_index = min(distances, key=lambda x: x[0])
        return nearest_index
    else:
        return None

# Define the draw_path_to_empty_spot function 
def draw_path_to_empty_spot(fig, axs):
    nearest_empty_spot_index = find_nearest_empty_spot(positions, original_matrix)
    fig.lines.clear()

    # If there are no available spots
    if nearest_empty_spot_index is None:
        fig.text(0, 0.93, 'No Available Parking Spots.', ha='center', va='center', fontsize=16, color='red')
        plt.savefig('path.png', bbox_inches='tight')
        return  # Exit the function

    # Highlight the nearest empty spot by filling the entire box with green
    row, col = positions[nearest_empty_spot_index]
    axs[row, col].clear()  # Clear the subplot to remove any existing content (like images or circles)
    axs[row, col].set_facecolor('lightgreen')  # Fill the entire box with green
    axs[row, col].set_xticks([])  # Remove x-ticks
    axs[row, col].set_yticks([])  # Remove y-ticks
    axs[row, col].spines['top'].set_visible(True)  # Optionally, adjust visibility of the subplot borders
    axs[row, col].spines['right'].set_visible(True)
    axs[row, col].spines['left'].set_visible(True)
    axs[row, col].spines['bottom'].set_visible(True)

    # Find the final location of the the optimal path and draw path
    finalY = 0.91 - 0.167 * (row - entrance[0])
    finalX = 0.175 + 0.133 * (col - entrance[1])

    # Vertical Line
    vertical_line = plt.Line2D((-0.1, -0.1), (0.945, finalY), transform=fig.transFigure, figure=fig, color='green', linewidth=2.5)
    fig.lines.extend([vertical_line])

    # Horizontal Line
    horizontal_line = plt.Line2D((-0.1, finalX), (finalY, finalY), transform=fig.transFigure, figure=fig, color='green', linewidth=2.5)
    fig.lines.extend([horizontal_line])

    # Add a vertical arrow
    vertical_line = plt.Line2D((finalX, finalX), (finalY, finalY - 0.03), transform=fig.transFigure, figure=fig, color='green', linewidth=2.5)
    fig.lines.extend([vertical_line])

    plt.savefig('path.png', bbox_inches='tight') #save the illustration 

update()

######################################################################################
# Part 3: Dash app set up 

# Function to encode images to base64
def encode_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf8')

# Encode images
encoded_parking_image = encode_image("status.png")
encoded_parking_spots_image = encode_image("path.png")

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Parking Spot Finder", style={'textAlign': 'center'}),
    html.Div([
        html.Button("Find Spot", id="find-spot-btn", n_clicks=0, style={'fontSize': '20px', 'margin': '10px'}),
        html.Button("Refresh", id="refresh-btn", n_clicks=0, style={'fontSize': '20px', 'margin': '10px'})
    ], style={'textAlign': 'center'}),
    html.Img(id='parking-image', src=f'data:image/png;base64,{encoded_parking_image}', style={'width': '80%', 'height': 'auto', 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto'}),
], style={'textAlign': 'center', 'width': '40%'})

# Callback to update the displayed image based on button clicks
@app.callback(
    Output('parking-image', 'src'),
    [Input('find-spot-btn', 'n_clicks'), Input('refresh-btn', 'n_clicks')]
)

def update_image_src(find_clicks, refresh_clicks):
    if find_clicks > refresh_clicks:
        return f'data:image/png;base64,{encode_image("path.png")}'
    else:
        return f'data:image/png;base64,{encode_image("status.png")}'

######################################################################################
# Part 4: Set up Arduino Cloud Client

# Arduino IoT Cloud Thing "UserEnd"
DEVICE_ID = b"574903a4-ba42-41c2-aacb-ef41b219597f" 
SECRET_KEY = b"GFaB79rQ4n3y!lI#Q!QOLRGL0"

def logging_func():
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

# Callback functions for each spot 
def on_switch_changed_1(client, value):
    print("spot changed1: ", value)
    original_matrix[0, 0] = value
    update()

def on_switch_changed_2(client, value):
    print("spot changed2: ", value)
    original_matrix[0, 1] = value
    update()

def on_switch_changed_3(client, value):
    print("spot changed3: ", value)
    original_matrix[0, 2] = value
    update()

def on_switch_changed_4(client, value):
    print("spot changed4: ", value)
    original_matrix[0, 3] = value
    update()

def on_switch_changed_5(client, value):
    print("spot changed5: ", value)
    original_matrix[0, 4] = value
    update()

# Client initialization w/ asyncio event loop
async def start_iot_client():
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("spot1", on_write=on_switch_changed_1)
    client.register("spot2", on_write=on_switch_changed_2)
    client.register("spot3", on_write=on_switch_changed_3)
    client.register("spot4", on_write=on_switch_changed_4)
    client.register("spot5", on_write=on_switch_changed_5)
    print("finished registration, starting client")

    client.start() 

######################################################################################
# Part 5: Run
    
# Asynchronous function main()
async def main():
  app.run_server(port=8555, debug=False)
  await start_iot_client()

# Run the Dash app server and start the IoT client asynchronously 
if __name__ == '__main__':
    asyncio.run(main())

