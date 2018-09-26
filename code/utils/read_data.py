import pandas as pd


'''
parameters:
fname (str): the file going to be read. 
sel_col_names [str]: the columns to be returned in the exactly same order

returns: 
X (a pandas DataFrame): the data in the input file
'''
def read_single_csv(fname, sel_col_names = "All"):
    X = pd.read_csv(fname, index_col=0)
    if sel_col_names == "All":
        return X
    else:
        available_col = X.columns
        choosen_col =[]
        missing_col = []
        for col_name in sel_col_names:
            if col_name in available_col:
                choosen_col.append(col_name)
            else:
                missing_col.append(col_name)
        if len(missing_col)!=0:
            print("Available columns are following: "+str(list(available_col)))
            print("The following columns are missing: " + str(missing_col))
    return X[choosen_col]
'''

'''
def merge_data_frame(X, Y):
    return pd.concat([X, Y], axis=1, sort=True)


'''

'''
def process_missing_value(X):
    sta_ind = 0
    for i in range(X.shape[0]):
        if X.iloc[i].isnull().values.any():
            sta_ind = i + 1
    return X[sta_ind:], sta_ind

def process_missing_value_v2(X):
    return X.dropna()
