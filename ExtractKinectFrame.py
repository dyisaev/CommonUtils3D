from pyk4a import PyK4APlayback
import cv2
import argparse
from pyk4a_helpers import convert_to_bgra_if_required,colorize,info



kinect_get_fps = lambda total_captures,total_duration_seconds: total_captures / total_duration_seconds

def extract_kinect_frame(playback,offset_in_sec):
    playback.seek(int(offset_in_sec * 10**6))
    capture = playback.get_next_capture()
    if capture.color is not None:
        color_image = convert_to_bgra_if_required(playback.configuration["color_format"], capture.color)
    else:
        print(f'Color image is not available at {offset_in_sec} seconds')
        color_image = None
    if capture.depth is not None:
        depth_image = colorize(capture.depth, (None, 5000))
    else:
        print(f'Depth image is not available at {offset_in_sec} seconds')
        depth_image = None
    return color_image, depth_image

def save_color_image(color_image, filename):
    cv2.imwrite(filename, color_image)
def save_depth_image(depth_image, filename):
    cv2.imwrite(filename, depth_image)


parser = argparse.ArgumentParser()
parser.add_argument('--sec', type=float, required = True)
parser.add_argument('--kinect_file', type=str, required=True)
parser.add_argument('--color_file', type=str, required=True)
parser.add_argument('--depth_file', type=str, required=True)

#args = parser.parse_args()
if __name__ == '__main__':

    args=parser.parse_args()
    playback = PyK4APlayback(args.kinect_file)
    playback.open()
    total_captures=info(playback)
    color_image, depth_image = extract_kinect_frame(playback,args.sec)
    playback.close()

    save_color_image(color_image, args.color_file)
    save_depth_image(depth_image, args.depth_file)


