import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns


def ioplot(A, coords, shade=True, samples=None, kde=True,
           x=0, y=1, n_levels=10,
           pre_cmap="Purples", post_cmap="Greens", alpha=1,
           fig=None, figsize=(5,5), s=4):
    # pre_cmap, post_cmap = "Purples", "Greens"
    samples = samples or len(coords)
    # pre_coords = np.vstack(map(lambda i: coords[np.nonzero(A[:,i])] - coords[i], range(samples)))
    # post_coords = np.vstack(map(lambda i: coords[np.nonzero(A[i,:])] - coords[i], range(samples)))
    pre_coords = np.vstack([coords[np.nonzero(A[:,i])] - coords[i] for i in range(samples)])
    post_coords = np.vstack([coords[np.nonzero(A[i,:])] - coords[i] for i in range(samples)])

    fig = fig or plt.figure(figsize=figsize)
    if kde:
        ax0 = sns.kdeplot(pre_coords[:,x], pre_coords[:,y], n_levels=n_levels,
                          cmap=pre_cmap, shade=shade, shade_lowest=False, label="pre", zorder=11)
        # if shade:
        # [h.set_alpha(a) for h,a, in zip(ax0.collections,np.linspace(0,1,len(ax0.collections)))]
        ax1 = sns.kdeplot(post_coords[:,x], post_coords[:,y], n_levels=n_levels, ax=ax0,
                          cmap=post_cmap, shade=shade, shade_lowest=True, label="post", zorder=10)
        if shade:
            plt.gca().set_facecolor( ax0.collections[n_levels].get_facecolor()[0] )       # fix seaborn's kdeplot bug
            ax0.collections[n_levels].set_alpha(0)

            # [h.set_alpha(.75) for h in ax0.collections if h.get_alpha()!=0 ]

            # [h.set_alpha(a) for h,a, in zip(ax0.collections,np.linspace(0,1,len(ax0.collections)))]
            # [h.set_alpha(a) for h,a, in zip(ax1.collections,np.linspace(0,1,len(ax1.collections)))]
            # [h.set_alpha(a) for h,a, in zip(ax1.collections,np.tile(np.linspace(0,1,len(ax1.collections)/2),2))]    # because ax0==ax1, a BUG?

            # [h.set_alpha(a) for h,a, in zip(ax1.collections,np.tile(np.sqrt(np.linspace(0,1,n_levels)),2))]    # because ax0==ax1, a BUG?
            [h.set_alpha(a) for h,a, in zip(ax1.collections,
                                            np.sqrt(np.hstack([np.linspace(0,1,n_levels),np.linspace(0,1,n_levels)[1:]])))]    # because ax0==ax1, a BUG?

        # plt.axis('equal')
        plt.gca().set_aspect('equal', 'box')
        plt.xlabel('$\Delta$' + 'xyz'[x])
        plt.ylabel('$\Delta$' + 'xyz'[y])
    else:
        ax = fig.gca(projection='3d')
        # ax.view_init(elev=90, azim=-90)  # x,y
        # ax.view_init(elev=0, azim=90)    # x,z
        ax.view_init(elev=10, azim=45)  # x,y,z

        # ax.set_aspect('equal')

        ax.scatter(pre_coords[:,0], pre_coords[:,1], pre_coords[:,2], marker='D', s=s, c=[sns.color_palette(pre_cmap, 3)[-1]])
        ax.scatter(post_coords[:,0], post_coords[:,1], post_coords[:,2], s=s, c=[sns.color_palette(post_cmap, 3)[-1]])
        ax.set_xlabel('$\Delta$x')
        ax.set_ylabel('$\Delta$y')
        ax.set_zlabel('$\Delta$z')
        # ax.set_yticklabels([])

    plt.title("%d samples (out of %s nodes)" % (samples, len(coords)))