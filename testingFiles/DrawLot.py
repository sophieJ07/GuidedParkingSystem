# for testing parking lot status and path illustrations 

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

entrance = (0, 0)

original_matrix = np.array([[False, False, True, False, False, False]])

# Define the positions in the 5x6 matrix that will map to the original 1x6 matrix
positions = [(0, 5), (1, 1), (2, 0), (3, 2), (4, 3)]

# Load the uploaded car images
car_image_path = 'red_car.png'  # Regular car image
car_image = mpimg.imread(car_image_path)

# Create a 5x6 grid of subplots with added space between rows
fig, axs = plt.subplots(5, 6, figsize=(5, 10), gridspec_kw={'hspace': 0.7})

# Loop over the grid and initially fill specified cells with highlighter color
for row, col in positions:
    axs[row, col].set_facecolor('yellow')  

    # Place car image in all cells 
    for i in range(5):
      for j in range(6):
          ax = axs[i, j]
          ax.set_xticks([])
          ax.set_yticks([])
          ax.spines['top'].set_visible(True)
          ax.spines['right'].set_visible(True)
          ax.spines['left'].set_visible(True)
          ax.spines['bottom'].set_visible(True)

          # Use regular car image for all positions including (0,0)
          imagebox = OffsetImage(car_image, zoom=0.15)
          ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, box_alignment=(0.5, 0.5))
          ax.add_artist(ab)

# Add an entrance label
fig.text(-0.1, 0.95, 'Entrance', ha='center', va='center', fontsize=20, color='blue')

# Draw status
def draw_status():
  # Highlight the borders and replace the car with an open green circle at specified positions if the original value is True
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

# find_nearest_empty_spot function 
def find_nearest_empty_spot():
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

# draw_path_to_empty_spot function 
def draw_path_to_empty_spot():
    nearest_empty_spot_index = find_nearest_empty_spot()
    fig.lines.clear()

    # If there are no available spots
    if nearest_empty_spot_index is None:
        fig.text(0, 0.93, 'No Available Parking Spots.', ha='center', va='center', fontsize=16, color='red')
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

    
