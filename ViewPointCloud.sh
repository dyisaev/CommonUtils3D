#!/usr/bin/bash

# get to the directory where this script is located
cd "$(dirname "$0")"

echo "DISPLAY variable should be set if working remotely"
echo "If not set, run the following command:"
echo "export DISPLAY=:<..>"
echo "where <..> is the display number"

# This script is used to view point cloud data in .ply format
# Usage: ./ViewPointCloud.sh <path_to_ply_file>
if [[ $# -lt 1 ]]; then
    echo "Usage: ./ViewPointCloud.sh <path_to_ply_file> [voxel_size]" 
    exit 1
fi

if [ -n $2 ]; then
    VOXEL_SIZE="--voxel_size $2"
fi

echo "python3 ./ViewPointCloud.py --ply_file $1 $VOXEL_SIZE"
eval "python3 ./ViewPointCloud.py --ply_file $1 $VOXEL_SIZE"

