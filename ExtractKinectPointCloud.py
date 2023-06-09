from pyk4a import PyK4APlayback, ColorResolution, DepthMode
import open3d as o3d
import numpy as np
import argparse
from pyk4a_helpers import info

def extract_kinect_pointcloud(playback,offset_in_sec,zaxis_threshold):
    playback.seek(int(offset_in_sec * 10**6))
    capture = playback.get_next_capture()
    if capture.depth is not None:
        point_cloud = capture.transformed_depth_point_cloud.reshape(-1, 3)
        relevant_indices = np.where(point_cloud[:,2] < zaxis_threshold)[0]
        point_cloud = point_cloud[relevant_indices,:]
        o3d_point_cloud = o3d.geometry.PointCloud()
        o3d_point_cloud.points = o3d.utility.Vector3dVector(point_cloud)
    else:
        print(f'Depth image is not available at {offset_in_sec} seconds')
        o3d_point_cloud = None
    return o3d_point_cloud

parser = argparse.ArgumentParser()
parser.add_argument('--sec', type=float, required = True)
parser.add_argument('--kinect_file', type=str, required=True)
parser.add_argument('--pointcloud_file', type=str, required=True)
parser.add_argument('--zaxis_threshold', type=float, required=True)


#args = parser.parse_args()
if __name__ == '__main__':

    args=parser.parse_args()
    playback = PyK4APlayback(args.kinect_file)
    playback.open()
    total_captures=info(playback)
    kinect_point_cloud = extract_kinect_pointcloud(playback,args.sec,args.zaxis_threshold)
    playback.close()

    o3d.io.write_point_cloud(args.pointcloud_file, kinect_point_cloud)
