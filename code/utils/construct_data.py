import numpy as np
import pandas as pd
from copy import copy
import os
import sys
from datetime import datetime
sys.path.insert(0,os.path.abspath(os.path.join(sys.path[0],"..")))
from utils.normalize_feature import normalize_3mspot_spread,normalize_3mspot_spread_ex,normalize_OI,normalize_volume
from utils.Technical_indicator import ad, divergence_ad, pvt, divergence_pvt
from sklearn import preprocessing


def construct(time_series, ground_truth, start_ind, end_ind, T, h, norm_method):
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
    for ind in range(start_ind, end_ind):
        if not time_series.iloc[ind - T + 1: ind + 1].isnull().values.any():
            num += 1
    X = np.zeros([num, T, time_series.shape[1]], dtype=np.float32)
    y = np.zeros([num, 1], dtype=np.float32)

    sample_ind = 0
    for ind in range(start_ind, end_ind):
        if not time_series.iloc[ind - T + 1 : ind + 1].isnull().values.any():
            if norm_method == "log_1d_return":
                X[sample_ind] = time_series.values[ind - T + 1: ind + 1, :]
            elif norm_method == "log_nd_return":
                X[sample_ind] = np.flipud(np.add.accumulate(np.flipud(time_series.values[ind - T + 1: ind + 1, :])))
            y[sample_ind, 0] = ground_truth.values[ind]
            sample_ind += 1
    
    return X,y


def construct_keras_data(time_series, ground_truth_index, sequence_length):
    """
    data process
    
    Arguments:
    time_series -- DataFrame of raw data
    ground_truth_index -- index of ground truth in the dataframe, use to form ground truth label
    sequence_length -- An integer of how many days should be looked at in a row
    
    Returns:
    X_train -- A tensor of shape (N, S, F) that will be inputed into the model to train it
    Y_train -- A tensor of shape (N,) that will be inputed into the model to train it--spot price
    X_test -- A tensor of shape (N, S, F) that will be used to test the model's proficiency
    Y_test -- A tensor of shape (N,) that will be used to check the model's predictions
    Y_daybefore -- A tensor of shape (267,) that represents the spot price ,the day before each Y_test value
    unnormalized_bases -- A tensor of shape (267,) that will be used to get the true prices from the normalized ones
    window_size -- An integer that represents how many days of X values the model can look at at once
    """

    #raw_data
    val_date = '2015-01-02'
    tes_date = '2016-01-04'
    val_ind = time_series.index.get_loc(val_date)
    tes_ind = time_series.index.get_loc(tes_date)
    raw_data = time_series.values
    #Convert the file to a list
    data = raw_data.tolist()
    
    #Convert the data to a 3D array (a x b x c) 
    #Where a is the number of days, b is the window size, and c is the number of features in the data file
    result = []
    for index in range(len(data) - sequence_length + 1):
        result.append(data[index: index + sequence_length])

    #Normalizing data by going through each window
    #Every value in the window is divided by the first value in the window, and then 1 is subtracted
    d0 = np.array(result)
    dr = np.zeros_like(d0)
    dr[:,1:,:] = d0[:,1:,:] / d0[:,0:1,:] - 1
    #Keeping the unnormalized prices for Y_test
    #Useful when graphing spot price over time later
    #The first value in the window
    end = int(dr.shape[0] + 1)
    unnormalized_bases_val = d0[val_ind:tes_ind, 0:1, ground_truth_index]
    unnormalized_bases_tes = d0[tes_ind:end, 0:1, ground_truth_index]
    #Splitting data set into training validating and testing data
    split_line = val_ind
    training_data = dr[:int(split_line), :]

    
    #Training Data
    X_train = training_data[:, :-1]
    Y_train = training_data[:, -1,:]
    Y_train = Y_train[:, ground_truth_index]
    X_val = dr[val_ind:tes_ind,:-1]
    Y_val = dr[val_ind:tes_ind,-1]
    Y_val = Y_val[:, ground_truth_index]

    #Testing data
    X_test = dr[tes_ind:, :-1]
    Y_test = dr[tes_ind:, -1]
    Y_test = Y_test[:, ground_truth_index]

    #Get the day before Y_test's price
    Y_daybefore_val = dr[val_ind:tes_ind, -2, :]
    Y_daybefore_val = Y_daybefore_val[:, ground_truth_index]
    Y_daybefore_tes = dr[tes_ind:, -2, :]
    Y_daybefore_tes = Y_daybefore_tes[:, ground_truth_index]
    
    #Get window size and sequence length
    sequence_length = sequence_length
    window_size = sequence_length - 1 #because the last value is reserved as the y value
    
    return X_train, Y_train, X_val, Y_val, X_test, Y_test, Y_daybefore_val, Y_daybefore_tes, unnormalized_bases_val, unnormalized_bases_tes, window_size


def normalize(X,train_end, params):
    ans = {"nVol":False,"nSpread":False,"nEx":False}

    cols = X.columns.values.tolist()
    ex = False
    if "CNYUSD" in cols:
        print("Considering Exchange Rate")
        ex = True
    
    for col in cols:
        if "OI" in col:
            print("Normalizing OI:"+"=>".join((col,col[:-2]+"nOI")))
            X[col[:-2]+"nOI"] = normalize_OI(copy(X[col]),train_end,strength = params['strength'], both = params['both'])
        if "Volume" in col:
            setting = col[:-6]
            if setting+"OI" in cols:
                ans["nVol"] = True
                print("Normalizing Volume:"+"=>".join((col,setting+"OI")))
                X[setting+"nVolume"] = normalize_volume(copy(X[col]), train_end = train_end, OI = copy(X[setting+"OI"]),
                                                        len_ma = params['len_ma'],version = params['vol_norm'], 
                                                        strength = params['strength'], both = params['both'])
        if "Close" in col:
            setting = col[:-5]
            if setting+"Spot" in cols:
                ans["nSpread"] = True
                print("Normalizing Spread:"+"=>".join((col,setting+"Spot")))
                X[setting+"n3MSpread"] = normalize_3mspot_spread(copy(X[col]),copy(X[setting+"Spot"]),
                                                                len_update=params['len_update'],
                                                                version = params['spot_spread_norm'])
        if "SHFE" in col and "Close" in col and ex:
            metal = col.split("_")[1]
            if "_".join(("LME",metal,"Spot")) in cols:
                ans["nEx"] = True
                print("+".join((col,"_".join(("LME",metal,"Spot"))))+"=>"+"_".join(("SHFE",metal,"nEx3MSpread")))
                X["_".join(("SHFE",metal,"nEx3MSpread"))] = normalize_3mspot_spread_ex(copy(X["_".join(("LME",metal,"Spot"))]),
                                                                                    copy(X[col]),copy(X["CNYUSD"]),
                                                                                    len_update=params['len_update'],
                                                                                    version = params['ex_spread_norm'])
            if "_".join(("LME",metal,"Close")) in cols:
                ans["nEx"] = True
                print("+".join((col,"_".join(("LME",metal,"Close"))))+"=>"+"_".join(("SHFE",metal,"nEx3MSpread")))
                X["_".join(("SHFE",metal,"nExSpread"))] = normalize_3mspot_spread_ex(copy(X["_".join(("LME",metal,"Close"))]),
                                                                                    copy(X[col]),copy(X["CNYUSD"]),
                                                                                    len_update=params['len_update'],
                                                                                    version = params['ex_spread_norm'])
            
    return X, ans


def technical_indication(X,train_end,params):
    cols = X.columns.values.tolist()
    for col in cols:
        if "Close" in col:
            setting = col[:-5]
            if setting+"Volume" in cols:
                print("+".join((col,setting+"Volume"))+"=>"+"+".join((setting+"PVT",setting+"divPVT")))
                X[setting+"PVT"] = pvt(copy(X[col]),copy(X[setting+"Volume"]))
                X[setting+"divPVT"] = divergence_pvt(copy(X[col]),copy(X[setting+"PVT"]),train_end, 
                                                            params = params)
            
    return X


def rescale(X):
    X_copy = copy(X)
    X_copy = X_copy.applymap(np.abs)
    average = X_copy.apply(np.mean,axis = 0)

    for i in range(len(average)):
        mean = average[i]
    
        while mean < 0.1:
            mean = mean * 10
            X[X.columns[i]] = X[X.columns[i]] * 10
        while mean > 1:
            mean = mean * 0.1
            X[X.columns[i]] = X[X.columns[i]] * 0.1

    return X


def labelling(X,horizon, ground_truth_columns):
    assert ground_truth_columns != []
    ans = []
    for ground_truth in ground_truth_columns:
        labels = copy(X[ground_truth])
        labels = labels.shift(-horizon) - labels
        labels = labels > 0
        labels = labels.rename("Label")
        ans.append(labels)
    return ans


def deal_with_abnormal_value(data):
    #deal with the big value
    column_list = []
    for column in data.columns:
        if "_OI" in column:
            column_list.append(column)
    year_list = list(range(int(data.index[0].split("-")[0]),int(data.index[-1].split("-")[0])))
    month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for column_name in column_list:   
        for year in year_list:
            for month in month_list:
                start_time = str(year)+'-'+month+'-'+'01'
                end_time = str(year)+'-'+month+'-'+'31'
                value_dict = {}
                value_list=[]
                temp = copy(data.loc[(data.index >= start_time)&(data.index <= end_time)])
                if len(temp) == 0 or len(temp[column_name].dropna()) == 0:
                    continue
                average = np.mean(temp[column_name].dropna())
                data.at[temp[column_name].idxmax(),column_name] = average
                
    #deal with the minor value in OI
    for column_name in column_list:
        temp = data[column_name]
        nsmallest = temp.nsmallest(n = 20).index
        for ind in nsmallest:
            start_time = ind[:-2]+'01'
            end_time = ind[:-2]+'31'
            data.at[ind,column_name] = np.mean(data.loc[(data.index >= start_time)&(data.index <= end_time)][column_name])
    #missing value interpolate
    data = data.interpolate(axis = 0)

    return data

def scaling(X,train_end):
    scaler = preprocessing.StandardScaler()
    scaler.fit(X.iloc[:train_end,].values)
    X = pd.DataFrame(scaler.transform(X), index = X.index, columns = X.columns)
    return X

        



                    



        
