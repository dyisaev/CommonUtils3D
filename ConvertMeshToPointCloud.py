import open3d as o3d
import argparse
def convert_mesh_to_pointcloud(mesh, number_of_points):
    point_cloud = mesh.sample_points_uniformly(number_of_points=number_of_points)
    return point_cloud

parser = argparse.ArgumentParser()
parser.add_argument('--mesh_file', type=str, required=True)
parser.add_argument('--point_cloud_file', type=str, required=True)
parser.add_argument('--npoints', type=int, required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    mesh = o3d.io.read_triangle_mesh(args.mesh_file)
    point_cloud = convert_mesh_to_pointcloud(mesh, args.npoints)
    print (point_cloud)
    o3d.io.write_point_cloud(args.point_cloud_file, point_cloud)