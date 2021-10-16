import json

def load_json_snakes(fp):
    if not fp.lower().endswith(".json"):
        raise Exception("Json snake filename '{}' should end in '.json'".format(fp))

    with open(fp, "r") as f:
        data = json.load(f)
    snake_list = data["snakes"]
    metadata = data["metadata"]

    return snake_list, metadata

def save_json_snakes(fp, snake_list, offset_pixels, dims_pixels, pixel_size_um):
    """ Arguments:
    fp            - filepath to save json file
    snake_list    - list of snake points [{"pos": [x,y,z], "fg": ...}, {"pos": [x,y,z], ...}, ...]
    offset_pixels - [x,y,z] if this is a section of all snakes, this says where the box actually
                    starts within the tif image. If the snake coordinate system has its origin
                    at the origin of the original image coordinates, then offset should be [0,0,0]
    dims_pixels   - [xsize,ysize,zsize], the pixel dimensions of the 3D image region that
                    these snakes are made for.
    pixel_size_um - [dx,dy,dz], the micrometer spacing between pixels in x,y and z
    """

    if not fp.lower().endswith(".json"):
        raise Exception("Json snake filename '{}' should end in '.json'".format(fp))

    data = {
        "metadata": {
            "offset_pixels": offset_pixels,
            "dims_pixels": dims_pixels,
            "pixel_size_um": pixel_size_um,
        },
        "snakes": snake_list,
    }

    json_str = json.dumps(data)

    with open(fp, 'w') as f:
        f.write(json_str)