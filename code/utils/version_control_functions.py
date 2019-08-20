from utils.construct_data import *
from utils.read_data import process_missing_value_v3
from utils.normalize_feature import log_1d_return

def generate_version_params(version):
    ans = {"deal_with_abnormal_value":"v2", "labelling":"v1", "process_missing_value":"v1", 
            "normalize_without_1d_return": "v1", "technical_indication":"v1",
            "remove_unused_columns":"v1", "price_normalization":"v1", "scaling":"v2",
            "construct":"v1"}
    ver = version.split("_")
    v = ver[0]
    ex = ver[1] if len(ver) > 1 else None

    if v == "v7":
        ans['technical_indication'] = "v2"

    if ex == "ex1":
        ans['labelling'] = "v1_ex1"
    if ex == "ex2":
        ans['labelling'] = "v1_ex2"
        ans['construct'] = "v1_ex2"
    if ex == "ex3":
        ans['technical_indication'] = ans['technical_indication']+"_ex3"
    return ans

def deal_with_abnormal_value(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        includes processing abnormally large and small values and interpolation for missing values
        '''
        return deal_with_abnormal_value_v1(time_series)
    elif version == "v2":
        '''
        includes processing abnormally large values and interpolation for missing values
        '''
        return deal_with_abnormal_value_v2(time_series)

def labelling(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        standard labelling
        '''
        return labelling_v1(time_series, arguments['horizon'], arguments['ground_truth_columns'])
    elif version == "v1_ex1":
        '''
        labelling increases and decreases respective to some price before current time point.
        '''
        return labelling_v1_ex1(time_series, arguments['horizon'], 
                                arguments['ground_truth_columns'], arguments['lags'])

    elif version == "v1_ex2":
        '''
        three classifier
        '''
        return labelling_v1_ex2(time_series, arguments['horizon'],
                                arguments['ground_truth_columns'], arguments['split_dates'][2])


def process_missing_value(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        drop NA rows
        '''
        return process_missing_value_v3(time_series)

def normalize_without_1d_return(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        automated normalization for all possible combinations
        '''
        return normalize_without_1d_return_v1(time_series,time_series.index.get_loc(arguments['split_dates'][1]),
                                                arguments['norm_params'])


def technical_indication(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        automated generation of divPVT for all possible combinations (only PVT)
        '''
        return technical_indication_v1(time_series,time_series.index.get_loc(arguments['split_dates'][1]),
                                        arguments['tech_params'],arguments['ground_truth_columns'])
                                        
    elif version == "v1_ex3":
        '''
        automated generation of technical indicators for all possible combinations (only LME Ground Truth)
        '''
        return technical_indication_v1_ex3(time_series,time_series.index.get_loc(arguments['split_dates'][1]),
                                        arguments['tech_params'],arguments['ground_truth_columns'])
    
    elif version == "v2":
        '''
        automated generation of divPVT for all possible combinations
        '''
        return technical_indication_v2(time_series,time_series.index.get_loc(arguments['split_dates'][1]),
                                        arguments['tech_params'],arguments['ground_truth_columns'])
    
    elif version == "v2_ex3":
        '''
        automated generation of technical indicators for all possible combinations (only LME Ground Truth)
        '''
        return technical_indication_v2_ex3(time_series,time_series.index.get_loc(arguments['split_dates'][1]),
                                        arguments['tech_params'],arguments['ground_truth_columns'])
    


def remove_unused_columns(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        remove columns that will not be used in model
        '''
        return remove_unused_columns_v1(time_series,arguments['org_cols'])



def price_normalization(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        daily log returns
        '''
        return log_1d_return(time_series,arguments['org_cols'])

def insert_date_into_feature(arguments):
    time_series = arguments['time_series']

    return insert_date_into_feature_v1(time_series)

def scaling(arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        standard scaling
        '''
        return scaling_v1(time_series,time_series.index.get_loc(arguments['split_dates'][1]))
    if version == "v2":
        '''
        scaling without affecting categorical variables
        '''
        return scaling_v2(time_series,time_series.index.get_loc(arguments['split_dates'][1]),arguments['cat_cols'])


def construct(ind, arguments, version):
    time_series = arguments['time_series']
    if version == "v1":
        '''
        construct ndarray for standard labelling
        '''
        return construct_v1(time_series[ind][arguments['all_cols'][ind]], time_series[ind]["Label"], 
                            arguments['start_ind'], arguments['end_ind'], 
                            arguments['lags'], arguments['horizon'])
    elif version =="v1_ex2":
        '''
        construct ndarray for three classifier
        '''
        return construct_v1_ex2(time_series[ind][arguments['all_cols'][ind]], time_series[ind]["Label"], 
                            arguments['start_ind'], arguments['end_ind'], 
                            arguments['lags'], arguments['horizon'])

