import pandas as pd
import numpy as np
import sys
import json

# input_file_path = './input/raw_test.csv'
# output_file_path = './output/metadata/metadata.json'

input_file_path = sys.argv[1]
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

def createColumnObj(column, type, count, nullCount, max, min, mean):
    return {
        "column": column,   
        "type": type,
        "count": count,
        "nullCount": nullCount,
        "max": max,
        "min": min,
        "mean": mean,
    }

df = pd.read_csv(input_file_path)

columns = list(df.columns)
rowSize = df.shape[0]
columnSize = df.shape[1]
columnList = []

for column in columns:
    type = df.dtypes[column].name
    if type == "object":
        type = "string"
    count = df[column].count()
    nullCount = rowSize - df[column].count()

    max = None
    min = None
    mean = None
    if type != "string":
        max = df[column].max()
        min = df[column].min()
        mean = df[column].mean()
        
    columnList.append(createColumnObj(column, type, count, nullCount, max, min, mean));

metadata = {
    "columns": columnList,
    "rowSize": rowSize,
    "columnSize": columnSize,
}

with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, cls=NpEncoder)