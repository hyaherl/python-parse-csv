import pandas as pd

data = pd.read_csv('/curate/input/raw_test.csv')

with open('/curate/output/metadata.json', 'w', encoding='utf-8') as f:
    data.to_json(f, force_ascii=False, orient='records')