import open3d as o3d
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ply_file', type=str, required=True)
parser.add_argument('--voxel_size', type=float, required=False, default=5.00)

if __name__ == '__main__':
    args = parser.parse_args()
    # Load the point cloud data from the .ply file on the remote server
    point_cloud = o3d.io.read_point_cloud(args.ply_file)
    downsampled_point_cloud = point_cloud.voxel_down_sample(voxel_size=args.voxel_size)
    # Visualize the point cloud
    o3d.visualization.draw_geometries([downsampled_point_cloud])





