import numpy as np
import pandas as pd

def construct(time_series, ground_truth, start_ind, end_ind, T, norm_method):
    num = 0
    '''
        convert 2d numpy array of time series data into 3d numpy array, with extra dimension for lags, i.e.
        input of (n_samples, n_features) becomes (n_samples, T, n_features)
        time_series (2d np.array): financial time series data
        ground_truth (1d np.array): column which is used as ground truth
        start_index (string): string which is the date that we wish to begin including from.
        end_index (string): string which is the date that we wish to include last.
        T (int): number of lags
        norm_method (string): normalization method
    '''
    for ind in range(start_ind + 1, end_ind + 1):
        if not time_series.iloc[ind - T: ind].isnull().values.any():
            num += 1
    X = np.zeros([num, T, time_series.shape[1]], dtype=np.float32)
    y = np.zeros([num, 1], dtype=np.float32)

    sample_ind = 0
    for ind in range(start_ind + 1, end_ind + 1):
        if not time_series.iloc[ind - T: ind].isnull().values.any():
            if norm_method == "log_1d_return":
                X[sample_ind] = time_series.values[ind - T: ind, :]
            elif norm_method == "log_nd_return":
                X[sample_ind] = np.flipud(np.add.accumulate(np.flipud(time_series.values[ind - T: ind, :])))
            y[sample_ind, 0] = ground_truth.values[ind - 1]
            sample_ind += 1

    return X,y