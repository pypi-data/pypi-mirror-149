import logging

import numpy as np
import pandas as pd


def xy_to_polar(x, y):
    r = np.hypot(x, y)
    angle = np.arctan2(y, x)
    return r, angle


def polar_to_xy(r, angle):
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    return x, y


def xyz_to_spherical(xyz):
    r2 = xyz[:,0]**2 + xyz[:,1]**2
    rho = np.sqrt(r2 + xyz[:,2]**2)
    az = np.arctan2(xyz[:,1], xyz[:,0])
    el = np.arctan2(np.sqrt(r2), xyz[:,2])     # inclination angle, defined from Z-axis down
    # el = np.arctan2(xyz[:,2], np.sqrt(xy))     # elevation angle, defined from XY-plane up
    return np.array([rho, az, el]).transpose()


def cartesian_to_cylindrical_wrapper(coords):
    assert coords.shape[1] == 3, 'coords is not an array of 3d coordinates'

    r, angle = xy_to_polar(coords[:, 0], coords[:, 1])
    z = coords[:, 2]
    return np.vstack([r, angle, z]).T


def cylindrical_to_cartesian_wrapper(coords):
    assert coords.shape[1] == 3, 'coords is not an array of 3d coordinates'

    x, y = polar_to_xy(coords[:, 0], coords[:, 1])
    z = coords[:, 2]
    return np.vstack([x, y, z]).T


def core_connectivity_features(positions, A=None):
    if isinstance(positions, np.ndarray):
        logging.debug('Converting positions numpy array to pandas dataframe..')
        positions = pd.DataFrame(positions, columns=list('xyz'))
    logging.debug('positions: {}'.format(positions.shape))

    n = positions.shape[0]
    A = A if A is not None else np.zeros((n,n), dtype=np.int)
    # A = A if A is not None else np.full((n,n), np.nan)

    pairs = pd.DataFrame(A).stack().reset_index().rename(columns={'level_0':'from', 'level_1':'to', 0:'contacts'})
    pairs['connection'] = (pairs['contacts']!=0).astype(np.int)
    pairs = pairs[pairs['from']!=pairs['to']]
    logging.debug('pairs: {}'.format(pairs.shape))

    core_features = pairs \
        .merge(positions.add_prefix('from_'), left_on='from', right_index=True) \
        .merge(positions.add_prefix('to_'), left_on='to', right_index=True)

    return core_features


def enrich_connections(connections, skip_validations=False):
    """

    """
    assert connections.filter(regex='from_|to_').notna().values.all(), \
        'Position coordinates can not contain NaN values!'

    dxyz = (connections.filter(regex='to_') - connections.filter(regex='from_').values) \
        .rename(columns=lambda x: x.replace('to_','d'))

    data = connections.join(dxyz)
    data['sign_dz'] = np.sign(data['dz'])
    offset_spherical = pd.DataFrame(xyz_to_spherical(data[['dx', 'dy', 'dz']].values), index=data.index, columns=['rho', 'az', 'el']).add_prefix('offset_')
    offset_from = pd.DataFrame(xyz_to_spherical(data[['from_x', 'from_y', 'from_z']].values), index=data.index, columns=['rho', 'az', 'el']).add_prefix('from_')

    data = data.join(offset_spherical).join(offset_from)

    if not skip_validations:
        logging.debug('Validations..')
        for (x,y,z, rho,az,el) in [('from_x', 'from_y', 'from_z', 'from_rho', 'from_az', 'from_el'),
                                   ('dx', 'dy', 'dz', 'offset_rho', 'offset_az', 'offset_el')]:
            assert np.allclose(np.linalg.norm(data[[x,y,z]], axis=1), data[rho])
            assert np.allclose(np.arctan2(data[y], data[x]), data[az])
            assert np.allclose(np.arctan2(np.linalg.norm(data[[x,y]], axis=1), data[z]), data[el])

    return data


def connectivity_features(positions, A=None):
    core_features = core_connectivity_features(positions, A)
    features = enrich_connections(core_features)
    return features