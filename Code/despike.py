# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 15:47:26 2014

@author: Alex
"""

def rolling_window(data, block):
    shape = data.shape[:-1] + (data.shape[-1] - block + 1, block)
    strides = data.strides + (data.strides[-1],)
    return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)


def despike(dataSeries, n1=2, n2=20, block=100, keep=0):
    """
    Wild Edit Seabird-like function. Passes with Standard deviation
    `n1` and `n2` with window size `block`.
    """
    data = dataSeries.values.astype(float).copy()
    roll = rolling_window(data, block)
    roll = np.ma.masked_invalid(roll)
    std = n1 * roll.std(axis=1)
    mean = roll.mean(axis=1)
    # Use the last value to fill-up.
    std = np.r_[std, np.tile(std[-1], block - 1)]
    mean = np.r_[mean, np.tile(mean[-1], block - 1)]
    mask = (np.abs(data - mean.filled(fill_value=np.NaN)) >
    std.filled(fill_value=np.NaN))
    data[mask] = np.NaN
    # Pass two recompute the mean and std without the flagged values from pass
    # one and removed the flagged data.
    roll = rolling_window(data, block)
    roll = np.ma.masked_invalid(roll)
    std = n2 * roll.std(axis=1)
    mean = roll.mean(axis=1)
    # Use the last value to fill-up.
    std = np.r_[std, np.tile(std[-1], block - 1)]
    mean = np.r_[mean, np.tile(mean[-1], block - 1)]
    mask = (np.abs(dataSeries.values.astype(float) - mean.filled(fill_value=np.NaN))> std.filled(fill_value=np.NaN))
    clean = dataSeries.astype(float).copy()
    clean[mask] = np.NaN
    return clean
kw = dict(n1=2, n2=20, block=6)
LBJ_OBS['FNUd']= despike(LBJ_OBS['FNU'],**kw)
fig, (ax1) = plt.subplots(nrows=1)
LBJ_OBS['FNUd'].plot(ax=ax1,c='r')
LBJ_OBS['FNU'].plot(ax=ax1, color='b')
mask = np.isnan(LBJ_OBS['FNUd'])
ax1.plot(LBJ_OBS.index[mask], LBJ_OBS['FNU'][mask], 'ro', alpha=0.3, label='Two-pass')
mask = np.abs(LBJ_OBS['FNU']) > 3 * np.abs(LBJ_OBS['FNU']).std()
ax1.plot(LBJ_OBS.index[mask], LBJ_OBS['FNU'][mask], 'g.', label=r'$3\times \sigma$')
plt.show()