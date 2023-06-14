# RANSAC Global Registration of two point clouds. Totally copied from tutorial on Open3D website.
# http://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html

import open3d as o3d
import numpy as np
import argparse
from pyk4a_helpers import save_transformation_to_txt

def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, required=True)
parser.add_argument('--target', type=str, required=True)
parser.add_argument('--voxel_size', type=float, required=False, default=5.00)
parser.add_argument('--output_transform', type=str, required=True)
parser.add_argument('--output_ply', type=str, required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    # Load the two point clouds
    source = o3d.io.read_point_cloud(args.source)
    target = o3d.io.read_point_cloud(args.target)
    voxel_size = args.voxel_size

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    result_ransac = execute_global_registration(source_down, target_down,
                                                source_fpfh, target_fpfh,
                                                voxel_size)
    
    print(result_ransac)
    source_transformed=source.transform(result_ransac.transformation)
    o3d.io.write_point_cloud(args.output_ply, source_transformed)
    save_transformation_to_txt(result_ransac.transformation,args.output_transform,)

