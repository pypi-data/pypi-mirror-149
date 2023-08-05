import numpy as np
import trimesh.creation
import matplotlib.pyplot as plt

prototype_cylinder = trimesh.creation.cylinder(1, 1, 10)

def to_mesh(x, y, z1, z2, values, cmap="viridis", nan_color=[0, 1, 0, 1], normalize=True):
    if isinstance(cmap, str):
        cmap = plt.cm.get_cmap(cmap)
    nan_color = (np.array(nan_color) * 255).astype(int)

    if normalize:
        if isinstance(normalize, tuple):
            vmin, vmax = normalize
        else:
            vmin, vmax = np.nanmin(values), np.nanmax(values)
        values = values - vmin
        values = values / vmax
    
    colors = (cmap(values) * 255).astype(int)
    for i in range(4):
        colors[np.isnan(values),i] = nan_color[i]

    h = z2 - z1
        
    ms = []
    for i in range(len(x)):
        m = prototype_cylinder.copy()
        
        t = np.identity(4)
        t[2,2] = h[i]
        m.apply_transform(t)
        m.apply_transform(trimesh.transformations.translation_matrix([x[i], y[i], z1[i]]))

        for j in range(4):
            m.visual.face_colors[:,j] = colors[i,j]
        ms.append(m)

    return trimesh.util.concatenate(ms)
