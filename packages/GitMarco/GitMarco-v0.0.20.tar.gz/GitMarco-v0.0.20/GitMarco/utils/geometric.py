import os
import random

import numpy as np
import pandas as pd
import pymeshlab
import tqdm
from scipy.interpolate import LinearNDInterpolator


def stl2mesh3d(stl_mesh):
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d

    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)

    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles

    vertices, ixr = np.unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    i = np.take(ixr, [3 * k for k in range(p)])
    j = np.take(ixr, [3 * k + 1 for k in range(p)])
    k = np.take(ixr, [3 * k + 2 for k in range(p)])

    return vertices, i, j, k


def grid2grid_interp(grid, new_grid, feature, fill_value=None,
                     correction: bool = False, n: int = 25):
    """
    :param grid: original grid
    :param new_grid: new_grid to interpolate on
    :param feature: values on the original grid
    :param fill_value: filling value for intepolation failures
    :param correction: apply or not a correction on nan values based on n neighbors
    :param n: number of neighbors
    :return:

    Intepolates features from grid to new_grid, filling wrong values with fill_value or nan and
    applying a correction to nan averaging with n closest neighbors
    """

    if fill_value is None:
        interp = LinearNDInterpolator(list(zip(grid[:, 0], grid[:, 1], grid[:, 2])),
                                      feature,
                                      rescale=False,
                                      )
    else:
        interp = LinearNDInterpolator(list(zip(grid[:, 0], grid[:, 1], grid[:, 2])),
                                      feature,
                                      rescale=False,
                                      fill_value=fill_value
                                      )
    y = interp(new_grid[:, 0], new_grid[:, 1], new_grid[:, 2])

    if correction and fill_value is None:
        for i, item in enumerate(y):
            if np.isnan(item):
                y[i] = node_neighbors_average(new_grid[i:i + 1], new_grid, y, n=n)

    return y


def node_neighbors_average(
        node,
        nodes,
        values,
        n: int = 50):
    """
    :param node: objective node
    :param nodes: grid nodes
    :param values: values calculated in nodes
    :param n: number of neighbors
    :return value: averaged value

    Find the the average value for a node based on n closest neighbors
    """

    nodes = np.asarray(nodes)

    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)

    df = pd.DataFrame()
    df['dist_2'] = dist_2
    df['values'] = values
    df.sort_values('dist_2', inplace=True)
    df = df.iloc[:n, :]

    new_values = df['values'][np.array(df.index, dtype=int)]
    new_values = new_values[~np.isnan(new_values)]

    value = np.mean(new_values)

    return value


class PointSampler(object):
    """!
    Introduction of a desired number of points within the geometry.
    These fall exactly on the triangular patches of the surface grid.
    The points are redistributed according to the weighted average over the triangular path size.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, int)
        self.output_size = output_size

    def triangle_area(self, pt1, pt2, pt3):
        side_a = np.linalg.norm(pt1 - pt2)
        side_b = np.linalg.norm(pt2 - pt3)
        side_c = np.linalg.norm(pt3 - pt1)
        s = 0.5 * (side_a + side_b + side_c)
        return max(s * (s - side_a) * (s - side_b) * (s - side_c), 0) ** 0.5

    def sample_point(self, pt1, pt2, pt3):
        # barycentric coordinates on a triangle
        s, t = sorted([random.random(), random.random()])
        f = lambda i: s * pt1[i] + (t - s) * pt2[i] + (1 - t) * pt3[i]
        return (f(0), f(1), f(2))

    def __call__(self, mesh):
        verts, faces = mesh
        verts = np.array(verts)
        areas = np.zeros((len(faces)))

        for i in range(len(areas)):
            areas[i] = (self.triangle_area(verts[faces[i][0]],
                                           verts[faces[i][1]],
                                           verts[faces[i][2]]))

        sampled_faces = (random.choices(faces,
                                        weights=areas,
                                        cum_weights=None,
                                        k=self.output_size))

        sampled_points = np.zeros((self.output_size, 3))

        for i in range(len(sampled_faces)):
            sampled_points[i] = (self.sample_point(verts[sampled_faces[i][0]],
                                                   verts[sampled_faces[i][1]],
                                                   verts[sampled_faces[i][2]]))

        return sampled_points


class Normalize(object):
    """!
    Normalizzazione dei dati per centrare la geometria nell'origine
    """

    def __call__(self, pointcloud):
        assert len(pointcloud.shape) == 2

        norm_pointcloud = pointcloud - np.mean(pointcloud, axis=0)
        norm_pointcloud /= np.max(np.linalg.norm(norm_pointcloud, axis=1))

        return norm_pointcloud


def norm_pointclouds(pointclouds: list) -> list:
    """!
    Normalizing pointclouds, each one indipendently
    """
    normed = []
    norm = Normalize()
    for pointcloud in pointclouds: normed.append(norm(pointcloud))
    return normed


def remesh_stl_to_target_faces(
        source: str,
        dest: str,
        target: int,
) -> None:
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(source)
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target)
    ms.save_current_mesh(dest)


def remesh_stl_files_to_min_faces(
        source_path: str,
        dest_path: str,
) -> None:
    if not os.path.exists(source_path):
        raise FileNotFoundError('Source path does not exist')
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    stl_files = [file for file in os.listdir(source_path) if '.stl' in file]

    assert len(stl_files) > 0, ValueError('No stl files detected')

    faces_number = []
    for stl_file in tqdm.tqdm(stl_files):
        file_path = os.path.join(source_path, stl_file)
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(file_path)
        faces_number.append(ms.current_mesh().face_number())

    target = min(faces_number)
    print(f'Remeshing to minimum number of faces: {target}')
    for stl_file in tqdm.tqdm(stl_files):
        file_path = os.path.join(source_path, stl_file)
        new_file_path = os.path.join(dest_path, stl_file)

        remesh_stl_to_target_faces(
            source=file_path,
            dest=new_file_path,
            target=target
        )
