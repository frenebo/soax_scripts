from snakeutils.files import readable_dir
import os
import argparse
from PIL import Image

def slice_range(arg_str):
    split_by_dash = arg_str.split('-')

    if len(split_by_dash) != 2:
        raise argparse.ArgumentTypeError("Argument {} should have start and end slice index separated by one dash. Ex: '10-13'".format(arg_str))

    try:
        start = int(split_by_dash[0])
    except ValueError as e:
        raise argparse.ArgumentTypeError("Couldn't parse {} as integer in range {}: {}".format(split_by_dash[0],arg_str,str(e)))

    try:
        end = int(split_by_dash[1])
    except ValueError as e:
        raise argparse.ArgumentTypeError("Couldn't parse {} as integer in range {}: {}".format(split_by_dash[1],arg_str,str(e)))

    if end < start:
        raise argparse.ArgumentTypeError("Start slice index {} is greater than end {}".format(start,end))

    return start,end



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try some parameters for snakes')
    parser.add_argument('slice_range',type=slice_range,help="Range of TIF slices to keep. Ex 10-20 to keep slices 10-20, inclusive")
    parser.add_argument('source_dir',type=readable_dir,help="Directory where source tif files are")
    parser.add_argument('target_dir',type=readable_dir,help="Directory to save subslice tifs")

    args = parser.parse_args()

    start_slice,end_slice = args.slice_range
    new_n_frames = end_slice - start_slice + 1

    for src_tif_fn in os.listdir(args.source_dir):
        fp = os.path.join(args.source_dir,src_tif_fn)
        print("Processing {}".format(fp))

        pil_img = Image.open(fp)

        img_is_3d = getattr(pil_img, "n_frames", 1) != 1

        if not img_is_3d:
            raise Exception("Cannot slice {}, is not a 3D tif file".format(fp))

        if pil_img.n_frames < end_slice + 1:
            raise Exception("Can't take slices {}-{}, tif only has {} frames".format(start_slice,end_slice,pil_img.n_frames))

        new_img_arr = np.zeros((pil_img.height,pil_img.width,new_n_frames),dtype=np.array(pil_img).dtype)

        print("Extracting slices {}-{} from depth {} image")
        for frame_idx in range(start_slice,end_slice + 1):
            pil_img.seek(frame_idx)
            new_img_arr[:,:, frame_idx - start_slice] = np.array(pil_img)

        new_tif_fn = "{}-{}sliced_" + src_tif_fn
        new_fp = os.path.join(args.target_dir, new_tif_fn)
        print("Saving sliced image as {}".format(new_fp))

        tifffile.imsave(new_fp, new_img_arr)