import open3d as o3d
import argparse

def draw_point_cloud_pair(pcd1, pcd2):
    pcd1.paint_uniform_color([1, 0.706, 0])
    pcd2.paint_uniform_color([0, 0.651, 0.929])
    o3d.visualization.draw_geometries([pcd1, pcd2],
                                      zoom=0.4559,
                                      front=[0.6452, -0.3036, -0.7011],
                                      lookat=[1.9892, 2.0208, 1.8945],
                                      up=[-0.2779, -0.9482, 0.1556])

parser = argparse.ArgumentParser()
parser.add_argument('--point_cloud_1', type=str, required=True, help='Path to the point cloud 1')
parser.add_argument('--point_cloud_2', type=str, required=True, help='Path to the point cloud 2')
parser.add_argument('--voxel_size', type=float, default=2.0, help='Voxel size for downsampling')

if __name__ == '__main__':
    args = parser.parse_args()
    pcd1 = o3d.io.read_point_cloud(args.point_cloud_1)
    pcd2 = o3d.io.read_point_cloud(args.point_cloud_2)

    pcd1 = pcd1.voxel_down_sample(voxel_size=args.voxel_size)
    pcd2 = pcd2.voxel_down_sample(voxel_size=args.voxel_size)
    pcd1.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    pcd2.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    

    draw_point_cloud_pair(pcd1, pcd2)