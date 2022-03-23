from flask import Flask, request, abort, jsonify
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_pixels():

    # Validate request formatting and datatypes. Abort if invalid.
    err_msg = validate_request(request)
    if err_msg:
        abort(400, err_msg)

    # Put inputs from request body into numpy arrays
    image_dimensions = np.array(request.json['image_dimensions'])
    corner_points = np.array(request.json['corner_points'])

    # Create x and y vectors for evenly spaced points within the rectangle
    corner_x = corner_points[:, 0]
    corner_y = corner_points[:, 1]

    # Additional validation of corner_points
    if (corner_x.min() == corner_x.max()) or (corner_y.min() == corner_y.max()):
        abort(400, 'Corner points must define a rectangle')
    norms = np.linalg.norm(corner_points - [corner_x.mean(), corner_y.mean()],
        axis=1)
    if any(norms != norms[0]):
        abort(400, 'Corner points must define a rectangle')

    # Assemble matrix of pixel coordinates, return as json
    pixels_x = np.linspace(corner_x.min(), corner_x.max(), image_dimensions[1])
    pixels_y = np.linspace(corner_y.min(), corner_y.max(), image_dimensions[0])
    pixels = [[[x, y] for x in pixels_x] for y in pixels_y[::-1]]
    return {'pixels': pixels}


def validate_request(r):
    """
    Validates that the request body is formatted correctly and contains the
    required key-value pairs. This function also checks the values for correct
    data type and dimensions. NOTE: Beyond formatting and datatypes, this
    function does not check that the input is actually corner points of a valid
    rectangle.

    Parameters
    r - Flask request object

    Returns
    error_msg (str) - Description of the error. Otherwise, returns None if
        validation succeeds.
    """
    # Request must be sent as json
    if not r.json:
        return 'Could not parse request'

    # Request missing required key, or value is the wrong datatype
    for key in ['image_dimensions', 'corner_points']:
        if key not in r.json.keys():
            return f'Required key {key} was missing from the request'
        if type(r.json[key]) not in (list, tuple):
            return f'Expected type list or tuple for parameter {key}'

    # Request must contain exacty 2 dimensions
    if len(r.json['image_dimensions']) != 2:
        return 'Expected 2 dimensions for parameter image_dimensions'

    # Dimensions must be of type int
    if not all([type(dim) == int for dim in r.json['image_dimensions']]):
        return 'The values provided in image_dimensions must be of type int'

    # Request must contain exactly 4 corner_points
    if len(r.json['corner_points']) != 4:
        return 'Expected 4 points for parameter corner_points'

    # Corner points must be exactly two dimensions
    if not all([len(pt) == 2 for pt in r.json['corner_points']]):
        return 'Corner points must each contain two dimensions'

    # All coords in corner_points must be of type int or float
    if not all([type(coord) in (int, float) for point in \
    r.json['corner_points'] for coord in point]):
        return 'All coordinates in corner_points must be of type int or float'


@app.errorhandler(400)
def error_bad_request(e):
    return jsonify(str(e)), 400
