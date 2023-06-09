from pyk4a import PyK4APlayback
import cv2
import argparse
from pyk4a_helpers import convert_to_bgra_if_required
from moviepy.editor import VideoFileClip


def info(playback: PyK4APlayback):
    #    number of captures
    total_captures = playback.length
    print(f"Total frames: {total_captures}\n")
    return total_captures

kinect_get_fps = lambda total_captures,total_duration_seconds: total_captures / total_duration_seconds

def extract_kinect_frame(playback,offset_in_sec,frame_rate):
    playback.seek(int(offset_in_sec * frame_rate))
    capture = playback.get_next_capture()
    color_image = convert_to_bgra_if_required(playback.configuration['color_format'],capture.color)
    depth_image = capture.depth
    return color_image, depth_image
def save_color_image(color_image, filename):
    cv2.imwrite(filename, color_image)
def save_depth_image(depth_image, filename):
    cv2.imwrite(filename, depth_image)

#Usage:
# color_image, depth_image = extract_kinect_frame(100, 'kinect.mkv')
# save_color_image(color_image, 'color.png')
# save_depth_image(depth_image, 'depth.png')
# Note: The depth image is saved as a 16-bit PNG file.
# Note: The color image is saved as a 24-bit PNG file.

parser = argparse.ArgumentParser()
parser.add_argument('--frame_num', type=int, default=100)
parser.add_argument('--kinect_file', type=str, required=True)
parser.add_argument('--color_file', type=str, required=True)
parser.add_argument('--depth_file', type=str, required=True)

#args = parser.parse_args()
#if __name__ == '__main__':

#    --frame_num 1800 --kinect_file /diskA/Temp_videos/dmitry/dmitry_test_1/1685459232_000704314112.mkv --color_file /diskB/data/tmp/color1800.png --depth_file /diskB/data/depth1800.png
offset_in_sec = 30
kinect_file = '/diskA/Temp_videos/dmitry/dmitry_test_1/1685459232_000704314112.mkv'
color_file = '/diskB/data/tmp/color1800.png'
depth_file = '/diskB/data/tmp/depth1800.png'



clip = VideoFileClip(kinect_file)
duration_seconds = clip.duration

playback = PyK4APlayback(kinect_file)
playback.open()
total_captures=info(playback)
frame_rate = kinect_get_fps(total_captures,duration_seconds)
print(f'Duration_seconds: {duration_seconds}\nFrame rate: {frame_rate}')

color_image, depth_image = extract_kinect_frame(playback,offset_in_sec,frame_rate)
playback.close()

save_color_image(color_image, color_file)
save_depth_image(depth_image, depth_file)


