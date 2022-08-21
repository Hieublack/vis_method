import pandas as pd 
import numpy as np 
from sklearn.ensemble import ExtraTreesClassifier

def get_columns(df, number=26):
    del df['Date_Buy'], df['BUY'], df['SELL']
    shape = df.shape[1]
    if shape - 3 < number:
        return 0, 'Invalid', shape-3
    # Feature Importance with Extra Trees Classifier
    dataframe = df.copy()
    # fillna 
    dataframe.fillna(0, inplace=True)
    col_add = ['PROFIT', 'Symbol', 'Exchange', 'Time', 'Time_Investment_Number']
    X = dataframe.drop(columns = col_add).values
    temp = dataframe.drop(columns =col_add)
    # dataframe['PROFIT'] = [label_logit(i) for i in dataframe['PROFIT']]
    dataframe['PROFIT'] = (np.array(dataframe['PROFIT']) > 1.4 )*1
    Y = dataframe['PROFIT'].values
    # feature extraction
    model = ExtraTreesClassifier(n_estimators=10)
    model.fit(X, Y)
    # extract feature importances 
    # print(model.feature_importances_)

    result3 = pd.DataFrame({'column' : temp.columns, 'important': model.feature_importances_})
    result3 = result3.sort_values(by=['important'], ascending=False)
    a = list(result3['column'])[:number]
    for col in col_add:
        a.append(col)
    return df[a], 'Valid', 'Valid'

def process_columns(dat):
    
    dat, status, max_value = get_columns(dat)
    if status == 'Invalid':
        print('status = {}, max columns = {}'.format(status, max_value))
        raise Exception 
    else:
        features = dat.columns[:-5]
        data = pd.DataFrame()
        data['TIME'] = dat['Time_Investment_Number']
        data['PROFIT'] = dat['PROFIT']
        data['SYMBOL'] = dat['Symbol']
        data['EXCHANGE'] = dat['Exchange']
        data[features] = dat[features]
        data = data.sort_values(by=['TIME', 'SYMBOL'], ascending= [False, True])
        return data
