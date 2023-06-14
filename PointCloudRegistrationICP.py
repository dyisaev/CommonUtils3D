import open3d as o3d
import argparse 
from pyk4a_helpers import save_transformation_to_txt, load_transformation_from_txt

def execute_icp_registration(source,target,threshold,trans_init):
    reg_p2p = o3d.t.pipelines.registration.icp(
        source, target, threshold, trans_init,
        o3d.t.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.t.pipelines.registration.ICPConvergenceCriteria(max_iteration=1000))
    return reg_p2p


parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, required=True)
parser.add_argument('--target', type=str, required=True)
parser.add_argument('--threshold', type=float, required=False, default=5.00)
parser.add_argument('--init_transform', type=str, required=True, default=None)
parser.add_argument('--output_transform', type=str, required=True)
parser.add_argument('--output_ply', type=str, required=True)

if __name__ == '__main__':
    args=parser.parse_args()
    source = o3d.t.io.read_point_cloud(args.source).cuda()
    target = o3d.t.io.read_point_cloud(args.target).cuda()
    threshold = args.threshold
    init_transform = load_transformation_from_txt(args.init_transform)
    print ('Initial transformation:')
    print (init_transform)
    print ('Initial evaluation:')
    evaluation = o3d.t.pipelines.registration.evaluate_registration(
        source, target, threshold, init_transform)
    print(f'Fitness: {evaluation.fitness:.4f}, RMSE: {evaluation.inlier_rmse:.4f}')

    reg_p2p = execute_icp_registration(source,target,threshold,init_transform)
    print ('Resulting transformation:')
    print(reg_p2p.transformation)
    print('Resulting evaluation:')
    evaluation = o3d.t.pipelines.registration.evaluate_registration(
        source, target, threshold, reg_p2p.transformation)
    print(f'Fitness: {evaluation.fitness:.4f}, RMSE: {evaluation.inlier_rmse:.4f}')

    source_transformed = source.transform(reg_p2p.transformation)
    o3d.t.io.write_point_cloud(args.output_ply, source_transformed)
    save_transformation_to_txt(reg_p2p.transformation.numpy(),args.output_transform)

