import pandas as pd
import numpy as np
import glob
import sys
import json

# input_dir_path = './input'
# output_file_path = './output/metadata/dm.json'

input_dir_path = sys.argv[1]
output_file_path = sys.argv[2]

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def createNumberColumnObj(column, type, valid, missing, mean, std, min, quantile25, median, quantile75, max):
    return {
        "name": column,
        "type": type,
        "valid": valid,
        "missing": missing,
        "mean": mean,
        "std": std,
        "min": min,
        "quantile25": quantile25,
        "median": median,
        "quantile75": quantile75,
        "max": max,
    }

def createStringColumnObj(column, type, valid, missing, unique, modeFirst, modeFirstCnt, modeSecond, modeSecondCnt):
    return {
        "name": column,  
        "type": type,  
        "valid": valid,
        "missing": missing,
        "unique": unique,
        "modeFirst": modeFirst,
        "modeFirstCnt": modeFirstCnt,
        "modeSecond": modeSecond,
        "modeSecondCnt": modeSecondCnt,
    }

def createBoolColumnObj(column, type, valid, missing, true, false):
    return {
        "name": column,  
        "type": type,  
        "valid": valid,
        "missing": missing,
        "true": true,
        "false": false,
    }

def createDateColumnObj(column, type, valid, missing, min, mean, max):
    return {
        "name": column,  
        "type": type,  
        "valid": valid,
        "missing": missing,
        "min": min,
        "mean": mean,
        "max": max,
    }

file_list = glob.glob(input_dir_path + "/*")
file_list_csv = [file for file in file_list if file.endswith(".csv")]

input_file_path = file_list_csv[0]

df = pd.read_csv(input_file_path)

columns = list(df.columns)
rowSize = df.shape[0]
columnSize = df.shape[1]
columnList = []

for column in columns:
    type = df.dtypes[column].name

    if type == 'object':
        try:
            df[column] = pd.to_datetime(df[column])
            type = 'date'
        except ValueError:
            pass
    
    valid = df[column].count()
    missing = df[column].isnull().sum()

    if type == "object":
        unique = df[column].nunique()
        ser = df[column].value_counts(dropna=False)
        modeFirst = ser.idxmax()
        modeFirstCnt = ser[modeFirst]
        if pd.isna(modeFirst):
            modeFirst = '[null]'
        
        if unique != 1:
            modeSecond = ser.index[1]
            modeSecondCnt = ser[modeSecond]
        else:
            modeSecond = 0
            modeSecondCnt = 0

        columnList.append(createStringColumnObj(column, type, valid, missing, unique, modeFirst, modeFirstCnt, modeSecond, modeSecondCnt))
    elif type == "date":
        min = df[column].min().strftime("%m/%d/%Y")
        mean = df[column].mean().strftime("%m/%d/%Y")
        max = df[column].max().strftime("%m/%d/%Y")

        columnList.append(createDateColumnObj(column, type, valid, missing, min, mean, max))
    elif type == "bool":
        true = df[column].value_counts()[True]
        false = df[column].value_counts()[False]

        columnList.append(createBoolColumnObj(column, type, valid, missing, true, false))
    else:
        mean = df[column].mean()
        std = df[column].std()
        min = df[column].min()
        quantile25 = df[column].quantile(0.25)
        median = df[column].median()
        quantile75 = df[column].quantile(0.75)
        max = df[column].max()

        columnList.append(createNumberColumnObj(column, type, valid, missing, mean, std, min, quantile25, median, quantile75, max))

metadata = {
    "columns": columnList,
    "rowSize": rowSize,
    "columnSize": columnSize,
}

with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, cls=NpEncoder)