import numpy as np
import tifffile
import PIL
from PIL import Image

def get_single_tiff_info(tiff_path):
    data = Image.open(tiff_path)
    shape = data.size
    stack_height = data.n_frames
    arr = np.array(data)
    dtype = str(arr.dtype)
    min_val = arr.min()
    max_val = arr.max()
    avg = np.average(arr)

    return shape, stack_height, dtype

# numpy arr should have (height,width,depth)
def save_3d_tif(fp,numpy_arr):
    # tifffile takes (depth,height,width)
    numpy_arr = np.swapaxes(numpy_arr,2,1)
    numpy_arr = np.swapaxes(numpy_arr,1,0)

    tifffile.imsave(fp,numpy_arr)

def open_tiff_as_np_arr(img_path):
    pil_img = Image.open(img_path)

    return pil_img_3d_to_np_arr(pil_img)

def pil_img_3d_to_np_arr(pil_img):
    frames = getattr(pil_img, "n_frames", 1)
    # If just one frame
    if frames == 1:
        arr_2d = np.array(pil_img)
        arr = np.zeros((pil_img.height,pil_img.width,frames),dtype=arr_2d.dtype)
        arr[:,:,0] = arr_2d
        return arr
    else:
        arr = np.zeros((pil_img.height,pil_img.width,frames),dtype=np.array(pil_img).dtype)
        for frame_idx in range(frames):
            pil_img.seek(frame_idx)
            arr[:,:,frame_idx] = np.array(pil_img)

        return arr