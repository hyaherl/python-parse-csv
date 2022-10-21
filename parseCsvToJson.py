import pandas as pd

data = pd.read_csv('./raw_test.csv')

with open('./raw_data.json', 'w', encoding='utf-8') as f:
    data.to_json(f, force_ascii=False, orient='records')