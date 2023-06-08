from pyk4a import PyK4APlayback
import cv2
import argparse

def extract_kinect_frame(frame_num, kinect_file):
    playback = PyK4APlayback(kinect_file)
    playback.open()
    playback.seek(frame_num)
    capture = playback.get_next_capture()
    color_image = cv2.imdecode(capture.color, cv2.IMREAD_COLOR)
    depth_image = capture.depth
    playback.close()
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
frame_num = 1800
kinect_file = '/diskA/Temp_videos/dmitry/dmitry_test_1/1685459232_000704314112.mkv'
color_file = '/diskB/data/tmp/color1800.png'
depth_file = '/diskB/data/tmp/depth1800.png'

color_image, depth_image = extract_kinect_frame(frame_num, kinect_file)
save_color_image(color_image, color_file)
save_depth_image(depth_image, depth_file)


