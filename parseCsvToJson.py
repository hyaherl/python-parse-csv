import pandas as pd

input_dir = "./input"
output_dir = "./output"

data = pd.read_csv(file_path)

with open('output_file_path', 'w', encoding='utf-8') as f:
    data.to_json(f, force_ascii=False, orient='records')
    