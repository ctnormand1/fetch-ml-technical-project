from flask import Flask, request, abort
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_pixels():

    # Put inputs from request body into numpy arrays
    image_dimensions = np.array(request.json['image_dimensions'])
    corner_points = np.array(request.json['corner_points'])

    # Create x and y vectors for evenly spaced points within the rectangle
    corner_x = corner_points[:, 0]
    corner_y = corner_points[:, 1]
    pixels_x = np.linspace(corner_x.min(), corner_x.max(), image_dimensions[1])
    pixels_y = np.linspace(corner_y.min(), corner_y.max(), image_dimensions[0])

    # Assemble matrix of pixel coordinates, return as json
    pixels = [[[x, y] for x in pixels_x] for y in pixels_y[::-1]]
    return {'pixels': pixels}
