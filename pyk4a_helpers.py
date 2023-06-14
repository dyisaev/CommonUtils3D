# helpers from pyk4a examples
# source: https://github.com/etiennedub/pyk4a/blob/master/example/helpers.py
# retrieval date: 2023-06-09

from typing import Optional, Tuple

import cv2
import numpy as np
import open3d as o3d
import os

from pyk4a import ImageFormat,PyK4APlayback


def convert_to_bgra_if_required(color_format: ImageFormat, color_image):
    # examples for all possible pyk4a.ColorFormats
    if color_format == ImageFormat.COLOR_MJPG:
        color_image = cv2.imdecode(color_image, cv2.IMREAD_COLOR)
    elif color_format == ImageFormat.COLOR_NV12:
        color_image = cv2.cvtColor(color_image, cv2.COLOR_YUV2BGRA_NV12)
        # this also works and it explains how the COLOR_NV12 color color_format is stored in memory
        # h, w = color_image.shape[0:2]
        # h = h // 3 * 2
        # luminance = color_image[:h]
        # chroma = color_image[h:, :w//2]
        # color_image = cv2.cvtColorTwoPlane(luminance, chroma, cv2.COLOR_YUV2BGRA_NV12)
    elif color_format == ImageFormat.COLOR_YUY2:
        color_image = cv2.cvtColor(color_image, cv2.COLOR_YUV2BGRA_YUY2)
    return color_image


def colorize(
    image: np.ndarray,
    clipping_range: Tuple[Optional[int], Optional[int]] = (None, None),
    colormap: int = cv2.COLORMAP_HSV,
) -> np.ndarray:
    if clipping_range[0] or clipping_range[1]:
        img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
    else:
        img = image.copy()
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img = cv2.applyColorMap(img, colormap)
    return img

def info(playback: PyK4APlayback):
    #    number of captures
    total_captures = playback.length
    print(f"Total recording time in usec: {total_captures}\n")
    return total_captures

def save_transformation_to_txt(transformation, filename):
    np.savetxt(filename, transformation, delimiter=' ', fmt='%f')

def load_transformation_from_txt(filename):
    return np.loadtxt(filename, delimiter=' ', dtype=np.float32)

def read_obj(file_path):
    # Lists to store vertices and faces
    vertices = []
    faces = []
    normals = []
    with open(file_path, 'r') as file:
        for line in file:
            components = line.strip(' \n').split()
            if len(components) == 0 or components[0] == '#':
                continue
            if components[0] == 'v':  # vertex information
                vertices.append([float(components[1]), float(components[2]), float(components[3])])
            elif components[0] == 'vn':  # vertex normal information
                normals.append([float(components[1]), float(components[2]), float(components[3])])
            elif components[0] == 'f':  # face information
                face_components = components[1:]  # remove 'f'
                # split each component into its parts and get the vertex index
                face = [int(comp.split('/')[0])-1 for comp in face_components]
                faces.append(face)
    # Create TriangleMesh
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(np.array(vertices))
    mesh.triangles = o3d.utility.Vector3iVector(np.array(faces))
    if len(normals) > 0:
        mesh.vertex_normals = o3d.utility.Vector3dVector(np.array(normals))
    return mesh

    
# from https://raw.githubusercontent.com/YZWarren/PointNet-AE-3DMM/master/prepare_data/prepare_data.py
def list_filenames(folder,ext='.obj'):
    """Walk through every files in a directory"""
    filenames = []
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            fname,extension = os.path.splitext(filename)
            if extension == ext:
                filenames.append(os.path.abspath(os.path.join(dirpath, fname)))
    return filenames
