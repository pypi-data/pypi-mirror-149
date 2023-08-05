import numpy as np
import trimesh
import matplotlib.pyplot as plt

# y, x, z order
single_cube_offsets = np.array([[0, 0, 0],
                                [0, 1, 0],
                                [1, 1, 0],
                                [1, 0, 0],
                                [0, 0, 1],
                                [0, 1, 1],
                                [1, 1, 1],
                                [1, 0, 1]])
single_cube_faces = np.array([[0, 5, 4],
                              [0, 1, 5],

                              [1, 6, 5],
                              [1, 2, 6],

                              [2, 7, 6],
                              [2, 3, 7],
                             
                              [3, 4, 7],
                              [3, 0, 4],
                              
                              [4, 6, 7],
                              [4, 5, 6],
                              
                              [1, 3, 2],
                              [1, 0, 3]])

def to_mesh(values, xd=1, yd=1, zd=1, xs=None, ys=None, zs=None, normalize=True, cmap="viridis"):
    if isinstance(cmap, str):
        cmap = plt.cm.get_cmap(cmap)

    xi, yi, zi = np.meshgrid(
        np.arange(values.shape[1]),
        np.arange(values.shape[0]),
        np.arange(values.shape[2]))

    if xs is None: xs = xi * xd
    if ys is None: ys = yi * yd
    if zs is None: zs = zi * zd

    vertices = np.full((xs.shape[0] + 1, xs.shape[1] + 1, xs.shape[2] + 1, 3), np.nan)
    for xa in (0, 1):
        for ya in (0, 1):
            for za in (0, 1):
                xb = vertices.shape[1] - 1 + xa
                yb = vertices.shape[0] - 1 + ya
                zb = vertices.shape[2] - 1 + za

                xsign = [-1,1][xa]
                ysign = [-1,1][ya]
                zsign = [-1,1][za]
                vertices[ya:yb,xa:xb,za:zb, 0] = xs + xsign*xd
                vertices[ya:yb,xa:xb,za:zb, 1] = ys + ysign*yd
                vertices[ya:yb,xa:xb,za:zb, 2] = zs + zsign*zd


    # 6 sides per cube, 2 triangles per face, 3 sides to a triangle
    faces = np.full(xs.shape[:3] + (12, 3), -1)
    facecolors = np.full(xs.shape[:3] + (12, 4), -1)

    if normalize:
        if isinstance(normalize, tuple):
            vmin, vmax = normalize
        else:
            vmin, vmax = np.nanmin(values), np.nanmax(values)
        values = values - vmin
        values = values / vmax

    # Front left bottom
    for facei in range(12):
        for corneri in range(3):
            yo, xo, zo = single_cube_offsets[single_cube_faces[facei, corneri]]

            faces[:,:,:, facei, corneri] = np.ravel_multi_index((yi+yo, xi+xo, zi+zo), vertices.shape[:3])

        facecolors[:,:,:, facei, :] = np.where(
            np.repeat(np.isnan(values).reshape(values.shape + (1,)), 4, -1),
            -1,
            (255 * cmap(values)).astype(int))
    
    vertices_array = vertices.reshape((vertices.shape[0]*vertices.shape[1]*vertices.shape[2], vertices.shape[3]))
    faces_array = faces.reshape((faces.shape[0]*faces.shape[1]*faces.shape[2]*faces.shape[3], faces.shape[4]))
    facecolors_array=facecolors.reshape((facecolors.shape[0]*facecolors.shape[1]*facecolors.shape[2]*facecolors.shape[3], facecolors.shape[4]))
    
    filt = facecolors_array[:,3]  != -1
    faces_array = faces_array[filt, :]
    facecolors_array = facecolors_array[filt, :]

    return trimesh.Trimesh(vertices=vertices_array,
                           faces=faces_array,
                           visual = trimesh.visual.ColorVisuals(face_colors=facecolors_array)
                          )
